from sympy.logic.boolalg import And, Or, Not, Xor
from models.circuit import Circuit, CircuitNode

def build_circuit(expr):
    nodes = []
    counter = [0]
    def walk(e):
        counter[0] += 1
        nid = f"n{counter[0]}"
        if isinstance(e, Not):
            inp = walk(e.args[0])
            nodes.append(CircuitNode(nid, "NOT", [inp]))
        elif isinstance(e, And):
            ins = [walk(a) for a in e.args]
            nodes.append(CircuitNode(nid, "AND", ins))
        elif isinstance(e, Or):
            ins = [walk(a) for a in e.args]
            nodes.append(CircuitNode(nid, "OR", ins))
        elif isinstance(e, Xor):
            ins = [walk(a) for a in e.args]
            nodes.append(CircuitNode(nid, "XOR", ins))
        else:
            nodes.append(CircuitNode(nid, "INPUT", [], str(e)))
        return nid
    out = walk(expr)
    return Circuit(expr, nodes, "F")
