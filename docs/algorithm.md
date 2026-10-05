# Algorithm Documentation

## 1. Depth-First Search (DFS)
DFS explores a graph by going as deep as possible along one path, then backing up to the
last place that still has unexplored options. A maze grid is a graph: every cell is a node
and every pair of neighbouring cells is a possible edge (a wall that may be removed).

## 2. Stack-based DFS
Recursion would need one Python call per cell, and Python limits recursion depth (about
1000), so a large maze could crash. We keep our own **stack** (a Python list):

```
stack = [start]
while stack:
    current = stack[-1]          # look at the top (do not pop yet)
    if current has unvisited neighbours:
        next = random choice
        remove wall(current, next)
        mark next visited
        stack.append(next)       # go deeper
    else:
        stack.pop()              # backtrack
```

## 3. Backtracking
A dead end is a cell whose neighbours are all visited. Popping the stack returns to the
previous cell, which may still have unvisited neighbours, so a new branch starts there.
The animation shows backtracked cells in dark blue.

## 4. Randomized neighbour selection
`random.choice` over the unvisited neighbours makes each maze different. Without
randomness DFS would always carve the same boring corridor pattern.

## 5. Wall removal
Cells A and B share one wall, stored on both cells. Removing the wall means:

```
A=(r,c), B=(r,c+1):   A.walls["right"] = False
                      B.walls["left"]  = False
```
`OPPOSITE` maps each direction to the other side (top<->bottom, left<->right).

## 6. Maze representation
```
Cell(row, col, visited=False, walls={"top":True,"right":True,"bottom":True,"left":True})
Maze.grid[row][col] -> Cell
```
Dataclass chosen for named fields and type hints. Start = (0,0), end = (rows-1, cols-1).

ASCII example (3x3) before and after removing the wall between (0,0) and (0,1):

```
+--+--+--+        +--+--+--+
|  |  |  |        |     |  |
+--+--+--+   ->   +--+--+--+
|  |  |  |        |  |  |  |
```

## 7. Properties of the result
DFS visits each cell once and removes exactly one wall per newly visited cell, so a maze
with N cells has N-1 passages: a spanning tree. Therefore every cell is reachable, there are
no loops, and there is exactly one path between any two cells (a *perfect maze*). Mazes made
by DFS have long corridors and few dead ends compared with Prim's algorithm.

## 8. BFS maze solving
BFS uses a **queue** (FIFO) and explores all cells at distance 1, then 2, and so on.

```
queue = [start]; parent = {start: None}
while queue:
    cell = queue.popleft()
    if cell == end: stop
    for each neighbour reachable without crossing a wall:
        if neighbour not in parent:
            parent[neighbour] = cell
            queue.append(neighbour)
```
Rebuild the path by following `parent` from `end` back to `start` and reversing it.
Because BFS reaches every cell by the fewest steps, the path is the shortest one. (In a
perfect maze there is only one path anyway; BFS is still the right tool for mazes with loops.)

## 9. Complexity
Let R x C be the number of cells.

| | Time | Space |
|-|------|-------|
| DFS generation | O(R x C): each cell pushed and popped once, up to 4 neighbours checked | O(R x C): stack in the worst case, plus the grid |
| BFS solving | O(R x C): each cell enqueued once | O(R x C): queue + parent map |

## 10. Why the GUI stays responsive
Both algorithms are Python generators that `yield` one event per step. The GUI takes a few
events at a time and then calls `root.after(delay, ...)`, which returns control to Tk so the
window can still repaint, resize and handle clicks. `time.sleep()` is never used.
