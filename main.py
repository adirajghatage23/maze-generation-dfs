"""Entry point: run ``python main.py`` to start the Maze Generator."""

import sys


def main() -> None:
    try:
        import tkinter as tk
    except ImportError:
        sys.exit(
            "Tkinter is not installed. On Ubuntu/Debian run: "
            "sudo apt install python3-tk"
        )
    from src.gui import MazeApp

    root = tk.Tk()
    MazeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
