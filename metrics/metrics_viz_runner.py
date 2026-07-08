from metrics.metrics import run_metrics

def run_all_visuals(results):

    run_counts = {
        k: v["run_counts"]
        for k, v in results.items()
    }

    plot_boxplot(run_counts)

    heatmap_data = {
        k: v["mbt"] for k, v in results.items() if v["mbt"]
    }

    plot_heatmap(heatmap_data)