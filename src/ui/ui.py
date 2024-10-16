import tkinter as tk
from adjustable_matrix import Adjustable_Matrix
from paintboard import PaintBoard
from description import Description
from solver import Solver
from scrollable_window import Scrollable_Window
from src.image_recognition.main import get_two_vector_matrices


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

        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0)

        solve_button = tk.Button(button_frame, text="Solve", command=self.solve)
        solve_button.grid(row=0, column=0)

        reset_button = tk.Button(button_frame, text="Reset", command=self.reset)
        reset_button.grid(row=1, column=0)

        export_button = tk.Button(button_frame, text="Export", command=self.export_file)
        export_button.grid(row=2, column=0)

        import_button = tk.Button(button_frame, text="Import", command=self.import_file)
        import_button.grid(row=3, column=0)

        import_plus_button = tk.Button(button_frame, text="Import+", command=self.import_by_screenshot)
        import_plus_button.grid(row=4, column=0)

    def solve(self):
        description = Description()
        width = len(self.cols.get_vectors())
        height = len(self.rows.get_vectors())
        description.from_matrices(self.rows.get_vectors(), self.cols.get_vectors(), width, height)
        solver = Solver(description)
        solver.verbose = False
        sol = solver.solve()
        if sol is None:
            print('No solution')
        else:
            self.paintboard.render_picture(sol.pixels)

    def reset(self):
        self.rows.set_to_zero()
        self.cols.set_to_zero()
        self.paintboard.render_picture([[False for _ in range(self.rows.rows)] for _ in range(self.cols.columns)])

    def export_file(self):
        save_content = [f'width {self.rows.rows}', f'height {self.cols.columns}\n\nrows']
        for vector in self.rows.get_vectors():
            save_content.append(','.join([str(component) for component in vector]))
        save_content.append('\ncolumns')
        for vector in self.cols.get_vectors():
            save_content.append(','.join([str(component) for component in vector]))
        with open('../save.non', 'w') as file:
            file.writelines([f'{line}\n' for line in save_content])

    def import_file(self):
        description = Description()
        description.from_file('../save.non')
        self.rows.load(description.row_descriptions)
        self.cols.load(description.column_descriptions)
        self.paintboard.render_picture([[False for _ in range(self.rows.rows)] for _ in range(self.cols.columns)])

    def import_by_screenshot(self):
        rows_vectors, cols_vectors, width, height = get_two_vector_matrices()
        description = Description()
        description.from_matrices(rows_vectors, cols_vectors, width, height)
        self.rows.load(description.row_descriptions)
        self.cols.load(description.column_descriptions)
        self.paintboard.render_picture([[False for _ in range(self.rows.rows)] for _ in range(self.cols.columns)])


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Nonogram!")
    scrollable_window = Scrollable_Window(root)
    scrollable_window.pack(fill="both", expand=True)
    scrollable_window.canvas.config(width=1000, height=1000)

    ui = UI(scrollable_window.scrollable_frame)
    ui.pack()

    # Run the application
    root.mainloop()
