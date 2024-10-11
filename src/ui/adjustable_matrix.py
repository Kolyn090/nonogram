import tkinter as tk
from adjustable_num_entry import Adjustable_Num_Entry


class Adjustable_Matrix(tk.Frame):
    def __init__(self, master=None,
                 rows=4, columns=4, entry_width=5,
                 matrix_padx=0, matrix_pady=0, max_value=999, **kwargs):
        super().__init__(master, **kwargs)
        self.rows = rows
        self.columns = columns
        self.matrix = []
        self.entry_width = entry_width
        self.matrix_padx = matrix_padx
        self.matrix_pady = matrix_pady
        self.max_value = max_value

        # Frame for the buttons
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(row=0, column=0, sticky='nsew')

        # Store references to the buttons for adding/removing rows and columns
        self.add_row_button = tk.Button(self.buttons_frame, text="+ Row", command=self.add_row)
        self.add_row_button.grid(row=0, column=0, padx=0, pady=5, sticky='ew')

        self.remove_row_button = tk.Button(self.buttons_frame, text="- Row", command=self.remove_row)
        self.remove_row_button.grid(row=0, column=1, padx=0, pady=5, sticky='ew')

        self.add_column_button = tk.Button(self.buttons_frame, text="+ Column", command=self.add_column)
        self.add_column_button.grid(row=0, column=2, padx=0, pady=5, sticky='ew')

        self.remove_column_button = tk.Button(self.buttons_frame, text="- Column", command=self.remove_column)
        self.remove_column_button.grid(row=0, column=3, padx=0, pady=5, sticky='ew')

        # Frame for the matrix of entries
        self.matrix_frame = tk.Frame(self)
        self.matrix_frame.grid(row=1, column=0, sticky='nsew')

        # Initialize the matrix with given rows and columns
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                entry = Adjustable_Num_Entry(self.matrix_frame, max_value=self.max_value, entry_width=entry_width)
                entry.grid(row=i, column=j, padx=matrix_padx, pady=matrix_pady)
                row.append(entry)
            self.matrix.append(row)

        # Position the buttons
        self.update_buttons()

    def add_row(self):
        """Add a new row of Adjustable_Num_Entry widgets."""
        new_row = []
        row_index = len(self.matrix)
        for col_index in range(self.columns):
            entry = Adjustable_Num_Entry(self.matrix_frame, max_value=self.max_value, entry_width=self.entry_width)
            entry.grid(row=row_index, column=col_index, padx=self.matrix_padx, pady=self.matrix_pady)
            new_row.append(entry)
        self.matrix.append(new_row)
        self.rows += 1
        self.update_buttons()

    def add_column(self):
        """Add a new column of Adjustable_Num_Entry widgets."""
        col_index = self.columns
        for row_index, row in enumerate(self.matrix):
            entry = Adjustable_Num_Entry(self.matrix_frame, max_value=self.max_value, entry_width=self.entry_width)
            entry.grid(row=row_index, column=col_index, padx=self.matrix_padx, pady=self.matrix_pady)
            row.append(entry)
        self.columns += 1
        self.update_buttons()

    def remove_row(self):
        """Remove the last row of Adjustable_Num_Entry widgets."""
        if self.rows > 0:
            last_row = self.matrix.pop()
            for entry in last_row:
                entry.destroy()  # Remove the widget from the grid
            self.rows -= 1
            self.update_buttons()

    def remove_column(self):
        """Remove the last column of Adjustable_Num_Entry widgets."""
        if self.columns > 0:
            for row in self.matrix:
                entry = row.pop()
                entry.destroy()  # Remove the widget from the grid
            self.columns -= 1
            self.update_buttons()

    def update_buttons(self):
        """Update the position of the add/remove row and column buttons."""
        # Enable or disable the remove buttons based on the matrix size
        if self.rows <= 1:
            self.remove_row_button.config(state='disabled')
        else:
            self.remove_row_button.config(state='normal')

        if self.columns <= 1:
            self.remove_column_button.config(state='disabled')
        else:
            self.remove_column_button.config(state='normal')


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Dynamic Adjustable Matrix")

    # Create an instance of the AdjustableMatrix class
    matrix = Adjustable_Matrix(root, rows=4, columns=4)
    matrix.pack(padx=10, pady=10)

    # Run the application
    root.mainloop()
