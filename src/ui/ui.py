import tkinter as tk
from adjustable_matrix import Adjustable_Matrix
from paintboard import PaintBoard


class UI(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        rows = Adjustable_Matrix(self, rows=10, columns=10,
                                 entry_width=2, matrix_pady=10,
                                 max_value=20, notify_on_row_change=True)
        rows.grid(row=1, column=0)
        cols = Adjustable_Matrix(self, rows=2, columns=10,
                                 entry_width=2, matrix_padx=0,
                                 max_value=20, notify_on_row_change=False)
        cols.grid(row=0, column=1)
        paintboard = PaintBoard(self, pixel_size=47)
        paintboard.grid(row=1, column=1, pady=(40, 0))

        rows.register_observer(paintboard)
        cols.register_observer(paintboard)


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Nonogram!")

    ui = UI(root)
    ui.pack()

    # Run the application
    root.mainloop()
