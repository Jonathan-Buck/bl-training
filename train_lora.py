import os
os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"
import argparse
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, TaskType
from trl import SFTTrainer, SFTConfig

# ── Supported models ──
MODELS = {
    "functiongemma": "google/functiongemma-270m-it",
    "smollm2-instruct": "HuggingFaceTB/SmolLM2-135M-Instruct",
    "smollm2-base": "HuggingFaceTB/SmolLM2-135M",
}


def train(model_key: str):
    model_id = MODELS[model_key]
    output_dir = f"./berry_lora_{model_key}"
    merged_dir = f"./finetuned_{model_key}_merged"

    print(f"{'='*60}")
    print(f"  Model:      {model_id}")
    print(f"  Output:     {output_dir}")
    print(f"  Merged to:  {merged_dir}")
    print(f"{'='*60}\n")

    # 1. Load dataset
    dataset_file = "dataset_gemma.json" if "gemma" in model_key else "dataset_chatml.json"
    print(f"Loading dataset from: {dataset_file}")
    dataset = load_dataset("json", data_files=dataset_file)
    split_dataset = dataset["train"].train_test_split(test_size=0.1, seed=42)

    # Determine the end-of-turn EOS marker based on model type
    eos_marker = "<end_of_turn>" if "gemma" in model_key else "<|im_end|>"

    # Format dataset to prompt-completion structure expected by SFTTrainer for completion_only_loss.
    # We append the appropriate EOS token to completion so the model learns when to stop generating.
    def format_dataset(example):
        return {
            "prompt": example["prompt"],
            "completion": example["response"] + eos_marker
        }

    train_dataset = split_dataset["train"].map(format_dataset).remove_columns(["response", "full_text"])
    eval_dataset = split_dataset["test"].map(format_dataset).remove_columns(["response", "full_text"])

    # 2. Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.padding_side = "right"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # 3. Device & precision
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using device: {device}")

    # MPS and CUDA work best with bfloat16 (smaller memory footprint and fast compute)
    torch_dtype = torch.bfloat16 if (device == "mps" or device == "cuda") else torch.float32

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch_dtype,
        device_map="auto" if device == "cuda" else None
    )

    if device != "cuda":
        model = model.to(device)

    # 4. Measure max sequence length from actual dataset
    sample_lengths = []
    for item in train_dataset:
        tokens = tokenizer(item["prompt"] + item["completion"], return_tensors="pt", truncation=False)
        sample_lengths.append(tokens["input_ids"].shape[1])

    p95_length = sorted(sample_lengths)[int(len(sample_lengths) * 0.95)]
    max_length = sorted(sample_lengths)[-1]
    # Use p95 + headroom, capped at 8192
    max_seq_length = min(p95_length + 64, max_length, 8192)

    print(f"Token lengths → p50: {sorted(sample_lengths)[len(sample_lengths)//2]}, "
          f"p95: {p95_length}, max: {max_length}")
    print(f"Using max_length: {max_seq_length}")
    print(f"  ({sum(1 for l in sample_lengths if l > max_seq_length)} samples will be truncated)")

    # 5. Configure LoRA
    target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

    peft_config = LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=target_modules,
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )

    # Gemma models have a huge 256k vocabulary size, leading to extremely large logit tensors.
    # To prevent MPS out-of-memory (OOM) errors on large sequences, we use a batch size of 1 for functiongemma.
    if model_key == "functiongemma" and (device == "mps" or device == "cuda"):
        batch_size = 1
        grad_accum = 16
    elif device == "mps" or device == "cuda":
        batch_size = 8
        grad_accum = 2
    else:
        batch_size = 2
        grad_accum = 8

    # 6. SFTConfig (extends TrainingArguments with SFT-specific fields)
    sft_config = SFTConfig(
        output_dir=output_dir,
        per_device_train_batch_size=batch_size,
        gradient_accumulation_steps=grad_accum,     # effective batch size = 16
        warmup_ratio=0.03,
        num_train_epochs=3,
        learning_rate=2e-4,
        logging_steps=10,
        save_strategy="epoch",
        eval_strategy="epoch",
        fp16=(device == "cuda"),
        bf16=(device == "cuda" or device == "mps"),
        report_to="none",
        dataloader_pin_memory=False,       # required for MPS
        # SFT-specific fields
        max_length=max_seq_length,
        packing=False,
        completion_only_loss=True,
    )

    # 7. Initialize SFTTrainer
    import gc
    from transformers import TrainerCallback

    class MPSCallback(TrainerCallback):
        def on_substep_end(self, args, state, control, **kwargs):
            if torch.backends.mps.is_available():
                gc.collect()
                torch.mps.empty_cache()

        def on_step_end(self, args, state, control, **kwargs):
            if torch.backends.mps.is_available():
                gc.collect()
                torch.mps.empty_cache()

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        peft_config=peft_config,
        processing_class=tokenizer,
        args=sft_config,
        callbacks=[MPSCallback()],
    )

    # 8. Train
    print(f"\nStarting training...")
    print(f"  Train samples: {len(train_dataset)}")
    print(f"  Eval samples:  {len(eval_dataset)}")
    print(f"  Epochs: {sft_config.num_train_epochs}")
    print(f"  Effective batch size: {sft_config.per_device_train_batch_size * sft_config.gradient_accumulation_steps}")
    trainer.train()

    # 10. Merge & save
    print("\nTraining finished. Merging adapters and saving merged model...")
    merged_model = trainer.model.merge_and_unload()
    merged_model.save_pretrained(merged_dir)
    tokenizer.save_pretrained(merged_dir)
    print(f"Model saved to {merged_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BerryLauncher LoRA fine-tuning")
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        default="functiongemma",
        help="Which model to fine-tune: " + ", ".join(f"{k} ({v})" for k, v in MODELS.items()),
    )
    args = parser.parse_args()
    train(args.model)
