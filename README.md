# Maze Generation Using Depth-First Search (DFS)

A desktop mini project that **generates random mazes with DFS + backtracking**,
animates every step, and **solves them with BFS (shortest path)**.
Built with Python 3 and Tkinter only (no third-party packages).

> Replace the placeholders marked `YOUR ...` (see [Author](#author) and `LICENSE`) before submitting.

## About

Pick a size, press **Generate**, and watch DFS carve passages through a grid of
walls. Press **Solve** and watch BFS flood outward and then draw the shortest path.

## Features

- Randomized DFS maze generation using an **explicit stack** (no recursion limit)
- Live animation: current cell, visited cells, chosen neighbour, wall removal, backtracking
- BFS solver with animated search and final path
- Speed slider (Slow to Fast); the UI never freezes (uses `after()`, never `sleep()`)
- Rows/columns input with validation (2-60), friendly error messages
- Status panel and statistics (cells, visited, times, path length)
- Keyboard shortcuts, dark theme, resizable window
- Unit tests with `unittest`

## Demo

Add your screenshots to `screenshots/` and link them here (see [Screenshots](#screenshots)).

## Algorithms Used

| Task | Algorithm | Why |
|------|-----------|-----|
| **Generation** | **DFS with backtracking** | Goes deep first, creating long winding corridors; dead ends trigger backtracking |
| **Solving** | **BFS** | Explores level by level, so the first time it reaches the end is the **shortest** path |

- **DFS**: explore as far as possible along one branch before going back.
- **Backtracking**: when a cell has no unvisited neighbours, pop the stack and return to the previous cell.
- **BFS**: uses a queue; every cell remembers its *parent* so the path can be rebuilt from end to start.
- **Randomized generation**: the next neighbour is chosen with `random.choice`, so each maze differs.

## How It Works

1. Create a grid where every cell has 4 walls (top, right, bottom, left).
2. Start at `(0, 0)`, mark it visited, push it on the stack.
3. Look at the top cell of the stack. Collect its **unvisited** neighbours.
4. If there are any: pick one at random, **remove the wall** between the two cells, mark it visited, push it.
5. If there are none: **pop** the stack (backtrack).
6. Repeat until the stack is empty. Every cell is now connected and there are no loops
   (a *perfect maze*: exactly one path between any two cells).

Maze representation: each cell is a small `dataclass` (`Cell`) with `row`, `col`, `visited`
and a `walls` dictionary. A dataclass was chosen over plain dicts because it gives named
fields, type hints and safe default values, which keeps the code readable.

## Technologies

```
Python 3 | Tkinter | DFS | BFS | unittest | Git/GitHub
```

## Project Structure

```
maze-generation-dfs/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── main.py                # entry point
├── src/
│   ├── __init__.py
│   ├── constants.py       # sizes, speeds, colours
│   ├── maze.py            # Cell + Maze (grid, walls, neighbours)
│   ├── algorithms.py      # DFS generation, BFS solving (generators)
│   └── gui.py             # Tkinter window, drawing, animation
├── tests/
│   ├── __init__.py
│   └── test_maze.py
├── docs/
│   ├── project-report.md
│   ├── algorithm.md
│   ├── viva-questions.md
│   └── demo-script.md
└── screenshots/
    └── .gitkeep
```

## Installation

Check Python (3.8 or newer):

```
python --version
```
or
```
python3 --version
```

Get Python from https://www.python.org/downloads/ if needed.
On Ubuntu/Debian also run `sudo apt install python3-tk`.

### Clone Repository

```
git clone https://github.com/YOUR_GITHUB_USERNAME/maze-generation-dfs.git
cd maze-generation-dfs
```

### Virtual Environment (optional but recommended)

Windows:
```
python -m venv venv
venv\Scripts\activate
```
Linux / macOS:
```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```
pip install -r requirements.txt
```
There are **no third-party dependencies**; `requirements.txt` only contains explanatory comments.

## Run

```
python main.py
```
(use `python3 main.py` on Linux/macOS)

## Controls

| Control | Action |
|---------|--------|
| Rows / Columns | Maze size, 2-60 each |
| Speed slider | Animation speed, can be changed while animating |
| **Generate Maze** (`G`) | Create and animate a new maze |
| **Solve Maze** (`S`) | Animate BFS and draw the shortest path |
| **Clear** | Remove the solution colours, keep the maze |
| **Reset** (`R`) | Remove the maze and restore defaults |
| `Esc` | Stop the running animation (generation is cancelled; solving is cleared) |

Shortcuts are ignored while you are typing in the Rows/Columns boxes.

Colours: green = start, red = end, yellow = current cell, blue = visited,
dark blue = backtracked, purple = final solution path.

## Testing

```
python -m unittest discover
```
(use `python3` on Linux/macOS). Expected result: all tests pass (`OK`).

## Complexity

| Algorithm | Time | Space |
|-----------|------|-------|
| DFS generation | O(R x C) | O(R x C) |
| BFS solving | O(R x C) | O(R x C) |

R x C is the number of cells. Each cell is pushed/visited once.

## Future Scope

- Other generators (Prim, Kruskal, Recursive Division) with a comparison mode
- A* and DFS solvers; choose start/end by clicking
- Save/load mazes, export as image
- Braided mazes (with loops) and larger mazes with a faster renderer

## Screenshots

Take these and save them in `screenshots/`:

1. `01-main-window.png` - application just after starting
2. `02-generating.png` - maze mid-generation (yellow current cell visible)
3. `03-completed-maze.png` - finished maze
4. `04-solving.png` - BFS exploring (blue cells spreading)
5. `05-solution.png` - purple final path
6. `06-github-page.png` - your repository page on GitHub

Then reference them, for example: `![Main window](screenshots/01-main-window.png)`

## Author

```
Name: YOUR NAME
Roll No: YOUR ROLL NUMBER
College: YOUR COLLEGE NAME
Department: YOUR DEPARTMENT
```

## License

MIT - see `LICENSE` (replace `YEAR` and `YOUR NAME`).
