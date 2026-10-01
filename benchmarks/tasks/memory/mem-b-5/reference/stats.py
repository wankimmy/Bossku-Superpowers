"""Stat sheet for tracking fantasy-league player stats."""

from formula import FormulaError, evaluate_formula


class StatSheet:
    def __init__(self):
        self._values = {}
        self._formulas = {}

    def set_cell(self, name, value):
        self._values[name] = value
        self._formulas.pop(name, None)

    def get_cell(self, name):
        return self._values[name]

    def total(self):
        return sum(self._values[name] for name in self._values)

    def set_formula(self, name, expression):
        self._formulas[name] = expression
        self._values.pop(name, None)

    def value_of(self, name):
        if name in self._formulas:
            def resolve(other_name):
                if other_name not in self._values and other_name not in self._formulas:
                    raise FormulaError(f"unknown name in formula: {other_name}")
                return self.value_of(other_name)

            return evaluate_formula(self._formulas[name], resolve)
        return self._values[name]
