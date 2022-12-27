from typing import List, Deque, Union
from collections import deque
from functools import cmp_to_key
from utils import ISolution


OutputType = int

InputType = List[List[str]]


RList = List[Union["RList", int]]


class Day13Solution(ISolution):

    _DAY_STRING: str = "13"
    __count = 0

    @classmethod
    def __parse_str(cls, list_str: str):
        acc = ""
        list_stack: Deque[List] = deque([])
        last_list_has_closed = False
        for char in list_str:
            if char == ",":
                if acc != "":
                    list_stack[-1].append(int(acc))
                    acc = ""
                elif last_list_has_closed:
                    last_list = list_stack.pop()
                    list_stack[-1].append(last_list)
                    last_list_has_closed = False
            elif char == "[":

                list_stack.append([])
                last_list_has_closed = False
            elif char == "]":

                if acc != "":
                    list_stack[-1].append(int(acc))
                    acc = ""
                elif last_list_has_closed:
                    last_list = list_stack.pop()
                    list_stack[-1].append(last_list)
                last_list_has_closed = True
            else:
                acc += char
        return list_stack[0]

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return [section.split("\n") for section in raw_input.split("\n\n")]

    @classmethod
    def __compare_el(cls, lft: Union[RList, int], rgt: Union[RList, int]):
        if isinstance(lft, list) and isinstance(rgt, list):
            return cls.__compare(lft, rgt)
        elif isinstance(lft, list) and isinstance(rgt, int):
            rgt_list: RList = [rgt]
            return cls.__compare(lft, rgt_list)
        elif isinstance(rgt, list) and isinstance(lft, int):
            lft_list: RList = [lft]
            return cls.__compare(lft_list, rgt)
        elif isinstance(lft, int) and isinstance(rgt, int):
            if lft < rgt:
                return 1
            elif lft > rgt:
                return -1
            else:
                return 0

    @classmethod
    def __compare(cls, lft: RList, rgt: RList):
        if len(lft) == 0 and len(rgt) > 0:
            return 1
        if len(lft) > 0 and len(rgt) == 0:
            return -1
        if len(lft) == 0 and len(rgt) == 0:
            return 0
        el_comp = cls.__compare_el(lft[0], rgt[0])
        return cls.__compare(lft[1:], rgt[1:]) if el_comp == 0 else el_comp

    @classmethod
    def _part_one(cls, pairs: InputType) -> OutputType:
        answer = 0
        for (i, pair) in enumerate(pairs):
            ll = cls.__parse_str(pair[0])
            rl = cls.__parse_str(pair[1])
            if cls.__compare(ll, rl) == 1:
                answer += i + 1
        return answer

    @classmethod
    def _part_two(cls, pairs: InputType) -> OutputType:
        answer = 1
        lists: List[RList] = []
        for pair in pairs:
            lists.append(cls.__parse_str(pair[0]))
            lists.append(cls.__parse_str(pair[1]))
        lists.append([[2]])
        lists.append([[6]])
        sorted_list = sorted(lists, key=cmp_to_key(cls.__compare), reverse=True)
        for i, l in enumerate(sorted_list):
            if len(l) == 1 and isinstance(l[0], list):
                if len(l[0]) == 1 and (l[0][0] == 2 or l[0][0] == 6):
                    answer *= i + 1
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day13Solution.do_solution()
    print("===ACTUAL===")
    Day13Solution.do_solution(False)
