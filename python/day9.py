from typing import List, Set, Tuple

from utils import ISolution, Pint, sign

InputType = List[Tuple[str, int]]
OutputType = int


class Day9Solution(ISolution):

    _DAY_STRING: str = "9"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        lines = raw_input.split("\n")
        moves = []
        for line in lines:
            tokens = line.split(" ")
            moves.append((tokens[0], int(tokens[1])))
        return moves

    @classmethod
    def _move_tail(cls, head_pos: Pint, tail_pos: Pint, visited: Set[Pint]) -> Pint:
        dx = head_pos[0] - tail_pos[0]
        dy = head_pos[1] - tail_pos[1]
        nx = tail_pos[0]
        ny = tail_pos[1]
        if abs(dx) >= 2:
            nx += sign(dx)
            if abs(dy) == 1:
                ny += sign(dy)
        if abs(dy) >= 2:
            ny += sign(dy)
            if abs(dx) == 1:
                nx += sign(dx)
        visited.add((nx, ny))
        return (nx, ny)

    @classmethod
    def _part_one(cls, moves: InputType) -> OutputType:
        tail_pos: Pint = (0, 0)
        head_pos: Pint = (0, 0)
        visited = {tail_pos}
        for (dir_c, dist) in moves:
            for _ in range(dist):
                if dir_c == "U":
                    head_pos = (head_pos[0], head_pos[1] + 1)
                elif dir_c == "D":
                    head_pos = (head_pos[0], head_pos[1] - 1)
                elif dir_c == "L":
                    head_pos = (head_pos[0] - 1, head_pos[1])
                elif dir_c == "R":
                    head_pos = (head_pos[0] + 1, head_pos[1])
                tail_pos = cls._move_tail(head_pos, tail_pos, visited)
        return len(visited)

    @classmethod
    def _part_two(cls, moves: InputType) -> OutputType:
        knots: List[Pint] = [(0, 0) for _ in range(10)]
        visited: Set[Pint] = {(0, 0)}
        for (dir_c, dist) in moves:
            for _ in range(dist):
                if dir_c == "U":
                    knots[0] = (knots[0][0], knots[0][1] + 1)
                elif dir_c == "D":
                    knots[0] = (knots[0][0], knots[0][1] - 1)
                elif dir_c == "L":
                    knots[0] = (knots[0][0] - 1, knots[0][1])
                elif dir_c == "R":
                    knots[0] = (knots[0][0] + 1, knots[0][1])
                for i in range(1, len(knots)):
                    knots[i] = cls._move_knot(knots[i - 1], knots[i])
                visited.add(knots[-1])
        return len(visited)

    @classmethod
    def _move_knot(cls, prev_pos: Pint, cur_pos: Pint) -> Pint:
        dx = prev_pos[0] - cur_pos[0]
        dy = prev_pos[1] - cur_pos[1]
        nx = cur_pos[0]
        ny = cur_pos[1]
        if abs(dx) >= 2:
            nx += sign(dx)
            if abs(dy) == 1:
                ny += sign(dy)
        if abs(dy) >= 2:
            ny += sign(dy)
            if abs(dx) == 1:
                nx += sign(dx)
        return (nx, ny)


if __name__ == "__main__":
    print("===SAMPLE===")
    Day9Solution.do_solution()
    print("===ACTUAL===")
    Day9Solution.do_solution(False)
