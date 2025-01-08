from description import Description
from solver import Solver


if __name__ == "__main__":
    description = Description()
    description.from_file('save.non')
    solver = Solver(description)
    solver.verbose = False
    sol = solver.solve()
    if sol is None:
        print('No solution')
    print(sol)

