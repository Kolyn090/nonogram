import tkinter as tk
from tkinter import ttk


class Adjustable_Num_Entry(tk.Frame):
    def __init__(self, master=None, max_value=20, entry_width=3, **kwargs):
        super().__init__(master, **kwargs)
        self.max_value = max_value

        # Create a style for the Spinbox using ttk
        style = ttk.Style(self)
        style.configure(
            "Custom.TSpinbox",
            arrowsize=15,  # Adjust the size of the arrows if desired
            background="gray",  # Background for the entry and arrows
            foreground="white",  # Text color
            fieldbackground="lightgray"  # Background of the entry area (field)
        )

        # Create a validation function for numeric input
        vcmd = (self.register(self.validate_numeric_input), '%P')

        # Create the Spinbox using ttk and apply the custom style
        self.spinbox = ttk.Spinbox(
            self,
            from_=1,
            to=self.max_value,
            increment=1,
            width=entry_width,
            style="Custom.TSpinbox",  # Use the custom style
            validate='key',  # Trigger validation on keypress
            validatecommand=vcmd  # Use the validation function
        )
        self.spinbox.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.spinbox.set(1)

    def validate_numeric_input(self, new_value):
        # Allow only empty input or digits within the specified range
        if new_value.isdigit() or new_value == "":
            if new_value == "":
                return True
            if 1 <= int(new_value) <= self.max_value:
                return True
        return False

    # Function to get the value from the Spinbox
    def get_spinbox_value(self):
        value = self.spinbox.get()
        print(f"Spinbox Value: {value}")
        return value
