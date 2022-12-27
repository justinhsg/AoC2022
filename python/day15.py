from typing import List, Tuple
import re
from utils import ISolution, Pint


OutputType = int

InputType = List[Tuple[Pint, Pint]]


class Day15(ISolution):

    _DAY_STRING: str = "15"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        pattern = re.compile(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
        )
        lines = raw_input.split("\n")
        proc_input = []
        for line in lines:
            matches = pattern.match(line)
            if matches is not None:
                groups = tuple(map(int, matches.groups()))
                proc_input.append(((groups[0], groups[1]), (groups[2], groups[3])))

        return proc_input

    @classmethod
    def _merge_ranges(cls, lst):
        sorted_lst = sorted(lst)
        new_lst = []
        new_p = None
        for (s, e) in sorted_lst:
            if new_p is None:
                new_p = (s, e)
            else:
                if s <= new_p[1]:
                    new_p = (min(s, new_p[0]), max(e, new_p[1]))
                else:
                    new_lst.append(new_p)
                    new_p = (s, e)
        if new_p is not None:
            new_lst.append(new_p)
        return new_lst

    @classmethod
    def _count_ranges(cls, lst):
        answer = 0
        for (s, e) in lst:
            answer += (e - s) + 1
        return answer

    @classmethod
    def _part_one(cls, ranges: InputType) -> OutputType:
        target = 10 if ranges[0][0][0] == 2 else 2000000
        rs = []
        on_target = set()
        for (sx, sy), (bx, by) in ranges:
            if by == target:
                on_target.add(bx)
            dist = abs(bx - sx) + abs(by - sy)
            rem_dist = dist - abs(target - sy)
            if rem_dist >= 0:
                rs.append((sx - rem_dist, sx + rem_dist))
        return cls._count_ranges(cls._merge_ranges(rs)) - len(on_target)

    @classmethod
    def _part_two(cls, ranges: InputType) -> OutputType:
        search_space = 20 if ranges[0][0][0] == 2 else 4000000
        xpy_tl = set()
        xpy_br = set()
        xmy_tr = set()
        xmy_bl = set()
        sensors = dict()
        for (sx, sy), (bx, by) in ranges:
            dist = abs(bx - sx) + abs(by - sy)
            sensors[(sx, sy)] = dist
            xpy_t1 = sy - (sx + dist)
            if -search_space <= xpy_t1 <= search_space:
                xpy_tl.add(xpy_t1)
            xpy_t2 = sy - (sx - dist)
            if -search_space <= xpy_t2 <= search_space:
                xpy_br.add(xpy_t2)
            xmy_t1 = sy + (sx + dist)
            if 0 <= xmy_t1 <= 2 * search_space:
                xmy_tr.add(xmy_t1)
            xmy_t2 = sy + (sx - dist)
            if 0 <= xmy_t2 <= 2 * search_space:
                xmy_bl.add(xmy_t2)

        p_candidates = set()
        for pt in xpy_br:
            if pt + 2 in xpy_tl:
                p_candidates.add(pt + 1)
        m_candidates = set()
        for pt in xmy_tr:
            if pt + 2 in xmy_bl:
                m_candidates.add(pt + 1)
        for pt in p_candidates:
            for mt in m_candidates:
                by = (mt + pt) // 2
                bx = (mt - pt) // 2
                in_range = False
                for (sx, sy) in sensors:
                    t_dist = abs(bx - sx) + abs(by - sy)
                    if t_dist <= sensors[(sx, sy)]:
                        in_range = True
                        break
                if not in_range:
                    return bx * 4000000 + by
        return -1


if __name__ == "__main__":
    print("===SAMPLE===")
    Day15.do_solution()
    print("===ACTUAL===")
    Day15.do_solution(False)
