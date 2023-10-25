import sympy as sp
from settings import TinyGPSettings
from generator import TinyGPGenerator


class Task:
    task_id: int
    formula: sp.Expr
    settings: TinyGPSettings
    bounds: list[tuple[float, float]]
    data_point_count: int

    def __init__(self, task_id: int, formula: sp.Expr, settings: TinyGPSettings, bounds: list[tuple[float, float]], data_point_count: int):
        self.task_id = task_id
        self.formula = formula
        self.settings = settings
        self.bounds = bounds
        self.data_point_count = data_point_count

    def run(self):
        bounds_for_each_task = self.prepare_bounds_for_vars()
        for bound_id, bound in enumerate(bounds_for_each_task):
            TinyGPGenerator.generate_data(self.formula, bound, self.data_point_count, self.settings,
                                          self.filename(bound_id))

    def prepare_bounds_for_vars(self) -> list[dict[sp.Symbol, tuple[float, float]]]:
        bounds_for_each_task = []
        for bound in self.bounds:
            bounds_for_each_task.append({var: bound for var in self.formula.free_symbols})
        return bounds_for_each_task

    def filename(self, bound_id: int):
        return f'data/problem_{self.task_id}_{bound_id}.dat'