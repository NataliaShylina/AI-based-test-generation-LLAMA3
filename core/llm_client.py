import requests

def call_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False,

            "options":{
                "num_predict":4096,
                "temperature":0.2,
                "top_p":0.9
            }
        },
        timeout=600
    )

    print(response.status_code)

    print(response.text[:500])

    return response.json()["response"]