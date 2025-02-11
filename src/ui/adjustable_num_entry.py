import tkinter as tk
from tkinter import ttk


class Adjustable_Num_Entry(tk.Frame):
    def __init__(self, master=None, min_value=0, max_value=20, entry_width=3, **kwargs):
        super().__init__(master, **kwargs)
        self.min_value = min_value
        self.max_value = max_value

        # Create a style for the Spinbox using ttk
        style = ttk.Style(self)
        style.configure(
            "Custom.TSpinbox",
            arrowsize=15,  # Adjust the size of the arrows if desired
            background="gray",  # Background for the entry and arrows
            foreground="black",  # Text color
            fieldbackground="lightgray"  # Background of the entry area (field)
        )

        # Create a validation function for numeric input
        vcmd = (self.register(self.validate_numeric_input), '%P')

        # Create the Spinbox using ttk and apply the custom style
        self.spinbox = ttk.Spinbox(
            self,
            from_=min_value,
            to=self.max_value,
            increment=1,
            width=entry_width,
            style="Custom.TSpinbox",  # Use the custom style
            validate='key',  # Trigger validation on keypress
            validatecommand=vcmd  # Use the validation function
        )
        self.spinbox.grid(row=0, column=0, padx=0, pady=0, sticky='ew')
        self.spinbox.set(self.min_value)

    def validate_numeric_input(self, new_value):
        # Allow only empty input or digits within the specified range
        if new_value.isdigit() or new_value == "":
            if new_value == "":
                return True
            if self.min_value <= int(new_value) <= self.max_value:
                return True
        return False

    # Function to get the value from the Spinbox
    def get_spinbox_value(self):
        value = self.spinbox.get()
        return int(value)

    def set_to(self, num):
        self.spinbox.set(num)
