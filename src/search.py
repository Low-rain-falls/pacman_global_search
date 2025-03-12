import heapq

# left - right - top - down
direction = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def print_board_with_path(board, path):
    if path is None:
        return
    board_copy = [row[:] for row in board]
    for x, y in path:
        board_copy[x][y] = '*'  # mark the path by '*'
    for row in board_copy:
        print("   ".join(str(cell) for cell in row))

# dfs search
def dfs(boards, start, goal, countNodes):
    stack = [(start, [start])]
    visited = set()
    cols = len(boards[0])
    countNodes[0] = 0
    
    while stack:
        (x, y), path = stack.pop()
        
        if (x, y) in visited:
            continue
        
        visited.add((x, y))
        countNodes[0] += 1
        
        if (x, y) == goal:
            return path
        
        for dx, dy in direction:
            nx, ny = x + dx, y + dy
            if 0 <= ny < cols and boards[nx][ny] <= 2 and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))
    
    return None

# bfs search
def bfs(boards, start, end, countNodes):
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
            
            if 0 <= ny < cols and (nx, ny) not in visited:
                if boards[nx][ny] <= 2:
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

        for dx, dy in direction:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and boards[nx][ny] <= 2:
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

        for dx, dy in direction:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and boards[nx][ny] <= 2:
                new_cost = f_score[(x, y)] + 1

                if (nx, ny) not in f_score or new_cost < f_score[(nx, ny)]:
                    parent[(nx, ny)] = (x, y)
                    f_score[(nx, ny)] = new_cost
                    g_score[(nx, ny)] = new_cost + heuristic((nx, ny), end)
                    heapq.heappush(pq, (g_score[(nx, ny)], (nx, ny)))
    
    return None

# demo

# grid = [
#     [3, 3, 3, 3, 3, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 1, 1, 1, 1, 3],
#     [3, 3, 3, 3, 3, 3]
# ]

# start = (2, 3)
# end = (8, 4)

# print("DFS path")
# dfs_path = dfs(grid, start, end)
# print_board_with_path(grid, dfs_path)

# print("BFS path")
# bfs_path = bfs(grid, start, end)
# print_board_with_path(grid, bfs_path)

# print("UCS path")
# ucs_path = ucs(grid, start, end)
# print_board_with_path(grid, ucs_path)

# print("A* path")
# astar_path = astar(grid, start, end)
# print_board_with_path(grid, astar_path)