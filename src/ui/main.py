import tkinter as tk
from src.ui.ui import UI
from src.ui.scrollable_window import Scrollable_Window


def main():
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


if __name__ == '__main__':
    main()
