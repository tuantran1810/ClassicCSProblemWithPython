from csp import CSP, Constraint
from typing import List, NamedTuple, Optional, Dict
from random import choice
from string import ascii_uppercase

Grid = List[List[str]]

class GridLocation(NamedTuple):
    row: int
    column: int

def generate_grid(rows: int, columns: int) -> Grid:
    return [[choice(ascii_uppercase) for _ in range(columns)] for _ in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))

def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    for row in range(height):
        for column in range(width):
            rows: range = range(row, row + length + 1)
            columns: range = range(column, column + length + 1)
            if column + length <= width:
                domain.append([GridLocation(row, c) for c in columns])
                if row + length <= height:
                    domain.append([GridLocation(r, column + (r - row)) for r in rows])
            if row + length <= height:
                domain.append([GridLocation(r, column) for r in rows])
                if column + length <= width:
                    domain.append([GridLocation(r, column - (r - row)) for r in rows])
    return domain

class WordSearchConstrain(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)

if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, Dict[str, List[GridLocation]]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstrain(words))
    solutions: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solutions is None:
        print("No solution found!")
    else:
        for word, grid_locations in solutions.items():
            if choice([True, False]):
                grid_locations.reverse()
            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = letter
        display_grid(grid)



