import numpy as np

def update_robot_plot(ax, canvas, joints):
    ax.clear()

    angles = [np.radians(j.get() if hasattr(j, 'get') else j) for j in joints]

    x = y = z = 0
    L = 2

    for i in range(len(angles)):
        prev_x, prev_y, prev_z = x, y, z

        x += L * np.cos(sum(angles[:i+1]))
        y += L * np.sin(sum(angles[:i+1]))
        z += L * np.sin(angles[i])

        ax.plot([prev_x, x], [prev_y, y], [prev_z, z], color='orange', linewidth=3)
        ax.scatter(x, y, z)

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([0, 10])

    canvas.draw()