import json

def extract_json(text: str):
    """
    Safe JSON extractor for LLM outputs.
    Handles:
    - markdown
    - extra text
    - truncated outputs (best effort)
    """

    # remove markdown
    text = text.replace("```json", "").replace("```", "").strip()

    # try direct parse first (BEST CASE)
    try:
        return json.loads(text)
    except:
        pass

    # fallback: extract largest JSON-like block manually
    start = text.find("{")
    if start == -1:
        raise ValueError("No JSON start found")

    # brute-force balance braces
    brace_count = 0
    end = None

    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1

        if brace_count == 0:
            end = i
            break

    if end is None:
        raise ValueError("Unclosed JSON object (model output truncated)")

    candidate = text[start:end+1]

    try:
        return json.loads(candidate)
    # except json.JSONDecodeError as e:
    #     print("JSON parse error:", e)
    #     print("Broken snippet (first 800 chars):")
    #     print(candidate[:800])
    #     raise
    except json.JSONDecodeError:
        candidate += "}"
        return json.loads(candidate)

def is_complete_json(text: str) -> bool:
    return text.strip().endswith("}")