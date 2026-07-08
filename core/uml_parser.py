import re
import networkx as nx


def parse_mmd(file_path: str):
    """
    Parses Mermaid flowchart TD into a graph
    """

    with open(file_path, "r") as f:
        lines = f.readlines()

    edges = []
    nodes = set()

    pattern = re.compile(r"(\w+)\[([^\]]+)\]\s*-->\s*(\w+)\[([^\]]+)\]")

    for line in lines:
        match = pattern.search(line)
        if match:
            src_id, src_label, dst_id, dst_label = match.groups()

            nodes.add(src_label.strip())
            nodes.add(dst_label.strip())

            edges.append((src_label.strip(), dst_label.strip()))

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    return {
        "graph": G,
        "nodes": list(nodes),
        "edges": edges
    }