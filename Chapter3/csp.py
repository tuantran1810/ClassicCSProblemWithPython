from typing import TypeVar, Generic, List, Dict, Optional
from abc import ABC, abstractmethod

V = TypeVar('V')
D = TypeVar('D')

class Constraint(Generic[V, D], ABC):
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satified(self, assigment: Dict[V, D]) -> bool:
        ...

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V, D]]] = {}
        for variable in self.variables:
            self.constraints[variable]: List[Constraint[V, D]] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable: V, assigment: Dict[V, D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satified(assigment): return False
        return True

    def backtracking_search(self, assigment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        if (len(assigment) == len(self.variables)): return assigment
        unassigned: List[V] = [v for v in self.variables if v not in assigment]
        first: V = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assigment.copy()
            local_assignment[first] = value
            if self.consistent(first, local_assignment):
                result : Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
                if result is not None: return result
        return None

