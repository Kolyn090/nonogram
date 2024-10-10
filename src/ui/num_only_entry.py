import tkinter as tk


class Num_Only_Entry(tk.Entry):
    def __init__(self, master=None, max_value=18, **kwargs):
        # Call the parent constructor with the given arguments
        super().__init__(master, **kwargs)
        self.max_value = max_value

        # Register the validation function
        vcmd = (self.register(self.validate_input), '%P')

        # Configure the entry widget with the validation command
        self.config(validate='key', validatecommand=vcmd)

    def validate_input(self, new_value):
        # Allow only empty input or digits that are less than max_value and is not zero
        if new_value.isdigit():
            return int(new_value) <= self.max_value and int(new_value) != 0
        return new_value.isdigit() or new_value == ""
