from typing import List, Tuple
import re
from utils import ISolution

OutputType = int
InputType = Tuple[List[str], List[Tuple[int, str]]]


class Day22Solution(ISolution):

    _DAY_STRING: str = "22"
    _drcs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        sections = raw_input.split("\n\n")
        raw_grid = sections[0].split("\n")
        dir_pattern = re.compile(r"(\d+)(L|R)(.*)")
        dirs = []
        cur_s = sections[1]
        while len(cur_s) != 0:
            m = dir_pattern.match(cur_s)
            if m:
                gs = m.groups()
                dirs.append((int(gs[0]), gs[1]))
                cur_s = gs[2]
            else:
                break
        if len(cur_s) != 0:
            dirs.append((int(cur_s), None))
        return (raw_grid, dirs)

    @classmethod
    def _find_wrap(cls, row: int, col: int, grid: List[str], face: int):
        if face == 0:
            # face right
            for (new_col, val) in enumerate(grid[row]):
                if val == "." or val == "#":
                    return (row, new_col)
        if face == 1:
            # face down
            for new_row, r in enumerate(grid):
                if len(r) <= col:
                    continue
                if r[col] == "." or r[col] == "#":
                    return (new_row, col)
        if face == 2:
            # face left
            for new_col in range(len(grid[row]) - 1, -1, -1):
                val = grid[row][new_col]
                if val == "." or val == "#":
                    return (row, new_col)
        if face == 3:
            # face up
            for new_row in range(len(grid) - 1, -1, -1):
                r = grid[new_row]
                if len(r) <= col:
                    continue
                if r[col] == "." or r[col] == "#":
                    return (new_row, col)
        raise Exception()

    @classmethod
    def _find_cube_wrap(cls, row: int, col: int, face: int, grid: List[str]):
        facel = len(grid[0]) // 3
        facer = row % 50
        facec = col % 50
        if face == 0:
            if 0 <= row < facel:
                assert col == 3 * facel - 1
                new_r = (facel - facer - 1) + facel * 2
                new_c = 2 * facel - 1
                new_face = 2
            elif facel <= row < 2 * facel:
                assert col == 2 * facel - 1
                new_r = facel - 1
                new_c = 2 * facel + facer
                new_face = 3
            elif facel * 2 <= row < 3 * facel:
                assert col == 2 * facel - 1
                new_r = facel - facer - 1
                new_c = 3 * facel - 1
                new_face = 2
            elif face * 3 <= row < 4 * facel:
                assert col == facel - 1
                new_r = 3 * facel - 1
                new_c = facel + facer
                new_face = 3
            else:
                raise Exception()
        elif face == 1:
            if 0 <= col < facel:
                assert row == 4 * facel - 1
                new_r = 0
                new_c = facel * 2 + facec
                new_face = 1
            elif facel <= col < 2 * facel:
                assert row == 3 * facel - 1
                new_r = 3 * facel + facec
                new_c = facel - 1
                new_face = 2
            elif 2 * facel <= col < 3 * facel:
                assert row == facel - 1
                new_r = facel + facec
                new_c = 2 * facel - 1
                new_face = 2
            else:
                raise Exception()
        elif face == 2:
            if 0 <= row < facel:
                assert col == facel
                new_r = (facel - facer - 1) + facel * 2
                new_c = 0
                new_face = 0
                # print(new_r, new_c, new_face)
            elif facel <= row < 2 * facel:
                assert col == facel
                new_r = 2 * facel
                new_c = facer
                new_face = 1
            elif facel * 2 <= row < 3 * facel:
                assert col == 0
                new_r = facel - facer - 1
                new_c = facel
                new_face = 0
            elif face * 3 <= row < 4 * facel:
                assert col == 0
                new_r = 0
                new_c = facel + facer
                new_face = 1
            else:
                raise Exception()
        elif face == 3:
            if 0 <= col < facel:
                assert row == 2 * facel
                new_r = facec + facel
                new_c = facel
                new_face = 0
            elif facel <= col < 2 * facel:
                assert row == 0
                new_r = 3 * facel + facec
                new_c = 0
                new_face = 0
            elif facel * 2 <= col < 3 * facel:
                assert row == 0
                new_r = 4 * facel - 1
                new_c = facec
                new_face = 3
            else:
                raise Exception()
        else:
            raise Exception()
        return (new_r, new_c, new_face)

    @classmethod
    def _part_one(cls, f_input: InputType) -> OutputType:
        grid, dirs = f_input
        cur_col = 0
        while grid[0][cur_col] == " ":
            cur_col += 1
        cur_rc: Tuple[int, int] = (0, cur_col)
        cur_face = 0

        portals = dict()
        for (fw, turn) in dirs:
            for _ in range(fw):
                dr, dc = cls._drcs[cur_face]
                r, c = cur_rc
                if not (
                    0 <= r + dr < len(grid)
                    and 0 <= c + dc < len(grid[r + dr])
                    and grid[r + dr][c + dc] != " "
                ):
                    if (r, c, cur_face) not in portals:
                        (nr, nc) = cls._find_wrap(r, c, grid, cur_face)
                        portals[(r, c, cur_face)] = (nr, nc)
                    else:
                        (nr, nc) = portals[(r, c, cur_face)]
                else:
                    (nr, nc) = (r + dr, c + dc)
                if grid[nr][nc] == "#":
                    break
                cur_rc = (nr, nc)

            if turn == "L":
                cur_face = (cur_face - 1) % 4
            elif turn == "R":
                cur_face = (cur_face + 1) % 4
        fr, fc = cur_rc
        return 1000 * (fr + 1) + 4 * (fc + 1) + cur_face

    @classmethod
    def _part_two(cls, f_input: InputType) -> OutputType:
        grid, dirs = f_input
        cur_col = 0
        while grid[0][cur_col] == " ":
            cur_col += 1
        cur_rc: Tuple[int, int] = (0, cur_col)
        cur_face = 0

        portals = dict()
        for (fw, turn) in dirs:
            for _ in range(fw):

                dr, dc = cls._drcs[cur_face]
                r, c = cur_rc
                if not (
                    0 <= r + dr < len(grid)
                    and 0 <= c + dc < len(grid[r + dr])
                    and grid[r + dr][c + dc] != " "
                ):
                    if (r, c, cur_face) not in portals:
                        (nr, nc, nf) = cls._find_cube_wrap(r, c, cur_face, grid)
                        portals[(r, c, cur_face)] = (nr, nc, nf)
                    else:
                        (nr, nc, nf) = portals[(r, c, cur_face)]
                else:
                    (nr, nc, nf) = (r + dr, c + dc, cur_face)
                if grid[nr][nc] == "#":
                    break
                cur_rc = (nr, nc)
                cur_face = nf
            if turn == "L":
                cur_face = (cur_face - 1) % 4
            elif turn == "R":
                cur_face = (cur_face + 1) % 4

        fr, fc = cur_rc
        return 1000 * (fr + 1) + 4 * (fc + 1) + cur_face


if __name__ == "__main__":
    print("===SAMPLE===")
    Day22Solution.do_solution()
    print("===ACTUAL===")
    Day22Solution.do_solution(False)
