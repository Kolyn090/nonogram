from enum import Enum


# Original Java Version by fedimser: https://github.com/fedimser/nonolab
# Translated by Kolyn090

class SolverResult(Enum):
    SOLVED = 0
    AMBIGUOUS = 1
    IMPOSSIBLE = 2
    NOT_ATTEMPTED = 3
