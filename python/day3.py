from typing import List

from utils import ISolution


class Day2Solution(ISolution):

    _DAY_STRING: str = "3"

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[str]:
        parsed_input = raw_input.split("\n")
        return parsed_input

    @classmethod
    def __get_priority(cls, item: str) -> int:
        if ord(item) >= ord("a"):
            return ord(item) - ord("a") + 1
        else:
            return ord(item) - ord("A") + 27

    @classmethod
    def _part_one(cls, rucksacks: List[str]) -> int:
        score = 0
        for rucksack in rucksacks:
            midpt = len(rucksack) // 2
            front_items = set()
            for front_item in rucksack[:midpt]:
                front_items.add(front_item)
            for rear_item in rucksack[midpt:]:
                if rear_item in front_items:
                    score += cls.__get_priority(rear_item)
                    break
        return score

    @classmethod
    def _part_two(cls, rucksacks: List[str]) -> int:
        score = 0
        for fst_i in range(0, len(rucksacks), 3):
            common_items = set(rucksacks[fst_i]).intersection(set(rucksacks[fst_i + 1]))
            common_items = common_items.intersection(set(rucksacks[fst_i + 2]))
            common_item = common_items.pop()
            score += cls.__get_priority(common_item)
        return score


if __name__ == "__main__":
    print("===SAMPLE===")
    Day2Solution.do_solution()
    print("===ACTUAL===")
    Day2Solution.do_solution(False)
