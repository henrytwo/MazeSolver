from pygame import *
import queue

maze = image.load('maze.png')#input('Maze Image: '))

graph = []

# Use bfs to traverse maze and build graph

STARTING = (1, 1)
ENDING = (maze.get_width() - 2 , maze.get_height() - 2)

found_start = False
found_end = False

for x in range(maze.get_width()):
    for y in range(maze.get_height()):
        if maze.get_at((x, y)) == (0, 255, 0):
            print('Found starting point at:', x, y)

            STARTING = (x, y)

            found_start = True

        if maze.get_at((x, y)) == (255, 0, 0):
            print('Found ending point at:', x, y)

            ENDING = (x, y)

            found_end = True

        if found_end and found_start:
            break

    if found_end and found_start:
            break

q = queue.Queue()
q.put([STARTING, STARTING, (-1, -1)])

nodes = {STARTING}
edges = set()

TRAVEL_TO = [
    [(0, -1),
    (0, 1)],
    [(-1, 0),
    (1, 0)]
]

traversed = {STARTING}

def valid_point(x, y):
    return 0 <= x < maze.get_width() and 0 <= y < maze.get_height() and maze.get_at((x, y)) == (255, 255, 255)

while not q.empty():
    coords, origin, last_step = q.get()

    x, y = coords

    connection_count = 0 # It is a node if it connects to more than one thing or it's a dead end

    queuing_queue = queue.Queue()

    for direction in TRAVEL_TO:
        for tx, ty in direction:
            nx, ny = tx + x, ty + y


            if (nx, ny) not in traversed and valid_point(nx, ny):
                queuing_queue.put((nx, ny))

                traversed.add((nx, ny))

                connection_count += 1

                ox, oy = last_step

                # ADD LAST COORDINATE
                if (x - ox, y - oy) not in direction:
                    connection_count += 2

    is_node = False

    # ADD 90 DEGREE TURNS

    if connection_count == 0 or connection_count > 1: # A node either has no connections or directly connects to more than 1
        nodes.add((x, y))
        edges.add((origin, (x, y)))

        is_node = True

    while not queuing_queue.empty():
        q.put([queuing_queue.get(), (x, y) if is_node else origin, (x, y)])


#thingie = [[' ' for _ in range(maze.get_height())] for __ in range(maze.get_width())]

#for x, y in nodes:
#    thingie[y][x] = '*'

#print('\n'.join([str(n) for n in thingie]))

#import pprint
#pprint.pprint(thingie)



