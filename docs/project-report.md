# Mini Project Report

## 1. Title
**Maze Generation Using Depth-First Search (DFS)**

Name: YOUR NAME | Roll No: YOUR ROLL NUMBER | College: YOUR COLLEGE NAME | Department: YOUR DEPARTMENT

## 2. Abstract
This project implements a desktop application that generates random mazes with the Depth-First
Search (DFS) backtracking algorithm and solves them with Breadth-First Search (BFS). The
application is written in Python 3 with Tkinter and uses only the standard library. Generation
and solving are animated step by step so the behaviour of both algorithms can be observed. The
code is separated into a data model, algorithms and a GUI, and is covered by unit tests.

## 3. Introduction
Mazes are a classic example of graph traversal. A rectangular grid can be treated as a graph
whose nodes are cells and whose edges are the openings between neighbouring cells. Generating
a maze means choosing which walls to remove; solving it means finding a route from the entrance
to the exit. Visualising these steps makes data structures such as stacks and queues easy to understand.

## 4. Problem Statement
To design and implement an application that (a) generates a random, fully connected maze using
DFS with backtracking, (b) animates the process, and (c) finds and displays the shortest path
between the start and the end cells.

## 5. Objectives
- Apply DFS, backtracking, stack, BFS and queue to a practical problem.
- Produce a different, valid maze on every run with no isolated cells.
- Animate generation and solving without freezing the user interface.
- Provide input validation, status messages and statistics.
- Practise modular design, unit testing, documentation and Git/GitHub.

## 6. Existing System
Many online maze demos show only the finished maze, or are written as single large scripts
with recursive DFS that can hit Python's recursion limit and with blocking animation loops.
Textbook examples often omit input validation, tests and documentation.

## 7. Proposed System
A modular Tkinter application with an explicit-stack DFS generator, a BFS solver, event-driven
animation using `after()`, a speed control, validation and statistics, plus tests and documentation.

## 8. Hardware Requirements
- Any PC/laptop capable of running Python 3 (Windows, Linux or macOS)
- Minimum 2 GB RAM, around 50 MB free disk space, a display of 1024 x 768 or larger, mouse and keyboard

## 9. Software Requirements
- Python 3.8 or newer with Tkinter
- Any text editor or IDE (VS Code, PyCharm, IDLE)
- Git (for version control) and a GitHub account
- No third-party Python packages

## 10. Technologies Used
Python 3, Tkinter (GUI), `random`, `collections.deque`, `dataclasses`, `unittest`, Git/GitHub.

## 11. System Architecture
```
 +------------+     +----------------+     +-----------------+
 |  main.py   | --> |  gui.py        | --> |  algorithms.py  |
 | (entry)    |     |  window, draw, |     |  DFS generate   |
 +------------+     |  animation     |     |  BFS solve      |
                    +-------+--------+     +--------+--------+
                            |                       |
                            v                       v
                    +------------------------------------+
                    |  maze.py : Cell, Maze (grid, walls)|
                    +------------------------------------+
                    constants.py : sizes, speeds, colours
```
The algorithms know nothing about Tkinter; the GUI only consumes the events they yield.

## 12. Algorithm
1. Build a grid of cells with four walls each.
2. DFS (stack) removes walls to create a spanning tree of the grid.
3. BFS (queue) searches the tree from start to end and records parents.
4. The path is rebuilt from the parents and drawn.

## 13. DFS Explanation
DFS repeatedly moves to an unvisited neighbour (chosen at random) and removes the wall between
the cells. When no unvisited neighbour exists the algorithm backtracks by popping the stack. It
ends when the stack is empty, which means every cell has been visited. Each cell is handled once.

## 14. BFS Explanation
BFS puts the start in a queue and repeatedly removes the first cell, adding its not-yet-seen,
reachable neighbours to the queue and storing their parent. Cells are discovered in order of
distance, so when the end is reached the path of parents is a shortest path.

