"""Shared constants: sizes, speeds and the dark-theme colour palette."""

APP_TITLE = "MAZE GENERATOR"
APP_SUBTITLE = "Depth-First Search (DFS) with Backtracking"

# Maze size limits (the GUI redraws every cell, so keep the maximum sensible).
MIN_SIZE = 2
MAX_SIZE = 60
DEFAULT_ROWS = 20
DEFAULT_COLS = 20

# Animation speed slider (1 = slowest, 10 = fastest).
MIN_SPEED = 1
MAX_SPEED = 10
DEFAULT_SPEED = 5

# Window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 780
MIN_WINDOW_HEIGHT = 640
CANVAS_PADDING = 16

# Colours
COLOR_BG = "#121212"
COLOR_PANEL = "#1E1E1E"
COLOR_WALL = "#FFFFFF"
COLOR_UNVISITED = "#1E1E1E"
COLOR_VISITED = "#3498DB"
COLOR_BACKTRACK = "#1F618D"   # darker blue: cell finished, DFS has backtracked
COLOR_CURRENT = "#F1C40F"
COLOR_START = "#2ECC71"
COLOR_END = "#E74C3C"
COLOR_PATH = "#9B59B6"
COLOR_TEXT = "#ECECEC"
COLOR_MUTED = "#9A9A9A"
