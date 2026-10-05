from sympy.logic.boolalg import simplify_logic
from sympy import false, true

def simplify_expression(expr):
    return simplify_logic(expr, form="dnf", force=True)

def equivalent(a, b):
    return simplify_logic(a ^ b, force=True) == false

def expression_to_text(expr):
    if expr is true:
        return "1"
    if expr is false:
        return "0"
    s = str(expr)
    s = s.replace(" & ", "·").replace(" | ", " + ")
    s = s.replace("~", "¬")
    return s
