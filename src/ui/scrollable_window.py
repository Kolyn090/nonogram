import tkinter as tk
from tkinter import ttk


class Scrollable_Window(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        # Create a frame inside the canvas to hold the content
        self.scrollable_frame = tk.Frame(self.canvas)

        # Bind the frame to the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # Create a window inside the canvas that contains the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configure the canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar into the main frame
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")


if __name__ == "__main__":
    # Create the main application window
    root = tk.Tk()
    root.title("Scrollable Window Example")

    # Create a scrollable window frame inside the root window
    scrollable_window = Scrollable_Window(root, width=400, height=300)
    scrollable_window.pack(fill="both", expand=True)

    # Add some widgets inside the scrollable frame for demonstration
    for i in range(50):
        label = tk.Label(scrollable_window.scrollable_frame, text=f"Label {i}")
        label.pack(pady=5)

    # Run the main loop
    root.mainloop()
