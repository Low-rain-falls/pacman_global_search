import heapq

# left - right - up - down
direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]
valid_path = {0, 1, 2, 9}

def get_priority_directions(start, end):
    x, y = start
    ex, ey = end
    direction.sort(key=lambda d: abs((x + d[0]) - ex) + abs((y + d[1]) - ey))

    return direction

# dfs search
def dfs(boards, start, end, countNodes):
    rows = len(boards)
    cols = len(boards[0])

    stack = [(start, [start])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()
        countNodes[0] += 1

        if (x, y) == end:
            return path

        if (x, y) in visited:
            continue

        visited.add((x, y))

        for dx, dy in get_priority_directions((x, y), end):
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and boards[nx][ny] in valid_path and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))

    return None


# bfs search
def bfs(boards, start, end, countNodes):
    rows = len(boards)
    cols = len(boards[0])

    # queue has child and their path
    queue = [(start, [start])]
    # check visited
    visited = set()
    visited.add(start)
    countNodes[0] += 1

    while queue:
        (x, y), path = queue.pop(0)

        if (x, y) == end:
            return path

        for dx, dy in direction:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited and boards[nx][ny] in valid_path:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))
                countNodes[0] += 1

    return None

# ucs search
def ucs(boards, start, end, countNodes):
    rows, cols = len(boards), len(boards[0])
    pq = [(0, start)]
    parent = {}
    cost = {start: 0}
    visited = set()

    while pq:
        cur_cost, (x, y) = heapq.heappop(pq)
        countNodes[0] += 1
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == end:
            path = []
            while (x, y) in parent:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in get_priority_directions((x, y), end):
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and boards[nx][ny] in valid_path and (nx, ny) not in visited:
                new_cost = cur_cost + 1

                if (nx, ny) not in cost or new_cost < cost[(nx, ny)]:
                    cost[(nx, ny)] = new_cost
                    heapq.heappush(pq, (new_cost, (nx, ny)))
                    parent[(nx, ny)] = (x, y)

    return None

def heuristic (a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(boards, start, end, countNodes):
    rows, cols = len(boards), len(boards[0])
    pq = [(0, start)]
    parent = {}
    f_score = {start: 0}
    g_score = {start: heuristic(start, end)}
    visited = set()

    while pq:
        cur_cost, (x, y) = heapq.heappop(pq)
        countNodes[0] += 1
        if (x, y) in visited:
            continue
        visited.add((x, y))

        if (x, y) == end:
            path = []
            while (x, y) in parent:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in get_priority_directions((x, y), end):
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and boards[nx][ny] in valid_path and (nx, ny) not in visited:
                new_cost = f_score[(x, y)] + 1

                if (nx, ny) not in f_score or new_cost < f_score[(nx, ny)]:
                    parent[(nx, ny)] = (x, y)
                    f_score[(nx, ny)] = new_cost
                    g_score[(nx, ny)] = new_cost + heuristic((nx, ny), end)
                    heapq.heappush(pq, (g_score[(nx, ny)], (nx, ny)))

    return None
