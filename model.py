import itertools
import random

# Directions
NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]

REVERSE = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

OFFSET = {
    NORTH: -16,
    EAST: 1,
    SOUTH: 16,
    WEST: -1,
}

# Masks
M_NORTH = 0x01
M_EAST  = 0x02
M_SOUTH = 0x04
M_WEST  = 0x08
M_ROBOT = 0x10

M_LOOKUP = {
    NORTH: M_NORTH,
    EAST: M_EAST,
    SOUTH: M_SOUTH,
    WEST: M_WEST,
}

# Colors
RED = 'R'
GREEN = 'G'
BLUE = 'B'
YELLOW = 'Y'
MAGENTA = 'M'
ANY = 'A'

ROBOT_COLORS = [RED, GREEN, BLUE, YELLOW, MAGENTA]
TARGET_COLORS = [RED, GREEN, BLUE, YELLOW]

# Shapes
CIRCLE = 'C'
TRIANGLE = 'T'
SQUARE = 'Q'
HEXAGON = 'H'
VORTEX = 'V'

SHAPES = [CIRCLE, TRIANGLE, SQUARE, HEXAGON]

# Tokens
TOKENS = [''.join(token) for token in itertools.product(TARGET_COLORS, SHAPES)]
# TOKENS.append('AV')

# Quadrants
QUAD_A2 = (
    'NW,N,N,N,NE,NW,N,N,'
    'W,S,X,X,X,X,SEYH,W,'
    'WE,NWGT,X,X,X,X,N,X,'
    'W,X,X,X,X,X,X,X,'
    'W,X,X,X,X,X,S,X,'
    'SW,X,X,X,X,X,NEBQ,W,'
    'NW,X,E,SWRC,X,X,X,S,'
    'W,X,X,N,X,X,E,NW'
)

QUAD_A1 = (
    'NW,NE,NW,N,NS,N,N,N,'
    'W,S,X,E,NWRC,X,X,X,'
    'W,NEGT,W,X,X,X,X,X,'
    'W,X,X,X,X,X,SEYH,W,'
    'W,X,X,X,X,X,N,X,'
    'SW,X,X,X,X,X,X,X,'
    'NW,X,E,SWBQ,X,X,X,S,'
    'W,X,X,N,X,X,E,NW'
)

# QUAD_C1 = (
#     'NW,N,N,NE,NW,N,N,N,'
#     'W,X,X,X,X,E,SWBC,X,'
#     'W,S,X,X,X,X,N,X,'
#     'W,NEYT,W,X,X,S,X,X,'
#     'W,X,X,X,E,NWGQ,X,X,'
#     'W,X,SERH,W,X,X,X,SEAV,'
#     'SW,X,N,X,X,X,X,SN,'
#     'NW,X,X,X,X,X,E,NW'
# )

QUAD_C1 = (
    'NW,N,N,NE,NW,N,N,N,'
    'W,X,X,X,X,E,SWBC,X,'
    'W,S,X,X,X,X,N,X,'
    'W,NEYT,W,X,X,S,X,X,'
    'W,X,X,X,E,NWGQ,X,X,'
    'W,X,SERH,W,X,X,X,SE,'
    'SW,X,N,X,X,X,X,SN,'
    'NW,X,X,X,X,X,E,NW'
)

# QUAD_C2 = (
#     'NW,N,N,N,NE,NW,N,N,'
#     'W,X,SERH,W,X,X,X,X,'
#     'W,X,N,X,X,X,X,X,'
#     'WE,SWGQ,X,X,X,X,S,X,'
#     'SW,N,X,X,X,E,NWYT,X,'
#     'NW,X,X,X,X,S,X,X,'
#     'W,X,X,X,X,NEBC,W,S,'
#     'W,X,X,SEAV,W,X,E,NW'
# )

QUAD_C2 = (
    'NW,N,N,N,NE,NW,N,N,'
    'W,X,SERH,W,X,X,X,X,'
    'W,X,N,X,X,X,X,X,'
    'WE,SWGQ,X,X,X,X,S,X,'
    'SW,N,X,X,X,E,NWYT,X,'
    'NW,X,X,X,X,S,X,X,'
    'W,X,X,X,X,NEBC,W,S,'
    'W,X,X,SE,W,X,E,NW'
)

QUAD_B2 = (
    'NW,N,N,NE,NW,N,N,N,'
    'W,X,X,X,X,SEGH,W,X,'
    'WE,SWRQ,X,X,X,N,X,X,'
    'SW,N,X,X,X,X,S,X,'
    'NW,X,X,X,X,E,NWYC,X,'
    'W,X,S,X,X,X,X,X,'
    'W,X,NEBT,W,X,X,X,S,'
    'W,X,X,X,X,X,E,NW'
)

