import httpx
import sys

URL = "http://localhost:11434/v1/chat/completions"

def create_payload(prompt):
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": "You are a tutor who is teaching how Large Language Models work."},
            {"role": "user", "content":prompt}
        ]
    }

    return payload

prompt = input("Write your prompt here: ")

try:
    r = httpx.post(URL, json = create_payload(prompt), timeout=30.0)
    r.raise_for_status()
except:
    print("Can't reach Ollama. is it running?")
    sys.exit(1)
else:
    response = r.json()

    print(response["choices"][0]["message"]["content"])
    print(f"Token In : {response['usage']['prompt_tokens']}, Token Out: {response['usage']['completion_tokens']}")