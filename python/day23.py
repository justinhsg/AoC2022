from typing import List, Dict, Set
from utils import ISolution, Pint

OutputType = int
InputType = List[List[str]]


class Day23Solution(ISolution):

    _DAY_STRING: str = "23"
    _considers = [
        [(-1, -1), (0, -1), (1, -1)],
        [(-1, 1), (0, 1), (1, 1)],
        [(-1, -1), (-1, 0), (-1, 1)],
        [(1, -1), (1, 0), (1, 1)],
    ]
    _dirs = list("NSWE")
    _neighbours = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return [list(line) for line in raw_input.split("\n")]

    @classmethod
    def _print_grid(cls, elves: Set[Pint]) -> None:
        xs = [x for x, _ in elves]
        ys = [y for _, y in elves]
        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        grid = [["." for _ in range(minx, maxx + 1)] for _ in range(miny, maxy + 1)]
        print(f"Top-left is {(miny, minx)}")
        for (x, y) in elves:
            grid[y - miny][x - minx] = "#"
        for line in grid:
            print("".join(line))

    @classmethod
    def _part_one(cls, grid: InputType) -> OutputType:
        elves: Set[Pint] = set()
        for y, line in enumerate(grid):
            for x, col in enumerate(line):
                if col == "#":
                    elves.add((x, y))
        to_move: Dict[Pint, List[Pint]] = {}
        consider_idx = 0
        for _ in range(10):
            to_move.clear()
            for (x, y) in sorted(elves):
                can_place = True
                ns = 0
                for (dx, dy) in cls._neighbours:
                    if (x + dx, y + dy) in elves:
                        ns += 1
                if ns == 0:
                    continue
                for i in range(4):
                    can_place = True
                    consider_arr = cls._considers[(i + consider_idx) % 4]
                    for (dx, dy) in consider_arr:
                        tx = x + dx
                        ty = y + dy
                        if (tx, ty) in elves:
                            can_place = False
                            break
                    if can_place:
                        nx = x + consider_arr[1][0]
                        ny = y + consider_arr[1][1]
                        if (nx, ny) not in to_move:
                            to_move[(nx, ny)] = []
                        to_move[(nx, ny)].append((x, y))
                        break
            for key, value in to_move.items():
                if len(value) == 1:
                    assert value[0] in elves
                    assert key not in elves
                    elves.add(key)
                    elves.remove(value[0])
            consider_idx = (consider_idx + 1) % 4
        xs = [x for x, _ in elves]
        ys = [y for _, y in elves]
        return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) - len(elves)

    @classmethod
    def _part_two(cls, grid: InputType) -> OutputType:
        elves: Set[Pint] = set()
        for y, line in enumerate(grid):
            for x, col in enumerate(line):
                if col == "#":
                    elves.add((x, y))
        to_move: Dict[Pint, List[Pint]] = {}
        consider_idx = 0
        elves_moved = 1
        rnd = 0
        while elves_moved != 0:
            elves_moved = 0
            rnd += 1
            to_move.clear()
            for (x, y) in sorted(elves):
                can_place = True
                ns = 0
                for (dx, dy) in cls._neighbours:
                    if (x + dx, y + dy) in elves:
                        ns += 1
                if ns == 0:
                    continue
                for i in range(4):
                    can_place = True
                    consider_arr = cls._considers[(i + consider_idx) % 4]
                    for (dx, dy) in consider_arr:
                        tx = x + dx
                        ty = y + dy
                        if (tx, ty) in elves:
                            can_place = False
                            break
                    if can_place:
                        nx = x + consider_arr[1][0]
                        ny = y + consider_arr[1][1]
                        if (nx, ny) not in to_move:
                            to_move[(nx, ny)] = []
                        to_move[(nx, ny)].append((x, y))
                        break
            for key, value in to_move.items():
                if len(value) == 1:
                    assert value[0] in elves
                    assert key not in elves
                    elves.add(key)
                    elves.remove(value[0])
                    elves_moved += 1
            consider_idx = (consider_idx + 1) % 4
        return rnd


if __name__ == "__main__":
    print("===SAMPLE===")
    Day23Solution.do_solution()
    print("===ACTUAL===")
    Day23Solution.do_solution(False)