QUAD_B1 = (
    'NW,N,NS,N,NE,NW,N,N,'
    'W,E,NWYC,X,X,X,X,X,'
    'W,X,X,X,X,X,X,X,'
    'W,X,X,X,X,E,SWBT,X,'
    'SW,X,X,X,S,X,N,X,'
    'NW,X,X,X,NERQ,W,X,X,'
    'W,SEGH,W,X,X,X,X,S,'
    'W,N,X,X,X,X,E,NW'
)

QUAD_D2 = (
    'NW,N,N,NE,NW,N,N,N,'
    'W,X,X,X,X,X,X,X,'
    'W,X,X,X,X,SEBH,W,X,'
    'W,X,S,X,X,N,X,X,'
    'SW,X,NEGC,W,X,X,X,X,'
    'NW,S,X,X,X,X,E,SWRT,'
    'WE,NWYQ,X,X,X,X,X,SN,'
    'W,X,X,X,X,X,E,NW'
)

QUAD_D1 = (
    'NW,N,N,NE,NW,N,N,N,'
    'WE,SWRT,X,X,X,X,S,X,'
    'W,N,X,X,X,X,NEGC,W,'
    'W,X,X,X,X,X,X,X,'
    'W,X,SEBH,W,X,X,X,S,'
    'SW,X,N,X,X,X,E,NWYQ,'
    'NW,X,X,X,X,X,X,S,'
    'W,X,X,X,X,X,E,NW'
)

QUAD_A3 = (
    'NW,NE,NW,NS,N,N,N,N,'
    'W,X,E,NWGT,X,X,X,X,'
    'W,X,X,X,X,X,X,X,'
    'W,X,X,X,X,X,SEYH,W,'
    'WE,SWRC,X,X,X,X,N,X,'
    'W,N,X,X,S,X,X,X,'
    'SW,X,X,X,NEBQ,W,X,S,'
    'NW,X,X,X,X,X,E,NW'
)

QUAD_A4 = (
    'NW,N,N,N,N,NE,NW,N,'
    'W,X,X,X,X,X,X,X,'
    'W,S,X,X,X,X,X,X,'
    'WE,NWRC,X,X,X,X,X,X,'
    'W,X,X,X,X,X,SEYH,W,'
    'SW,X,S,X,X,X,N,X,'
    'NW,X,NEGT,SWBQ,X,X,X,S,'
    'W,X,X,N,X,X,E,NW'
)

QUAD_B3 = (
    'NW,N,N,N,N,NE,NW,N,'
    'W,X,X,S,X,X,X,X,'
    'W,X,E,NWYC,X,X,X,X,'
    'SW,X,S,X,E,SWBT,X,X,'
    'NW,X,NERQ,W,X,N,X,X,'
    'W,X,X,X,SEGH,W,X,X,'
    'W,X,X,X,N,X,X,S,'
    'W,X,X,X,X,X,E,NW'
)

QUAD_B4 = (
    'NW,N,NE,NW,N,N,N,N,'
    'W,X,X,X,X,X,S,X,'
    'W,X,X,X,X,SEGH,NWYC,X,'
    'W,X,X,X,X,N,X,X,'
    'W,X,X,X,X,X,X,X,'
    'W,SERQ,W,X,X,X,X,X,'
    'SW,N,X,X,S,X,X,S,'
    'NW,X,X,X,NEBT,W,E,NW'
)

# QUAD_C3 = (
#     'NW,N,NE,NW,N,N,N,N,'
#     'W,X,X,X,E,SWBC,X,X,'
#     'W,X,X,X,X,N,X,SEAV,'
#     'SW,X,X,X,X,X,X,N,'
#     'NW,X,X,SERH,W,X,S,X,'
#     'W,S,X,N,X,X,NEGQ,W,'
#     'W,NEYT,W,X,X,X,X,S,'
#     'W,X,X,X,X,X,E,NW'
# )

QUAD_C3 = (
    'NW,N,NE,NW,N,N,N,N,'
    'W,X,X,X,E,SWBC,X,X,'
    'W,X,X,X,X,N,X,SE,'
    'SW,X,X,X,X,X,X,N,'
    'NW,X,X,SERH,W,X,S,X,'
    'W,S,X,N,X,X,NEGQ,W,'
    'W,NEYT,W,X,X,X,X,S,'
    'W,X,X,X,X,X,E,NW'
)

