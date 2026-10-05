"""Tkinter user interface: drawing, controls, animation and status panels."""

from __future__ import annotations

import time
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Dict, Iterator, List, Optional, Tuple

from . import constants as const
from .algorithms import bfs_solve_steps, dfs_generate_steps
from .maze import Coord, Maze

FONT = "Helvetica"


class MazeApp:
    """Main application window.

    The UI never blocks: every animation is a generator whose events are
    consumed a few at a time from a Tk ``after`` callback.
    """

    IDLE, GENERATING, SOLVING = "idle", "generating", "solving"

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Maze Generator - DFS with Backtracking")
        root.configure(bg=const.COLOR_BG)
        root.geometry(f"{const.WINDOW_WIDTH}x{const.WINDOW_HEIGHT}")
        root.minsize(const.MIN_WINDOW_WIDTH, const.MIN_WINDOW_HEIGHT)

        self.maze: Optional[Maze] = None
        self.state = self.IDLE
        self.cell_colors: Dict[Coord, str] = {}
        self._layout: Tuple[int, int, int] = (0, 0, 1)  # x0, y0, cell size
        self._events: Optional[Iterator] = None
        self._handler: Optional[Callable] = None
        self._on_done: Optional[Callable[[], None]] = None
        self._after_id: Optional[str] = None
        self._resize_id: Optional[str] = None
        self._algo_time = 0.0
        self._bfs_explored = 0
        self._solution: List[Coord] = []

        self._build_widgets()
        self._bind_keys()
        self._reset_all()

    # ------------------------------------------------------------ widget setup
    def _build_widgets(self) -> None:
        root = self.root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)

        header = tk.Frame(root, bg=const.COLOR_BG)
        header.grid(row=0, column=0, sticky="ew", pady=(12, 4))
        tk.Label(header, text=const.APP_TITLE, font=(FONT, 24, "bold"),
                 fg=const.COLOR_WALL, bg=const.COLOR_BG).pack()
        tk.Label(header, text=const.APP_SUBTITLE, font=(FONT, 11),
                 fg=const.COLOR_VISITED, bg=const.COLOR_BG).pack()

        controls = tk.Frame(root, bg=const.COLOR_PANEL, padx=10, pady=8)
        controls.grid(row=1, column=0, sticky="ew", padx=12, pady=4)

        self.rows_var = tk.StringVar(value=str(const.DEFAULT_ROWS))
        self.cols_var = tk.StringVar(value=str(const.DEFAULT_COLS))
        self.speed_var = tk.IntVar(value=const.DEFAULT_SPEED)

        self._label(controls, "Rows").pack(side="left", padx=(0, 4))
        self._entry(controls, self.rows_var).pack(side="left", padx=(0, 10))
        self._label(controls, "Columns").pack(side="left", padx=(0, 4))
        self._entry(controls, self.cols_var).pack(side="left", padx=(0, 14))

        self._label(controls, "Speed:  Slow").pack(side="left")
        tk.Scale(controls, from_=const.MIN_SPEED, to=const.MAX_SPEED,
                 orient="horizontal", variable=self.speed_var, showvalue=False,
                 length=130, bg=const.COLOR_PANEL, fg=const.COLOR_TEXT,
                 troughcolor=const.COLOR_BG, highlightthickness=0
                 ).pack(side="left", padx=4)
        self._label(controls, "Fast").pack(side="left", padx=(0, 14))

        buttons = (
            ("Generate (G)", self.on_generate, "#2980B9"),
            ("Solve (S)", self.on_solve, "#8E44AD"),
            ("Clear", self.on_clear, "#7F8C8D"),
            ("Reset (R)", self.on_reset, "#C0392B"),
        )
        for text, command, color in buttons:
            tk.Button(controls, text=text, command=command, bg=color,
                      fg="white", activebackground=color, activeforeground="white",
                      relief="flat", padx=10, pady=4, font=(FONT, 10, "bold")
                      ).pack(side="left", padx=3)

        self.canvas = tk.Canvas(root, bg=const.COLOR_BG, highlightthickness=0)
        self.canvas.grid(row=2, column=0, sticky="nsew", padx=12, pady=4)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        info = tk.Frame(root, bg=const.COLOR_PANEL, padx=12, pady=8)
        info.grid(row=3, column=0, sticky="ew", padx=12, pady=(4, 12))
        info.columnconfigure(0, weight=1)
        info.columnconfigure(1, weight=1)

        self.status_var = tk.StringVar()
        self.algorithm_var = tk.StringVar()
        self.size_var = tk.StringVar()
        self.phase_var = tk.StringVar()
        left = tk.Frame(info, bg=const.COLOR_PANEL)
        left.grid(row=0, column=0, sticky="nw")
        for var in (self.status_var, self.algorithm_var, self.size_var, self.phase_var):
            self._label(left, textvariable=var).pack(anchor="w")

        self.stat_vars = {key: tk.StringVar() for key in
                          ("cells", "visited", "gen", "explored", "solve", "path")}
        right = tk.Frame(info, bg=const.COLOR_PANEL)
        right.grid(row=0, column=1, sticky="nw")
        for var in self.stat_vars.values():
            self._label(right, textvariable=var).pack(anchor="w")

    @staticmethod
    def _label(parent: tk.Widget, text: str = "", **kwargs) -> tk.Label:
        return tk.Label(parent, text=text, bg=parent.cget("bg"),
                        fg=const.COLOR_TEXT, font=(FONT, 10), **kwargs)

    @staticmethod
    def _entry(parent: tk.Widget, variable: tk.StringVar) -> tk.Entry:
        return tk.Entry(parent, textvariable=variable, width=5, justify="center",
                        bg=const.COLOR_BG, fg=const.COLOR_TEXT,
                        insertbackground=const.COLOR_TEXT, relief="flat",
                        highlightthickness=1, highlightbackground="#444444",
                        highlightcolor=const.COLOR_VISITED)

    def _bind_keys(self) -> None:
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Escape>", lambda _event: self.on_escape())

    def _on_key(self, event: tk.Event) -> None:
        try:
            focused = self.root.focus_get()
        except KeyError:
            focused = None
        if isinstance(focused, tk.Entry):   # let the user type numbers freely
            return
        key = event.keysym.lower()
        if key == "g":
            self.on_generate()
        elif key == "s":
            self.on_solve()
        elif key == "r":
            self.on_reset()

    # ------------------------------------------------------------- text panels
    def _set_status(self, text: str) -> None:
        self.status_var.set(f"Status: {text}")

    def _reset_stats(self) -> None:
        for var, text in zip(self.stat_vars.values(), (
                "Total cells: -", "Visited cells (DFS): -",
                "Generation time: -", "Cells explored (BFS): -",
                "Solving time: -", "Solution path length: -")):
            var.set(text)

    def _clear_solve_stats(self) -> None:
        self.stat_vars["explored"].set("Cells explored (BFS): -")
        self.stat_vars["solve"].set("Solving time: -")
        self.stat_vars["path"].set("Solution path length: -")

    # ---------------------------------------------------------------- drawing
    def _on_canvas_resize(self, _event: tk.Event) -> None:
        if self._resize_id is not None:
            self.root.after_cancel(self._resize_id)
        self._resize_id = self.root.after(80, self._redraw_all)

    def _compute_layout(self) -> None:
        if self.maze is None:
            return
        width = max(self.canvas.winfo_width(), 1)
        height = max(self.canvas.winfo_height(), 1)
        pad = const.CANVAS_PADDING
        size = max(2, min((width - 2 * pad) // self.maze.cols,
                          (height - 2 * pad) // self.maze.rows))
        x0 = (width - size * self.maze.cols) // 2
        y0 = (height - size * self.maze.rows) // 2
        self._layout = (x0, y0, size)

    def _color_of(self, coord: Coord) -> str:
        assert self.maze is not None
        if coord == self.maze.start:
            return const.COLOR_START
        if coord == self.maze.end:
            return const.COLOR_END
        return self.cell_colors.get(coord, const.COLOR_UNVISITED)

    def _draw_cell(self, coord: Coord) -> None:
        """(Re)draw one cell: its fill colour and whichever walls still exist."""
        assert self.maze is not None
        row, col = coord
        x0, y0, size = self._layout
        tag = f"cell_{row}_{col}"
        self.canvas.delete(tag)
        left, top = x0 + col * size, y0 + row * size
        right, bottom = left + size, top + size
        self.canvas.create_rectangle(left, top, right, bottom,
                                     fill=self._color_of(coord), outline="", tags=tag)
        walls = self.maze.cell(coord).walls
        width = 2 if size >= 12 else 1
        segments = {"top": (left, top, right, top), "right": (right, top, right, bottom),
                    "bottom": (left, bottom, right, bottom), "left": (left, top, left, bottom)}
        for name, points in segments.items():
            if walls[name]:
                self.canvas.create_line(*points, fill=const.COLOR_WALL,
                                        width=width, capstyle="projecting", tags=tag)

    def _set_color(self, coord: Coord, color: str) -> None:
        self.cell_colors[coord] = color
        self._draw_cell(coord)

    def _redraw_all(self) -> None:
        self._resize_id = None
        self.canvas.delete("all")
        if self.maze is None:
            return
        self._compute_layout()
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                self._draw_cell((row, col))

    # -------------------------------------------------------------- animation
    def _speed_params(self) -> Tuple[int, int]:
        """Return (delay in ms, events per tick) for the current slider value."""
        speed = self.speed_var.get()
        return max(1, 200 >> (speed - 1)), 1 + max(0, speed - 8) * 4

    def _start_animation(self, events: Iterator, handler: Callable,
                         on_done: Callable[[], None]) -> None:
        self._events, self._handler, self._on_done = events, handler, on_done
        self._after_id = self.root.after(1, self._tick)

    def _stop_animation(self) -> None:
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
        self._after_id = None
        self._events = self._handler = self._on_done = None

    def _tick(self) -> None:
        self._after_id = None
        if self._events is None or self._handler is None:
            return
        delay, batch = self._speed_params()
        for _ in range(batch):
            began = time.perf_counter()
            try:
                event = next(self._events)
            except StopIteration:
                self._algo_time += time.perf_counter() - began
                callback = self._on_done
                self._events = self._handler = self._on_done = None
                if callback:
                    callback()
                return
            self._algo_time += time.perf_counter() - began
            self._handler(event)
        self._after_id = self.root.after(delay, self._tick)

    # ----------------------------------------------------------- generate flow
    def _read_size(self) -> Tuple[int, int]:
        try:
            rows = int(self.rows_var.get().strip())
            cols = int(self.cols_var.get().strip())
        except ValueError:
            raise ValueError("Rows and columns must be whole numbers, e.g. 20.") from None
        Maze.validate_size(rows, cols)
        return rows, cols

    def on_generate(self) -> None:
        if self.state != self.IDLE:
            messagebox.showwarning(
                "Busy", "An animation is running. Wait for it to finish or press Esc.")
            return
        try:
            rows, cols = self._read_size()
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return
        self.maze = Maze(rows, cols)
        self.cell_colors.clear()
        self._solution = []
        self._reset_stats()
        self.stat_vars["cells"].set(f"Total cells: {rows * cols}")
        self.size_var.set(f"Cells: {rows} \u00d7 {cols}")
        self.algorithm_var.set("Algorithm: DFS (generation)")
        self.phase_var.set("Generation: In progress")
        self._set_status("Generating maze...")
        self.state = self.GENERATING
        self._algo_time = 0.0
        self._redraw_all()
        self._start_animation(dfs_generate_steps(self.maze),
                              self._handle_generation_event, self._finish_generation)

    def _handle_generation_event(self, event: Tuple[str, Coord, Optional[Coord]]) -> None:
        kind, first, second = event
        if kind == "start":
            self._set_color(first, const.COLOR_CURRENT)
        elif kind == "carve":                       # wall removed between first/second
            self._set_color(first, const.COLOR_VISITED)
            self._set_color(second, const.COLOR_CURRENT)    # type: ignore[arg-type]
        elif kind == "backtrack":
            self._set_color(first, const.COLOR_BACKTRACK)
            if second is not None:
                self._set_color(second, const.COLOR_CURRENT)

    def _finish_generation(self) -> None:
        assert self.maze is not None
        self.cell_colors.clear()
        self._redraw_all()
        self.state = self.IDLE
        self.stat_vars["visited"].set(f"Visited cells (DFS): {self.maze.count_visited()}")
        self.stat_vars["gen"].set(f"Generation time: {self._algo_time * 1000:.2f} ms")
        self.phase_var.set("Generation: Complete")
        self._set_status("Maze generated successfully")

    # --------------------------------------------------------------- solve flow
    def on_solve(self) -> None:
        if self.maze is None:
            messagebox.showwarning("No maze", "Generate a maze first (press G).")
            return
        if self.state != self.IDLE:
            messagebox.showwarning(
                "Busy", "An animation is running. Wait for it to finish or press Esc.")
            return
        self._clear_solution_visuals()
        self.state = self.SOLVING
        self.algorithm_var.set("Algorithm: BFS (solving)")
        self._set_status("Solving maze using BFS...")
        self._algo_time = 0.0
        self._bfs_explored = 0
        self._solution = []
        self._start_animation(bfs_solve_steps(self.maze),
                              self._handle_search_event, self._after_search)

    def _handle_search_event(self, event: Tuple[str, object]) -> None:
        kind, payload = event
        if kind == "visit":
            self._bfs_explored += 1
            self._set_color(payload, const.COLOR_VISITED)       # type: ignore[arg-type]
        elif kind == "done":
            self._solution = list(payload)                      # type: ignore[arg-type]

    def _after_search(self) -> None:
        self.stat_vars["explored"].set(f"Cells explored (BFS): {self._bfs_explored}")
        self.stat_vars["solve"].set(f"Solving time: {self._algo_time * 1000:.2f} ms")
        if not self._solution:
            self.state = self.IDLE
            self._set_status("No solution found")
            return
        self._set_status("Drawing solution path...")
        self._start_animation(iter(self._solution),
                              self._handle_path_event, self._finish_solving)

    def _handle_path_event(self, coord: Coord) -> None:
        self._set_color(coord, const.COLOR_PATH)

    def _finish_solving(self) -> None:
        self.state = self.IDLE
        self.stat_vars["path"].set(f"Solution path length: {len(self._solution)} cells")
        self._set_status("Solution found!")

    # -------------------------------------------------- clear / reset / escape
    def _clear_solution_visuals(self) -> None:
        self.cell_colors.clear()
        self._solution = []
        self._clear_solve_stats()
        self._redraw_all()

    def on_clear(self) -> None:
        if self.maze is None:
            return
        if self.state == self.GENERATING:
            messagebox.showwarning("Busy", "Maze generation is running. Press Esc to cancel it.")
            return
        self._stop_animation()
        self.state = self.IDLE
        self._clear_solution_visuals()
        self.algorithm_var.set("Algorithm: DFS (generation)")
        self._set_status("Solution cleared - maze kept")

    def on_reset(self) -> None:
        self._reset_all()

    def on_escape(self) -> None:
        if self.state == self.GENERATING:       # half-built maze is useless
            self._reset_all()
            self._set_status("Generation cancelled")
        elif self.state == self.SOLVING:
            self._stop_animation()
            self.state = self.IDLE
            self._clear_solution_visuals()
            self._set_status("Solving stopped")

    def _reset_all(self) -> None:
        self._stop_animation()
        self.state = self.IDLE
        self.maze = None
        self.cell_colors.clear()
        self._solution = []
        self.rows_var.set(str(const.DEFAULT_ROWS))
        self.cols_var.set(str(const.DEFAULT_COLS))
        self.speed_var.set(const.DEFAULT_SPEED)
        self._reset_stats()
        self.algorithm_var.set("Algorithm: DFS (generation)")
        self.size_var.set("Cells: -")
        self.phase_var.set("Generation: Not started")
        self._set_status("Ready - press Generate Maze")
        self._redraw_all()
