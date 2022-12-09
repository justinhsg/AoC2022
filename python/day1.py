from typing import List

from utils import ISolution


class Day1Solution(ISolution):

    _DAY_STRING: str = "1"

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[List[int]]:
        raw_elves = raw_input.split("\n\n")
        parsed_input = []
        for elf in raw_elves:
            parsed_input.append([int(raw_cal) for raw_cal in elf.split("\n")])
        return parsed_input

    @classmethod
    def __get_totals(cls, elves: List[List[int]]) -> List[int]:
        return [sum(elf) for elf in elves]

    @classmethod
    def _part_one(cls, problem_input) -> int:
        return max(cls.__get_totals(problem_input))

    @classmethod
    def _part_two(cls, problem_input) -> int:
        return sum(sorted(cls.__get_totals(problem_input), reverse=True)[:3])


if __name__ == "__main__":
    print("===SAMPLE===")
    Day1Solution.do_solution()
    print("===ACTUAL===")
    Day1Solution.do_solution(False)
