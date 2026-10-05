import re

def validate_variable_names(names):
    cleaned = [n.strip() for n in names if n.strip()]
    if not cleaned:
        raise ValueError("Debe existir al menos una variable.")
    if len(cleaned) != len(set(cleaned)):
        raise ValueError("Los nombres de entrada no pueden repetirse.")
    for name in cleaned:
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
            raise ValueError(f"Nombre de entrada no válido: {name}")
    return cleaned
