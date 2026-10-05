"""Maze data structure: a grid of cells, each with four walls."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from . import constants as const

Coord = Tuple[int, int]  # (row, column)

# Direction name -> (row offset, column offset)
DIRECTIONS: Dict[str, Coord] = {
    "top": (-1, 0),
    "right": (0, 1),
    "bottom": (1, 0),
    "left": (0, -1),
}
OPPOSITE: Dict[str, str] = {
    "top": "bottom",
    "bottom": "top",
    "left": "right",
    "right": "left",
}


@dataclass
class Cell:
    """One square of the maze. A wall value of True means the wall exists."""

    row: int
    col: int
    visited: bool = False
    walls: Dict[str, bool] = field(
        default_factory=lambda: {name: True for name in DIRECTIONS}
    )


class Maze:
    """A rectangular grid of :class:`Cell` objects.

    The start is the top-left cell and the end is the bottom-right cell.
    """

    def __init__(self, rows: int, cols: int) -> None:
        self.validate_size(rows, cols)
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Cell]] = [
            [Cell(r, c) for c in range(cols)] for r in range(rows)
        ]
        self.start: Coord = (0, 0)
        self.end: Coord = (rows - 1, cols - 1)

    # ------------------------------------------------------------------ setup
    @staticmethod
    def validate_size(rows: int, cols: int) -> None:
        """Raise ValueError unless rows and cols are ints within the limits."""
        for name, value in (("rows", rows), ("cols", cols)):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{name} must be a whole number.")
            if not const.MIN_SIZE <= value <= const.MAX_SIZE:
                raise ValueError(
                    f"{name} must be between {const.MIN_SIZE} and {const.MAX_SIZE}."
                )

    # ---------------------------------------------------------------- queries
    def in_bounds(self, coord: Coord) -> bool:
        row, col = coord
        return 0 <= row < self.rows and 0 <= col < self.cols

    def cell(self, coord: Coord) -> Cell:
        return self.grid[coord[0]][coord[1]]

    def neighbors(self, coord: Coord) -> List[Tuple[str, Coord]]:
        """All in-bounds neighbours as (direction, coordinate) pairs."""
        result = []
        for name, (d_row, d_col) in DIRECTIONS.items():
            neighbor = (coord[0] + d_row, coord[1] + d_col)
            if self.in_bounds(neighbor):
                result.append((name, neighbor))
        return result

    def unvisited_neighbors(self, coord: Coord) -> List[Tuple[str, Coord]]:
        """In-bounds neighbours that DFS has not visited yet."""
        return [(n, c) for n, c in self.neighbors(coord) if not self.cell(c).visited]

    def open_neighbors(self, coord: Coord) -> List[Coord]:
        """Neighbours reachable from coord (no wall in between)."""
        walls = self.cell(coord).walls
        return [c for name, c in self.neighbors(coord) if not walls[name]]

    def direction_between(self, first: Coord, second: Coord) -> str:
        """Direction from first to second; ValueError if not adjacent."""
        delta = (second[0] - first[0], second[1] - first[1])
        for name, offset in DIRECTIONS.items():
            if offset == delta:
                return name
        raise ValueError(f"Cells {first} and {second} are not adjacent.")

    # -------------------------------------------------------------- mutations
    def remove_wall(self, first: Coord, second: Coord) -> None:
        """Knock down the wall between two adjacent cells (both sides)."""
        if not (self.in_bounds(first) and self.in_bounds(second)):
            raise ValueError("Both cells must be inside the maze.")
        direction = self.direction_between(first, second)
        self.cell(first).walls[direction] = False
        self.cell(second).walls[OPPOSITE[direction]] = False

    def reset_visited(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.visited = False

    # ------------------------------------------------------------- statistics
    def count_visited(self) -> int:
        return sum(cell.visited for row in self.grid for cell in row)

    def passage_count(self) -> int:
        """Number of removed walls (each shared wall counted once)."""
        total = 0
        for row in self.grid:
            for cell in row:
                total += not cell.walls["right"] and cell.col < self.cols - 1
                total += not cell.walls["bottom"] and cell.row < self.rows - 1
        return total

    def reachable_cells(self) -> int:
        """Cells reachable from the start by walking through open passages."""
        seen = {self.start}
        stack = [self.start]
        while stack:
            for neighbor in self.open_neighbors(stack.pop()):
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return len(seen)

    def all_reachable(self) -> bool:
        return self.reachable_cells() == self.rows * self.cols
