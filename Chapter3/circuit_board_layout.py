from csp import CSP, Constraint
from typing import List, NamedTuple, Dict, Optional

class GridLocation(NamedTuple):
    row: int
    col: int

class Block(NamedTuple):
    n: int
    w: int
    h: int

class Grid:
    def __init__(self, w: int, h: int) -> None:
        self._grid: List[List[str]] = []
        for i in range(h):
            self._grid.append([])
            for _ in range(w):
                self._grid[i].append('.')

    def applyBlock(self, name: str, locs: List[GridLocation]):
        for l in locs:
            self._grid[l.row][l.col] = name

    def __repr__(self):
        result: str = ""
        for row in self._grid:
            result = result + "".join(row) + "\n"
        return result

class CircuitBoardConstraint(Constraint[int, List[List[GridLocation]]]):
    def __init__(self, blocks: List[int]) -> None:
        super().__init__(blocks)
        self.blocks: List[int] = blocks

    def satisfied(self, assigment: Dict[int, List[GridLocation]]) -> bool:
        allLocations: List[GridLocation] = [loc for values in assigment.values() for loc in values]
        return len(set(allLocations)) == len(allLocations)

def buildBlockDomain(block: Block, gridw: int, gridh: int) -> List[List[GridLocation]]:
    lst: List[List[GridLocation]] = []
    for i in range(gridh):
        for j in range(gridw):
            if i + block.h <= gridh and j + block.w <= gridw:
                tmp: List[GridLocation] = []
                for r in range(i, i + block.h):
                    for c in range(j, j + block.w):
                        tmp.append(GridLocation(r, c))
                lst.append(tmp)
    return lst

if __name__ == "__main__":
    blocks: List[Block] = [Block(1, 1, 6), Block(2, 4, 4), Block(3, 3, 3), Block(4, 2, 2), Block(5, 5, 2)]
    blockDomains: Dict[Block, List[List[GridLocation]]] = {}
    for b in blocks:
        blockDomains[b] = buildBlockDomain(b, 9, 9)
    csp: CSP[Block, List[List[GridLocation]]] = CSP(blocks, blockDomains)
    csp.add_constraint(CircuitBoardConstraint(blocks))
    solution: Optional[Dict[Block, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        grid: Grid = Grid(9, 9)
        for block, locs in solution.items():
            grid.applyBlock(str(block.n), locs)
        print(grid)

