from dataclasses import dataclass, field
from sympy import Expr

@dataclass
class BooleanExpression:
    original_text: str
    expression: Expr
    variables: list = field(default_factory=list)
    simplified: Expr | None = None
    minterms: list[int] = field(default_factory=list)
    dont_cares: list[int] = field(default_factory=list)
    variable_labels: list[str] = field(default_factory=list)
