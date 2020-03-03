from csp import Constraint, CSP
from typing import List, Dict

class QueensConstraint(Constraint[int, int]):
    def __init__(self, columns: List[int]):
        super().__init__(columns)
        self.columns: List[int] = columns

    def satisfied(self, assigment: Dict[int, int]) -> bool:
        for q1c, q1r in assigment.items():
            for q2c in range(q1c + 1, len(self.columns)):
                if q2c in assigment:
                    q2r: int = assigment[q2c]
                    if q1r == q2r: return False
                    if abs(q1r - q2r) == abs(q1c - q2c): return False
        return True

if __name__ == "__main__":
    columns: List[int] = [i for i in range(1, 9)]
    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = [i for i in range(1, 9)]
    csp: CSP[int, int] = CSP(columns, rows)
    csp.add_constraint(QueensConstraint(columns))
    solution: Dict[int, int] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)
