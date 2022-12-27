from typing import List, Union, Deque, Tuple
from collections import deque
from functools import reduce
from utils import ISolution

OutputType = Union[int, str]


class Monkey:
    def __init__(self) -> None:
        self.items: "deque[int]" = deque([])
        self.op: str
        self.rhs: Union[int, str]
        self.div_test: int = 1
        self.true_monkey = -1
        self.false_monkey = -1


InputType = Tuple[List[Monkey], List[Deque[int]]]


class Day11Solution(ISolution):

    _DAY_STRING: str = "11"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        monkey_sections = [section.split("\n") for section in raw_input.split("\n\n")]
        monkeys = []
        items = []
        for monkey_section in monkey_sections:
            new_monkey = Monkey()
            raw_items = monkey_section[1].split(": ")[1].split(",")
            items.append(deque([int(item) for item in raw_items]))

            operation_elements = monkey_section[2].split("= ")[1].split(" ")

            new_monkey.op = operation_elements[1]
            right_element = operation_elements[2]
            new_monkey.rhs = (
                right_element if right_element == "old" else int(right_element)
            )

            new_monkey.div_test = int(monkey_section[3].split(" ")[-1])
            new_monkey.true_monkey = int(monkey_section[4].split(" ")[-1])
            new_monkey.false_monkey = int(monkey_section[5].split(" ")[-1])
            monkeys.append(new_monkey)
        return (monkeys, items)

    @classmethod
    def _part_one(cls, input_tuple: InputType) -> OutputType:
        for monkey, items in zip(*input_tuple):
            monkey.items = deque([item for item in items])
        monkeys = input_tuple[0]
        inspects = [0 for _ in monkeys]
        for _ in range(1, 21):
            for i, cur_monkey in enumerate(monkeys):
                cur_monkey = monkeys[i]
                while len(cur_monkey.items) != 0:
                    cur_item = cur_monkey.items.popleft()
                    inspects[i] += 1
                    rhs = cur_item if cur_monkey.rhs == "old" else int(cur_monkey.rhs)
                    if cur_monkey.op == "+":
                        new_item = (cur_item + rhs) // 3
                    else:
                        new_item = (cur_item * rhs) // 3
                    if new_item % cur_monkey.div_test == 0:
                        monkeys[cur_monkey.true_monkey].items.append(new_item)
                    else:
                        monkeys[cur_monkey.false_monkey].items.append(new_item)
        inspects.sort(reverse=True)
        return inspects[0] * inspects[1]

    @classmethod
    def _part_two(cls, input_tuple: InputType) -> OutputType:
        for monkey, items in zip(*input_tuple):
            monkey.items = deque([item for item in items])
        monkeys = input_tuple[0]
        inspects = [0 for _ in monkeys]
        prod = reduce(lambda acc, m: acc * m.div_test, monkeys, 1)
        for _ in range(1, 10001):
            for i, cur_monkey in enumerate(monkeys):
                cur_monkey = monkeys[i]
                while len(cur_monkey.items) != 0:
                    cur_item = cur_monkey.items.popleft()
                    inspects[i] += 1
                    rhs = cur_item if cur_monkey.rhs == "old" else int(cur_monkey.rhs)
                    if cur_monkey.op == "+":
                        new_item = (cur_item + rhs) % prod
                    else:
                        new_item = (cur_item * rhs) % prod
                    if new_item % cur_monkey.div_test == 0:
                        monkeys[cur_monkey.true_monkey].items.append(new_item)
                    else:
                        monkeys[cur_monkey.false_monkey].items.append(new_item)
        inspects.sort(reverse=True)
        return inspects[0] * inspects[1]


if __name__ == "__main__":
    print("===SAMPLE===")
    Day11Solution.do_solution()
    print("===ACTUAL===")
    Day11Solution.do_solution(False)
