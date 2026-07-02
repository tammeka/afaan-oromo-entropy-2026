from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

model_name = "EthioNLP/ethio-llm-base"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Loading model (this will take 5-15 minutes on USB)...")
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="cpu")

print("EthioLLM loaded successfully!")
print("Model loaded on:", model.device)