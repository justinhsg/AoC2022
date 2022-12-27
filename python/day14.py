from typing import List
from utils import ISolution, Pint


OutputType = int

InputType = List[List[Pint]]


class Day14Solution(ISolution):

    _DAY_STRING: str = "14"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        lines = raw_input.split("\n")
        final_input = []
        for line in lines:
            final_input.append(
                [tuple(map(int, pair.split(","))) for pair in line.split(" -> ")]
            )
        return final_input

    @classmethod
    def _collapse_obstacles(cls, obs_list: List[Pint]):
        new_obs_list = []
        sorted_obs = sorted(obs_list)
        new_obs = None
        for (s, e) in sorted_obs:
            if new_obs is None:
                new_obs = (s, e)
            else:
                if s <= new_obs[1]:
                    new_obs = (min(s, new_obs[0]), max(e, new_obs[1]))
                else:
                    new_obs_list.append(new_obs)
                    new_obs = (s, e)
        if new_obs is not None:
            new_obs_list.append(new_obs)
        return new_obs_list

    @classmethod
    def _build_obstacles(cls, final_input: InputType):
        obstacles = [[] for _ in range(550)]
        for line in final_input:
            for i, start in enumerate(line[:-1]):
                end = line[i + 1]
                if start[0] == end[0]:
                    start_depth = min(start[1], end[1])
                    end_depth = max(start[1], end[1])
                    obstacles[start[0]].append((start_depth, end_depth))
                else:
                    start_pos = min(start[0], end[0])
                    end_pos = max(start[0], end[0])
                    for x in range(start_pos, end_pos + 1):
                        obstacles[x].append((start[1], start[1]))
        return obstacles

    @classmethod
    def _add_obstacle(cls, depth: int, obs_list: List[Pint]):
        new_obs_list = []
        cur_i = 0
        while cur_i < len(obs_list):
            (s, e) = obs_list[cur_i]
            if e == depth - 1:
                new_obs_list.append((s, obs_list[cur_i + 1][1]))
                cur_i += 1
            elif s == depth + 1:
                new_obs_list.append((depth, e))
            else:
                new_obs_list.append((s, e))
            cur_i += 1
        return new_obs_list

    @classmethod
    def _drop_sand(cls, x, depth, obstacles):
        candidate = None
        for (s, e) in obstacles[x]:
            if s <= depth <= e:
                return (-1, -1)
            if depth < s:
                candidate = (x, s - 1)
                break
        if candidate is None:
            return None
        left_candidate = cls._drop_sand(candidate[0] - 1, candidate[1] + 1, obstacles)
        if left_candidate == (-1, -1):
            right_candidate = cls._drop_sand(
                candidate[0] + 1, candidate[1] + 1, obstacles
            )
            if right_candidate == (-1, -1):
                return candidate
            else:
                return right_candidate
        else:
            return left_candidate

    @classmethod
    def _get_floor(cls, points: InputType) -> int:
        floor = 0
        for lines in points:
            for (_, depth) in lines:
                floor = max(floor, depth)
        return floor + 2

    @classmethod
    def _part_one(cls, points: InputType) -> OutputType:
        obstacles = cls._build_obstacles(points)
        for i, obs in enumerate(obstacles):
            if len(obs) != 0:
                obstacles[i] = cls._collapse_obstacles(obs)
        answer = 0
        while True:
            attempt = cls._drop_sand(500, 0, obstacles)

            if attempt is not None:
                answer += 1
                # print(answer, attempt)

                (x, depth) = attempt
                obstacles[x] = cls._add_obstacle(depth, obstacles[x])
            else:
                break
        return answer

    @classmethod
    def _part_two(cls, points: InputType) -> OutputType:
        obstacles = cls._build_obstacles(points)
        floor = cls._get_floor(points)
        for i, obs in enumerate(obstacles):
            obstacles[i].append((floor, floor))
            if len(obs) != 0:
                obstacles[i] = cls._collapse_obstacles(obs)
        for _ in range(500, floor + 500):
            obstacles.append([(floor, floor)])
        answer = 0
        while True:
            attempt = cls._drop_sand(500, 0, obstacles)

            if attempt is not None and attempt != (-1, -1):
                answer += 1

                (x, depth) = attempt
                obstacles[x] = cls._add_obstacle(depth, obstacles[x])
            else:
                break
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day14Solution.do_solution()
    print("===ACTUAL===")
    Day14Solution.do_solution(False)