# QUAD_C4 = (
#     'NW,N,N,N,NE,NW,N,N,'
#     'W,X,X,X,X,X,S,X,'
#     'W,X,S,X,X,E,NWYT,X,'
#     'W,X,NEBC,SWGQ,X,X,X,X,'
#     'W,X,X,N,X,X,X,X,'
#     'W,SERH,W,X,X,X,X,X,'
#     'SW,N,X,X,X,X,X,S,'
#     'NW,X,X,X,X,SEAV,EW,NW'
# )

QUAD_C4 = (
    'NW,N,N,N,NE,NW,N,N,'
    'W,X,X,X,X,X,S,X,'
    'W,X,S,X,X,E,NWYT,X,'
    'W,X,NEBC,SWGQ,X,X,X,X,'
    'W,X,X,N,X,X,X,X,'
    'W,SERH,W,X,X,X,X,X,'
    'SW,N,X,X,X,X,X,S,'
    'NW,X,X,X,X,SE,EW,NW'
)

QUAD_D3 = (
    'NW,NE,NW,N,NS,N,N,N,'
    'W,X,X,X,NEGC,W,X,X,'
    'W,X,X,X,X,X,X,X,'
    'WE,SWRT,X,X,X,X,X,X,'
    'W,N,X,X,X,S,X,X,'
    'SW,X,X,X,E,NWYQ,X,X,'
    'NW,X,X,SEBH,W,X,X,S,'
    'W,X,X,N,X,X,E,NW'
)

QUAD_D4 = (
    'NW,N,N,N,NE,NW,N,N,'
    'W,X,X,X,X,X,X,X,'
    'SW,X,X,X,X,X,SEBH,W,'
    'NW,X,S,X,X,X,N,X,'
    'W,X,NEGC,SWRT,X,X,X,X,'
    'W,X,X,N,X,S,X,X,'
    'W,X,X,X,E,NWYQ,X,S,'
    'W,X,X,X,X,X,E,NW'
)

QUADS = [
    (QUAD_A1, QUAD_A2, QUAD_A3, QUAD_A4),
    (QUAD_B1, QUAD_B2, QUAD_B3, QUAD_B4),
    (QUAD_C1, QUAD_C2, QUAD_C3, QUAD_C4),
    (QUAD_D1, QUAD_D2, QUAD_D3, QUAD_D4),
]

# Rotation
ROTATE_QUAD = [
    56, 48, 40, 32, 24, 16,  8,  0,
    57, 49, 41, 33, 25, 17,  9,  1,
    58, 50, 42, 34, 26, 18, 10,  2,
    59, 51, 43, 35, 27, 19, 11,  3,
    60, 52, 44, 36, 28, 20, 12,  4,
    61, 53, 45, 37, 29, 21, 13,  5,
    62, 54, 46, 38, 30, 22, 14,  6,
    63, 55, 47, 39, 31, 23, 15,  7,
]

ROTATE_WALL = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
}

# Helper Functions
def idx(x, y, size=16):
    return y * size + x

def xy(index, size=16):
    x = index % size
    y = index / size
    return (x, y)

def rotate_quad(data, times=1):
    for i in range(times):
        result = [data[index] for index in ROTATE_QUAD]
        result = [''.join(ROTATE_WALL.get(c, c) for c in x) for x in result]
        data = result
    return data

def create_grid(quads=None):
    if quads is None:
        quads = [random.choice(pair) for pair in QUADS]
        random.shuffle(quads)
    quads = [quad.split(',') for quad in quads]
    quads = [rotate_quad(quads[i], i) for i in [0, 1, 3, 2]]
    result = [None for i in range(16 * 16)]
    for i, quad in enumerate(quads):
        dx, dy = xy(i, 2)
        for j, data in enumerate(quad):
            x, y = xy(j, 8)
            x += dx * 8
            y += dy * 8
            index = idx(x, y)
            result[index] = data

    #stich seams
    for row in range(16):
        stichIdx = row*16+7
        left = result[stichIdx]
        right = result[stichIdx+1]
        if EAST in left and not WEST in right:
            result[stichIdx+1] += WEST
        if WEST in right and not EAST in left:
            result[stichIdx] += EAST

    for col in range(16):
        stichIdx = 7*16+col
        upper = result[stichIdx]
        lower = result[stichIdx+16]
        if SOUTH in upper and not NORTH in lower:
            result[stichIdx+16] = NORTH + result[stichIdx+16]
        if NORTH in lower and not SOUTH in upper:
            result[stichIdx] = SOUTH + result[stichIdx]

    return result

def to_mask(cell):
    result = 0
    for letter, mask in M_LOOKUP.items():
        if letter in cell:
            result |= mask
    return result

