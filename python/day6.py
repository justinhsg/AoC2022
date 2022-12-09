from typing import List

from utils import ISolution


class Day6Solution(ISolution):

    _DAY_STRING: str = "6"

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[str]:
        return raw_input.split("\n")

    @classmethod
    def _part_one(cls, streams: List[str]) -> List[int]:
        solution = []
        for stream in streams:
            chars = {}
            for init_char in stream[:3]:
                if init_char not in chars:
                    chars[init_char] = 0
                chars[init_char] += 1
            for i in range(len(stream) - 3):
                cur_char = stream[i]
                next_idx = i + 3
                next_char = stream[next_idx]
                if next_char not in chars:
                    chars[next_char] = 0
                chars[next_char] += 1
                if len(chars) == 4:
                    solution.append(next_idx + 1)
                    break
                chars[cur_char] -= 1
                if chars[cur_char] == 0:
                    del chars[cur_char]
        return solution

    @classmethod
    def _part_two(cls, streams: List[str]) -> List[int]:
        solution = []
        for stream in streams:
            chars = {}
            for init_char in stream[:13]:
                if init_char not in chars:
                    chars[init_char] = 0
                chars[init_char] += 1
            for i in range(len(stream) - 3):
                cur_char = stream[i]
                next_idx = i + 13
                next_char = stream[next_idx]
                if next_char not in chars:
                    chars[next_char] = 0
                chars[next_char] += 1
                if len(chars) == 14:
                    solution.append(next_idx + 1)
                    break
                chars[cur_char] -= 1
                if chars[cur_char] == 0:
                    del chars[cur_char]
        return solution


if __name__ == "__main__":
    print("===SAMPLE===")
    Day6Solution.do_solution()
    print("===ACTUAL===")
    Day6Solution.do_solution(False)
