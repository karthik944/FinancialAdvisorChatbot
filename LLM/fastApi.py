from fastapi import FastAPI
from pydantic import BaseModel
import subprocess
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize FastAPI app
app = FastAPI()

# Load GPT-2 model and tokenizer (only once at startup)
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Request model schema
class GenerateRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 1.0
    max_tokens: int = 100

@app.post("/api/generate")
async def generate(request: GenerateRequest):
    # Preprocess the prompt (Query Preprocessing)
    prompt = preprocess_prompt(request.prompt)

    if request.model == "llama3":
        # Use subprocess to run the Llama command
        try:
            # Adjust the command based on Llama's requirements
            command = ["ollama", "run", "llama3.2"]  # Ensure this is the correct command
            result = subprocess.run(
                command,
                input=prompt,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )

            if result.returncode == 0:
                response = result.stdout.strip()
            else:
                response = f"Error: {result.stderr.strip()}"

        except Exception as e:
            response = f"Exception occurred: {str(e)}"

    elif request.model == "gpt2":
        # Use Hugging Face transformers to generate text with GPT-2
        inputs = gpt2_tokenizer.encode(prompt, return_tensors="pt")
        output = gpt2_model.generate(
            inputs,
            max_length=request.max_tokens,
            temperature=request.temperature,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95
        )
        response = gpt2_tokenizer.decode(output[0], skip_special_tokens=True)

    else:
        response = "Model not supported."

    # Post-process the response (Response Post-Processing)
    cleaned_response = postprocess_response(response)

    return {"output": cleaned_response}


def preprocess_prompt(prompt: str) -> str:
    # Simple query preprocessing, such as removing unnecessary characters or formatting
    prompt = prompt.lower().strip()
    prompt = re.sub(r'[^\w\s]', '', prompt)
    return prompt

def postprocess_response(response: str) -> str:
    # Remove unwanted tokens or special characters from the response
    response = re.sub(r'<\|endoftext\|>', '', response)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

