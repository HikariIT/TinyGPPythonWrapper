import sympy as sp

from presentation import TinyGPPresentation
from task import Task
from settings import TinyGPSettings
from task_runner import TinyGPRunner


# Options are in format task_id.bound_id, divided by spaces.
def generate_functions(tasks: list[Task], options: str = ''):
    if options == '':
        for task in tasks:
            for i in range(len(task.bounds)):
                print(f'Running task {task.task_id} with bounds {task.bounds[i]}')
                task_runner = TinyGPRunner(task.filename(i))
                task_runner.run()
                print(f'Finished running task {task.task_id} with bounds {task.bounds[i]}')
    else:
        for task_bound_id in options.split(' '):
            task_id = int(task_bound_id.split('.')[0]) - 1
            bound_id = int(task_bound_id.split('.')[1])

            task = tasks[task_id]

            print(f'Running task {task_id + 1} with bounds {task.bounds[bound_id]}')
            task_runner = TinyGPRunner(task.filename(bound_id))
            task_runner.run()
            print(f'Finished running task {task.task_id + 1} with bounds {task.bounds[bound_id]}')


# Options are task IDs with spaces in between.
def generate_presentations(tasks: list[Task], options: str = ''):
    if options == '':
        for task in tasks:
            presentation = TinyGPPresentation(task)
            presentation.presentation_generation()
            print(f'Finished generating presentation of task {task.task_id}')
    else:
        for task_id in options.split(' '):
            task = tasks[int(task_id) - 1]
            presentation = TinyGPPresentation(task)
            presentation.presentation_generation()
            print(f'Finished generating presentation of task {task.task_id}')


def main():
    n = 100
    x = sp.Symbol('x')
    y = sp.Symbol('y')
    settings = TinyGPSettings(10, -5.0, 5.0)

    tasks = [
        Task(1, 5 * x ** 3 - 2 * x ** 2 + 3 * x - 17, settings, [(-10.0, 10.0), (0.0, 100.0), (-1.0, 1.0), (-1000, 1000)], n),
        Task(2, sp.sin(x) + sp.cos(x), settings, [(-3.14, 3.14), (0.0, 7.0), (0.0, 100.0), (-100, 100)], n),
        Task(3, 2 * sp.ln(x + 1), settings, [(0.0, 4.0), (0.0, 9.0), (0.0, 99.0), (0.0, 999.0)], n),
        Task(4, x + 2 * y, settings, [(0.0, 1.0), (-10.0, 10.0), (0.0, 100.0), (-1000, 1000)], int(n ** 0.5)),
        Task(5, sp.sin(x / 2) + 2 * sp.cos(x), settings, [(-3.14, 3.14), (0.0, 7.0), (0.0, 100.0), (-100, 100)], n),
        Task(6, x ** 2 + 3 * x * y - 7 * y + 1, settings, [(-10.0, 10.0), (0.1, 100.0), (-1.0, 1.0), (-1000, 1000)], int(n ** 0.5))
    ]

    for task in tasks:
        task.run()
        print(f'Finished generation of task {task.task_id}')

    generate_functions(tasks)
    generate_presentations(tasks)


if __name__ == '__main__':
    main()
