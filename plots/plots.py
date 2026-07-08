import matplotlib.pyplot as plt


def plot_metrics(ai, mbt, save_path="comparison.png"):
    labels = ["Coverage", "Traceability"]

    x = range(len(labels))

    plt.figure()

    plt.bar(x, ai, width=0.4, label="AI", align="edge")
    plt.bar(x, mbt, width=-0.4, label="MBT", align="edge")

    plt.xticks(x, labels)
    plt.legend()
    plt.title("AI vs MBT Comparison")

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_metric(values, labels, title, save_path=None):
    plt.figure()
    plt.bar(labels, values)
    plt.title(title)

    if save_path is None:
        save_path = f"{title.replace(' ', '_')}.png"

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()