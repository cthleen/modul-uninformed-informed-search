"""Eksperimen KKA: input, urutan tetangga, dan penghitung yang eksplisit."""
from collections import deque
from heapq import heappop, heappush
from itertools import count

MAZE = (
    (0, 0, 0, 0, 0),
    (1, 1, 0, 1, 1),
    (0, 0, 0, 0, 0),
    (0, 1, 1, 1, 0),
    (0, 0, 0, 0, 0),
)
START, GOAL = (0, 0), (4, 4)
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def grid_neighbors(grid, node):
    r, c = node
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] == 0:
            yield (nr, nc), 1


def result(path, cost, expanded, frontier_peak, trace):
    return dict(path=path, cost=cost, expanded=expanded,
                frontier_peak=frontier_peak, trace=trace)


def best_first(start, goal, neighbors, heuristic=lambda _: 0, weight=1, greedy=False):
    """UCS/A*/Weighted A*/GBFS; g-score membuka ulang state jika g membaik.

    expanded = state non-goal yang successor-nya dibangkitkan, termasuk re-expansion.
    Tie: FIFO; entri usang tidak dihitung. frontier_peak termasuk entri usang.
    """
    if weight < 0:
        raise ValueError('weight harus nonnegatif')
    serial = count()
    frontier = [(weight * heuristic(start), next(serial), 0, start)]
    costs, parents = {start: 0}, {start: None}
    trace, peak = [], 1
    while frontier:
        _, _, g, node = heappop(frontier)
        if g != costs[node]:
            continue
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parents[node]
            return result(path[::-1], g, len(trace), peak, trace)
        trace.append(node)
        for child, step_cost in neighbors(node):
            if step_cost <= 0:
                raise ValueError('Eksperimen ini mensyaratkan biaya edge positif')
            new_g = g + step_cost
            if new_g < costs.get(child, float('inf')):
                costs[child], parents[child] = new_g, node
                priority = heuristic(child) if greedy else new_g + weight * heuristic(child)
                heappush(frontier, (priority, next(serial), new_g, child))
        peak = max(peak, len(frontier))
    return result(None, float('inf'), len(trace), peak, trace)


def maze_search(method, grid=MAZE, start=START, goal=GOAL, limit=12):
    neighbors = lambda node: grid_neighbors(grid, node)
    if method in ('UCS', 'GBFS', 'A*'):
        h = (lambda node: manhattan(node, goal)) if method != 'UCS' else (lambda _: 0)
        return best_first(start, goal, neighbors, h, greedy=method == 'GBFS')
    if method in ('DLS', 'IDS'):
        trace, peak = [], 1

        def visit(node, path, remaining):
            nonlocal peak
            peak = max(peak, len(path))
            if node == goal:
                return path
            if remaining == 0:
                return None
            trace.append(node)
            for child, _ in neighbors(node):
                if child not in path:
                    found = visit(child, path + [child], remaining - 1)
                    if found is not None:
                        return found
            return None

        for bound in range(limit + 1) if method == 'IDS' else (limit,):
            path = visit(start, [start], bound)
            if path is not None:
                return result(path, len(path) - 1, len(trace), peak, trace)
        return result(None, float('inf'), len(trace), peak, trace)
    if method not in ('DFS', 'BFS'):
        raise ValueError(method)
    frontier = deque([(start, [start])])
    visited, trace, peak = set(), [], 1
    while frontier:
        node, path = frontier.pop() if method == 'DFS' else frontier.popleft()
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return result(path, len(path) - 1, len(trace), peak, trace)
        trace.append(node)
        for child, _ in neighbors(node):
            if child not in visited:
                frontier.append((child, path + [child]))
        peak = max(peak, len(frontier))
    return result(None, float('inf'), len(trace), peak, trace)


def bidirectional_path(neighbors, start, goal, stats=None):
    """BFS dua arah per LAPISAN; graf tak berarah, biaya tiap edge = 1."""
    if stats is not None:
        stats.update(expanded=0, frontier_peak=2, trace=[])
    if start == goal:
        return [start]
    fronts = [deque([start]), deque([goal])]
    parents = [{start: None}, {goal: None}]
    distances = [{start: 0}, {goal: 0}]
    while all(fronts):
        for side in (0, 1):
            meetings = []
            for _ in range(len(fronts[side])):
                node = fronts[side].popleft()
                if stats is not None:
                    stats['expanded'] += 1
                    stats['trace'].append((side, node))
                for child in neighbors(node):
                    if child not in parents[side]:
                        parents[side][child] = node
                        distances[side][child] = distances[side][node] + 1
                        fronts[side].append(child)
                        if child in parents[1 - side]:
                            meetings.append(child)
                if stats is not None:
                    stats['frontier_peak'] = max(stats['frontier_peak'], sum(map(len, fronts)))
            if meetings:
                meeting = min(meetings, key=lambda n: distances[0][n] + distances[1][n])
                left, right, node = [], [], meeting
                while node is not None:
                    left.append(node)
                    node = parents[0][node]
                node = parents[1][meeting]
                while node is not None:
                    right.append(node)
                    node = parents[1][node]
                return left[::-1] + right
    return None


PUZZLE_GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
PUZZLE_START = (7, 2, 4, 5, 0, 6, 8, 3, 1)


def puzzle_neighbors(state):
    blank = state.index(0)
    r, c = divmod(blank, 3)
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            child = list(state)
            j = 3 * nr + nc
            child[blank], child[j] = child[j], child[blank]
            yield tuple(child), 1


def misplaced(state):
    return sum(tile != 0 and tile != PUZZLE_GOAL[i] for i, tile in enumerate(state))


def puzzle_manhattan(state):
    return sum(manhattan(divmod(i, 3), divmod(tile - 1, 3))
               for i, tile in enumerate(state) if tile)


def animate_expansion(grid, search_result, start=START, goal=GOAL):
    """Animasi HTML dari trace aktual; tidak memerlukan GIF eksternal/ffmpeg."""
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from matplotlib.colors import ListedColormap
    from IPython.display import HTML

    fig, ax = plt.subplots(figsize=(4, 4))
    base = np.array(grid, dtype=int)
    picture = ax.imshow(base, cmap=ListedColormap(['white', 'black', '#87ceeb', '#70c070']), vmin=0, vmax=3)
    ax.scatter([start[1], goal[1]], [start[0], goal[0]], c=['orange', 'purple'])
    trace, path = search_result['trace'], search_result['path'] or []

    def update(frame):
        canvas = base.copy()
        for r, c in trace[:frame]:
            canvas[r, c] = 2
        if frame == len(trace):
            for r, c in path:
                canvas[r, c] = 3
        picture.set_data(canvas)
        ax.set_title(f'Ekspansi {frame}/{len(trace)}')
        return (picture,)

    animation = FuncAnimation(fig, update, frames=len(trace) + 1, interval=200)
    html = HTML(animation.to_jshtml())
    plt.close(fig)
    return html
