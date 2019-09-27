from pygame import *
import queue

maze = image.load('maze.png')#input('Maze Image: '))

def parse_maze(maze):
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
        return 0 <= x < maze.get_width() and 0 <= y < maze.get_height() and maze.get_at((x, y)) in [(255, 255, 255), (255, 0, 0), (0, 255, 0)]

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

    return (nodes, edges, STARTING, ENDING)

def bfs(nodes, edges, STARTING, ENDING):

    bfs_q = queue.Queue()

    bfs_q.put((STARTING, [STARTING]))

    visited = {STARTING}

    connections = {}

    for n in nodes:
        connections[n] = set()

        for e in edges:
            if len(set(e)) > 1:
                if e[0] == n:
                    connections[n].add(e[1])
                elif e[1] == n:
                    connections[n].add(e[0])

    found = None

    while not bfs_q.empty():
        coords, before = bfs_q.get()

        x, y = coords

        if (x, y) == ENDING:
            print('Path found', before)

            found = before

            break

    
        for c in connections[(x, y)]:

            if c not in visited:
                visited.add(c)

                bfs_q.put((c, before + [c]))

    return found

nodes, edges, STARTING, ENDING = parse_maze(maze)
path = bfs(nodes, edges, STARTING, ENDING)

new_maze = maze.copy()

if path:
    for e in range(len(path) - 1):
        draw.line(new_maze, (255, 0, 0), path[e], path[e + 1], 1)

image.save(new_maze, 'solved.png')
