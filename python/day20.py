from typing import List, Dict
from utils import ISolution, Pint

OutputType = int
InputType = List[int]


class Node:
    prev: "Node"
    next: "Node"
    val: Pint

    def __init__(self, val: Pint) -> None:
        self.prev = self
        self.next = self
        self.val = val

    def insert_after(self, other: "Node"):
        next_node = self.next

        self.next = other

        other.prev = self
        other.next = next_node

        next_node.prev = other

    def insert_before(self, other: "Node"):
        prev_node = self.prev

        prev_node.next = other

        other.prev = prev_node
        other.next = self

        self.prev = other

    def extract_node(self):
        prev_node = self.prev
        next_node = self.next

        self.prev.next = next_node
        self.next.prev = prev_node

        self.prev = self
        self.next = self
        return self


class Day20Solution(ISolution):

    _DAY_STRING: str = "20"

    @classmethod
    def _parse_input(cls, raw_input: str) -> InputType:
        return list(map(int, raw_input.split("\n")))

    @classmethod
    def _part_one(cls, int_list: InputType) -> OutputType:
        sequence: List[Pint] = []
        to_node: Dict[Pint, Node] = {}

        for (i, val) in enumerate(int_list):
            sequence.append((i, val))
            to_node[(i, val)] = Node((i, val))
        for (i, pi) in enumerate(sequence):
            to_node[pi].prev = to_node[sequence[i - 1]]
            to_node[pi].next = to_node[sequence[(i + 1) % len(sequence)]]

        cycle_length = len(sequence) - 1

        for pi in sequence:
            cur_node = to_node[pi]
            to_traverse = pi[1] % cycle_length

            go_next = to_traverse < (cycle_length // 2)
            if go_next:
                t_node = cur_node.prev
                node_to_add = cur_node.extract_node()
                for _ in range(to_traverse):
                    t_node = t_node.next
                t_node.insert_after(node_to_add)
            else:
                t_node = cur_node.next
                node_to_add = cur_node.extract_node()
                for _ in range(cycle_length - to_traverse):
                    t_node = t_node.prev
                t_node.insert_before(node_to_add)

        start_node = None
        for (i, v) in sequence:
            if v == 0:
                start_node = to_node[(i, v)]
        numbers = []
        if start_node is not None:
            t_node = start_node
            to_traverse = 1000 % len(sequence)
            for _ in range(3):
                for _ in range(to_traverse):
                    t_node = t_node.next
                numbers.append(t_node.val[1])
        return sum(numbers)

    @classmethod
    def _part_two(cls, int_list: InputType) -> OutputType:
        sequence: List[Pint] = []
        to_node: Dict[Pint, Node] = {}

        for (i, val) in enumerate(int_list):
            decrypt_val = val * 811589153
            sequence.append((i, decrypt_val))
            to_node[(i, decrypt_val)] = Node((i, decrypt_val))

        for (i, pi) in enumerate(sequence):
            to_node[pi].prev = to_node[sequence[i - 1]]
            to_node[pi].next = to_node[sequence[(i + 1) % len(sequence)]]

        cycle_length = len(sequence) - 1
        for _ in range(10):
            for pi in sequence:
                cur_node = to_node[pi]
                to_traverse = pi[1] % cycle_length

                go_next = to_traverse < (cycle_length // 2)
                if go_next:
                    t_node = cur_node.prev
                    node_to_add = cur_node.extract_node()
                    for _ in range(to_traverse):
                        t_node = t_node.next
                    t_node.insert_after(node_to_add)
                else:
                    t_node = cur_node.next
                    node_to_add = cur_node.extract_node()
                    for _ in range(cycle_length - to_traverse):
                        t_node = t_node.prev
                    t_node.insert_before(node_to_add)

        start_node = None
        for (i, v) in sequence:
            if v == 0:
                start_node = to_node[(i, v)]
        numbers = []
        if start_node is not None:
            t_node = start_node
            to_traverse = 1000 % len(sequence)
            for _ in range(3):
                for _ in range(to_traverse):
                    t_node = t_node.next
                numbers.append(t_node.val[1])
        return sum(numbers)


if __name__ == "__main__":
    print("===SAMPLE===")
    Day20Solution.do_solution()
    print("===ACTUAL===")
    Day20Solution.do_solution(False)
