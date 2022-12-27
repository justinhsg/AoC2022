from typing import List
from utils import ISolution


OutputType = str
InputType = List[str]


class Day25Solution(ISolution):

    _DAY_STRING: str = "25"
    _neighbours = [(-1, 0), (0, -1), (0, 0), (0, 1), (1, 0)]

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return raw_input.split("\n")

    @classmethod
    def _snafu_to_int(cls, snafu_str: str) -> int:
        f_int = 0
        for (i, c) in enumerate(reversed(snafu_str)):
            cv = 0
            if c == "0":
                cv = 0
            elif c == "1":
                cv = 1
            elif c == "2":
                cv = 2
            elif c == "-":
                cv = -1
            elif c == "=":
                cv = -2
            else:
                raise Exception("Unidentified char")
            f_int += (5**i) * cv
        return f_int

    @classmethod
    def _int_to_snafu(cls, i: int) -> str:
        rev_snafu = []
        ti = i
        while ti != 0:
            v = ti % 5
            rem = ti // 5
            if v <= 2:
                rev_snafu.append(str(v))
            elif v == 4:
                rev_snafu.append("-")
                rem += 1
            elif v == 3:
                rev_snafu.append("=")
                rem += 1
            ti = rem

        return "".join(reversed(rev_snafu))

    @classmethod
    def _part_one(cls, lines: InputType) -> OutputType:
        acc = 0
        for line in lines:
            acc += cls._snafu_to_int(line)
        return cls._int_to_snafu(acc)

    @classmethod
    def _part_two(cls, _: InputType) -> OutputType:
        return ":)"


if __name__ == "__main__":
    print("===SAMPLE===")
    Day25Solution.do_solution()
    print("===ACTUAL===")
    Day25Solution.do_solution(False)
