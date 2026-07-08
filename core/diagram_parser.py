import re


def load_mermaid_file(path: str):
    """
    Converts .mmd flowchart TD into graph structure:
    {
        "nodes": set(),
        "edges": [(a,b), (c,d)]
    }
    """

    with open(path, "r") as f:
        lines = f.readlines()

    nodes = set()
    edges = []

    pattern = re.compile(r"(\w+)\[(.*?)\]\s*-->\s*(\w+)\[(.*?)\]")

    for line in lines:
        match = pattern.search(line)
        if match:
            src = match.group(2).strip()
            dst = match.group(4).strip()

            nodes.add(src)
            nodes.add(dst)
            edges.append((src, dst))

    return {
        "nodes": list(nodes),
        "edges": edges
    }


# =========================================================
# UML PARSER (.mmd → graph)
# =========================================================
def parse_mmd(path):
    nodes = set()
    edges = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if "-->" in line:
                parts = line.split("-->")
                if len(parts) == 2:
                    a = parts[0].strip().split("[")[-1].split("]")[0]
                    b = parts[1].strip().split("[")[-1].split("]")[0]

                    nodes.add(a)
                    nodes.add(b)
                    edges.append((a, b))

    return {
        "nodes": list(nodes),
        "edges": edges
    }


# =========================================================
# MBT COVERAGE (NODE + EDGE)
# =========================================================
def compute_node_edge_coverage(uml_graph, tests):
    nodes = set(uml_graph["nodes"])
    edges = set(tuple(e) for e in uml_graph["edges"])

    covered_nodes = set()
    covered_edges = set()

    for t in tests:
        def normalize_steps(steps):
            normalized = []
            for s in steps:
                if isinstance(s, dict):
                    normalized.append(s.get("step", ""))
                elif isinstance(s, str):
                    normalized.append(s)
            return " ".join(normalized)

        text = normalize_steps(t.get("steps", [])).lower()

        # NODE coverage
        for n in nodes:
            if n.lower() in text:
                covered_nodes.add(n)

        # EDGE coverage
        for a, b in edges:
            if a.lower() in text and b.lower() in text:
                covered_edges.add((a, b))

    return {
        "node_coverage": len(covered_nodes) / len(nodes) if nodes else 0,
        "edge_coverage": len(covered_edges) / len(edges) if edges else 0,
        "covered_nodes": len(covered_nodes),
        "covered_edges": len(covered_edges),
        "total_nodes": len(nodes),
        "total_edges": len(edges),
    }