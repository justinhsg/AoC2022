from typing import List, Tuple

from utils import ISolution


class Day2Solution(ISolution):

    _DAY_STRING: str = "2"

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[Tuple[str, str]]:
        parsed_input = [(line[0], line[2]) for line in raw_input.split("\n")]
        return parsed_input

    @classmethod
    def __pair_score(cls, opp: str, cur: str):
        opp_code = ord(opp) - ord("A")
        cur_code = ord(cur) - ord("X")
        if opp_code == cur_code:
            return 3
        if (cur_code - opp_code) % 3 == 1:
            return 6
        else:
            return 0

    @classmethod
    def __get_response(cls, opp: str, strat: str) -> str:
        opp_code = ord(opp) - ord("A")
        if strat == "X":
            return chr((opp_code - 1) % 3 + ord("X"))
        if strat == "Y":
            return chr(opp_code + ord("X"))
        return chr((opp_code + 1) % 3 + ord("X"))

    @classmethod
    def _part_one(cls, problem_input: Tuple[str, str]) -> int:
        score = 0
        for (opp, cur) in problem_input:
            score += cls.__pair_score(opp, cur)
            score += ord(cur) - ord("X") + 1
        return score

    @classmethod
    def _part_two(cls, problem_input) -> int:
        score = 0
        for (opp, strat) in problem_input:

            cur = cls.__get_response(opp, strat)
            score += cls.__pair_score(opp, cur)
            score += ord(cur) - ord("X") + 1
        return score


if __name__ == "__main__":
    print("===SAMPLE===")
    Day2Solution.do_solution()
    print("===ACTUAL===")
    Day2Solution.do_solution(False)
