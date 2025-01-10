import cv2
import tkinter as tk
from src.solve.solver import Solver
from src.ui.paintboard import Paintboard
from src.ui.adjustable_matrix import Adjustable_Matrix
from src.image_recognition.main import get_two_vector_matrices
from src.solve.description import Description
from src.draw.binary_to_ascii_art import Binary_To_Ascii_Art
from src.draw.pixels_to_description import Pixels_To_Description


class UI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.draw_mode = False

        self.rows = Adjustable_Matrix(self, rows=10, columns=2,
                                      entry_width=2, matrix_pady=10,
                                      max_value=20, notify_on_row_change=True)
        self.rows.grid(row=1, column=0)
        self.cols = Adjustable_Matrix(self, rows=2, columns=10,
                                      entry_width=2, matrix_padx=0,
                                      max_value=20, notify_on_row_change=False)
        self.cols.grid(row=0, column=1)
        self.paintboard = Paintboard(self, pixel_size=47)
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

        experimental_button = tk.Button(button_frame, text="Experimental", command=self.import_by_screenshot)
        experimental_button.grid(row=4, column=0)

        self.draw_text = "Draw"
        self.stop_draw_text = "Stop draw"
        self.draw_button = tk.Button(button_frame, text=self.draw_text, command=self.press_draw_button)
        self.draw_button.grid(row=5, column=0)

        self.finish_button = tk.Button(button_frame, text="Finish", command=self.finish_draw)
        self.finish_button.grid(row=6, column=0)
        self.finish_button.config(state=tk.DISABLED)

        self.default_buttons = [solve_button, reset_button, export_button,
                                import_button, experimental_button, self.draw_button]
        self.draw_mode_buttons = [reset_button, self.draw_button, self.finish_button]

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
        self.paintboard.reset()

    def export_file(self):
        save_content = [f'width {self.rows.rows}', f'height {self.cols.columns}\n\nrows']
        for vector in self.rows.get_vectors():
            save_content.append(','.join([str(component) for component in vector]))
        save_content.append('\ncolumns')
        for vector in self.cols.get_vectors():
            save_content.append(','.join([str(component) for component in vector]))
        with open('../solve/save.non', 'w') as file:
            file.writelines([f'{line}\n' for line in save_content])

    def import_file(self):
        description = Description()
        description.from_file('../solve/save.non')
        self.rows.load(description.row_descriptions)
        self.cols.load(description.column_descriptions)
        self.paintboard.reset()

    def import_by_screenshot(self):
        rows_vectors, cols_vectors, width, height = get_two_vector_matrices()
        description = Description()
        description.from_matrices(rows_vectors, cols_vectors, width, height)
        self.rows.load(description.row_descriptions)
        self.cols.load(description.column_descriptions)
        self.paintboard.reset()

    def press_draw_button(self):
        def enter_draw_mode():
            self.draw_mode = True
            self.paintboard.start_draw_mode()
            self.draw_button.config(text=self.stop_draw_text)
            for i in range(len(self.default_buttons)):
                self.default_buttons[i].config(state=tk.DISABLED)
            for i in range(len(self.draw_mode_buttons)):
                self.draw_mode_buttons[i].config(state=tk.NORMAL)

        def exit_draw_mode():
            self.draw_mode = False
            self.paintboard.end_draw_mode()
            self.draw_button.config(text=self.draw_text)
            for i in range(len(self.draw_mode_buttons)):
                self.draw_mode_buttons[i].config(state=tk.DISABLED)
            for i in range(len(self.default_buttons)):
                self.default_buttons[i].config(state=tk.NORMAL)

        if not self.draw_mode:
            enter_draw_mode()
        else:
            exit_draw_mode()
        self.paintboard.reset()

    def finish_draw(self):
        binary_image = self.paintboard.get_binary_image()
        cv2.imwrite('test.png', binary_image)
        btaa = Binary_To_Ascii_Art(binary_image)
        ptd = Pixels_To_Description(btaa.pixels)
        description = ptd.description
        self.rows.load(description.row_descriptions)
        self.cols.load(description.column_descriptions)
        self.paintboard.render_picture(btaa.pixels)
