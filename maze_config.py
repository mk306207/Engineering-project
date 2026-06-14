import random


TILE_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 15

CLASSIC_MAZE = [
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,0,1,0,1],
    [1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,0,1,0,1,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
]

MAZE_SETTINGS = {
    "mutation_rate": 0.05,
    "satisfactory_fitness": 1700,
    "maze_type": "Classic",
    "maze_size": 15,
    "population_size": 50,
    "chromosome_length": 200,
    "generated_seed": None,
}

MAZE_TYPE_OPTIONS = ["Classic", "Open", "Generated"]
MAZE_SIZE_OPTIONS = [11, 15, 21, 25]
MAZE = []
START_POSITION = (1, 0)
FINISH_LINE = (13, 14)
WINNER_START_POSITION = START_POSITION
WINNER_FINISH_LINE = FINISH_LINE
SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE + 60
BEST_FINISH = 30
SIM_SPEED = 30
SATISFACTORY_FITNESS = MAZE_SETTINGS["satisfactory_fitness"]


def _odd_size(size):
    size = int(size)
    return size if size % 2 == 1 else size + 1


def _scale_classic(size):
    if size == 15:
        return [row[:] for row in CLASSIC_MAZE], (1, 0), (13, 14)

    size = _odd_size(size)
    grid = [[1 for _ in range(size)] for _ in range(size)]
    for y in range(size):
        for x in range(size):
            source_y = min(14, int(y * 15 / size))
            source_x = min(14, int(x * 15 / size))
            grid[y][x] = CLASSIC_MAZE[source_y][source_x]

    start = (1, 0)
    finish = (size - 2, size - 1)
    grid[start[1]][start[0]] = 0
    grid[finish[1]][finish[0]] = 0
    for y in range(1, size - 1):
        grid[y][1] = 0
    for x in range(1, size - 1):
        grid[size - 2][x] = 0
    return grid, start, finish


def _open_maze(size):
    size = _odd_size(size)
    grid = [[1 for _ in range(size)] for _ in range(size)]
    for y in range(1, size - 1):
        for x in range(1, size - 1):
            grid[y][x] = 0

    start = (1, 0)
    finish = (size - 2, size - 1)
    grid[start[1]][start[0]] = 0
    grid[finish[1]][finish[0]] = 0
    return grid, start, finish


def _generated_maze(size, seed=None):
    size = _odd_size(size)
    grid = [[1 for _ in range(size)] for _ in range(size)]
    rng = random.Random(seed)

    def carve(x, y):
        grid[y][x] = 0
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        rng.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < size - 1 and 1 <= ny < size - 1 and grid[ny][nx] == 1:
                grid[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    carve(1, 1)
    start = (1, 0)
    finish = (size - 2, size - 1)
    grid[start[1]][start[0]] = 0
    grid[1][1] = 0
    grid[finish[1]][finish[0]] = 0
    grid[size - 2][size - 2] = 0
    return grid, start, finish


def build_maze(maze_type=None, maze_size=None):
    maze_type = maze_type or MAZE_SETTINGS["maze_type"]
    maze_size = maze_size or MAZE_SETTINGS["maze_size"]
    if maze_type == "Open":
        return _open_maze(maze_size)
    if maze_type == "Generated":
        return _generated_maze(maze_size, MAZE_SETTINGS["generated_seed"])
    return _scale_classic(maze_size)


def apply_maze_settings(settings=None):
    global MAZE, START_POSITION, FINISH_LINE, WINNER_START_POSITION, WINNER_FINISH_LINE
    global MAZE_WIDTH, MAZE_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, SATISFACTORY_FITNESS

    if settings:
        MAZE_SETTINGS.update(settings)
    if MAZE_SETTINGS["maze_type"] == "Generated" and MAZE_SETTINGS["generated_seed"] is None:
        MAZE_SETTINGS["generated_seed"] = random.randint(1, 1_000_000_000)

    MAZE, START_POSITION, FINISH_LINE = build_maze()
    WINNER_START_POSITION = START_POSITION
    WINNER_FINISH_LINE = FINISH_LINE
    MAZE_HEIGHT = len(MAZE)
    MAZE_WIDTH = len(MAZE[0])
    SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE
    SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE + 60
    SATISFACTORY_FITNESS = MAZE_SETTINGS["satisfactory_fitness"]
    return MAZE_SETTINGS


apply_maze_settings()
