import re
from collections import deque
from typing import List, Tuple, Union

from utils import ISolution


class InputDTO:
    stacks: "dict[int,list[str]]"
    instructions: "list[InstructionDTO]"

    def __init__(self) -> None:
        self.stacks = {}
        self.instructions = []


class InstructionDTO:
    qty: int
    src: int
    dst: int

    def __init__(self, tup: Tuple[str, str, str]) -> None:
        self.qty = int(tup[0])
        self.src = int(tup[1])
        self.dst = int(tup[2])

    def __str__(self) -> str:
        return f"qty -> {self.qty}, src -> {self.src}, dst -> {self.dst}"

    def __repr__(self) -> str:
        return f"qty -> {self.qty}, src -> {self.src}, dst -> {self.dst}"


class Day5Solution(ISolution):

    _DAY_STRING: str = "5"
    _INSTRUCTION_REGEX: re.Pattern = re.compile(r"^move (\d+) from (\d+) to (\d+)")

    @classmethod
    def __parse_stacks(cls, raw_section: str) -> "dict[int,list[str]]":
        lines = raw_section.split("\n")
        n_stacks = (len(lines[0]) + 1) // 4
        n_lines = len(lines)
        stacks = {}
        for i in range(n_stacks):
            val_idx = 4 * i + 1
            stack_list = list(
                filter(
                    lambda x: x != " ", [line[val_idx] for line in lines[: n_lines - 1]]
                )
            )
            stack_id = int(lines[-1][val_idx])
            stacks[stack_id] = stack_list
        return stacks

    @classmethod
    def __parse_instructions(cls, raw_section: str) -> List[InstructionDTO]:
        instructions = []
        lines = raw_section.split("\n")
        for line in lines:
            match: Union[re.Match, None] = cls._INSTRUCTION_REGEX.match(line)
            if match:
                instructions.append(InstructionDTO(match.groups()))
        return instructions

    @classmethod
    def _parse_input(cls, raw_input: str):
        sections = raw_input.split("\n\n")
        parsedInput = InputDTO()
        parsedInput.stacks = cls.__parse_stacks(sections[0])
        parsedInput.instructions = cls.__parse_instructions(sections[1])
        return parsedInput

    @classmethod
    def _part_one(cls, inputDTO: InputDTO) -> str:
        stacks = {}
        for (key, val) in inputDTO.stacks.items():
            stacks[key] = deque([el for el in val])
        for inst in inputDTO.instructions:
            for _ in range(inst.qty):
                top = stacks[inst.src].popleft()
                stacks[inst.dst].appendleft(top)
        soln = "".join([stacks[id][0] for id in range(1, len(stacks) + 1)])
        return soln

    @classmethod
    def _part_two(cls, inputDTO: InputDTO) -> str:
        stacks = {}
        for (key, val) in inputDTO.stacks.items():
            stacks[key] = deque([el for el in val])
        for inst in inputDTO.instructions:
            to_move = []
            for _ in range(inst.qty):
                to_move.append(stacks[inst.src].popleft())
            to_move.reverse()
            for crate in to_move:
                stacks[inst.dst].appendleft(crate)
        soln = "".join([stacks[id][0] for id in range(1, len(stacks) + 1)])
        return soln


if __name__ == "__main__":
    print("===SAMPLE===")
    Day5Solution.do_solution()
    print("===ACTUAL===")
    Day5Solution.do_solution(False)
