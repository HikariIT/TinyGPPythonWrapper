import sympy as sp

from presentation import TinyGPPresentation
from task import Task
from settings import TinyGPSettings
from task_runner import TinyGPRunner


def main():
    n = 100
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    settings = TinyGPSettings(10, -5.0, 5.0)

    tasks = [
        Task(1, 5 * x ** 3 - 2 * x ** 2 + 3 * x - 17, settings, [(-10.0, 10.0), (0.0, 100.0), (-1.0, 1.0), (-1000, 1000)], n),
        Task(2, sp.sin(x) + sp.cos(x), settings, [(-3.14, 3.14), (0.0, 7.0), (0.0, 100.0), (-100, 100)], n),
        Task(3, 2 * sp.ln(x + 1), settings, [(0.0, 4.0), (0.0, 9.0), (0.0, 99.0), (0.0, 999.0)], n),
        Task(4, x + 2 * y, settings, [(0.0, 1.0), (-10.0, 10.0), (0.0, 100.0), (-1000, 1000)], n // 10),
        Task(5, sp.sin(x / 2) + 2 * sp.cos(x), settings, [(-3.14, 3.14), (0.0, 7.0), (0.0, 100.0), (-100, 100)], n),
        Task(6, x ** 2 + 3 * x * y - 7 * y + 1, settings, [(-10.0, 10.0), (0.1, 100.0), (-0.99, 1.0), (-1000, 1000)], n // 10)
    ]

    for task in tasks:
        task.run()
        print(f'Finished generation of task {task.task_id}')

    for task in tasks[3:]:
        for i in range(len(task.bounds)):
            print(f'Running task {task.task_id} with bounds {task.bounds[i]}')
            task_runner = TinyGPRunner(task.filename(i))
            task_runner.run()
            print(f'Finished running task {task.task_id} with bounds {task.bounds[i]}')
        presentation = TinyGPPresentation(task)
        presentation.presentation_generation()
        print(f'Finished generating presentation of task {task.task_id}')

    """
    for task in tasks[:3]:
        presentation = TinyGPPresentation(task)
        presentation.presentation_generation()
        print(f'Finished generating presentation of task {task.task_id}')
    """

if __name__ == '__main__':
    main()