## 15. Flowchart
```
Generation                               Solving
 [Start]                                  [Start]
    |                                        |
 [Create grid, mark (0,0), push]          [Queue = start, parent[start]=None]
    |                                        |
 <Stack empty?> --yes--> [End]            <Queue empty?> --yes--> [No path]
    | no                                     | no
 [current = top of stack]                 [cell = dequeue]
    |                                        |
 <Unvisited neighbour?> --no--> [Pop]     <cell == end?> --yes--> [Rebuild path] --> [End]
    | yes                                    | no
 [Pick random, remove wall,               [For each open unseen neighbour:
  mark visited, push]                      set parent, enqueue]
    |                                        |
    +--> back to <Stack empty?>              +--> back to <Queue empty?>
```

## 16. Pseudocode
```
GENERATE(maze):
    mark start visited; stack <- [start]
    while stack not empty:
        current <- top(stack)
        options <- unvisited neighbours of current
        if options not empty:
            next <- random(options)
            remove wall between current and next
            mark next visited; push next
        else:
            pop stack

SOLVE(maze):
    queue <- [start]; parent[start] <- none
    while queue not empty:
        cell <- dequeue
        if cell = end: break
        for n in open neighbours of cell:
            if n not in parent: parent[n] <- cell; enqueue n
    path <- follow parent from end to start; reverse
```

## 17. Implementation Details
- `src/maze.py`: `Cell` dataclass and `Maze` class (neighbours, wall removal, reachability checks, size validation 2-60).
- `src/algorithms.py`: `dfs_generate_steps` and `bfs_solve_steps` are generators that yield events (`start/carve/backtrack`, `visit/done`); `generate_maze` and `solve_maze` run them to completion.
- `src/gui.py`: `MazeApp` draws cells on a Canvas, handles buttons/keys and runs animations with `root.after`. A state flag (idle/generating/solving) prevents conflicting actions. Algorithm time is measured with `time.perf_counter` around the algorithm steps only, excluding animation delay.
- Errors (non-numeric, empty, out-of-range input; solving before generating; starting while busy) show dialogs instead of crashing.

## 18. Testing
Unit tests (`unittest`) cover the model and algorithms. Run `python -m unittest discover`.
GUI behaviour was checked manually using the checklist in the test cases below.

## 19. Test Cases
| # | Test | Expected |
|---|------|----------|
| 1 | Grid creation 4 x 6 | 4 rows, 6 columns |
| 2 | New cell | 4 walls, unvisited |
| 3 | Neighbours of corner / edge / interior | 2 / 3 / 4 |
| 4 | Remove wall between two cells | Wall removed on both cells |
| 5 | Generate maze | All cells visited and reachable, N-1 passages |
| 6 | Same seed / different seed | Same / different maze |
| 7 | BFS path | Starts at start, ends at end, every step walkable, no repeats |
| 8 | BFS on a maze with a loop | Shortest route chosen |
| 9 | Invalid sizes (0, -3, 1, 61, "10", 10.5) | `ValueError` |
| 10 | GUI: Rows = `abc` | Error dialog, no crash |
| 11 | GUI: Solve before Generate | Warning dialog |
| 12 | GUI: Generate/Solve during animation | Warning dialog |
| 13 | GUI: Esc during generation | Maze cancelled, UI idle |
| 14 | GUI: Resize window | Maze redraws to fit |

## 20. Results
The application generates a different valid maze each time, animates generation and solving,
and displays status and statistics (cells, visited cells, times, path length). Insert your
screenshots here (`screenshots/`) and the output of `python -m unittest discover`.

## 21. Advantages
Easy to understand and demonstrate; no external dependencies; responsive animation; modular and tested; cross-platform.

## 22. Limitations
Maximum size 60 x 60; only a perfect maze (no loops); fixed start/end; DFS mazes have long
corridors and few branches; no save/export.

## 23. Future Scope
Other generators (Prim, Kruskal, Wilson), A* and DFS solvers, clickable start/end, loops,
saving as images, difficulty levels, a web version.

## 24. Conclusion
The project shows how DFS with backtracking can create mazes and how BFS finds shortest paths,
combining data structures, algorithms, GUI programming, testing and version control in one small application.

## 25. References
1. T. H. Cormen, C. E. Leiserson, R. L. Rivest, C. Stein, *Introduction to Algorithms*, MIT Press (DFS and BFS chapters).
2. Python documentation: https://docs.python.org/3/library/tkinter.html
3. Python documentation: https://docs.python.org/3/library/unittest.html
4. Wikipedia, "Maze generation algorithm" (randomized depth-first search).
5. Git documentation: https://git-scm.com/doc
