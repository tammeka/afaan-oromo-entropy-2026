from transformers import AutoTokenizer, AutoModelForCausalLM

# Use a MUCH smaller model (fits in memory)
model_name = "distilgpt2"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Loading small model...")
model = AutoModelForCausalLM.from_pretrained(model_name)

print("SUCCESS! Small model loaded perfectly.")
print("Neural entropy estimation is ready.")