from typing import List
from utils import ISolution


OutputType = int

InputType = str


class Day17Obstacles:

    obstacles: List[int]
    base: int

    def __init__(self):
        self.obstacles = []
        self.base = 0

    def highest_point(self):
        return len(self.obstacles) + self.base

    def add_rock(self, new_rock, rock_base):
        row_i = 0
        offset_height = rock_base - self.base
        while row_i + offset_height < len(self.obstacles) and row_i < len(new_rock):
            self.obstacles[row_i + offset_height] |= new_rock[row_i]
            row_i += 1
        for row in new_rock[row_i:]:
            self.obstacles.append(row)

    def collides(self, new_rock, rock_base):
        if rock_base == -1:
            return True
        elif rock_base >= self.highest_point() or rock_base < self.base:
            return False
        else:
            offset_height = rock_base - self.base
            row_i = 0
            collides = False
            while not collides:
                can_compare = row_i + offset_height < len(
                    self.obstacles
                ) and row_i < len(new_rock)
                if can_compare:
                    obs_row = self.obstacles[row_i + offset_height]
                    rock_row = new_rock[row_i]
                    if obs_row | rock_row != obs_row + rock_row:
                        collides = True
                else:
                    break
                row_i += 1
            return collides

    def drop_rock(self, rock, winds, wind_idx):
        rock_base = self.highest_point() + 3
        cur_rock = [row for row in rock]
        while True:
            wind_dir = winds[wind_idx]
            wind_idx = (wind_idx + 1) % len(winds)
            if wind_dir == ">":
                can_shift = True
                for row in cur_rock:
                    if row % 2 == 1:
                        can_shift = False
                        break
                if can_shift:
                    new_rock = [row >> 1 for row in cur_rock]
                    if not self.collides(new_rock, rock_base):
                        cur_rock = new_rock
            else:
                can_shift = True
                for row in cur_rock:
                    if row >= 64:
                        can_shift = False
                        break
                if can_shift:
                    new_rock = [row << 1 for row in cur_rock]
                    if not self.collides(new_rock, rock_base):
                        cur_rock = new_rock
            if self.collides(cur_rock, rock_base - 1):
                break
            else:
                rock_base -= 1
        self.add_rock(cur_rock, rock_base)
        return wind_idx


class Day17Solution(ISolution):

    _DAY_STRING: str = "17"
    # fmt:off
    _rocks:List[List[int]] = [
        [int("0011110", 2)],
        [int("0001000", 2), int("0011100", 2), int("0001000", 2)],
        [int("0011100", 2), int("0000100", 2), int("0000100", 2)],
        [int("0010000", 2), int("0010000", 2), int("0010000", 2), int("0010000", 2)],
        [int("0011000", 2), int("0011000", 2)],
    ]

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return raw_input

    @classmethod
    def _part_one(cls, winds: InputType) -> OutputType:
        wind_idx = 0
        obstacles = Day17Obstacles()
        for i in range(2022):
            cur_rock = [row for row in cls._rocks[i%5]]
            wind_idx = obstacles.drop_rock(cur_rock, winds, wind_idx)
        return obstacles.highest_point()

    @classmethod
    def _part_two(cls, winds: InputType) -> OutputType:
        wind_idx = 0
        obstacles = Day17Obstacles()
        patterns = dict()
        rock_i = 0
        N = 100
        times = 1000000000000
        has_cycled = False
        while rock_i < times:
            cur_rock = [row for row in cls._rocks[rock_i%5]]
            wind_idx = obstacles.drop_rock(cur_rock, winds, wind_idx)
            state = (rock_i%5, wind_idx, tuple(obstacles.obstacles[-N:]))
            if(state not in patterns or has_cycled):
                if(len(obstacles.obstacles) >= N):
                    patterns[state] = (rock_i, obstacles.highest_point())
            else:
                (prev_i, prev_highest) = patterns[state]
                period = rock_i - prev_i
                d_height = obstacles.highest_point() - prev_highest
                remainder = times - rock_i
                repeats = remainder // period
                obstacles.base = repeats * d_height
                rock_i += repeats * period
                has_cycled = True
            rock_i += 1
        return obstacles.highest_point()


if __name__ == "__main__":
    print("===SAMPLE===")
    Day17Solution.do_solution()
    print("===ACTUAL===")
    Day17Solution.do_solution(False)
