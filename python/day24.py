from typing import List
from utils import ISolution


OutputType = int
InputType = List[List[str]]


class Day24Solution(ISolution):

    _DAY_STRING: str = "24"
    _neighbours = [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return [list(line) for line in raw_input.split("\n")]

    @classmethod
    def _part_one(cls, grid: InputType) -> OutputType:

        grid_h = len(grid) - 2
        grid_w = len(grid[0]) - 2
        lefts = [set() for _ in range(grid_h)]
        rights = [set() for _ in range(grid_h)]
        ups = [set() for _ in range(grid_w)]
        downs = [set() for _ in range(grid_w)]
        for r, row in enumerate(grid[1:-1]):
            for c, col in enumerate(row[1:-1]):
                if col == "<":
                    lefts[r].add(c)
                elif col == ">":
                    rights[r].add(c)
                elif col == "^":
                    ups[c].add(r)
                elif col == "v":
                    downs[c].add(r)
        clear_left = []
        clear_right = []
        clear_horiz = []
        for r in range(grid_h):
            t_clear_left = set(range(grid_w)) - lefts[r]
            t_clear_right = set(range(grid_w)) - rights[r]
            clear_left.append([t_clear_left])
            clear_right.append([t_clear_right])
            clear_horiz.append([t_clear_left.intersection(t_clear_right)])
            for t in range(1, grid_w):
                t_clear_left = set((x - 1) % grid_w for x in clear_left[r][t - 1])
                t_clear_right = set((x + 1) % grid_w for x in clear_right[r][t - 1])
                clear_left[r].append(t_clear_left)
                clear_right[r].append(t_clear_right)
                clear_horiz[r].append(t_clear_left.intersection(t_clear_right))

        clear_up = []
        clear_down = []
        clear_vert = []
        for c in range(grid_w):
            t_clear_up = set(range(grid_h)) - ups[c]
            t_clear_down = set(range(grid_h)) - downs[c]
            clear_up.append([t_clear_up])
            clear_down.append([t_clear_down])
            clear_vert.append([t_clear_up.intersection(t_clear_down)])
            for t in range(1, grid_h):
                t_clear_up = set((x - 1) % grid_h for x in clear_up[c][t - 1])
                t_clear_down = set((x + 1) % grid_h for x in clear_down[c][t - 1])
                clear_up[c].append(t_clear_up)
                clear_down[c].append(t_clear_down)
                clear_vert[c].append(t_clear_up.intersection(t_clear_down))
        start = (-1, 0)
        end = (grid_h, grid_w - 1)
        to_explore = set([start])
        to_explore_next = set()
        t = 0
        while len(to_explore) != 0:
            t += 1
            to_explore_next.clear()
            for (r, c) in to_explore:
                for dr, dc in cls._neighbours:
                    nr = r + dr
                    nc = c + dc
                    if (nr, nc) == end:
                        return t
                    if (nr, nc) == start:
                        to_explore_next.add((nr, nc))
                    if 0 <= nr < grid_h and 0 <= nc < grid_w:
                        if (
                            nr in clear_vert[nc][t % grid_h]
                            and nc in clear_horiz[nr][t % grid_w]
                        ):
                            to_explore_next.add((nr, nc))
            to_explore.clear()
            to_explore = set(to_explore_next)
        return -1

    @classmethod
    def _part_two(cls, grid: InputType) -> OutputType:
        grid_h = len(grid) - 2
        grid_w = len(grid[0]) - 2
        lefts = [set() for _ in range(grid_h)]
        rights = [set() for _ in range(grid_h)]
        ups = [set() for _ in range(grid_w)]
        downs = [set() for _ in range(grid_w)]
        for r, row in enumerate(grid[1:-1]):
            for c, col in enumerate(row[1:-1]):
                if col == "<":
                    lefts[r].add(c)
                elif col == ">":
                    rights[r].add(c)
                elif col == "^":
                    ups[c].add(r)
                elif col == "v":
                    downs[c].add(r)
        clear_left = []
        clear_right = []
        clear_horiz = []
        for r in range(grid_h):
            t_clear_left = set(range(grid_w)) - lefts[r]
            t_clear_right = set(range(grid_w)) - rights[r]
            clear_left.append([t_clear_left])
            clear_right.append([t_clear_right])
            clear_horiz.append([t_clear_left.intersection(t_clear_right)])
            for t in range(1, grid_w):
                t_clear_left = set((x - 1) % grid_w for x in clear_left[r][t - 1])
                t_clear_right = set((x + 1) % grid_w for x in clear_right[r][t - 1])
                clear_left[r].append(t_clear_left)
                clear_right[r].append(t_clear_right)
                clear_horiz[r].append(t_clear_left.intersection(t_clear_right))

        clear_up = []
        clear_down = []
        clear_vert = []
        for c in range(grid_w):
            t_clear_up = set(range(grid_h)) - ups[c]
            t_clear_down = set(range(grid_h)) - downs[c]
            clear_up.append([t_clear_up])
            clear_down.append([t_clear_down])
            clear_vert.append([t_clear_up.intersection(t_clear_down)])
            for t in range(1, grid_h):
                t_clear_up = set((x - 1) % grid_h for x in clear_up[c][t - 1])
                t_clear_down = set((x + 1) % grid_h for x in clear_down[c][t - 1])
                clear_up[c].append(t_clear_up)
                clear_down[c].append(t_clear_down)
                clear_vert[c].append(t_clear_up.intersection(t_clear_down))
        start = (-1, 0)
        end = (grid_h, grid_w - 1)
        to_explore = set([(*start, 0)])
        to_explore_next = set()
        t = 0
        while len(to_explore) != 0:
            t += 1
            to_explore_next.clear()
            for (r, c, visited_flag) in to_explore:
                for dr, dc in cls._neighbours:
                    nr = r + dr
                    nc = c + dc
                    if (nr, nc) == end:
                        if visited_flag == 2:
                            return t
                        else:
                            to_explore_next.add((nr, nc, 1))
                        continue
                    if (nr, nc) == start:
                        if visited_flag == 1:
                            to_explore_next.add((nr, nc, 2))
                        else:
                            to_explore_next.add((nr, nc, visited_flag))
                        continue
                    if 0 <= nr < grid_h and 0 <= nc < grid_w:
                        if (
                            nr in clear_vert[nc][t % grid_h]
                            and nc in clear_horiz[nr][t % grid_w]
                        ):
                            to_explore_next.add((nr, nc, visited_flag))
            to_explore.clear()
            to_explore = set(to_explore_next)
        return -1


if __name__ == "__main__":
    print("===SAMPLE===")
    Day24Solution.do_solution()
    print("===ACTUAL===")
    Day24Solution.do_solution(False)
