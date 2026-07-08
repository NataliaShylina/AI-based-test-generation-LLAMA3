import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ==============================
# Configuration
# ==============================

BASE_DIR = "."
OUTPUT_DIR = "generated_figures"

APPROACHES = {
    "ai_basic": "AI Basic",
    "ai_advanced": "AI Advanced",
    "mbt": "LLM-assisted MBT"
}

APPLICATIONS = {
    "emr": "OpenEMR",
    "moodle": "Moodle",
    "opencart": "OpenCart"
}


os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================
# Helper functions
# ==============================

def load_json_files():

    rows = []

    for folder, approach_name in APPROACHES.items():

        folder_path = os.path.join(BASE_DIR, folder)

        for app_code, app_name in APPLICATIONS.items():

            tests_per_run = []

            all_tests = []


            for run in range(1, 4):

                file_path = os.path.join(
                    folder_path,
                    f"{app_code}_run{run}.json"
                )

                if not os.path.exists(file_path):
                    continue


                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)


                tests = data.get("tests", [])


                tests_per_run.append(len(tests))

                all_tests.extend(tests)


            if len(tests_per_run) == 0:
                continue


            mean_tests = np.mean(tests_per_run)
            variance = np.var(
                tests_per_run,
                ddof=1
            ) if len(tests_per_run) > 1 else 0


            duplicate_percentage = calculate_duplicates(
                all_tests
            )


            completeness = calculate_completeness(
                all_tests
            )


            distribution = calculate_distribution(
                all_tests
            )


            rows.append({

                "Application": app_name,
                "Approach": approach_name,

                "Mean tests/run": round(mean_tests,2),
                "Variance": round(variance,2),

                "Duplicate rate %": round(
                    duplicate_percentage,2
                ),

                "Completeness %": round(
                    completeness,2
                ),

                "Positive": distribution["Positive"],
                "Negative": distribution["Negative"],
                "Edge": distribution["Edge"],
                "Boundary": distribution["Boundary"],

                "Runs": len(tests_per_run)

            })


    return pd.DataFrame(rows)



def normalize_text(value):

    if isinstance(value, list):

        return " ".join(
            str(x)
            for x in value
        )

    if isinstance(value, dict):

        return json.dumps(
            value,
            sort_keys=True
        )

    return str(value)



def calculate_duplicates(tests):

    if len(tests) == 0:
        return 0


    descriptions = []


    for t in tests:

        text = (
            normalize_text(t.get("title",""))
            + " "
            + normalize_text(t.get("steps",""))
            + " "
            + normalize_text(t.get("expected_result",""))
        )

        descriptions.append(
            text.lower()
        )


    duplicates = 0
    unique = set()


    for item in descriptions:

        if item in unique:
            duplicates += 1

        else:
            unique.add(item)


    return duplicates / len(tests) * 100



def calculate_completeness(tests):

    if len(tests)==0:
        return 0


    required = [
        "preconditions",
        "steps",
        "expected_result"
    ]


    valid = 0


    for t in tests:

        if all(
            key in t and str(t[key]).strip()
            for key in required
        ):
            valid += 1


    return valid / len(tests) * 100



def calculate_distribution(tests):

    result = {
        "Positive":0,
        "Negative":0,
        "Edge":0,
        "Boundary":0
    }


    for t in tests:

        test_type = str(
            t.get(
                "test_type",
                ""
            )
        ).lower()


        if "positive" in test_type:
            result["Positive"] += 1

        elif "negative" in test_type:
            result["Negative"] += 1

        elif "edge" in test_type:
            result["Edge"] += 1

        elif "boundary" in test_type:
            result["Boundary"] += 1


    return result



# ==============================
# Plot functions
# ==============================


def save_barplot(
        df,
        value,
        filename,
        title
):

    plt.figure(figsize=(10,5))

    pivot = df.pivot(
        index="Application",
        columns="Approach",
        values=value
    )

    pivot.plot(
        kind="bar"
    )

    plt.title(title)

    plt.ylabel(value)

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            filename
        ),
        dpi=300
    )

    plt.close()



def create_distribution_plot(df):

    dist = df.melt(
        id_vars=[
            "Application",
            "Approach"
        ],
        value_vars=[
            "Positive",
            "Negative",
            "Edge",
            "Boundary"
        ],
        var_name="Type",
        value_name="Count"
    )


    plt.figure(figsize=(10,6))

    for approach in dist["Approach"].unique():

        subset = dist[
            dist["Approach"]==approach
        ]

        plt.plot(
            subset["Type"],
            subset["Count"],
            marker="o",
            label=approach
        )


    plt.title(
        "Distribution of generated test types"
    )

    plt.ylabel(
        "Number of tests"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "test_distribution.png"
        ),
        dpi=300
    )

    plt.close()



# ==============================
# Main
# ==============================


if __name__ == "__main__":


    df = load_json_files()


    print(df)


    csv_path = os.path.join(
        OUTPUT_DIR,
        "evaluation_results.csv"
    )

    df.to_csv(
        csv_path,
        index=False
    )


    save_barplot(
        df,
        "Duplicate rate %",
        "duplicate_rate.png",
        "Duplicate rate comparison"
    )


    save_barplot(
        df,
        "Mean tests/run",
        "mean_tests.png",
        "Average number of generated tests"
    )


    save_barplot(
        df,
        "Variance",
        "variance.png",
        "Generation variance"
    )


    save_barplot(
        df,
        "Completeness %",
        "completeness.png",
        "Completeness comparison"
    )


    create_distribution_plot(df)


    print(
        "\nFinished. Figures saved in:",
        OUTPUT_DIR
    )