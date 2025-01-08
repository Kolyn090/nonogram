import os
from src.solve.solver import Solver
from src.solve.description import Description


script_dir = os.path.dirname(os.path.abspath(__file__))
save_dir = os.path.join(script_dir, 'save.non')


if __name__ == "__main__":
    description = Description()
    description.from_file(save_dir)
    solver = Solver(description)
    solver.verbose = False
    solution = solver.solve()
    if solution is None:
        print('No solution')
    print(solution)
