import json


def build_prompt(system: dict,
                 app_context: dict,
                 requirements: dict,
                 uml=None,
                 mode="AI") -> str:

    uml_section = ""
    if uml is not None:
        uml_section = f"""
UML MODEL (MODEL-BASED INFORMATION):
{json.dumps(uml, indent=2)}
"""

    # =========================
    # MODE: AI BASIC
    # =========================
    ai_basic_rules = """
YOU ARE A STRICT JSON GENERATOR.

RULES:
- Output MUST be valid JSON (RFC 8259)
- No markdown, no explanation
- Generate 20–25 test cases
- Do NOT invent system features not in requirements

QUALITY RULES:
- Each test must be unique
- Cover positive, negative, edge cases
- Each step must be a full sentence

CRITICAL LENGTH RULE:
- Each test MUST be concise
- Max 2 steps per test case
- Each step max 20 words
- Avoid long explanations

CRITICAL JSON SAFETY RULE:
- You MUST ensure all brackets are closed
- Ensure valid JSON closure
- NEVER cut off output mid-array
- If you reach limit, reduce number of test cases instead of truncating JSON
"""

    # =========================
    # MODE: AI ADVANCED
    # =========================
    ai_advanced_rules = """
YOU ARE A STRICT TEST DESIGN ENGINE.

ADDITIONAL QUALITY REQUIREMENTS:
- Increase diversity of test cases
- Ensure deeper edge-case coverage
- Avoid semantic duplication
- Include workflow + error handling scenarios
- Prefer realistic user behavior sequences
"""

    # =========================
    # MODE: MBT (MODEL-BASED TESTING)
    # =========================
    mbt_rules = """
YOU ARE A SOFTWARE TEST ENGINEER USING A MODEL-BASED TESTING APPROACH.

STRICT RULES:
- Generate tests ONLY from UML model
- Do NOT invent functionality outside model
- Each UML node/transition MUST be covered
- Every test MUST be traceable to UML element
- Prefer state transitions and edge transitions
- Generate between 20 and 25 unique test cases.

Generate:
- positive tests
- negative tests
- boundary tests
- workflow tests

Every UML transition should be covered at least once.
Some transitions may require multiple test cases.

Do not stop after one test per node.

COVERAGE RULE:
- Each node/edge should map to at least one test case
"""

    # select mode rules
    if mode == "AI":
        mode_rules = ai_basic_rules
    elif mode == "AI_ADV":
        mode_rules = ai_advanced_rules
    elif mode == "MBT":
        mode_rules = mbt_rules
    else:
        mode_rules = ai_basic_rules

    return f"""
SYSTEM:
{system}

APP CONTEXT:
{json.dumps(app_context, indent=2)}

{uml_section}

REQUIREMENTS:
{json.dumps(requirements, indent=2)}

{mode_rules}

OUTPUT FORMAT (STRICT):
{{
  "tests": [
    {{
      "id": "string",
      "requirement": "string",
      "title": "string",
      "preconditions": "string",
      "steps": "string",
      "expected_result": "string",
      "priority": "High|Medium|Low",
      "test_type": "Positive|Negative|Boundary|Security|Edge"
    }}
  ]
}}

FINAL RULE:
Return ONLY valid JSON. No extra text.
"""