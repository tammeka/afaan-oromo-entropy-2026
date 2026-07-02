from datasets import load_dataset

print("Loading EthioSenti dataset...")
dataset = load_dataset("EthioNLP/EthioSenti")

print(f"Dataset splits: {dataset.keys()}")
print(f"Training examples: {len(dataset['train'])}")
print(f"First example: {dataset['train'][0]}")