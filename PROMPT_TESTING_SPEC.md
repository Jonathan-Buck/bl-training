# Spec: BerryLauncher Model Finetuning & Training

## 1. Goal
The objective is to train/finetune a custom **Function Gemma** model (`google/gemma-2b-it` or `google/gemma-2-2b-it`) to act as an on-device structured function caller. The model matches user natural language intents to either app-launch commands (`launch_apps`) or boredom interceptions (`trigger_boredom`). The resulting model will be exported as a quantized `.litertlm` (or `.tflite` / `.bin`) model for 100% local, private inference on Android.

## 2. Environment Setup
*   **Platform:** PyTorch, Hugging Face (`peft`, `trl`, `transformers`), and MediaPipe LLM Converter.
*   **Target Device:** Android (via LiteRT-LM / MediaPipe LLM Inference API).
*   **Dependencies:**
    ```bash
    pip install torch datasets transformers peft trl mediapipe
    ```

## 3. Finetuning Strategy & Template

### A. Template Design
We use the standard Gemma instruction-tuning chat template to format training examples:
```text
<start_of_turn>user
Apps:
- Chrome (com.android.chrome): Web browser
- Maps (com.google.android.apps.maps): Navigation

Query: find a path home
<end_of_turn>
<start_of_turn>model
launch_apps(package_names=["com.google.android.apps.maps"])<end_of_turn>
```

### B. Training Configuration
*   **Method:** Parameter-efficient fine-tuning via LoRA (rank=8, alpha=16) on all projection layers.
*   **SFT Masking:** Use `DataCollatorForCompletionOnlyLM` to compute loss solely on assistant response tokens, preserving the model's instruction template formatting.

## 4. Test & Training Dataset
We use a python-generated synthetic dataset:
*   `dataset_generator.py`: Script generating random subsets of installed apps (from a pool of 20+ common apps) paired with user queries mapping to app-launching, boredom responses, or fallback queries.
*   `dataset.json`: Output dataset file containing training inputs, models targets, and full training strings.

## 5. Deliverables
1.  **`dataset_generator.py`**: Synthetic dataset generation script.
2.  **`train_lora.py`**: Training script using Hugging Face SFT/LoRA.
3.  **`converted_model/`**: Merged and converted model outputs ready for on-device deployment in BerryLauncher.

## 6. Next Steps
1.  Verify dataset generation via `python3 dataset_generator.py`.
2.  Run the LoRA training loop locally or on GPU to verify SFT outputs.
3.  Export the model to LiteRT `.litertlm` using the MediaPipe GenAI converter.

