import tkinter as tk
from num_only_entry import Num_Only_Entry


class Adjustable_Num_Entry(tk.Frame):
    def __init__(self, master=None, max_value=20, font_size=16, **kwargs):
        # Call the parent constructor with the given arguments
        super().__init__(master, **kwargs)
        self.max_value = max_value

        # Create the Entry widget for numbers only
        self.number_entry = Num_Only_Entry(self)
        self.number_entry.grid(row=0, column=0, padx=0, sticky='ew')  # Stretch vertically

        # Create a frame to hold the increment and decrement buttons
        button_frame = tk.Frame(self, width=20)
        button_frame.grid(row=0, column=1, sticky='ns')  # Stretch vertically to match entry height
        button_frame.pack_propagate(False)  # Prevent frame from resizing to fit its content

        # Create the increment and decrement buttons with custom font size
        self.increment_button = tk.Button(
            button_frame,
            text="+",
            command=self.increment,
            font=("Helvetica", font_size),
            width=1
        )
        self.increment_button.grid(row=0, column=0, sticky='ew')  # Place in the first column

        self.decrement_button = tk.Button(
            button_frame,
            text="-",
            command=self.decrement,
            font=("Helvetica", font_size),
            width=1
        )
        self.decrement_button.grid(row=0, column=1, sticky='ew')  # Place in the second column

        # Configure column weights to allow resizing
        self.grid_columnconfigure(0, weight=1)  # Allow the entry column to expand
        self.grid_columnconfigure(1, weight=0)  # Keep the button frame's width fixed

    def get_value(self):
        # Return the current value as an integer, or 0 if empty or invalid
        try:
            return int(self.number_entry.get())
        except ValueError:
            return 0

    def set_value(self, value):
        # Set the value of the entry, ensuring it stays within the range
        if 0 <= value <= self.max_value:
            self.number_entry.delete(0, tk.END)
            self.number_entry.insert(0, str(value))

    def increment(self):
        # Increase the value by 1
        current_value = self.get_value()
        self.set_value(min(current_value + 1, self.max_value))

    def decrement(self):
        # Decrease the value by 1
        current_value = self.get_value()
        self.set_value(max(current_value - 1, 0))
