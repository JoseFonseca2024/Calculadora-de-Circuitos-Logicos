from dataclasses import dataclass, field

@dataclass
class CircuitNode:
    node_id: str
    gate: str
    inputs: list[str] = field(default_factory=list)
    output: str = ""

@dataclass
class Circuit:
    expression: object
    nodes: list[CircuitNode] = field(default_factory=list)
    output: str = "F"
