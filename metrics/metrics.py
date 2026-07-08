import json
import numpy as np
import pandas as pd
from collections import Counter
from pathlib import Path

from plots.metrics_viz import plot_all_thesis_visuals
from metrics.stats_ttest import run_ttest
from export.excel_export import export_latex
from core.diagram_parser import load_mermaid_file, parse_mmd, compute_node_edge_coverage

from core.diagram_parser import load_mermaid_file
# =========================================================
# LOAD TESTS
# =========================================================
def load_tests(path):
    with open(path, "r") as f:
        return json.load(f)["tests"]


# =========================================================
# DUPLICATES
# =========================================================
def compute_duplicates(tests):
    seen = set()
    dup = 0

    for t in tests:
        key = (t.get("title"), t.get("requirement"))
        if key in seen:
            dup += 1
        else:
            seen.add(key)

    return dup, len(tests)


# =========================================================
# DISTRIBUTION
# =========================================================
def compute_distribution(tests):
    c = Counter(t.get("test_type", "Unknown") for t in tests)

    return {
        "Positive": c.get("Positive", 0),
        "Negative": c.get("Negative", 0),
        "Edge": c.get("Edge", 0),
        "Boundary": c.get("Boundary", 0),
        "Security": c.get("Security", 0),
    }


# =========================================================
# COMPLETENESS
# =========================================================
def compute_completeness(tests):
    miss_pre = 0
    miss_exp = 0

    for t in tests:
        if not t.get("preconditions"):
            miss_pre += 1
        if not t.get("expected_result"):
            miss_exp += 1

    return {
        "missing_preconditions": miss_pre,
        "missing_expected": miss_exp
    }


# =========================================================
# VARIANCE
# =========================================================
def compute_variance(run_test_counts):
    arr = np.array(run_test_counts)

    return {
        "mean": float(np.mean(arr)),
        "variance": float(np.var(arr)),
        "std_dev": float(np.std(arr)),
        "min": int(np.min(arr)),
        "max": int(np.max(arr)),
        "all_run_counts": list(run_test_counts)
    }


# =========================================================
# ANALYZE ONE GROUP
# =========================================================
def analyze_group(files, uml_file=None):
    all_tests = []
    run_counts = []
    for f in files:
        tests = load_tests(f)
        all_tests.extend(tests)
        run_counts.append(len(tests))

    dup, total = compute_duplicates(all_tests)
    mbt_data = {}

    if uml_file:
        from core.diagram_parser import parse_mmd, compute_node_edge_coverage
        uml_graph = parse_mmd(uml_file)
        mbt_data = compute_node_edge_coverage(uml_graph, all_tests)

    return {
        "total_tests": total,
        "duplicates": dup,
        "duplicate_rate": dup / total if total else 0,
        "distribution": compute_distribution(all_tests),
        "completeness": compute_completeness(all_tests),
        "variance": compute_variance(run_counts),
        "run_counts": run_counts,
        "mbt": mbt_data
    }


def run_all_metrics():
    base = Path("outputs")
    experiments = {
        "AI_BASIC": {"files": sorted((base / "ai_basic").glob("*.json")), "uml": None},
        "AI_ADV": {"files": sorted((base / "ai_advanced").glob("*.json")), "uml": None},
        "MBT": {"files": sorted((base / "mbt").glob("*.json")), "uml": "diagrams/moodle.mmd"}
    }

    results = {group: analyze_group(cfg["files"], cfg["uml"]) for group, cfg in experiments.items()}

    # Exporting results
    export_to_csv_simple(results)
    export_latex(results)

    # Statistical analysis
    stats = run_ttest(
        results["AI_BASIC"]["run_counts"],
        results["AI_ADV"]["run_counts"],
        results["MBT"]["run_counts"]
    )
    print("\n--- STATISTICAL RESULTS ---")
    print(stats)

    # Visualization trigger
    print("Generating 10+ thesis plots in /plots folder...")
    plot_all_thesis_visuals(results)

    return results

def export_to_csv_simple(results):
    """Czysty eksport danych, bez mieszania z logiką wykresów."""
    data = []
    for g, d in results.items():
        row = {"Group": g, "Total": d["total_tests"], "DupRate": d["duplicate_rate"],
               "Mean": d["variance"]["mean"], "Std": d["variance"]["std_dev"]}
        if d.get("mbt"):
            row.update({"NodeCov": d["mbt"].get("node_coverage", 0),
                        "EdgeCov": d["mbt"].get("edge_coverage", 0)})
        data.append(row)
    pd.DataFrame(data).to_csv("summary_metrics.csv", index=False)

if __name__ == "__main__":
    run_all_metrics()