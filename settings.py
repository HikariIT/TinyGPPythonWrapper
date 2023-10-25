from dataclasses import dataclass


@dataclass
class TinyGPSettings:
    no_params: int
    min_param_value: float
    max_param_value: float
