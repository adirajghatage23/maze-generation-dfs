# Viva Questions and Answers

1. **What is DFS?** Depth-First Search explores as far as possible along one path before backtracking. It uses a stack (explicit or the recursion stack).
2. **Why is DFS used for maze generation?** Going deep and carving a passage each time you enter a new cell gives long winding corridors and guarantees every cell gets connected exactly once.
3. **What is backtracking?** Returning to the previous cell when the current one has no unvisited neighbours, so another branch can be tried.
4. **Why is a stack used?** Last-in-first-out order remembers the path taken, so we can retrace our steps from a dead end.
5. **Why an explicit stack instead of recursion?** Python's recursion limit (about 1000) would crash on large mazes, and an explicit stack is easier to animate and demonstrate.
6. **What is BFS?** Breadth-First Search visits cells level by level (distance 1, 2, 3...) using a queue.
7. **Why is BFS good for shortest paths?** It reaches every cell by the smallest number of steps, so the first time it reaches the end is the shortest route.
8. **Time complexity?** O(R x C) for both DFS generation and BFS solving, because each cell is processed once.
9. **Space complexity?** O(R x C): the grid, plus the stack (DFS) or queue and parent map (BFS).
10. **Why choose neighbours randomly?** To get a different maze each time; fixed order would always give the same pattern.
11. **What happens if there are no unvisited neighbours?** The cell is popped from the stack and the algorithm continues from the previous cell.
12. **Why remove walls?** Walls start everywhere; removing the wall between two cells creates a passage, which is how the maze is "carved".
13. **What data structure represents the maze?** A 2D list of `Cell` dataclass objects, each with `visited` and a dictionary of four walls.
14. **Why a dataclass instead of a dict?** Named fields, type hints, defaults and cleaner code.
15. **Why Tkinter?** It is part of Python's standard library, so there is nothing to install, and it is enough for a simple canvas animation.
16. **How does the animation avoid freezing the GUI?** Each algorithm yields one step at a time and `root.after()` schedules the next step, so Tkinter's event loop keeps running. `time.sleep()` would freeze the window.
17. **What happens if the maze size is very large?** Drawing and memory grow with R x C, so the app limits sizes to 2-60 and shows an error otherwise.
18. **Difference between DFS and BFS?** DFS uses a stack and goes deep first; BFS uses a queue and goes wide first. DFS does not guarantee the shortest path; BFS does.
19. **Difference between generation and solving?** Generation creates the passages (removes walls); solving finds a route through existing passages without changing walls.
20. **What is a perfect maze?** A maze with exactly one path between any two cells: no loops and no isolated areas (a spanning tree).
21. **How many walls are removed for N cells?** N - 1, one per newly visited cell.
22. **How is the BFS path reconstructed?** Every cell stores its parent when discovered; from the end we follow parents back to the start and reverse the list.
23. **How do you know all cells are connected?** DFS visits every cell, and tests check reachability from the start by flood fill.
24. **Why is the wall removed on both cells?** The wall is shared; each cell stores its own copy, so both sides must be updated to stay consistent.
25. **Which tests did you write?** Grid and cell creation, neighbour detection, wall removal, generation validity, reachability, BFS path correctness, and invalid dimensions (`python -m unittest discover`).
26. **How would you improve it?** Add Prim/Kruskal generators, A* solving, clickable start/end and saving mazes.
