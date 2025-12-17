# csp/constraints.py


class SumConstraint:
    """
    Enforces: sum(variables) == total, where each variable is 0/1.
    Works with partial assignments by checking feasibility.
    """

    def __init__(self, variables, total):
        self.variables = list(variables)
        self.total = int(total)

    def is_satisfied(self, assignment: dict) -> bool:
        assigned_vals = []
        unassigned = 0

        for v in self.variables:
            if v in assignment:
                assigned_vals.append(assignment[v])
            else:
                unassigned += 1

        s = sum(assigned_vals)

        # Too many mines already
        if s > self.total:
            return False

        # Even if all remaining were mines, still can't reach total
        if s + unassigned < self.total:
            return False

        return True
