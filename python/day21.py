from typing import List, Dict, Union, Tuple
from utils import ISolution

OutputType = int
InputType = List[Tuple[str, List[str]]]


class Node:
    name: str
    l: Union[str, None]
    r: Union[str, None]
    op: Union[str, None]
    val: Union[int, None]
    contains_humn: Union[bool, None]

    def __init__(self, n, l, r, op, val) -> None:
        self.name = n
        self.l = l
        self.r = r
        self.op = op
        self.val = val
        self.contains_humn = None if n != "humn" else True

    def evaluate(self, node_map: Dict[str, "Node"]) -> int:
        if self.val is not None:
            return self.val
        if self.l is not None and self.r is not None and self.op is not None:
            l_val = node_map[self.l].evaluate(node_map)
            r_val = node_map[self.r].evaluate(node_map)
            if self.op == "+":
                self.val = l_val + r_val
            elif self.op == "*":
                self.val = l_val * r_val
            elif self.op == "/":
                self.val = l_val // r_val
            elif self.op == "-":
                self.val = l_val - r_val
            else:
                raise Exception(f"Other op found {self.op}")
            return self.val
        raise Exception(f"Invalid node: {self.val} {self.l} {self.r} {self.op}")

    def has_humn(self, node_map: Dict[str, "Node"]) -> bool:
        if self.contains_humn is not None:
            return self.contains_humn
        if self.l is None:
            self.contains_humn = False
            return self.contains_humn
        if self.l is not None and self.r is not None:

            self.contains_humn = node_map[self.l].has_humn(node_map) or node_map[
                self.r
            ].has_humn(node_map)
            return self.contains_humn
        raise Exception(f"Invalid node: {self.val} {self.l} {self.r} {self.op}")

    def to_match(self, val: int, node_map: Dict[str, "Node"]):
        if self.name == "humn":
            return val
        assert self.l is not None and self.r is not None and self.op is not None
        l_n = node_map[self.l]
        r_n = node_map[self.r]
        if l_n.has_humn(node_map):
            r_v = r_n.evaluate(node_map)
            req_l = 0
            if self.op == "+":
                # solve val = req_l + r_v
                req_l = val - r_v
            elif self.op == "-":
                # solve val = req_l - r_v
                req_l = val + r_v
            elif self.op == "*":
                # solve val = req_l * r_v
                req_l = val // r_v
            elif self.op == "/":
                # solve val = req_l / r_v
                req_l = val * r_v
            else:
                raise Exception(f"Unidentifiable op {self.op}")
            return l_n.to_match(req_l, node_map)
        else:
            l_v = l_n.evaluate(node_map)
            req_r = 0
            if self.op == "+":
                # solve val = l_v + req_r
                req_r = val - l_v
            elif self.op == "-":
                # solve val = l_v - req_r
                req_r = l_v - val
            elif self.op == "*":
                # solve val = l_v * req_r
                req_r = val // l_v
            elif self.op == "/":
                # solve val = l_v / req_r
                req_r = l_v // val
            else:
                raise Exception(f"Unidentifiable op {self.op}")
            return r_n.to_match(req_r, node_map)


class Day21Solution(ISolution):

    _DAY_STRING: str = "21"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        raw_monkeys: InputType = []
        for line in raw_input.split("\n"):
            parts = line.split(": ")
            content = parts[1].split(" ")
            raw_monkeys.append((parts[0], content))
        return raw_monkeys

    @classmethod
    def _part_one(cls, raw_monkeys: InputType) -> OutputType:
        to_node: Dict[str, Node] = {}

        for (monkey_id, contents) in raw_monkeys:
            if len(contents) == 1:
                t_monkey = Node(
                    n=monkey_id, l=None, r=None, op=None, val=int(contents[0])
                )
            else:
                t_monkey = Node(
                    n=monkey_id, l=contents[0], r=contents[2], op=contents[1], val=None
                )
            to_node[monkey_id] = t_monkey

        return to_node["root"].evaluate(to_node)

    @classmethod
    def _part_two(cls, raw_monkeys: InputType) -> OutputType:
        to_node: Dict[str, Node] = {}

        for (monkey_id, contents) in raw_monkeys:
            if len(contents) == 1:
                t_monkey = Node(
                    n=monkey_id, l=None, r=None, op=None, val=int(contents[0])
                )
            else:
                t_monkey = Node(
                    n=monkey_id, l=contents[0], r=contents[2], op=contents[1], val=None
                )
            to_node[monkey_id] = t_monkey

        root_node = to_node["root"]
        assert root_node.l is not None and root_node.r is not None
        left_node = to_node[root_node.l]
        right_node = to_node[root_node.r]
        answer = None
        if left_node.has_humn(to_node):
            right_val = right_node.evaluate(to_node)
            answer = left_node.to_match(right_val, to_node)
        else:
            left_val = left_node.evaluate(to_node)
            answer = right_node.to_match(left_val, to_node)
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day21Solution.do_solution()
    print("===ACTUAL===")
    Day21Solution.do_solution(False)
