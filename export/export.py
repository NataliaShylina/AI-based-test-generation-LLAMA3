from metrics.stats_ttest import run_ttest
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

stats = run_ttest(results)

export_statistics_latex(stats)

print(stats)