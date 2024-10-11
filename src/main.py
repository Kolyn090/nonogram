import tkinter as tk
from description import Description
from solver import Solver
from ui.paintboard import PaintBoard


if __name__ == "__main__":
    description = Description()
    description.from_file('abc.non')
    solver = Solver(description)
    solver.verbose = False
    sol = solver.solve()
    if sol is None:
        print('No solution')
    print(sol)

    root = tk.Tk()
    root.title('Nonogram!')
    paintboard = PaintBoard(root, picture=sol.pixels)
    paintboard.pack()
    root.mainloop()
