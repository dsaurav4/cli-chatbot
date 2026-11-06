import httpx
import sys

URL = "http://localhost:11434/v1/chat/completions"

messages = [
    {"role": "system", "content": "You are a tutor who is teaching how Large Language Models work."},
]

while(True):
    prompt = input("Write your prompt here (Enter 'quit' to exit): ")

    if prompt == "quit":
        break
    else:
        messages.append({"role": "user", "content": prompt})
        
    try:
        r = httpx.post(URL, json = {
        "model": "llama3.2",
        "messages": messages
    }, timeout=30.0)
        r.raise_for_status()
    except httpx.ConnectError:
        print("Can't reach Ollama. is it running?")
        messages.pop()
        continue
    except httpx.HTTPStatusError as e:
        print(e.response.text)
        messages.pop()
        continue
    except httpx.TimeoutException:
        print("The model took too long to reply.")
        messages.pop()
        continue
    else:
        response = r.json()
        reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print(reply)
        print(f"Token In : {response['usage']['prompt_tokens']}, Token Out: {response['usage']['completion_tokens']}")