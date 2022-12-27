from typing import List, Tuple, Deque
import re
from collections import deque
from utils import ISolution, Pint


OutputType = int

InputType = List[List]


class Day16Solution(ISolution):

    _DAY_STRING: str = "16"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        pattern = re.compile(
            r"Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)"
        )
        lines = raw_input.split("\n")
        proc_input = []
        for line in lines:
            matches = pattern.match(line)
            if matches is not None:
                groups = matches.groups()
                proc_input.append([groups[0], int(groups[1]), groups[2].split(", ")])

        return proc_input

    @classmethod
    def _part_one(cls, pipes: InputType) -> OutputType:
        impt_pipes = []
        adj_list = dict()
        ps = dict()
        dists = dict()
        for pipe in pipes:
            adj_list[pipe[0]] = []
            dists[(pipe[0], pipe[0])] = 0
        for pipe in pipes:
            name = pipe[0]
            flow = pipe[1]
            if name == "AA" or flow != 0:
                impt_pipes.append(name)
                ps[name] = flow
            for dest in pipe[2]:
                adj_list[name].append(dest)
                adj_list[dest].append(name)
                dists[(name, dest)] = 1
                dists[(dest, name)] = 1

        for mid in adj_list:
            for start in adj_list:
                for end in adj_list:
                    if (start, mid) in dists and (mid, end) in dists:
                        if (start, end) not in dists:
                            dists[(start, end)] = (
                                dists[(start, mid)] + dists[(mid, end)]
                            )
                        else:
                            if (
                                dists[(start, end)]
                                > dists[(start, mid)] + dists[(mid, end)]
                            ):
                                dists[(start, end)] = (
                                    dists[(start, mid)] + dists[(mid, end)]
                                )
        to_explore = deque([])
        to_explore.append((0, 0, 0, "AA", ["AA"]))
        memo = dict()
        while len(to_explore) != 0:
            (pressure, time, permin, cur_valve, opened) = to_explore.popleft()
            o_set = set(opened)
            for next_valve in impt_pipes:
                if next_valve in o_set:
                    continue
                time_to_open_next = dists[(cur_valve, next_valve)] + 1
                new_time = time + time_to_open_next
                if new_time <= 30:
                    new_pressure = pressure + permin * time_to_open_next
                    new_permin = permin + ps[next_valve]
                    new_opened = [*opened, next_valve]
                    to_explore.append(
                        (new_pressure, new_time, new_permin, next_valve, new_opened)
                    )
            idle_time = 30 - time
            final_pressure = pressure + idle_time * permin
            sorted_opened = tuple(sorted(opened))
            if sorted_opened not in memo:
                memo[sorted_opened] = final_pressure
            else:
                memo[sorted_opened] = max(memo[sorted_opened], final_pressure)
        answer = 0
        for _, pressure in memo.items():
            answer = max(pressure, answer)
        return answer

    @classmethod
    def _part_two(cls, pipes: InputType) -> OutputType:
        impt_pipes = []
        adj_list = dict()
        ps = dict()
        dists = dict()
        for pipe in pipes:
            adj_list[pipe[0]] = []
            dists[(pipe[0], pipe[0])] = 0
        for pipe in pipes:
            name = pipe[0]
            flow = pipe[1]
            if name == "AA" or flow != 0:
                impt_pipes.append(name)
                ps[name] = flow
            for dest in pipe[2]:
                adj_list[name].append(dest)
                adj_list[dest].append(name)
                dists[(name, dest)] = 1
                dists[(dest, name)] = 1

        for mid in adj_list:
            for start in adj_list:
                for end in adj_list:
                    if (start, mid) in dists and (mid, end) in dists:
                        if (start, end) not in dists:
                            dists[(start, end)] = (
                                dists[(start, mid)] + dists[(mid, end)]
                            )
                        else:
                            if (
                                dists[(start, end)]
                                > dists[(start, mid)] + dists[(mid, end)]
                            ):
                                dists[(start, end)] = (
                                    dists[(start, mid)] + dists[(mid, end)]
                                )
        to_explore = deque([])
        to_explore.append((0, 0, 0, "AA", ["AA"]))
        memo = [dict() for _ in range(len(impt_pipes) + 1)]
        while len(to_explore) != 0:
            (pressure, time, permin, cur_valve, opened) = to_explore.popleft()
            o_set = set(opened)
            for next_valve in impt_pipes:
                if next_valve in o_set:
                    continue
                time_to_open_next = dists[(cur_valve, next_valve)] + 1
                new_time = time + time_to_open_next
                if new_time <= 26:
                    new_pressure = pressure + permin * time_to_open_next
                    new_permin = permin + ps[next_valve]
                    new_opened = [*opened, next_valve]
                    to_explore.append(
                        (new_pressure, new_time, new_permin, next_valve, new_opened)
                    )
            idle_time = 26 - time
            final_pressure = pressure + idle_time * permin
            sorted_opened = tuple(sorted(opened))
            if sorted_opened not in memo[len(sorted_opened)]:
                memo[len(sorted_opened)][sorted_opened] = final_pressure
            else:
                memo[len(sorted_opened)][sorted_opened] = max(
                    memo[len(sorted_opened)][sorted_opened], final_pressure
                )
        answer = 0
        for l, d in enumerate(memo):
            for opened in d:
                expected_valves = set(impt_pipes) - set(opened[1:])
                term_early = False
                for l_2 in range(len(memo) - l, 0, -1):
                    if term_early:
                        break
                    for opened_2 in memo[l_2]:
                        if set(opened_2).issubset(expected_valves):
                            term_early = True
                            answer = max(answer, d[opened] + memo[l_2][opened_2])
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day16Solution.do_solution()
    print("===ACTUAL===")
    Day16Solution.do_solution(False)
