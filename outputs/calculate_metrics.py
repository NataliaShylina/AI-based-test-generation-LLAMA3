import os
import json
import glob
import pandas as pd
import numpy as np

ROOT = "."

APPROACHS = {
    "ai_basic": "AI Basic",
    "ai_advanced": "AI Advanced",
    "mbt": "LLM-assisted MBT"
}


# -----------------------------------------------------
# helper
# -----------------------------------------------------

def load_cases(filename):

    with open(filename, encoding="utf-8") as f:
        data = json.load(f)

    # JSON is a list
    if isinstance(data, list):
        return data

    # Your format
    if "tests" in data:
        return data["tests"]

    # Other possible naming
    if "test_cases" in data:
        return data["test_cases"]

    if "generated_tests" in data:
        return data["generated_tests"]

    return []


def normalize(text):

    if text is None:
        return ""

    return " ".join(text.lower().split())


# -----------------------------------------------------
# duplicate rate
# -----------------------------------------------------

def duplicate_rate(cases):

    seen = set()
    duplicates = 0

    for tc in cases:

        description = normalize(
            str(tc.get("description", ""))
        )

        title = normalize(
            str(tc.get("title", ""))
        )

        requirement = normalize(
            str(tc.get("requirement", ""))
        )

        steps = tc.get("steps", "")

        # steps can be string, list, or dictionary
        if isinstance(steps, list):
            steps_text = " ".join(
                normalize(str(item))
                for item in steps
            )

        elif isinstance(steps, dict):
            steps_text = normalize(
                json.dumps(steps, sort_keys=True)
            )

        else:
            steps_text = normalize(
                str(steps)
            )


        signature = (
            title +
            "|" +
            requirement +
            "|" +
            steps_text
        )


        if signature in seen:
            duplicates += 1
        else:
            seen.add(signature)


    if len(cases) == 0:
        return 0


    return duplicates / len(cases) * 100


# -----------------------------------------------------
# completeness
# -----------------------------------------------------

def completeness(cases):
    required = [
        "requirement",
        "title",
        "preconditions",
        "steps",
        "expected_result"
    ]

    complete = 0

    for tc in cases:

        ok = True

        for field in required:

            if field not in tc:
                ok = False
                break

            if tc[field] is None:
                ok = False
                break

            if tc[field] == "":
                ok = False
                break

            if isinstance(tc[field], (list, dict)) and len(tc[field]) == 0:
                ok = False
                break

        if ok:
            complete += 1

    if len(cases) == 0:
        return 0

    return complete / len(cases) * 100


# -----------------------------------------------------
# test type distribution
# -----------------------------------------------------

def classify(tc):

    # If the model already provides test type,
    # use it directly
    if "test_type" in tc:
        return tc["test_type"]


    txt = (
        str(tc.get("title", "")) + " " +
        str(tc.get("description", "")) + " " +
        str(tc.get("expected_result", ""))
    ).lower()


    if any(x in txt for x in [
        "invalid",
        "error",
        "reject",
        "unauthorized",
        "incorrect",
        "missing",
        "fail"
    ]):
        return "Negative"


    if any(x in txt for x in [
        "boundary",
        "minimum",
        "maximum"
    ]):
        return "Boundary"


    if any(x in txt for x in [
        "edge",
        "limit"
    ]):
        return "Edge"


    return "Positive"

# -----------------------------------------------------

rows = []

for folder, approach_name in APPROACHS.items():

    path = os.path.join(ROOT, folder)

    files = sorted(glob.glob(path + "/*.json"))
    print(folder, files)

    applications = {}

    for f in files:

        name = os.path.basename(f)

        app = name.split("_")[0].capitalize()

        if app not in applications:
            applications[app] = []

        applications[app].append(f)

    for app, run_files in applications.items():

        run_sizes = []

        all_cases = []

        valid_json = 0

        positive = negative = edge = boundary = 0

        for f in run_files:

            try:

                cases = load_cases(f)

                valid_json += 1

            except Exception:

                continue

            run_sizes.append(len(cases))

            all_cases.extend(cases)

            for tc in cases:

                t = classify(tc)

                if t == "Positive":
                    positive += 1

                elif t == "Negative":
                    negative += 1

                elif t == "Edge":
                    edge += 1

                elif t == "Boundary":
                    boundary += 1

        rows.append({

            "Application": app,

            "Approach": approach_name,

            "Mean tests/run":
                round(np.mean(run_sizes),2),

            "Std":
                round(np.std(run_sizes,ddof=1),2),

            "Variance":
                round(np.var(run_sizes,ddof=1),2),

            "Duplicate rate %":
                round(duplicate_rate(all_cases),2),

            "Completeness %":
                round(completeness(all_cases),2),

            "Positive":
                positive,

            "Negative":
                negative,

            "Edge":
                edge,

            "Boundary":
                boundary,

            "Valid JSON":
                valid_json,

            "Runs":
                len(run_files)

        })


df = pd.DataFrame(rows)

print(df)

df.to_csv("metrics_summary.csv",index=False)

print("\nSaved to metrics_summary.csv")