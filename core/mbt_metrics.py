# def compute_node_edge_coverage(uml_graph, tests):
#     nodes = set(uml_graph["nodes"])
#     edges = set(uml_graph["edges"])
#
#     covered_nodes = set()
#     covered_edges = set()
#
#     for t in tests:
#         text = " ".join([s["step"].lower() for s in t.get("steps", [])])
#
#         # NODE coverage
#         for n in nodes:
#             if n.lower() in text:
#                 covered_nodes.add(n)
#
#         # EDGE coverage (A → B must both appear in sequence)
#         for a, b in edges:
#             if a.lower() in text and b.lower() in text:
#                 covered_edges.add((a, b))
#
#     return {
#         "node_coverage": len(covered_nodes) / len(nodes) if nodes else 0,
#         "edge_coverage": len(covered_edges) / len(edges) if edges else 0,
#         "covered_nodes": len(covered_nodes),
#         "covered_edges": len(covered_edges),
#         "total_nodes": len(nodes),
#         "total_edges": len(edges),
#     }