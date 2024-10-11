import tkinter as tk
from adjustable_matrix import Adjustable_Matrix
from paintboard import PaintBoard
from description import Description
from solver import Solver
from scrollable_window import Scrollable_Window


class UI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = Adjustable_Matrix(self, rows=10, columns=2,
                                      entry_width=2, matrix_pady=10,
                                      max_value=20, notify_on_row_change=True)
        self.rows.grid(row=1, column=0)
        self.cols = Adjustable_Matrix(self, rows=2, columns=10,
                                      entry_width=2, matrix_padx=0,
                                      max_value=20, notify_on_row_change=False)
        self.cols.grid(row=0, column=1)
        self.paintboard = PaintBoard(self, pixel_size=47)
        self.paintboard.grid(row=1, column=1, pady=(40, 0))

        self.rows.register_observer(self.paintboard)
        self.cols.register_observer(self.paintboard)

        solve_button = tk.Button(self, text="Solve", command=self.solve)
        solve_button.grid(row=0, column=2)

    def solve(self):
        description = Description()
        description.from_matrices(self.rows.get_vectors(), self.cols.get_vectors())
        solver = Solver(description)
        solver.verbose = False
        sol = solver.solve()
        if sol is None:
            print('No solution')
        else:
            self.paintboard.render_picture(sol.pixels)


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Nonogram!")
    scrollable_window = Scrollable_Window(root)
    scrollable_window.pack(fill="both", expand=True)

    ui = UI(scrollable_window.scrollable_frame)
    ui.pack()

    # Run the application
    root.mainloop()
