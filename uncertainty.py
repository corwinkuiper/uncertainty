from typing import Dict, List
import math
import sys


class MathsExpression:
    __globals__ = {
        "sin": math.sin,
        "sinh": math.sinh,
        "cos": math.cos,
        "cosh": math.cosh,
        "tan": math.tan,
        "tanh": math.tanh,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "asinh": math.asinh,
        "acosh": math.acosh,
        "atanh": math.atanh,
        "pi": math.pi,
        "e": math.e,
        "exp": math.exp,
        "log": math.log,
        "sqrt": math.sqrt,
        "__builtins__": None,
    }

    class Variable:
        class Coefficient(float):
            def __init__(self, value):
                self.value: float = float(value)
                self.functionParameters: List = []
                self.dry_run: bool = False

            def __call__(self, *arguments) -> float:
                self.functionParameters = list(arguments)
                return self.value

        variableLetterToListPosition: Dict[str, int] = {}
        variables: Dict[str, Coefficient] = {}
        dry_run: bool = True
        variableValues: List[float] = []

        def __getitem__(self, key: str):
            if len(key) == 1 and key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if not key in self.variableLetterToListPosition:
                    self.variableLetterToListPosition[key] = len(
                        self.variableLetterToListPosition
                    )
                if (
                    self.dry_run
                    and len(self.variableValues)
                    <= self.variableLetterToListPosition[key]
                ):
                    self.variables[key] = self.Coefficient(1.0)
                    self.variables[key].dry_run = True
                    return self.variables[key]
                return self.Coefficient(
                    self.variableValues[self.variableLetterToListPosition[key]]
                )
            raise KeyError

        def set_values(self, v: List[float]):
            self.variableValues = v

    @property
    def variables(self) -> Dict[str, List]:
        v = {}
        for name, coeff in self.__variables.variables.items():
            v[name] = coeff.functionParameters

        return v

    def __call__(self, values: Dict[str, float]):

        positionalValues = [0.0] * len(values)
        for name, value in values.items():
            position = self.__variables.variableLetterToListPosition[name]
            positionalValues[position] = value

        self.__variables.set_values(positionalValues)
        return eval(self.__expression, self.__globals__, self.__variables)

    def __init__(self, expression):
        self.__variables = self.Variable()
        eval(expression, self.__globals__, self.__variables)
        self.__variables.dry_run = False
        self.__expression = expression


class Value:
    def __init__(self, number, uncertainty):
        self.number = number
        self.uncertainty = uncertainty

    def __repr__(self):
        return f"{self.number} ± {self.uncertainty}"


if __name__ == "__main__":
    mathsFunctionString = sys.argv[1]
    function = MathsExpression(mathsFunctionString)

    EPSILON = 7.0 / 3 - 4.0 / 3 - 1

    variables = function.variables
    for _, i in variables.items():
        if not len(i) == 2:
            raise ValueError(
                "All defined function variables must have 2 parameters, a value and an uncertainty."
            )

    defaultConnections: Dict[str, float] = {}

    derivatives: Dict[str, float] = {}

    for name, numberUncertaintyList in variables.items():
        defaultConnections[name] = float(numberUncertaintyList[0])

    for name, numberUncertaintyList in variables.items():
        new_for_this = defaultConnections.copy()

        x = numberUncertaintyList[0]
        h = math.sqrt(EPSILON) * x
        xph = x + h
        dx = xph - x

        new_for_this[name] = xph
        slope = (function(new_for_this) - function(defaultConnections)) / dx

        derivatives[name] = slope

    summation = 0.0
    for name, slope in derivatives.items():
        summation += slope ** 2 * variables[name][1] ** 2

    print(Value(function(defaultConnections), math.sqrt(summation)))
