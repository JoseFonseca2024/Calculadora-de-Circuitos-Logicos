import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from sympy.logic.boolalg import And, Or, Not, Xor

def render_circuit(expr, path, title="Circuito lógico"):
    G = nx.DiGraph()
    labels = {}
    gate_types = {}
    counter = [0]
    levels = {}

    def walk(e, level=0):
        counter[0] += 1
        nid = f"n{counter[0]}"
        levels[nid] = level
        if isinstance(e, Not):
            gate_types[nid] = "NOT"
            child = walk(e.args[0], level+1)
            G.add_edge(child, nid)
        elif isinstance(e, And):
            gate_types[nid] = "AND"
            for a in e.args:
                G.add_edge(walk(a, level+1), nid)
        elif isinstance(e, Or):
            gate_types[nid] = "OR"
            for a in e.args:
                G.add_edge(walk(a, level+1), nid)
        elif isinstance(e, Xor):
            gate_types[nid] = "XOR"
            for a in e.args:
                G.add_edge(walk(a, level+1), nid)
        else:
            gate_types[nid] = "INPUT"
            labels[nid] = str(e)
        return nid

    output = walk(expr)
    G.add_node("F")
    G.add_edge(output, "F")
    gate_types["F"] = "OUTPUT"
    labels["F"] = "F"

    pos = {}
    by_level = {}
    for node, lvl in levels.items():
        by_level.setdefault(lvl, []).append(node)
    for lvl, nodes in by_level.items():
        for i, node in enumerate(nodes):
            pos[node] = (lvl, -i)
    pos["F"] = (max([p[0] for p in pos.values()], default=0)+1, 0)

    fig, ax = plt.subplots(figsize=(11, 6))
    for u,v in G.edges:
        x1,y1 = pos[u]; x2,y2 = pos[v]
        ax.annotate("", xy=(x2-0.12,y2), xytext=(x1+0.12,y1),
                    arrowprops=dict(arrowstyle="->", lw=1.4))
    for node,(x,y) in pos.items():
        kind = gate_types.get(node, "")
        if kind == "INPUT":
            label = labels[node]
            ax.text(x,y,label,ha="center",va="center",fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="black"))
        elif kind == "OUTPUT":
            ax.text(x,y,labels[node],ha="center",va="center",fontsize=11,
                    bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="black"))
        else:
            ax.text(x,y,kind,ha="center",va="center",fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.45", fc="white", ec="black"))
    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(fig)
