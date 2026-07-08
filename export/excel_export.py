import pandas as pd

# =========================================================
# EXPORT EXCEL (SAFE - fallback if no openpyxl)
# =========================================================
def export_excel(results, path="metrics.xlsx"):
    rows = []

    for group, data in results.items():
        print(f"DEBUG keys for {group}: {data['variance'].keys()}")
        rows.append({
            "Group": group,
            "Total": data["total_tests"],
            "Duplicates": data["duplicates"],
            "DupRate": data["duplicate_rate"],
            "Positive": data["distribution"]["Positive"],
            "Negative": data["distribution"]["Negative"],
            "Edge": data["distribution"]["Edge"],
            "Mean": data["variance"]["mean"],
            "Std": data["variance"]["std_dev"],
            "NodeCov": data.get("mbt", {}).get("node_coverage", None),
            "EdgeCov": data.get("mbt", {}).get("edge_coverage", None),
        })

    df = pd.DataFrame(rows)

    try:
        df.to_excel(path, index=False)
    except ImportError:
        print("openpyxl missing → saving CSV instead")
        df.to_csv(path.replace(".xlsx", ".csv"), index=False)


# =========================================================
# EXPORT LATEX
# =========================================================
def export_latex(results, path="metrics.tex"):
    latex = r"\begin{table}[h]\centering\begin{tabular}{lrrrrr}\hline\n"
    latex += "Group & Total & Duplicates & Mean & Std & NodeCov \\\\ \\hline\n"

    for g, d in results.items():
        latex += f"{g} & {d['total_tests']} & {d['duplicates']} & "
        # Change 'std' to 'std_dev' here:
        latex += f"{d['variance']['mean']:.2f} & {d['variance']['std_dev']:.2f} & "
        latex += f"{d.get('mbt', {}).get('node_coverage', 0):.2f} \\\\\n"

    latex += r"\hline\end{tabular}\caption{Test Generation Metrics}\end{table}"

    with open(path, "w") as f:
        f.write(latex)

def export_statistics_latex(stats, filename="statistics.tex"):

    with open(filename, "w") as f:

        f.write(r"\begin{table}[ht]" + "\n")
        f.write(r"\centering" + "\n")
        f.write(r"\caption{Statistical comparison}" + "\n")
        f.write(r"\begin{tabular}{lcc}" + "\n")
        f.write(r"\hline" + "\n")
        f.write(r"Comparison & t & p \\" + "\n")
        f.write(r"\hline" + "\n")

        for name, result in stats.items():

            if name in ("ANOVA", "summary"):
                continue

            f.write(
                f"{name.replace('_', ' ')} & "
                f"{result.statistic:.2f} & "
                f"{result.pvalue:.4f} \\\\\n"
            )

        f.write(r"\hline" + "\n")
        f.write(r"\end{tabular}" + "\n")
        f.write(r"\end{table}" + "\n")