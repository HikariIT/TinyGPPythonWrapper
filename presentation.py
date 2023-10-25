from task import Task
import matplotlib.pyplot as plt


class TinyGPPresentation:
    PRESENTATION_DIR = 'results'

    def __init__(self, task: Task):
        self.task = task

    def presentation_generation(self):
        file_name = f'{self.PRESENTATION_DIR}/task_{self.task.task_id}_presentation.py'
        with open(file_name, 'w') as f:
            f.write(self.generate_function_imports())
            f.write('\n')
            f.write(self.generate_plot_function_body())
            f.write(self.generate_main_function_body())

    def generate_function_imports(self) -> str:
        imports = 'import matplotlib.pyplot as plt\n'
        imports += 'import numpy as np\n'
        for i in range(len(self.task.bounds)):
            imports += f'from functions.problem_{self.task.task_id}_{i} import f_{self.task.task_id}_{i}\n'
        return imports + '\n'

    def generate_main_function_body(self) -> str:
        body = 'def main():\n'

        if len(self.task.formula.free_symbols) == 1:
            body += f'    fig, axes = plt.subplots(2, {len(self.task.bounds) // 2})\n'
            body += f'    fig.suptitle(\'Task {self.task.task_id}\')\n'
            body += f'    fig.set_size_inches(20, 12)\n\n'
            for i in range(len(self.task.bounds)):
                body += f'    plot_function(axes[{i // 2}][{i % 2}], f_{self.task.task_id}_{i}, {self.task.bounds[i]}, {i})\n'
        else:
            for i in range(len(self.task.bounds)):
                body += f'    plot_function(f_{self.task.task_id}_{i}, {self.task.bounds[i]}, {i})\n'

        body += '\n    plt.show()\n'

        if len(self.task.formula.free_symbols) == 1:
            body += '    fig.savefig(\'img/task_' + str(self.task.task_id) + '_plot.png\')\n\n\n'

        body += 'if __name__ == \'__main__\':\n'
        body += '    main()\n'
        return body

    def generate_plot_function_body(self) -> str:
        if len(self.task.formula.free_symbols) == 1:
            return self.generate_plot_function_body_1d()
        elif len(self.task.formula.free_symbols) == 2:
            return self.generate_plot_function_body_2d()

    def generate_plot_function_body_1d(self) -> str:
        body = 'def plot_function(ax, f, bounds: tuple[float, float], bound_id: int):\n'
        body += f'    x = np.linspace(bounds[0], bounds[1], {self.task.data_point_count})\n'
        body += '    y_pred = f(x)\n'
        body += '    ax.plot(x, y_pred, \'bo\')\n'
        body += '    y_true = np.zeros(len(x))\n'
        body += f'    with open(\'../data/problem_{self.task.task_id}_\' + str(bound_id) + \'.dat\')' + ' as file:\n'
        body += '        for i, line in enumerate(file.readlines()[1:]):\n'
        body += '            y_true[i] = float(line.split(\' \')[1])\n'
        body += '    ax.plot(x, y_true, \'r-\')\n'
        body += '    ax.set_title(f\'Bounds: {bounds}\')\n'
        body += '    ax.set_xlabel(\'x\')\n'
        body += '    ax.set_ylabel(\'y\')\n'

        return body + '\n\n'

    def generate_plot_function_body_2d(self) -> str:
        body = 'def plot_function(f, bounds: tuple[float, float], bound_id: int):\n'
        body += '    fig, ax = plt.subplots(subplot_kw={\'projection\': \'3d\'})\n\n'
        body += f'    x = np.linspace(bounds[0], bounds[1], {self.task.data_point_count})\n'
        body += f'    y = np.linspace(bounds[0], bounds[1], {self.task.data_point_count})\n'
        body += '    X, Y = np.meshgrid(x, y)\n'
        body += '    Z_pred = f(X, Y)\n'
        body += '    ax.plot_surface(X, Y, Z_pred, cmap=\'viridis\', edgecolor=\'none\')\n'
        body += f'    with open(\'../data/problem_{self.task.task_id}_\' + str(bound_id) + \'.dat\')' + ' as file:\n'
        body += '        for line in file.readlines()[1:]:\n'
        body += '            x, y, z = line.split(\' \')\n'
        body += '            ax.scatter(float(x), float(y), float(z), color=\'red\')\n'
        body += '    ax.set_title(f\'Bounds: {bounds}\')\n'
        body += '    ax.set_xlabel(\'x\')\n'
        body += '    ax.set_ylabel(\'y\')\n'
        body += '    ax.set_zlabel(\'z\')\n'
        body += '    fig.savefig(\'img/task_' + str(self.task.task_id) + '_plot_\' + str(bound_id) + \'.png\')\n\n\n'

        return body

"""
import sympy as sp
from settings import TinyGPSettings

x = sp.Symbol('x')
y = sp.Symbol('y')
settings = TinyGPSettings(10, -5.0, 5.0)
n = 100

t = Task(4, x + 2 * y, settings, [(0.0, 1.0), (-10.0, 10.0), (0.0, 100.0), (-1000, 1000)], n // 10)
presentation = TinyGPPresentation(t)
presentation.presentation_generation()
"""