"""Unit tests for the maze model and the DFS / BFS algorithms."""

import random
import unittest

from src import constants as const
from src.algorithms import bfs_solve_steps, dfs_generate_steps, generate_maze, solve_maze
from src.maze import Cell, Maze


class TestGridAndCells(unittest.TestCase):
    def test_grid_creation(self):
        maze = Maze(4, 6)
        self.assertEqual(len(maze.grid), 4)
        self.assertTrue(all(len(row) == 6 for row in maze.grid))

    def test_cell_creation_has_four_walls_and_unvisited(self):
        cell = Cell(1, 2)
        self.assertFalse(cell.visited)
        self.assertEqual(set(cell.walls), {"top", "right", "bottom", "left"})
        self.assertTrue(all(cell.walls.values()))

    def test_cells_do_not_share_wall_dicts(self):
        maze = Maze(3, 3)
        maze.grid[0][0].walls["top"] = False
        self.assertTrue(maze.grid[0][1].walls["top"])

    def test_start_and_end_cells(self):
        maze = Maze(5, 7)
        self.assertEqual(maze.start, (0, 0))
        self.assertEqual(maze.end, (4, 6))


class TestInvalidDimensions(unittest.TestCase):
    def test_too_small(self):
        for rows, cols in [(0, 5), (5, 0), (-3, 5), (1, 1)]:
            with self.assertRaises(ValueError):
                Maze(rows, cols)

    def test_too_large(self):
        with self.assertRaises(ValueError):
            Maze(const.MAX_SIZE + 1, 10)

    def test_wrong_type(self):
        for rows, cols in [("10", 10), (10.5, 10), (None, 10), (True, 10)]:
            with self.assertRaises(ValueError):
                Maze(rows, cols)


class TestNeighboursAndWalls(unittest.TestCase):
    def test_neighbor_counts(self):
        maze = Maze(5, 5)
        self.assertEqual(len(maze.neighbors((0, 0))), 2)   # corner
        self.assertEqual(len(maze.neighbors((0, 2))), 3)   # edge
        self.assertEqual(len(maze.neighbors((2, 2))), 4)   # interior

    def test_unvisited_neighbors_exclude_visited(self):
        maze = Maze(5, 5)
        maze.cell((2, 3)).visited = True
        found = {coord for _, coord in maze.unvisited_neighbors((2, 2))}
        self.assertEqual(found, {(1, 2), (3, 2), (2, 1)})

    def test_remove_wall_both_sides(self):
        maze = Maze(3, 3)
        maze.remove_wall((1, 1), (1, 2))
        self.assertFalse(maze.cell((1, 1)).walls["right"])
        self.assertFalse(maze.cell((1, 2)).walls["left"])
        self.assertTrue(maze.cell((1, 1)).walls["top"])

    def test_remove_wall_vertical(self):
        maze = Maze(3, 3)
        maze.remove_wall((0, 0), (1, 0))
        self.assertFalse(maze.cell((0, 0)).walls["bottom"])
        self.assertFalse(maze.cell((1, 0)).walls["top"])

    def test_remove_wall_rejects_non_adjacent_or_outside(self):
        maze = Maze(3, 3)
        with self.assertRaises(ValueError):
            maze.remove_wall((0, 0), (2, 2))
        with self.assertRaises(ValueError):
            maze.remove_wall((0, 0), (-1, 0))

    def test_open_neighbors_follow_removed_walls(self):
        maze = Maze(3, 3)
        self.assertEqual(maze.open_neighbors((1, 1)), [])
        maze.remove_wall((1, 1), (0, 1))
        self.assertEqual(maze.open_neighbors((1, 1)), [(0, 1)])


class TestGeneration(unittest.TestCase):
    def test_all_cells_visited(self):
        maze = generate_maze(Maze(12, 17), random.Random(1))
        self.assertEqual(maze.count_visited(), 12 * 17)

    def test_all_cells_reachable_for_many_seeds(self):
        for seed in range(30):
            rows, cols = random.Random(seed).randint(2, 15), random.Random(seed + 99).randint(2, 15)
            maze = generate_maze(Maze(rows, cols), random.Random(seed))
            self.assertTrue(maze.all_reachable(), f"seed {seed}")

    def test_perfect_maze_is_a_spanning_tree(self):
        maze = generate_maze(Maze(10, 10), random.Random(5))
        self.assertEqual(maze.passage_count(), 10 * 10 - 1)

    def test_walls_are_consistent_between_neighbours(self):
        maze = generate_maze(Maze(8, 8), random.Random(3))
        for row in maze.grid:
            for cell in row:
                for coord in maze.open_neighbors((cell.row, cell.col)):
                    self.assertIn((cell.row, cell.col), maze.open_neighbors(coord))

    def test_same_seed_same_maze_different_seed_different_maze(self):
        def walls(seed):
            maze = generate_maze(Maze(8, 8), random.Random(seed))
            return [dict(c.walls) for row in maze.grid for c in row]
        self.assertEqual(walls(7), walls(7))
        self.assertNotEqual(walls(7), walls(8))

    def test_event_types_and_backtracking_happens(self):
        kinds = [e[0] for e in dfs_generate_steps(Maze(6, 6), random.Random(2))]
        self.assertEqual(kinds[0], "start")
        self.assertEqual(kinds.count("carve"), 6 * 6 - 1)
        self.assertEqual(kinds.count("backtrack"), 6 * 6)

    def test_smallest_maze(self):
        maze = generate_maze(Maze(2, 2), random.Random(0))
        self.assertTrue(maze.all_reachable())
        self.assertEqual(maze.passage_count(), 3)


class TestSolving(unittest.TestCase):
    def setUp(self):
        self.maze = generate_maze(Maze(15, 15), random.Random(11))

    def test_path_starts_and_ends_correctly(self):
        path = solve_maze(self.maze)
        self.assertEqual(path[0], self.maze.start)
        self.assertEqual(path[-1], self.maze.end)

    def test_path_is_walkable(self):
        path = solve_maze(self.maze)
        for first, second in zip(path, path[1:]):
            self.assertIn(second, self.maze.open_neighbors(first))

    def test_path_has_no_repeated_cells(self):
        path = solve_maze(self.maze)
        self.assertEqual(len(path), len(set(path)))

    def test_bfs_path_is_shortest_when_loop_added(self):
        # Knock out an extra wall to make a loop, then BFS must still be shortest.
        maze = Maze(3, 3)
        for first, second in [((0, 0), (0, 1)), ((0, 1), (0, 2)), ((0, 2), (1, 2)),
                              ((1, 2), (2, 2)), ((0, 0), (1, 0)), ((1, 0), (2, 0)),
                              ((2, 0), (2, 1)), ((2, 1), (2, 2))]:
            maze.remove_wall(first, second)
        self.assertEqual(len(solve_maze(maze)), 5)

    def test_no_path_in_unopened_grid(self):
        self.assertEqual(solve_maze(Maze(3, 3)), [])

    def test_search_events_end_with_done(self):
        events = list(bfs_solve_steps(self.maze))
        self.assertEqual(events[0], ("visit", self.maze.start))
        self.assertEqual(events[-1][0], "done")


if __name__ == "__main__":
    unittest.main()
