from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("NaolBM/Oromo-BBPE")

text = "Dabalataan bu'uuraaleen misoomaa akka daandii qonnaan bultoonni omisha isaanii karaa salphaa ta'een gabaaf akka dhiyeessan carraa uumu himan."
tokens = tokenizer.tokenize(text)

print(f"Number of tokens: {len(tokens)}")
print(f"Tokens: {tokens}")