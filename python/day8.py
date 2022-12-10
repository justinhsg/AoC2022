from typing import List

from utils import ISolution


class Day8Solution(ISolution):

    _DAY_STRING: str = "8"

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[List[int]]:
        lines = raw_input.split("\n")
        grid = [[int(digit) for digit in list(line)] for line in lines]
        return grid

    @classmethod
    def _part_one(cls, grid: List[List[int]]) -> int:
        n_row = len(grid)
        n_col = len(grid[0])
        visible = set()
        for i in range(n_row):
            row = grid[i]
            vis_left = row[0]
            visible.add((i, 0))
            vis_right = row[n_col - 1]
            visible.add((i, n_col - 1))
            for j in range(n_col):
                test_left = row[j]
                if test_left > vis_left:
                    vis_left = test_left
                    visible.add((i, j))
                test_right = row[n_col - j - 1]
                if test_right > vis_right:
                    vis_right = test_right
                    visible.add((i, n_col - j - 1))
        for i in range(n_col):
            vis_top = grid[0][i]
            visible.add((0, i))
            vis_bot = grid[n_row - 1][i]
            visible.add((n_row - 1, i))
            for j in range(n_row):
                test_top = grid[j][i]
                if test_top > vis_top:
                    vis_top = test_top
                    visible.add((j, i))
                test_bot = grid[n_row - j - 1][i]
                if test_bot > vis_bot:
                    vis_bot = test_bot
                    visible.add((n_row - j - 1, i))
        return len(visible)

    @classmethod
    def _part_two(cls, grid: List[List[int]]) -> int:
        l_ct = [[0 for _ in row] for row in grid]
        r_ct = [[0 for _ in row] for row in grid]
        t_ct = [[0 for _ in row] for row in grid]
        b_ct = [[0 for _ in row] for row in grid]
        for i, row in enumerate(grid):
            for j in range(1, len(row)):
                val = grid[i][j]
                k = j - 1
                while k > 0 and grid[i][k] < val:
                    k -= 1
                l_ct[i][j] = j - k
            for j in range(len(row) - 2, -1, -1):
                val = grid[i][j]
                k = j + 1
                while k < len(grid[i]) - 1 and grid[i][k] < val:
                    k += 1
                r_ct[i][j] = k - j
        for j in range(len(grid[0])):
            for i in range(1, len(grid)):
                val = grid[i][j]
                k = i - 1
                while k > 0 and grid[k][j] < val:
                    k -= 1
                t_ct[i][j] = i - k
            for i in range(len(grid) - 2, -1, -1):
                val = grid[i][j]
                k = i + 1
                while k < len(grid) - 1 and grid[k][j] < val:
                    k += 1
                b_ct[i][j] = k - i
        answer = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                value = l_ct[i][j] * r_ct[i][j] * t_ct[i][j] * b_ct[i][j]
                if value > answer:
                    answer = value
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day8Solution.do_solution()
    print("===ACTUAL===")
    Day8Solution.do_solution(False)
