from itertools import product
from sympy import lambdify

def generate_truth_table(expr, simplified, variables):
    fn1 = lambdify(variables, expr, "math")
    fn2 = lambdify(variables, simplified, "math")
    rows = []
    for bits in product([0, 1], repeat=len(variables)):
        original = int(bool(fn1(*bits)))
        simple = int(bool(fn2(*bits)))
        rows.append((bits, original, simple))
    return rows

def minterms_from_expression(expr, variables):
    from itertools import product
    from sympy import lambdify
    fn = lambdify(variables, expr, "math")
    result = []
    for index, bits in enumerate(product([0,1], repeat=len(variables))):
        if bool(fn(*bits)):
            result.append(index)
    return result
