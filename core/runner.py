import json
from pathlib import Path

from core.llm_client import call_llm
from core.prompt_builder import build_prompt
from core.parser import extract_json


def run(
    requirements,
    base_prompt,
    app_config,
    output_path,
    uml=None,
    mode="AI",
    max_retries=3
):

    print("=" * 60)
    print("Generating:", output_path)
    print("Mode:", mode)

    # BUILD PROMPT (NOW supports MBT)
    prompt = build_prompt(
        system=base_prompt,
        app_context=app_config,
        requirements=requirements,
        uml=uml,
        mode=mode
    )

    parsed = None

    for attempt in range(max_retries):

        print(f"Attempt {attempt+1}")

        raw_output = call_llm(prompt)

        with open("raw_output.txt", "w") as f:
            f.write(raw_output)

        print("LLM output length:", len(raw_output))

        try:
            parsed = extract_json(raw_output)
            print("JSON parsed successfully")
            break

        except Exception as e:
            print("Parsing failed:", e)
            prompt += "\nIMPORTANT: Return ONLY valid JSON."

    if parsed is None:
        raise RuntimeError("Could not parse JSON.")

    print("Tests generated:", len(parsed["tests"]))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        json.dump(parsed, f, indent=2)

    print("Saved to:", output_path)
    print("=" * 60)

    return parsed