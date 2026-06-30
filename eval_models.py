import os
import torch
import json
import time
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

MODELS = {
    "functiongemma": "./finetuned_functiongemma_merged",
    "smollm2-instruct": "./finetuned_smollm2-instruct_merged",
    "smollm2-base": "./finetuned_smollm2-base_merged",
}

def clean_response(text):
    text = text.replace("<end_of_turn>", "").replace("<|im_end|>", "").strip()
    return text

def parse_intent(text):
    text = text.lower()
    if text.startswith("launch_apps"):
        return "launch_apps"
    elif text.startswith("trigger_boredom"):
        return "trigger_boredom"
    elif text.startswith("none"):
        return "none"
    return "unknown"

def evaluate_model(model_key, model_path, device):
    print(f"\nEvaluating model: {model_key} from {model_path}...")
    if not os.path.exists(model_path):
        print(f"Skipping: Merged model directory not found at {model_path}")
        return None

    # Load format-specific test set
    dataset_file = "dataset_gemma.json" if "gemma" in model_key else "dataset_chatml.json"
    print(f"Loading evaluation dataset: {dataset_file}")
    dataset = load_dataset("json", data_files=dataset_file)
    split_dataset = dataset["train"].train_test_split(test_size=0.1, seed=42)
    eos_marker = "<end_of_turn>" if "gemma" in model_key else "<|im_end|>"

    def format_dataset(example):
        return {
            "prompt": example["prompt"],
            "completion": example["response"] + eos_marker
        }
    test_dataset = split_dataset["test"].map(format_dataset)

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float32,
        device_map=None
    ).to(device)
    model.eval()

    correct_exact = 0
    correct_intent = 0
    total = len(test_dataset)
    total_time = 0.0

    print(f"Running inference on {total} test samples...")
    for idx, item in enumerate(test_dataset):
        prompt = item["prompt"]
        target = clean_response(item["completion"])
        target_intent = parse_intent(target)

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        prompt_len = inputs["input_ids"].shape[1]

        start_time = time.time()
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=64,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                do_sample=False
            )
        elapsed = time.time() - start_time
        total_time += elapsed

        generated_tokens = outputs[0][prompt_len:]
        pred = tokenizer.decode(generated_tokens, skip_special_tokens=True)
        pred = clean_response(pred)
        pred_intent = parse_intent(pred)

        exact_match = (pred == target)
        intent_match = (pred_intent == target_intent)

        if exact_match:
            correct_exact += 1
        if intent_match:
            correct_intent += 1

        if (idx + 1) % 5 == 0 or (idx + 1) == total:
            print(f"  Processed {idx + 1}/{total} samples...")

    avg_latency = (total_time / total) * 1000  # ms
    exact_acc = (correct_exact / total) * 100
    intent_acc = (correct_intent / total) * 100

    print(f"Results for {model_key}:")
    print(f"  Exact Match Accuracy: {exact_acc:.1f}% ({correct_exact}/{total})")
    print(f"  Intent Accuracy:      {intent_acc:.1f}% ({correct_intent}/{total})")
    print(f"  Average Latency:      {avg_latency:.1f} ms")

    return {
        "model": model_key,
        "exact_accuracy": exact_acc,
        "intent_accuracy": intent_acc,
        "avg_latency_ms": avg_latency
    }

def main():
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
    print(f"Using evaluation device: {device}")

    results = []
    for model_key, model_path in MODELS.items():
        res = evaluate_model(model_key, model_path, device)
        if res:
            results.append(res)

    if not results:
        print("\nNo models evaluated (none of the merged directories found).")
        return

    # Print markdown table
    print("\n" + "="*50)
    print("               EVALUATION SUMMARY")
    print("="*50)
    print("| Model Name | Exact Match Acc | Intent Acc | Avg Latency |")
    print("|------------|-----------------|------------|-------------|")
    for r in results:
        print(f"| {r['model']} | {r['exact_accuracy']:.1f}% | {r['intent_accuracy']:.1f}% | {r['avg_latency_ms']:.1f} ms |")
    print("="*50)

if __name__ == "__main__":
    main()