# Game
class Game(object):
    @staticmethod
    def bug():
        quads = [QUAD_B2, QUAD_A4, QUAD_C3, QUAD_D3]
        robots = [171, 19, 127, 14, 211]
        token = 'GT'
        return Game(quads=quads, robots=robots, token=token)
    @staticmethod
    def hardest():
        quads = [QUAD_C2, QUAD_D1, QUAD_B1, QUAD_A1]
        robots = [226, 48, 43, 18]
        token = 'BT'
        return Game(quads=quads, robots=robots, token=token)
    @staticmethod
    def medium():
         # C3,B2,A2,D4 -r red,11,1 -r blue,5,7 -r yellow,5,0 -r green,14,0 -g blue,circle
        quads = [QUAD_C3, QUAD_B2, QUAD_D4, QUAD_A2]
        robots = [177, 224, 87, 80]
        token = 'BC'
        return Game(quads=quads, robots=robots, token=token)
    def __init__(self, seed=None, quads=None, robots=None, token=None):
        if seed:
            random.seed(seed)
        self.grid = create_grid(quads)
        if robots is None:
            self.robots = self.place_robots()
        else:
            self.robots = dict(zip(ROBOT_COLORS, robots))
        self.token = token or random.choice(TOKENS)
        self.moves = 0
        self.last = None
    def place_robots(self):
        result = {}
        used = set()
        for color in ROBOT_COLORS:
            while True:
                index = random.randint(0, 255)
                if index in (119, 120, 135, 136):
                    continue
                if self.grid[index][-2:] in TOKENS:
                    continue
                if index in used:
                    continue
                result[color] = index
                used.add(index)
                break
        return result
    def get_robot(self, index):
        for color, position in self.robots.iteritems():
            if position == index:
                return color
        return None
    def can_move(self, color, direction):
        if self.last == (color, REVERSE[direction]):
            return False
        index = self.robots[color]
        if direction in self.grid[index]:
            return False
        new_index = index + OFFSET[direction]
        if new_index in self.robots.itervalues():
            return False
        return True
    def compute_move(self, color, direction):
        index = self.robots[color]
        robots = self.robots.values()
        while True:
            if direction in self.grid[index]:
                break
            new_index = index + OFFSET[direction]
            if new_index in robots:
                break
            index = new_index
        return index
    def do_move(self, color, direction):
        start = self.robots[color]
        last = self.last
        if last == (color, REVERSE[direction]):
            raise Exception
        end = self.compute_move(color, direction)
        if start == end:
            raise Exception
        self.moves += 1
        self.robots[color] = end
        self.last = (color, direction)
        return (color, start, last)
    def undo_move(self, data):
        color, start, last = data
        self.moves -= 1
        self.robots[color] = start
        self.last = last
    def get_moves(self, colors=None):
        result = []
        colors = colors or ROBOT_COLORS
        for color in colors:
            for direction in DIRECTIONS:
                if self.can_move(color, direction):
                    result.append((color, direction))
        return result
    def over(self):
        color = self.token[0]
        return self.token in self.grid[self.robots[color]]
    def key(self):
        return tuple(self.robots.itervalues())
    def search(self):
        #iterative depening
        max_depth = 1
        while True:
            #print 'Searching to depth:', max_depth
            result = self._search([], set(), 0, max_depth)
            if result is not None:
                return result
            max_depth += 1
            print "max depth increased"
    def _search(self, path, memo, depth, max_depth):
        if self.over():
            return list(path)
        if depth == max_depth:
            return None
        key = (depth, self.key())
        if key in memo:
            return None
        memo.add(key)
        if depth == max_depth - 1:
            colors = [self.token[0]]
        else:
            colors = None
        moves = self.get_moves(colors)
        for move in moves:
            data = self.do_move(*move)
            path.append(move)
            result = self._search(path, memo, depth + 1, max_depth)
            path.pop(-1)
            self.undo_move(data)
            if result:
                return result
        return None
    def export(self):
        grid = []
        token = None
        robots = []
        # for i in range(0, 8):
        #     if i < len(self.robots):
        #         index = ROBOT_COLORS[i]
        #         robots.append(self.robots[index])
        #     else:
        #         robots.append(0)
        for i in range(0, len(self.robots)):
            index = ROBOT_COLORS[i]
            robots.append(self.robots[index])

        for index, cell in enumerate(self.grid):
            mask = to_mask(cell)
            if index in robots:
                mask |= M_ROBOT
            grid.append(mask)
            if self.token in cell:
                token = index
        if self.token[0] == 'A':
            robot = None
        else:
            robot = ROBOT_COLORS.index(self.token[0])
        return {
            'grid': grid,
            'robot': robot,
            'robot_count': len(robots),
            'token': token,
            'robots': robots,
        }
