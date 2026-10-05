from itertools import product


GRAY = {
    1: ["0", "1"],

    2: ["00", "01", "11", "10"],

    3: [
        "000", "001", "011", "010",
        "110", "111", "101", "100"
    ],

    4: [
        "0000", "0001", "0011", "0010",
        "0110", "0111", "0101", "0100",
        "1100", "1101", "1111", "1110",
        "1010", "1011", "1001", "1000"
    ],
}


# ==============================================================
# DIMENSIONES DEL MAPA
# ==============================================================

def dimensions(n):

    if n == 1:
        return 1, 2

    if n == 2:
        return 2, 2

    if n == 3:
        return 2, 4

    if n == 4:
        return 4, 4

    return None


# ==============================================================
# COORDENADAS DE LAS CELDAS
# ==============================================================

def cell_coordinates(n):

    if n > 4:
        return None

    dims = dimensions(n)

    if dims is None:
        return None

    r, c = dims

    row_variable_count = max(1, n // 2)
    col_variable_count = max(1, n - row_variable_count)

    row_bits = GRAY[row_variable_count]
    col_bits = GRAY[col_variable_count]

    cells = []

    for ri in range(r):

        for ci in range(c):

            bits = (
                row_bits[ri]
                + col_bits[ci]
            )

            cells.append(
                (
                    ri,
                    ci,
                    int(bits, 2),
                    bits
                )
            )

    return cells


# ==============================================================
# CONSTRUIR MAPA
# ==============================================================

def build_kmap(n, minterms):

    coords = cell_coordinates(n)

    if coords is None:
        return None, {}

    data = {}

    for r, c, m, bits in coords:

        value = 1 if m in minterms else 0

        data[(r, c)] = (
            value,
            m
        )

    return dimensions(n), data


# ==============================================================
# AGRUPACIONES
# ==============================================================

def grouping_candidates(n, minterms):

    if n > 4:
        return []

    coords = cell_coordinates(n)

    if coords is None:
        return []

    cells = {
        (r, c): m
        for r, c, m, _ in coords
        if m in minterms
    }

    groups = []

    max_r, max_c = dimensions(n)

    sizes = [
        (1, 1),
        (1, 2),
        (1, 4),

        (2, 1),
        (2, 2),
        (2, 4),

        (4, 1),
        (4, 2),
        (4, 4),
    ]

    for h, w in sizes:

        if h > max_r or w > max_c:
            continue

        for r0 in range(max_r):

            for c0 in range(max_c):

                poss = {
                    (
                        (r0 + dr) % max_r,
                        (c0 + dc) % max_c
                    )
                    for dr in range(h)
                    for dc in range(w)
                }

                if not poss:
                    continue

                if not poss.issubset(cells):
                    continue

                ms = sorted(
                    cells[p]
                    for p in poss
                )

                if ms not in [
                    g["minterms"]
                    for g in groups
                ]:

                    groups.append(
                        {
                            "minterms": ms,
                            "cells": sorted(poss),
                            "size": h * w
                        }
                    )

    # Primero las agrupaciones más grandes
    groups.sort(
        key=lambda g: (
            -g["size"],
            len(g["minterms"])
        )
    )

    chosen = []
    covered = set()

    for group in groups:

        new = (
            set(group["minterms"])
            - covered
        )

        if new or not chosen:

            chosen.append(group)

            covered |= set(
                group["minterms"]
            )

        if covered >= set(minterms):
            break

    return chosen


# ==============================================================
# ETIQUETAS DEL MAPA DE KARNAUGH
# ==============================================================

def kmap_labels(variables):

    n = len(variables)

    if n < 2:
        raise ValueError(
            "El mapa de Karnaugh requiere al menos 2 variables."
        )

    if n > 4:
        raise ValueError(
            "El mapa gráfico está limitado a 4 variables."
        )

    row_count = max(
        1,
        n // 2
    )

    col_count = max(
        1,
        n - row_count
    )

    row_variables = variables[
        :row_count
    ]

    col_variables = variables[
        row_count:
    ]

    rows = GRAY[row_count]

    cols = GRAY[col_count]

    return (
        row_variables,
        col_variables,
        rows,
        cols
    )