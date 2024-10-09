from enum import Enum


class SolverResult(Enum):
    SOLVED = 0
    AMBIGUOUS = 1
    IMPOSSIBLE = 2
    NOT_ATTEMPTED = 3
