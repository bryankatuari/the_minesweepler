class Constraint:
    """
    Represents a Minesweeper sum constraint:
    sum(variables) = required_sum
    where variables are board coordinates (r, c)
    and values are 1 (mine) or 0 (safe)
    """

    def __init__(self, variables, required_sum):
        self.variables = list(variables)
        self.required_sum = required_sum

    def __repr__(self):
        return f"Constraint(vars={self.variables}, sum={self.required_sum})"
