import tkinter as tk
from src.ui.matrix_subject import Matrix_Subject
from src.ui.adjustable_num_entry import Adjustable_Num_Entry


class Adjustable_Matrix(tk.Frame, Matrix_Subject):
    def __init__(self, master=None,
                 rows=4, columns=4, entry_width=5,
                 matrix_padx=0, matrix_pady=0, max_value=999,
                 notify_on_row_change=False, **kwargs):
        super().__init__(master, **kwargs)
        self._observers = []
        self.rows = rows
        self.columns = columns
        self.matrix = []
        self.entry_width = entry_width
        self.matrix_padx = matrix_padx
        self.matrix_pady = matrix_pady
        self.max_value = max_value
        self.notify_on_row_change = notify_on_row_change

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
        self.matrix_frame.grid(row=1, column=0, sticky='es')

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
        if self.notify_on_row_change:
            self.update_observer_axis('col', self.rows)
        else:
            self.update_observer_axis('row', self.columns)

        if self.rows <= 1:
            self.remove_row_button.config(state='disabled')
        else:
            self.remove_row_button.config(state='normal')

        if self.columns <= 1:
            self.remove_column_button.config(state='disabled')
        else:
            self.remove_column_button.config(state='normal')

    def get_vectors(self):
        result = []
        if self.notify_on_row_change:
            for i in range(self.rows):
                vector = []
                for j in range(self.columns):
                    vector.append(self.matrix[i][j].get_spinbox_value())
                result.append(vector)
        else:
            for i in range(self.columns):
                vector = []
                for j in range(self.rows):
                    vector.append(self.matrix[j][i].get_spinbox_value())
                result.append(vector)
        return result

    def set_to_zero(self):
        for i in range(self.rows):
            for j in range(self.columns):
                self.matrix[i][j].set_to(0)

    def load(self, matrix):
        def len_of_longest_row(matrix):
            result = 0
            for row in matrix:
                if len(row) > result:
                    result = len(row)
            return result

        num_of_rows = len(matrix)
        num_of_cols = len_of_longest_row(matrix)

        if self.notify_on_row_change:
            while self.rows < num_of_rows:
                self.add_row()
            while self.rows > num_of_rows:
                self.remove_row()
            while self.columns < num_of_cols:
                self.add_column()
            while self.columns > num_of_cols:
                self.remove_column()
        else:  # The transpose
            while self.rows < num_of_cols:
                self.add_row()
            while self.rows > num_of_cols:
                self.remove_row()
            while self.columns < num_of_rows:
                self.add_column()
            while self.columns > num_of_rows:
                self.remove_column()

        for i in range(self.rows):
            for j in range(self.columns):
                if self.notify_on_row_change:
                    if 0 <= i < len(matrix) and 0 <= j < len(matrix[i]):
                        self.matrix[i][j].set_to(matrix[i][j])
                    else:
                        self.matrix[i][j].set_to(0)
                else:
                    if 0 <= j < len(matrix) and 0 <= i < len(matrix[j]):
                        self.matrix[i][j].set_to(matrix[j][i])
                    else:
                        self.matrix[i][j].set_to(0)


if __name__ == '__main__':
    # Create the main window
    root = tk.Tk()
    root.title("Dynamic Adjustable Matrix")

    # Create an instance of the AdjustableMatrix class
    matrix = Adjustable_Matrix(root, rows=4, columns=4)
    matrix.pack(padx=10, pady=10)

    # Run the application
    root.mainloop()
