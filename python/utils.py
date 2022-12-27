from abc import ABC, abstractmethod
import os
from functools import reduce
import operator
from typing import List, Tuple, Union, TypeVar


T = TypeVar("T")
Pint = Tuple[int, int]
Tint = Tuple[int, int, int]
int4 = Tuple[int, int, int, int]


def ceil_div(a, b):
    return -(a // -b)


def prod(iterable):
    return reduce(operator.mul, iterable, 1)


def pretty_print(xy: List[List]) -> None:
    print(os.linesep.join(map(lambda row: "\t".join(map(str, row)), xy)))
    print()


def int_mean(n: List[int]) -> Tuple[int, int]:
    if sum(n) % len(n) == 0:
        return (sum(n) // len(n), sum(n) // len(n))
    mean = sum(n) / len(n)
    return (int(mean), int(mean) + 1)


def int_median(n: List[int]) -> Tuple[int, int]:
    sorted_n = sorted(n)
    mid = len(n) // 2
    if len(n) % 2 == 1:
        return (sorted_n[mid], sorted_n[mid])
    else:
        return (sorted_n[mid], sorted_n[mid - 1])


def sign(x: Union[int, float]) -> int:
    if x == 0 or x == 0.0:
        return 0
    else:
        return -1 if x < 0 else 1


def or_fn(x: bool, y: bool) -> bool:
    return x or y


def and_fn(x: bool, y: bool) -> bool:
    return x and y


def flip_xy(xy: List[List[T]]) -> List[List[T]]:
    return [
        [xy[col_idx][row_idx] for col_idx in range(len(xy[row_idx]))]
        for row_idx in range(len(xy))
    ]


def get_raw_lines(raw_input: str) -> List[str]:
    return raw_input.split(os.linesep)


def bitmask_is_set(bitmask: int, pos: int) -> bool:
    return bitmask & 1 << pos != 0


def bitmask_set_bit(bitmask: int, pos: int) -> int:
    return bitmask | 1 << pos


def bitmask_unset_bit(bitmask: int, pos: int) -> int:
    return bitmask & ~(1 << pos)


class ISolution(ABC):

    _DAY_STRING: str = ""

    @classmethod
    def _parse_raw_input(cls, use_sample: bool) -> str:
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        ext_str = "sample" if use_sample else "input"
        input_path = os.path.join(parent_dir, f"../input/{cls._DAY_STRING}.{ext_str}")
        with open(input_path, "r", encoding="UTF-8") as infile:
            raw_input = infile.read()
        return raw_input

    @classmethod
    @abstractmethod
    def _parse_input(cls, raw_input):
        pass

    @classmethod
    @abstractmethod
    def _part_one(cls, problem_input):
        pass

    @classmethod
    @abstractmethod
    def _part_two(cls, problem_input):
        pass

    @classmethod
    def do_solution(cls, use_sample=True):
        raw_input = cls._parse_raw_input(use_sample)
        problem_input = cls._parse_input(raw_input)
        solution_one = cls._part_one(problem_input)
        print(f"Part One: {solution_one}")
        solution_two = cls._part_two(problem_input)
        print(f"Part Two: {solution_two}")
