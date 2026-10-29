"""Data contoh dan animasi KKA; algoritma didefinisikan di notebook."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from IPython.display import HTML


MAZE = (
    (0, 0, 0, 0, 0),
    (1, 1, 0, 1, 1),
    (0, 0, 0, 0, 0),
    (0, 1, 1, 1, 0),
    (0, 0, 0, 0, 0),
)
START, GOAL = (0, 0), (4, 4)
DIRECTIONS = ((0, 1), (1, 0), (0, -1), (-1, 0))
PUZZLE_GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
PUZZLE_START = (7, 2, 4, 5, 0, 6, 8, 3, 1)


def animate_expansion(grid, search_result, start=START, goal=GOAL):
    """Animasi HTML dari trace aktual; tidak memerlukan GIF eksternal/ffmpeg."""
    fig, ax = plt.subplots(figsize=(4, 4))
    base = np.array(grid, dtype=int)
    picture = ax.imshow(base, cmap=ListedColormap(['white', 'black', '#87ceeb', '#70c070']), vmin=0, vmax=3)
    ax.scatter([start[1], goal[1]], [start[0], goal[0]], c=['orange', 'purple'])
    trace, path = (search_result['trace'], search_result['path'] or [])

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
