import re

from sympy import symbols, true, false
from sympy.logic import SOPform


def _tokenize(text: str, variable_names: list[str]):
    """
    Convierte la expresión en tokens respetando las variables
    configuradas por el usuario.

    Ejemplo:

        A'B'CD'

    se convierte en:

        ~A * ~B * C * ~D

    y NO interpreta CD como una sola variable.
    """

    s = text.strip()

    # ----------------------------------------------------------
    # Normalización básica
    # ----------------------------------------------------------

    if "=" in s:
        s = s.split("=", 1)[1].strip()

    s = s.replace("¬", "~")
    s = s.replace("!", "~")

    s = s.replace("’", "'")
    s = s.replace("‘", "'")

    s = s.replace("·", "*")

    s = re.sub(
        r"\bAND\b",
        "*",
        s,
        flags=re.I
    )

    s = re.sub(
        r"\bOR\b",
        "+",
        s,
        flags=re.I
    )

    s = re.sub(
        r"\bNOT\b",
        "~",
        s,
        flags=re.I
    )

    # ----------------------------------------------------------
    # Variables
    # ----------------------------------------------------------

    # Las más largas primero.
    # Esto permite trabajar también con X1, X2, X10, etc.
    variables = sorted(
        variable_names,
        key=len,
        reverse=True
    )

    tokens = []

    i = 0

    while i < len(s):

        # Ignorar espacios
        if s[i].isspace():
            i += 1
            continue

        # ------------------------------------------------------
        # Operadores y paréntesis
        # ------------------------------------------------------

        if s[i] in "+*~^()":

            tokens.append(s[i])

            i += 1

            continue

        # ------------------------------------------------------
        # True / False
        # ------------------------------------------------------

        if s.startswith("True", i):

            tokens.append("True")

            i += 4

            continue

        if s.startswith("False", i):

            tokens.append("False")

            i += 5

            continue

        # ------------------------------------------------------
        # Buscar variable configurada
        # ------------------------------------------------------

        matched_variable = None

        for variable in variables:

            if s.startswith(variable, i):

                matched_variable = variable

                break

        if matched_variable is None:

            raise ValueError(
                "Símbolo o variable no reconocida "
                f"cerca de: {s[i:]}"
            )

        i += len(matched_variable)

        # ------------------------------------------------------
        # Complemento mediante apostrofe
        # ------------------------------------------------------

        complemented = False

        while i < len(s) and s[i] == "'":

            complemented = not complemented

            i += 1

        if complemented:

            tokens.append(
                "~" + matched_variable
            )

        else:

            tokens.append(
                matched_variable
            )

    return tokens


def _insert_implicit_multiplication(tokens):
    """
    Inserta * cuando existe multiplicación implícita.

    Ejemplos:

        AB       -> A * B
        A(B+C)   -> A * (B+C)
        (A+B)C   -> (A+B) * C
        A~B      -> A * ~B
    """

    result = []

    def is_operand_end(token):

        return (
            token == ")"
            or token == "True"
            or token == "False"
            or (
                token not in {
                    "+",
                    "*",
                    "~",
                    "^",
                    "(",
                    ")"
                }
            )
        )

    def is_operand_start(token):

        return (
            token == "("
            or token == "~"
            or token == "True"
            or token == "False"
            or (
                token not in {
                    "+",
                    "*",
                    "~",
                    "^",
                    "(",
                    ")"
                }
            )
        )

    for token in tokens:

        if result:

            previous = result[-1]

            if (
                is_operand_end(previous)
                and is_operand_start(token)
            ):

                result.append("*")

        result.append(token)

    return result


def _tokens_to_python(tokens):
    """
    Convierte los tokens a una expresión válida para SymPy/Python.
    """

    result = []

    for token in tokens:

        if token == "+":

            result.append("|")

        elif token == "*":

            result.append("&")

        elif token == "~":

            result.append("~")

        elif token == "^":

            result.append("^")

        elif token.startswith("~"):

            # Variable complementada.
            result.append(
                "~" + token[1:]
            )

        else:

            result.append(token)

    return " ".join(result)


def parse_expression(
    text: str,
    variable_names: list[str]
):
    """
    Analiza una expresión booleana respetando las variables
    configuradas por el usuario.
    """

    if not variable_names:

        raise ValueError(
            "No hay variables configuradas."
        )

    tokens = _tokenize(
        text,
        variable_names
    )

    tokens = _insert_implicit_multiplication(
        tokens
    )

    python_expr = _tokens_to_python(
        tokens
    )

    # ----------------------------------------------------------
    # Símbolos SymPy
    # ----------------------------------------------------------

    syms = {
        name: symbols(
            name,
            boolean=True
        )
        for name in variable_names
    }

    local = {
        **syms,
        "True": true,
        "False": false
    }

    # ----------------------------------------------------------
    # Evaluación segura
    # ----------------------------------------------------------

    try:

        expr = eval(
            python_expr,
            {
                "__builtins__": {}
            },
            local
        )

    except Exception as exc:

        raise ValueError(
            "No se pudo interpretar la expresión: "
            f"{exc}"
        ) from exc

    return expr


def parse_minterms(
    text: str,
    variable_names: list[str]
):
    """
    Convierte:

        Σm(0,1,2,5,8,9,10,13)

    en una expresión SOP de SymPy y devuelve también
    la lista de minterms.
    """

    compact = text.replace(
        " ",
        ""
    )

    # Acepta Σm(...) y Σ(...)
    match = re.search(
        r"Σm?\((.*?)\)",
        compact,
        flags=re.I
    )

    # También acepta sum(...) / summ(...)
    if not match:

        match = re.search(
            r"sum[m]?\((.*?)\)",
            compact,
            flags=re.I
        )

    if not match:

        raise ValueError(
            "Formato esperado: Σm(1,3,5,7)"
        )

    raw = match.group(1).strip()

    if not raw:

        raise ValueError(
            "Debe indicar al menos un minterm."
        )

    try:

        values = sorted(
            set(
                int(x)
                for x in raw.split(",")
                if x != ""
            )
        )

    except ValueError as exc:

        raise ValueError(
            "Los minterms deben ser números enteros."
        ) from exc

    limit = 2 ** len(variable_names)

    if any(
        x < 0 or x >= limit
        for x in values
    ):

        raise ValueError(
            f"Los minterms deben estar entre "
            f"0 y {limit - 1}."
        )

    syms = [
        symbols(
            variable,
            boolean=True
        )
        for variable in variable_names
    ]

    expression = SOPform(
        syms,
        values
    )

    return expression, values