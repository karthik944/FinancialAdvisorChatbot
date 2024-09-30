import sys
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load pre-trained model (weights) and tokenizer
model_name = "gpt2"  # You can also use 'gpt2-medium', 'gpt2-large', 'gpt2-xl' for larger models
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Read prompt from command line arguments
if len(sys.argv) < 2:
    print("Please provide a prompt.")
    sys.exit(1)

prompt = sys.argv[1]  # Get the prompt from the first command line argument

# Encode input text (convert the prompt to token IDs)
inputs = tokenizer.encode(prompt, return_tensors="pt")

# Generate continuation of the text
output = model.generate(
    inputs,
    max_length=100,  # Adjust this to limit the length of generated text
    num_return_sequences=1,  # Number of sequences to generate
    no_repeat_ngram_size=2,  # Prevent repeating phrases
    do_sample=True,  # Random sampling (enables diverse generation)
    top_k=50,  # Limits sampling to top k tokens (increases coherence)
    top_p=0.95,  # Nucleus sampling for probabilistic sampling (p controls diversity)
    temperature=1.0  # Lower temperature reduces randomness, higher increases randomness
)

# Decode and print the output
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print("Generated text:", generated_text)


