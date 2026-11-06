import httpx
import json

URL = "http://localhost:11434/v1/chat/completions"

messages = [
    {"role": "system", "content": "You are a tutor who is teaching how Large Language Models work."},
]

while True:
    prompt = input("\nWrite your prompt here (Enter 'quit' to exit)>")

    if prompt == "quit":
        print("Have a great day!")
        break
    else:
        messages.append({"role": "user", "content": prompt})

    reply = ""

    try:
        with httpx.stream("POST", URL, json = {
                    "model": "llama3.2",
                    "stream": True,
                    "stream_options": {"include_usage": True},
                    "messages": messages
                }, 
                timeout=30.0) as r:
            if r.is_error:
                r.read()
            r.raise_for_status()
            print("\nchatbot>", end="", flush=True)
            for line in r.iter_lines():
                if not line:
                    continue
                json_part = line.removeprefix("data: ")
                if json_part == "[DONE]":
                    break
                chunk = json.loads(json_part)
                if "usage" in chunk:
                    usage = chunk["usage"]
                if not chunk["choices"]:
                    continue
                piece = chunk['choices'][0]['delta'].get("content", "")
                reply += piece
                print(piece, end = "", flush=True)
            print("\n=====================================================================================")
            print(f"Token In: {usage['prompt_tokens']}, Token Out: {usage['completion_tokens']}")
            print("=====================================================================================")
    except httpx.ConnectError:
        print("Can't reach Ollama. is it running?")
        messages.pop()
        continue
    except httpx.HTTPStatusError as e:
        e.response.read()
        print(e.response.text)
        messages.pop()
        continue
    except httpx.TimeoutException:
        print("The model took too long to reply.")
        messages.pop()
        continue
    else:
        messages.append({"role": "assistant", "content": reply})
            