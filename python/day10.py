from typing import List, Union

from utils import ISolution

InputType = List[List[str]]
OutputType = Union[int, str]


class Day10Solution(ISolution):

    _DAY_STRING: str = "10"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return [line.split(" ") for line in raw_input.split("\n")]

    @classmethod
    def _part_one(cls, cmds: InputType) -> OutputType:
        strength = 0
        stall = False
        x = 1
        opc = 0
        for cycle in range(1, 241):
            if not stall:
                if opc < len(cmds):
                    cmd = cmds[opc]
                    if cmd[0] == "addx":
                        stall = True
            else:
                stall = False
            if cycle % 40 == 20:
                cur_str = x * cycle
                strength += cur_str
            if not stall:
                if cmds[opc][0] == "addx":
                    x += int(cmds[opc][1])
                opc += 1

        return strength

    @classmethod
    def _part_two(cls, cmds: InputType) -> OutputType:
        solution = [[" " for _ in range(40)] for _ in range(6)]
        stall = False
        x = 1
        opc = 0
        for cycle in range(1, 241):
            if not stall:
                if opc < len(cmds):
                    cmd = cmds[opc]
                    if cmd[0] == "addx":
                        stall = True
            else:
                stall = False
            pixel_xpos = (cycle - 1) % 40
            pixel_ypos = (cycle - 1) // 40
            if pixel_xpos - 1 <= x <= pixel_xpos + 1:
                solution[pixel_ypos][pixel_xpos] = "#"
            if not stall:
                if cmds[opc][0] == "addx":
                    x += int(cmds[opc][1])
                opc += 1
        return "\n" + "\n".join(["".join(row) for row in solution])


if __name__ == "__main__":
    print("===SAMPLE===")
    Day10Solution.do_solution()
    print("===ACTUAL===")
    Day10Solution.do_solution(False)
