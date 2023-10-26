import matplotlib.pyplot as plt
import numpy as np
from functions.problem_6_0 import f_6_0
from functions.problem_6_1 import f_6_1
from functions.problem_6_2 import f_6_2
from functions.problem_6_3 import f_6_3


def plot_function(f, bounds: tuple[float, float], bound_id: int):
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})

    x = np.linspace(bounds[0], bounds[1], 10)
    y = np.linspace(bounds[0], bounds[1], 10)
    X, Y = np.meshgrid(x, y)
    Z_pred = f(X, Y)
    ax.plot_surface(X, Y, Z_pred, cmap='viridis', edgecolor='none')
    with open('../data/problem_6_' + str(bound_id) + '.dat') as file:
        for line in file.readlines()[1:]:
            x, y, z = line.split(' ')
            ax.scatter(float(x), float(y), float(z), color='red')
    ax.set_title(f'Bounds: {bounds}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    fig.savefig('img/task_6_plot_' + str(bound_id) + '.png')


def main():
    plot_function(f_6_0, (-10.0, 10.0), 0)
    plot_function(f_6_1, (0.1, 100.0), 1)
    plot_function(f_6_2, (-1.0, 1.0), 2)
    plot_function(f_6_3, (-1000, 1000), 3)

    plt.show()
if __name__ == '__main__':
    main()
