import json
import os
import pandas as pd


# Foldery z eksperymentami
approaches = {
    "AI Basic": "ai_basic",
    "AI Advanced": "ai_advanced",
    "LLM-assisted MBT": "mbt"
}


# Mapowanie nazw plików -> aplikacje
applications = {
    "moodle": "Moodle",
    "opencart": "OpenCart",
    "emr": "OpenEMR"
}


def count_test_cases(json_data):
    """
    Counts generated test cases inside JSON file.
    Supports common structures:
    {
        "test_cases": [...]
    }

    or direct list:
    [
        {...},
        {...}
    ]
    """

    if isinstance(json_data, list):
        return len(json_data)

    if isinstance(json_data, dict):

        # possible key names
        possible_keys = [
            "test_cases",
            "testCases",
            "tests",
            "testcases"
        ]

        for key in possible_keys:
            if key in json_data:
                return len(json_data[key])

    return 0



results = []


for approach_name, folder in approaches.items():

    for filename in os.listdir(folder):

        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(folder, filename)

        # detect application
        application = None

        for key, value in applications.items():
            if key in filename.lower():
                application = value
                break

        if application is None:
            continue


        valid_json = True
        number_of_tests = 0


        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            number_of_tests = count_test_cases(data)

        except Exception as e:
            valid_json = False


        results.append(
            {
                "Application": application,
                "Approach": approach_name,
                "Run": filename,
                "Generated test cases": number_of_tests,
                "Valid JSON": valid_json
            }
        )



df = pd.DataFrame(results)


# Summary table
summary = (
    df.groupby(["Application", "Approach"])
    .agg(
        {
            "Generated test cases": "sum",
            "Valid JSON": "sum",
            "Run": "count"
        }
    )
    .reset_index()
)


summary.rename(
    columns={
        "Valid JSON": "Valid JSON responses",
        "Run": "Experimental runs"
    },
    inplace=True
)


print("\nDetailed results:")
print(df)


print("\nSummary table:")
print(summary)


# Save result
summary.to_csv(
    "generation_summary.csv",
    index=False
)

print("\nSaved: generation_summary.csv")