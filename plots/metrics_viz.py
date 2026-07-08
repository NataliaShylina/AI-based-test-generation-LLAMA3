import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Create plots folder if it doesn't exist
os.makedirs("plots", exist_ok=True)


def save_plot(name):
    plt.savefig(f"plots/{name}.pdf", dpi=300, bbox_inches="tight")
    plt.close()


def plot_all_thesis_visuals(results):
    # 1-3. Basic Stats
    plot_total_tests(results)
    plot_duplicate_rate(results)
    plot_mean_suite_size(results)

    # 4. Variance/Stability
    plot_boxplot_stability(results)

    # 5. Distributions
    plot_distribution_stacked(results)

    # 6. Completeness
    plot_completeness(results)

    # 7. MBT Coverage (Heatmap style)
    plot_mbt_coverage(results)

    # 8. Efficiency (DupRate vs Total)
    plot_efficiency_scatter(results)

    # 9. Test Type Ratios (Normalized)
    plot_normalized_distribution(results)

    # 10. Std Dev / Reliability
    plot_reliability_bar(results)


def plot_total_tests(results):
    df = pd.DataFrame({k: v["total_tests"] for k, v in results.items()}, index=["Total"]).T
    df.plot(kind='bar', color='skyblue', legend=False)
    plt.title("Total Test Cases Generated")
    save_plot("total_tests")


def plot_duplicate_rate(results):
    data = {k: v["duplicate_rate"] * 100 for k, v in results.items()}
    plt.bar(data.keys(), data.values(), color='salmon')
    plt.title("Duplicate Test Rate (%)")
    save_plot("dup_rate")


def plot_mean_suite_size(results):
    means = {k: v["variance"]["mean"] for k, v in results.items()}
    plt.bar(means.keys(), means.values(), color='lightgreen')
    plt.title("Average Test Suite Size")
    save_plot("mean_suite_size")


def plot_boxplot_stability(results):
    plt.figure()
    data = [v["run_counts"] for v in results.values()]
    plt.boxplot(data, labels=results.keys())
    plt.title("Test Suite Stability (Variance in Run Counts)")
    save_plot("boxplot_stability")


def plot_distribution_stacked(results):
    df = pd.DataFrame({k: v["distribution"] for k, v in results.items()}).T
    df.plot(kind='bar', stacked=True)
    plt.title("Test Type Distribution")
    save_plot("dist_stacked")


def plot_completeness(results):
    df = pd.DataFrame({k: v["completeness"] for k, v in results.items()}).T
    df.plot(kind='bar')
    plt.title("Missing Data Points (Completeness)")
    save_plot("completeness")


def plot_mbt_coverage(results):
    mbt_data = {k: v["mbt"] for k, v in results.items() if v["mbt"]}
    if not mbt_data: return
    df = pd.DataFrame(mbt_data).T[["node_coverage", "edge_coverage"]]
    df.plot(kind='bar')
    plt.title("MBT Coverage Analysis")
    save_plot("mbt_coverage")


def plot_efficiency_scatter(results):
    x = [v["total_tests"] for v in results.values()]
    y = [v["duplicate_rate"] for v in results.values()]
    plt.scatter(x, y)
    plt.xlabel("Total Tests");
    plt.ylabel("Dup Rate")
    plt.title("Efficiency: Total vs Duplicates")
    save_plot("efficiency_scatter")


def plot_normalized_distribution(results):
    df = pd.DataFrame({k: v["distribution"] for k, v in results.items()}).T
    df_norm = df.div(df.sum(axis=1), axis=0)
    df_norm.plot(kind='bar', stacked=True)
    plt.title("Normalized Test Type Distribution (%)")
    save_plot("norm_dist")


def plot_reliability_bar(results):
    data = {k: v["variance"]["std_dev"] for k, v in results.items()}
    plt.bar(data.keys(), data.values(), color='orange')
    plt.title("Suite Reliability (Standard Deviation)")
    save_plot("reliability_std")