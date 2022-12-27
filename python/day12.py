from typing import List, Tuple
import heapq as hq
from utils import ISolution, Pint

OutputType = int

InputType = List[List[str]]


class Day12Solution(ISolution):

    _DAY_STRING: str = "12"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return [list(line) for line in raw_input.split("\n")]

    @classmethod
    def _elevation(cls, val):
        if val == "S":
            return 0
        if val == "E":
            return 25
        return ord(val) - ord("a")

    @classmethod
    def _delta_elevation(cls, grid: InputType, cxy, nxy):
        cur_val = grid[cxy[0]][cxy[1]]
        next_val = grid[nxy[0]][nxy[1]]

        return cls._elevation(next_val) - cls._elevation(cur_val)

    @classmethod
    def _part_one(cls, grid: InputType) -> OutputType:
        width = len(grid[0])
        height = len(grid)
        start = (0, 0)
        end = (0, 0)
        for ri, row in enumerate(grid):
            for ci, col in enumerate(row):
                if col == "S":
                    start = (ri, ci)
                if col == "E":
                    end = (ri, ci)
        distances = [[width * height for _ in row] for row in grid]
        distances[start[0]][start[1]] = 0
        to_visit: List[Tuple[int, Pint]] = []
        dxys = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        hq.heappush(to_visit, (0, start))
        while len(to_visit) != 0:
            cur_d, cur_pos = hq.heappop(to_visit)
            cur_x, cur_y = cur_pos
            if distances[cur_x][cur_y] < cur_d:
                continue
            if cur_pos == end:
                return cur_d
            for dx, dy in dxys:
                n_x = cur_x + dx
                n_y = cur_y + dy
                if 0 <= n_x < height and 0 <= n_y < width:
                    d_d = cls._delta_elevation(grid, cur_pos, (n_x, n_y))

                    if d_d <= 1:
                        n_d = cur_d + 1
                        if n_d < distances[n_x][n_y]:
                            distances[n_x][n_y] = n_d
                            hq.heappush(to_visit, (n_d, (n_x, n_y)))
        return -1

    @classmethod
    def _part_two(cls, grid: InputType) -> OutputType:
        width = len(grid[0])
        height = len(grid)
        end = (0, 0)
        to_visit: List[Tuple[int, Pint]] = []
        distances = [[width * height for _ in row] for row in grid]
        for ri, row in enumerate(grid):
            for ci, col in enumerate(row):
                if col == "S" or col == "a":
                    distances[ri][ci] = 0
                    hq.heappush(to_visit, (0, (ri, ci)))
                if col == "E":
                    end = (ri, ci)

        dxys = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        while len(to_visit) != 0:
            cur_d, cur_pos = hq.heappop(to_visit)
            cur_x, cur_y = cur_pos
            if distances[cur_x][cur_y] < cur_d:
                continue
            if cur_pos == end:
                return cur_d
            for dx, dy in dxys:
                n_x = cur_x + dx
                n_y = cur_y + dy
                if 0 <= n_x < height and 0 <= n_y < width:
                    d_d = cls._delta_elevation(grid, cur_pos, (n_x, n_y))

                    if d_d <= 1:
                        n_d = cur_d + 1
                        if n_d < distances[n_x][n_y]:
                            distances[n_x][n_y] = n_d
                            hq.heappush(to_visit, (n_d, (n_x, n_y)))
        return -1


if __name__ == "__main__":
    print("===SAMPLE===")
    Day12Solution.do_solution()
    print("===ACTUAL===")
    Day12Solution.do_solution(False)
