from sympy import false, true
from sympy.logic.boolalg import And, Or, Not
from .boolean_engine import expression_to_text

def _factor_common(expr):
    # Produce educational transformations for common SOP cases.
    terms = list(expr.args) if isinstance(expr, Or) else [expr]
    if len(terms) < 2:
        return None
    factors = []
    for term in terms:
        factors.append(set(term.args) if isinstance(term, And) else {term})
    common = set.intersection(*factors) if factors else set()
    if common:
        common_expr = next(iter(common))
        rest = []
        for f in factors:
            remaining = f - common
            rest.append(next(iter(remaining)) if len(remaining)==1 else And(*remaining) if remaining else true)
        inside = Or(*rest)
        return common_expr, inside
    return None

def build_steps(original, simplified):
    steps = [("Paso 0", expression_to_text(original), "Función original")]
    factored = _factor_common(original)
    if factored:
        common, inside = factored
        steps.append(("Paso 1", f"{expression_to_text(common)}({expression_to_text(inside)})",
                      "Ley distributiva (factor común)"))
        # Complementary pair inside -> 1.
        args = list(inside.args) if isinstance(inside, Or) else [inside]
        if len(args) == 2 and any(a == ~b or b == ~a for a in args):
            steps.append(("Paso 2", expression_to_text(common), "Ley del complemento: X + X' = 1; ley de identidad: X·1 = X"))
    if expression_to_text(simplified) != expression_to_text(original):
        if not any(s[1] == expression_to_text(simplified) for s in steps):
            steps.append((f"Paso {len(steps)}", expression_to_text(simplified),
                          "Aplicación de leyes de álgebra booleana / simplificación lógica"))
    return steps
