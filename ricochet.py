from ctypes import *
# import timeit
from timeit import default_timer as timer

ROBOT_COLORS = {
    0: 'R',
    1: 'G',
    2: 'B',
    3: 'Y',
    4: 'M',
}

TARGET_COLORS = {
    0: 'R',
    1: 'G',
    2: 'B',
    3: 'Y',
}

DIRECTIONS = {
    1: 'N',
    2: 'E',
    4: 'S',
    8: 'W',
}

dll = CDLL('./_ricochet')

class Game(Structure):
    _fields_ = [
        ('grid', c_uint * 256),
        ('moves', c_uint * 256),
        ('robots', c_uint * 8),
        ('robot_count', c_uint),
        ('token', c_uint),
        ('last', c_uint),
    ]

CALLBACK_FUNC = CFUNCTYPE(None, c_uint, c_uint, c_uint, c_uint)

def search(game, callback=None):
    callback = CALLBACK_FUNC(callback) if callback else None
    data = game.export()
    cgame = Game()
    cgame.robot_count = data['robot_count']
    cgame.token = data['token']
    cgame.last = 0
    for index, value in enumerate(data['grid']):
        cgame.grid[index] = value
    for index, value in enumerate(data['robots']):
        cgame.robots[index] = value
    robot = data['robot']
    colors = list('RGBY')
    colors[0], colors[robot] = colors[robot], colors[0]
    game.robots[0], game.robots[robot] = game.robots[robot], game.robots[0]
    path = create_string_buffer(256)
    start = timer()
    depth = dll.search(byref(cgame), path, callback)
    end = timer()
    print(end - start)
    result = []
    for value in path.raw[:depth]:
        value = ord(value)
        color = colors[(value >> 4) & 0x0f]
        direction = DIRECTIONS[value & 0x0f]
        result.append((color, direction))
    return result

if __name__ == '__main__':
    import model
    import time
    import random
    import collections
    count = 0
    best = (0, 0)
    hist = collections.defaultdict(int)
    def callback(depth, nodes, inner, hits):
        print 'Depth: %d, Nodes: %d (%d inner, %d hits)' % (depth, nodes, inner, hits)
    seed = 0
    while True:
        count += 1
        #seed = random.randint(0, 0x7fffffff)
        seed += 1
        start = time.clock()
        path = search(model.Game(seed))#, callback)
        moves = len(path)
        hist[moves] += 1
        key = (moves, seed)
        if key > best:
            best = key
        path = [''.join(move) for move in path]
        path = ','.join(path)
        duration = time.clock() - start
        #print '%d. %2d (%.3f) %s [%s]'% (count, moves, duration, best, path)
        #print dict(hist)
        print '%d %d [%s]' % (seed, moves, path)
