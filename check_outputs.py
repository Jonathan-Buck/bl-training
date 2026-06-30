import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM

MODELS = {
    "smollm2-instruct": "./finetuned_smollm2-instruct_merged",
    "smollm2-base": "./finetuned_smollm2-base_merged",
    "functiongemma": "./finetuned_functiongemma_merged"
}

def main():
    device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

    # Load first 2 test items from both formats
    gemma_dataset = load_dataset("json", data_files="dataset_gemma.json")["train"].train_test_split(test_size=0.1, seed=42)
    chatml_dataset = load_dataset("json", data_files="dataset_chatml.json")["train"].train_test_split(test_size=0.1, seed=42)

    for i in range(2):
        print(f"\n--- TEST EXAMPLE {i+1} ---")
        gemma_item = gemma_dataset["test"][i]
        chatml_item = chatml_dataset["test"][i]
        
        target = gemma_item["response"]
        print(f"Target: {target}")

        for model_name, path in MODELS.items():
            dataset_item = gemma_item if "gemma" in model_name else chatml_item
            prompt = dataset_item["prompt"]

            tokenizer = AutoTokenizer.from_pretrained(path)
            model = AutoModelForCausalLM.from_pretrained(path, torch_dtype=torch.float32).to(device)
            inputs = tokenizer(prompt, return_tensors="pt").to(device)
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=64,
                    eos_token_id=tokenizer.eos_token_id,
                    pad_token_id=tokenizer.pad_token_id or tokenizer.eos_token_id,
                    do_sample=False
                )
            gen = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:])
            print(f"[{model_name} generated]: {repr(gen)}")

if __name__ == "__main__":
    main()
