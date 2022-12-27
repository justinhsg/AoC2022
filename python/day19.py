from typing import List, Tuple, Set
import re
from heapq import heappush as hpush, heappop as hpop
from utils import ISolution, int4, ceil_div


State = Tuple[int, int4, int4]


class Day19Recipe:
    ore_cost: int
    cly_cost: int
    obs_cost: int
    ore_bot: int
    cly_bot: int
    obs_bot: int
    geo_bot: int

    # fmt:off
    def __init__(self, ore_cost:int, clay_cost:int, obs_cost:int,
        ore_bot:int, clay_bot:int, obs_bot:int, geode_bot:int) -> None:
        self.ore_cost = ore_cost
        self.ore_bot = ore_bot
        self.cly_cost = clay_cost
        self.cly_bot = clay_bot
        self.obs_cost = obs_cost
        self.obs_bot = obs_bot
        self.geo_bot = geode_bot
    # fmt:on

    def wait_time(self, state: State):
        _, (oreb, clyb, obsb, _), (orer, clyr, obsr, _) = state
        ore_time = 0
        if self.ore_cost > 0 and orer < self.ore_cost:
            ore_time = ceil_div(self.ore_cost - orer, oreb)
        cly_time = 0
        if self.cly_cost > 0 and clyr < self.cly_cost:
            cly_time = ceil_div(self.cly_cost - clyr, clyb)
        obs_time = 0
        if self.obs_cost > 0 and obsr < self.obs_cost:
            obs_time = ceil_div(self.obs_cost - obsr, obsb)
        return max(ore_time, cly_time, obs_time) + 1

    def wait_to_build(self, state: State):
        t_elapsed, (oreb, clyb, obsb, geob), (orer, clyr, obsr, geor) = state
        wait_time = self.wait_time(state)
        new_state = (
            t_elapsed + wait_time,
            (
                oreb + self.ore_bot,
                clyb + self.cly_bot,
                obsb + self.obs_bot,
                geob + self.geo_bot,
            ),
            (
                orer - self.ore_cost + oreb * wait_time,
                clyr - self.cly_cost + clyb * wait_time,
                obsr - self.obs_cost + obsb * wait_time,
                geor + geob * wait_time,
            ),
        )
        return new_state


class Day19Blueprint:
    id: int
    ore_r: Day19Recipe
    cly_r: Day19Recipe
    obs_r: Day19Recipe
    geo_r: Day19Recipe
    max_ore: int
    max_cly: int
    max_obs: int

    def __init__(self, b_id, ore_r, cly_r, obs_r, geo_r) -> None:
        self.id = b_id
        self.ore_r = ore_r
        self.cly_r = cly_r
        self.obs_r = obs_r
        self.geo_r = geo_r

        self.max_ore = max(
            [
                self.ore_r.ore_cost,
                self.cly_r.ore_cost,
                self.obs_r.ore_cost,
                self.geo_r.ore_cost,
            ]
        )
        self.max_cly = self.obs_r.cly_cost
        self.max_obs = self.geo_r.obs_cost


OutputType = int
InputType = List[Day19Blueprint]


class Day19Solution(ISolution):

    _DAY_STRING: str = "19"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        blueprints: List[Day19Blueprint] = []
        input_pattern = re.compile(
            r"Blueprint (\d+): Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obsidian\."
        )
        for line in raw_input.split("\n"):
            matches = re.match(input_pattern, line)
            if matches:
                gs = matches.groups()
                b_id = int(gs[0])

                ore_recipe = Day19Recipe(int(gs[1]), 0, 0, 1, 0, 0, 0)
                clay_recipe = Day19Recipe(int(gs[2]), 0, 0, 0, 1, 0, 0)
                obs_recipe = Day19Recipe(int(gs[3]), int(gs[4]), 0, 0, 0, 1, 0)
                geo_recipe = Day19Recipe(int(gs[5]), 0, int(gs[6]), 0, 0, 0, 1)
                blueprints.append(
                    Day19Blueprint(
                        b_id, ore_recipe, clay_recipe, obs_recipe, geo_recipe
                    )
                )
        return blueprints

    @classmethod
    def get_next_states(cls, cur_state: State, bp: Day19Blueprint, time_budget: int):
        next_states: List[State] = []
        t_elapsed, (oreb, clyb, obsb, geob), (orer, clyr, obsr, geor) = cur_state
        if t_elapsed == time_budget:
            return next_states
        if 0 < oreb < bp.max_ore:
            next_state = bp.ore_r.wait_to_build(cur_state)
            if next_state[0] <= time_budget:
                next_states.append(next_state)

        if clyb < bp.max_cly and oreb > 0:
            next_state = bp.cly_r.wait_to_build(cur_state)
            if next_state[0] <= time_budget:
                next_states.append(next_state)

        if obsb < bp.max_obs and oreb > 0 and clyb > 0:
            next_state = bp.obs_r.wait_to_build(cur_state)
            if next_state[0] <= time_budget:
                next_states.append(next_state)

        if oreb > 0 and obsb > 0:
            next_state = bp.geo_r.wait_to_build(cur_state)
            if next_state[0] <= time_budget:
                next_states.append(next_state)
        if len(next_states) == 0:
            rem_time = time_budget - t_elapsed
            next_states.append(
                (
                    time_budget,
                    (oreb, clyb, obsb, geob),
                    (
                        orer + oreb * rem_time,
                        clyr + clyb * rem_time,
                        obsr + obsr * rem_time,
                        geor + geob * rem_time,
                    ),
                )
            )
        return next_states

    @classmethod
    def can_outperform(cls, cur_state: State, best_geodes: int, time_budget: int):
        time_elapsed, (_, _, _, geo_b), (_, _, _, geo) = cur_state
        time_remaining = time_budget - time_elapsed
        confirmed_geodes = geo + geo_b * time_remaining
        poss_geodes = (time_remaining * (time_remaining - 1)) // 2
        return (confirmed_geodes + poss_geodes) > best_geodes

    @classmethod
    def process_bp(cls, bp: Day19Blueprint, time_budget):

        pq: List[Tuple[int, State]] = []
        initial_state = (0, (1, 0, 0, 0), (0, 0, 0, 0))
        best_geodes = 0
        hpush(pq, (0, initial_state))
        seen_states: Set[State] = set([initial_state])
        while pq:
            geodes, cur_state = hpop(pq)
            geodes *= -1
            best_geodes = max(best_geodes, geodes)
            if cls.can_outperform(cur_state, best_geodes, time_budget):
                next_states = cls.get_next_states(cur_state, bp, time_budget)
                for state in next_states:
                    if state not in seen_states:
                        hpush(pq, (-state[2][3], state))
                        seen_states.add(state)
        return best_geodes

    @classmethod
    def _part_one(cls, blueprints: InputType) -> OutputType:
        answer = 0
        for bp in blueprints:
            out = cls.process_bp(bp, 24)
            answer += out * bp.id
        return answer

    @classmethod
    def _part_two(cls, blueprints: InputType) -> OutputType:
        answer = 1
        for bp in blueprints[:3]:
            out = cls.process_bp(bp, 32)
            answer *= out
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day19Solution.do_solution()
    print("===ACTUAL===")
    Day19Solution.do_solution(False)
