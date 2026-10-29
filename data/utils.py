from collections import deque
import heapq
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

def dfs(adj: dict, start, visited=None, path=None):
    if visited is None:
        visited = set()
        path = []
        
    visited.add(start)
    path.append(start)
    
    for neighbor in adj.get(start, []):
        if neighbor not in visited:
            dfs(adj, neighbor, visited, path)
            
    return path

def bfs(adj, start):
    visited = set()
    res = []
    
    q = deque()
    visited.add(start)
    q.append(start)

    while q:
        curr = q.popleft()
        res.append(curr)

        for neighbor in adj[curr]:
            if neighbor not in visited:
                visited.add(neighbor)
                q.append(neighbor)
                
    return res

def reconstruct_path(visited, start, goal):
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = visited[current][1]
    return path[::-1]

def uniform_cost_search(graph, start, goal):
    priority_queue = [(0, start)]
    visited = {start: (0, None)}
    
    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)
        
        if current_node == goal:
            return current_cost, reconstruct_path(visited, start, goal)
            
        for neighbor, cost in graph[current_node]:
            total_cost = current_cost + cost
            
            if neighbor not in visited or total_cost < visited[neighbor][0]:
                visited[neighbor] = (total_cost, current_node)
                heapq.heappush(priority_queue, (total_cost, neighbor))
                
    return None

def visualize_maze(maze, start, goal, path=None, algo='bfs'):
    cmap = ListedColormap(['white', 'black', 'red', 'blue', 'green'])
    bounds = [0, 0.5, 1.5, 2.5, 3.5, 4.5]
    norm = plt.Normalize(bounds[0], bounds[-1])
    
    fig, ax = plt.subplots()
    ax.imshow(maze, cmap=cmap, norm=norm)
    
    ax.scatter(start[1], start[0], color='yellow', marker='o', label='Start')
    ax.scatter(goal[1], goal[0], color='purple', marker='o', label='Goal')
    
    if path:
        for node in path[1:-1]:
            ax.scatter(node[1], node[0], color='green', marker='o')
    
    if algo == 'bfs':
        ax.set_title("Breadth-First Search (BFS)")
    else:
        ax.set_title("Depth-First Search (DFS)")
        
    ax.legend()
    plt.show()

def idastar_search(graph, heuristics, start, goal, stats=None):
    threshold = heuristics[start]
    if stats is not None:
        stats.update(thresholds=[], expanded=0, stack_peak=1, trace=[])
    
    def search(node, g, threshold, path):
        if stats is not None:
            stats['stack_peak'] = max(stats['stack_peak'], len(path) + 1)
        f = g + heuristics[node]
        if f > threshold:
            return f, None
        if node == goal:
            return -1, path + [node]
        if stats is not None:
            stats['expanded'] += 1
            stats['trace'].append(node)
            
        min_threshold = float('inf')
        for neighbor, cost in graph.get(node, []):
            if neighbor not in path:
                temp_curr, result_path = search(neighbor, g + cost, threshold, path + [node])
                if temp_curr == -1:
                    return -1, result_path
                if temp_curr < min_threshold:
                    min_threshold = temp_curr
        return min_threshold, None

    path = []
    while True:
        if stats is not None:
            stats['thresholds'].append(threshold)
        temp, result_path = search(start, 0, threshold, path)
        if temp == -1:
            return result_path, threshold
        if temp == float('inf'):
            return None, float('inf')
        threshold = temp

def rbfs_search(graph, heuristics, start, goal, stats=None):
    if stats is not None:
        stats.update(expanded=0, stack_peak=1, trace=[])
    def rbfs(node, g, node_f, f_limit, path):
        if stats is not None:
            stats['stack_peak'] = max(stats['stack_peak'], len(path) + 1)
        if node == goal:
            return True, path + [node], node_f
        if stats is not None:
            stats['expanded'] += 1
            stats['trace'].append(node)
            
        successors = graph.get(node, [])
        if not successors:
            return False, [], float('inf')
            
        succ_nodes = []
        for neighbor, cost in successors:
            if neighbor in path:
                continue
            total_g = g + cost
            child_f = max(total_g + heuristics[neighbor], node_f)
            succ_nodes.append([child_f, neighbor, cost])
        if not succ_nodes:
            return False, [], float('inf')
            
        while True:
            succ_nodes.sort(key=lambda x: x[0])
            best_f, best_node, best_cost = succ_nodes[0]
            
            if best_f == float('inf') or best_f > f_limit:
                return False, [], best_f
                
            alt_f = succ_nodes[1][0] if len(succ_nodes) > 1 else float('inf')
            
            result_bool, result_path, new_best_f = rbfs(
                best_node, g + best_cost, best_f, min(f_limit, alt_f), path + [node]
            )
            
            if result_bool:
                return True, result_path, best_f
                
            succ_nodes[0][0] = new_best_f

    success, path, _ = rbfs(start, 0, heuristics[start], float('inf'), [])
    return path if success else None

def sma_star_search(graph, heuristics, start, goal, max_memory=5, stats=None):
    """Demo frontier terbatas, BUKAN SMA* penuh: tanpa backup/regenerasi.

    max_memory membatasi jumlah entri frontier, bukan seluruh memori program.
    Tidak menjamin complete atau optimal.
    """
    if max_memory < 1:
        raise ValueError('max_memory minimal 1')
    if stats is not None:
        stats.update(pruned=0, frontier_peak=1, expanded=0, trace=[])
    open_list = [(heuristics[start], 0, [start])]
    
    while open_list:
        open_list.sort(key=lambda x: (x[0], -len(x[2])))
        current_f, current_g, path = open_list.pop(0)
        current_node = path[-1]
        
        if current_node == goal:
            return path, current_g
        if stats is not None:
            stats['expanded'] += 1
            stats['trace'].append(current_node)
            
        successors = graph.get(current_node, [])
        for neighbor, cost in successors:
            if neighbor not in path:
                g_new = current_g + cost
                f_new = max(current_f, g_new + heuristics[neighbor])
                open_list.append((f_new, g_new, path + [neighbor]))
                
        while len(open_list) > max_memory:
            open_list.sort(key=lambda x: (x[0], -len(x[2])))
            open_list.pop() 
            if stats is not None:
                stats['pruned'] += 1
        if stats is not None:
            stats['frontier_peak'] = max(stats['frontier_peak'], len(open_list))
            
    return None, float('inf')
