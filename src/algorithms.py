"""DFS maze generation and BFS maze solving.

Both algorithms are written as generators that yield one event per step.
The GUI pulls one event at a time (using Tk's ``after``) to animate them,
while the tests simply consume every event at once.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Dict, Iterator, List, Optional, Tuple

from .maze import Coord, Maze

# ("start", cell, None) | ("carve", from_cell, to_cell) | ("backtrack", cell, new_top)
GenerationEvent = Tuple[str, Coord, Optional[Coord]]
# ("visit", cell) | ("done", path)
SolveEvent = Tuple[str, object]


def dfs_generate_steps(
    maze: Maze, rng: Optional[random.Random] = None
) -> Iterator[GenerationEvent]:
    """Carve a perfect maze with an explicit-stack DFS (backtracking)."""
    rng = rng or random.Random()
    start = maze.start
    maze.cell(start).visited = True
    stack: List[Coord] = [start]
    yield ("start", start, None)

    while stack:
        current = stack[-1]
        candidates = maze.unvisited_neighbors(current)
        if candidates:
            _, chosen = rng.choice(candidates)       # random neighbour
            maze.remove_wall(current, chosen)        # carve a passage
            maze.cell(chosen).visited = True
            stack.append(chosen)                     # go deeper
            yield ("carve", current, chosen)
        else:
            stack.pop()                              # dead end: backtrack
            yield ("backtrack", current, stack[-1] if stack else None)


def generate_maze(maze: Maze, rng: Optional[random.Random] = None) -> Maze:
    """Run the whole DFS generation at once and return the maze."""
    for _ in dfs_generate_steps(maze, rng):
        pass
    return maze


def bfs_solve_steps(maze: Maze) -> Iterator[SolveEvent]:
    """Breadth-first search from maze.start to maze.end.

    Yields ("visit", cell) whenever a cell is discovered and finally
    ("done", path) where path is the shortest route (empty if none).
    """
    start, end = maze.start, maze.end
    queue = deque([start])
    parent: Dict[Coord, Optional[Coord]] = {start: None}
    yield ("visit", start)

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in maze.open_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
                yield ("visit", neighbor)

    path: List[Coord] = []
    if end in parent:
        node: Optional[Coord] = end
        while node is not None:                      # follow parents backwards
            path.append(node)
            node = parent[node]
        path.reverse()
    yield ("done", path)


def solve_maze(maze: Maze) -> List[Coord]:
    """Return the shortest path from start to end (empty list if none)."""
    path: List[Coord] = []
    for kind, payload in bfs_solve_steps(maze):
        if kind == "done":
            path = payload  # type: ignore[assignment]
    return path
