import matplotlib.pyplot as plt
import numpy as np
from functions.problem_1_0 import f_1_0
from functions.problem_1_1 import f_1_1
from functions.problem_1_2 import f_1_2
from functions.problem_1_3 import f_1_3


def plot_function(ax, f, bounds: tuple[float, float], bound_id: int):
    x = np.linspace(bounds[0], bounds[1], 100)
    y_pred = f(x)
    ax.plot(x, y_pred, 'bo')
    y_true = np.zeros(len(x))
    with open('../data/problem_1_' + str(bound_id) + '.dat') as file:
        for i, line in enumerate(file.readlines()[1:]):
            y_true[i] = float(line.split(' ')[1])
    ax.plot(x, y_true, 'r-')
    ax.set_title(f'Bounds: {bounds}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')


def main():
    fig, axes = plt.subplots(2, 2)
    fig.suptitle('Task 1')
    fig.set_size_inches(20, 12)

    plot_function(axes[0][0], f_1_0, (-10.0, 10.0), 0)
    plot_function(axes[0][1], f_1_1, (0.0, 100.0), 1)
    plot_function(axes[1][0], f_1_2, (-1.0, 1.0), 2)
    plot_function(axes[1][1], f_1_3, (-1000, 1000), 3)

    plt.show()
    fig.savefig('img/task_1_plot.png')


if __name__ == '__main__':
    main()
