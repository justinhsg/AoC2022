import re
from typing import List

from utils import ISolution


class Day4Solution(ISolution):

    _DAY_STRING: str = "4"
    Schedule = List[int]

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[Schedule]:
        lines = raw_input.split("\n")
        return [[int(raw) for raw in re.split(",|-", line)] for line in lines]

    @classmethod
    def _part_one(cls, schedules: List[Schedule]) -> int:
        found_pairs = 0
        for schedule in schedules:
            [s1, e1, s2, e2] = schedule
            if s2 >= s1 and e2 <= e1:
                found_pairs += 1
                continue
            if s1 >= s2 and e1 <= e2:
                found_pairs += 1
                continue

        return found_pairs

    @classmethod
    def _part_two(cls, schedules: List[Schedule]) -> int:
        found_pairs = 0
        for schedule in schedules:
            [s1, e1, s2, e2] = schedule
            if s2 >= s1 and s2 <= e1:
                found_pairs += 1
                continue
            if s1 >= s2 and s1 <= e2:
                found_pairs += 1
                continue

        return found_pairs


if __name__ == "__main__":
    print("===SAMPLE===")
    Day4Solution.do_solution()
    print("===ACTUAL===")
    Day4Solution.do_solution(False)
