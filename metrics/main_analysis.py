# main_analysis.py
from metrics.metrics import run_all_metrics
from plots.metrics_viz import plot_boxplot
from export.excel_export import export_latex
from export.excel_export import export_excel



# ... inne importy

def main():
    # 1. Oblicz metryki i wygeneruj wykresy (to wywoła też export_to_csv)
    results = run_all_metrics()

    # 2. Generowanie tabeli LaTeX
    export_latex(results)

    # 3. Export Excela
    export_excel(results)


if __name__ == "__main__":
    main()