"""Visualisasi untuk notebook pencarian KKA."""
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


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
