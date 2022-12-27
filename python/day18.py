from typing import List
from collections import deque
from utils import ISolution, Tint


OutputType = int

InputType = List[Tint]


class Day18Solution(ISolution):

    _DAY_STRING: str = "18"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return [
            tuple(int(el) for el in line.split(",")) for line in raw_input.split("\n")
        ]

    dp = [(-1, 0, 0), (1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    @classmethod
    def _part_one(cls, points: InputType) -> OutputType:
        answer = 0
        p_set = set(points)
        for (x, y, z) in p_set:
            for (dx, dy, dz) in cls.dp:
                np = (x + dx, y + dy, z + dz)
                if np not in p_set:
                    answer += 1
        return answer

    @classmethod
    def _part_two(cls, points: InputType) -> OutputType:
        a_map = dict()
        p_set = set(points)
        for (x, y, z) in p_set:
            for (dx, dy, dz) in cls.dp:
                np = (x + dx, y + dy, z + dz)
                if np not in p_set:
                    if np not in a_map:
                        a_map[np] = 0
                    a_map[np] += 1
        r_set = set()
        min_x = min(p[0] for p in points) - 1
        max_x = max(p[0] for p in points) + 1
        min_y = min(p[1] for p in points) - 1
        max_y = max(p[1] for p in points) + 1
        min_z = min(p[2] for p in points) - 1
        max_z = max(p[2] for p in points) + 1

        r_set.add((min_x, min_y, min_z))
        to_visit = deque([(min_x, min_y, min_z)])
        while to_visit:
            (cx, cy, cz) = to_visit.popleft()
            for (dx, dy, dz) in cls.dp:
                within_bounds = (
                    min_x <= cx + dx <= max_x
                    and min_y <= cy + dy <= max_y
                    and min_z <= cz + dz <= max_z
                )
                if within_bounds:
                    np = (cx + dx, cy + dy, cz + dz)
                    if np not in r_set and np not in p_set:
                        r_set.add(np)
                        to_visit.append(np)

        answer = 0
        for a_p, cnt in a_map.items():
            if a_p in r_set:
                answer += cnt
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day18Solution.do_solution()
    print("===ACTUAL===")
    Day18Solution.do_solution(False)
