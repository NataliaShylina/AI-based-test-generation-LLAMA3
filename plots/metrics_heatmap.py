import matplotlib.pyplot as plt
import numpy as np


def plot_heatmap(mbt_results):
    # Filter keys to only those that have the required data
    valid_labels = [k for k in mbt_results.keys()
                    if "node_coverage" in mbt_results[k]
                    and "edge_coverage" in mbt_results[k]]

    if not valid_labels:
        print("Error: No valid coverage data found.")
        return

    node_cov = [mbt_results[k]["node_coverage"] for k in valid_labels]
    edge_cov = [mbt_results[k]["edge_coverage"] for k in valid_labels]

    data = np.array([node_cov, edge_cov])

    plt.figure(figsize=(8, 4))
    plt.imshow(data, cmap="Blues", aspect="auto")

    plt.yticks([0, 1], ["Node Coverage", "Edge Coverage"])
    plt.xticks(range(len(valid_labels)), valid_labels)

    plt.colorbar(label="Coverage")

    plt.title("MBT Coverage Heatmap")

    plt.show()