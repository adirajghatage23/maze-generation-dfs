# Demonstration Script (3-5 minutes)

**0:00 - Introduction (30 s).** "This project generates mazes using Depth-First Search with
backtracking and solves them with Breadth-First Search. It is written in Python with Tkinter
and I have unit tests and documentation on GitHub."

**0:30 - Explain the screen (30 s).** Point to the header, Rows/Columns, speed slider, the four
buttons, the status panel (left) and statistics (right). "Green is the start, red the end."

**1:00 - Generate slowly (60 s).** Set 10 x 10, speed slow, click **Generate Maze**.
"Yellow is the current cell. DFS picks a random unvisited neighbour, removes the wall between
them and moves there. Blue cells are visited. When a cell has no unvisited neighbour, the
algorithm backtracks, shown in dark blue, using the stack."

**2:00 - Show the result (30 s).** "Every cell is connected and there are no loops, N cells
and N-1 passages. Generation time and visited cells are in the statistics."

**2:30 - Solve (60 s).** Click **Solve Maze**. "BFS uses a queue and spreads outward level by
level; each cell stores its parent. When it reaches red, we follow parents backwards to get the
shortest path, drawn in purple." Show path length and solving time.

**3:30 - Robustness (45 s).** Type `abc` in Rows and click Generate to show the error. Click Solve
during generation to show the warning. Use **Clear** (keeps maze), then **Reset**. Press `G`, `S`, `R`, `Esc`.

**4:15 - Close (30 s).** "Complexity is O(R x C) for both. Possible extensions are Prim/Kruskal
generators and A* solving." Show the GitHub page and tests: `python -m unittest discover`.
