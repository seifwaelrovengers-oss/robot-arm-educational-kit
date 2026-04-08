import matplotlib.pyplot as plt

def plot_arm(points):
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]

    ax = plt.figure().add_subplot(projection='3d')
    ax.plot(xs, ys, zs, '-o')
    plt.show()