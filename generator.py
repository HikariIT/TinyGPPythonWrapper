import sympy as sp
import numpy as np
import itertools as it
from settings import TinyGPSettings


class TinyGPGenerator:

    @staticmethod
    def generate_data(formula: sp.Expr, bounds: dict[sp.Symbol, tuple[float, float]], n: int,
                      settings: TinyGPSettings, filename: str):
        variables = list(bounds.keys())
        data_spans = []
        for var in variables:
            data_spans.append(np.linspace(bounds[var][0], bounds[var][1], n))

        data_points = it.product(*data_spans)
        subs = [{variables[i]: point[i] for i in range(len(variables))} for point in data_points]

        # Evaluate formula at each data point
        result = np.zeros(n ** len(variables))
        for i, sub in enumerate(subs):
            result[i] = formula.subs(subs[i])

        # Save data to csv file in form:
        # First line: no. variables, no. parameters, min parameter value, max parameter value, no. data points
        # Next lines: values of each variable, result
        with open(filename, 'w') as f:
            line = f'{len(bounds.keys())} {settings.no_params} {settings.min_param_value} {settings.max_param_value} {n ** len(variables)}\n'
            f.write(line)
            for i, sub in enumerate(subs):
                line = ''
                for var in variables:
                    line += f'{sub[var]} '
                line += f'{result[i]}\n'
                f.write(line)
