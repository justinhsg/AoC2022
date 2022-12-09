from typing import List, Union

from utils import ISolution


class DiskObject:

    size: Union[None, int]
    children: Union[None, List]

    def __init__(self, name, parent, is_dir) -> None:
        self.name = name
        self.size = None
        self.children = [] if is_dir else None
        self.parent = parent

    def __str__(self) -> str:
        if self.children is not None:
            return (
                f"{self.name}: {self.size}, {[child.name for child in self.children]}"
            )
        else:
            return f"{self.name}: {self.size}"


class Day7Solution(ISolution):

    _DAY_STRING: str = "7"

    @classmethod
    def _parse_input(cls, raw_input: str) -> List[str]:
        return raw_input.split("\n")

    @classmethod
    def _calc_sizes(cls, file_map: "dict[str, DiskObject]", cur_obj: DiskObject) -> int:
        if cur_obj.size is not None:
            return cur_obj.size
        else:
            total = 0
            if cur_obj.children is not None:
                for child in cur_obj.children:
                    total += cls._calc_sizes(file_map, child)
            cur_obj.size = total
            return total

    @classmethod
    def _pwd(cls, dirs: List[DiskObject]):
        if len(dirs) == 1:
            return "/"
        else:
            return f"/{'/'.join([dir.name for dir in dirs])}"

    @classmethod
    def _build_sizes(cls, lines: List[str]) -> "dict[str,DiskObject]":
        file_map: "dict[str, DiskObject]" = {}
        file_map["/"] = DiskObject("/", None, True)
        line_idx = 0
        cur_dir: List[DiskObject] = [file_map["/"]]
        while line_idx < len(lines):
            line = lines[line_idx]
            tokens = line.split(" ")
            if tokens[1] == "cd":
                if tokens[2] == "..":
                    cur_dir = cur_dir[:-1]
                else:
                    if cur_dir[-1].children is not None:
                        for child in cur_dir[-1].children:
                            if child.name == tokens[2]:
                                cur_dir.append(child)
                                break
            else:
                while line_idx + 1 < len(lines) and lines[line_idx + 1][0] != "$":
                    line_idx += 1
                    line = lines[line_idx]
                    tokens = line.split(" ")
                    object_name = tokens[1]
                    is_dir = tokens[0] == "dir"
                    new_obj = DiskObject(object_name, cur_dir[-1], is_dir)
                    if not is_dir:
                        new_obj.size = int(tokens[0])
                    if cur_dir[-1].children is not None:
                        cur_dir[-1].children.append(new_obj)
                    cwd = cls._pwd(cur_dir)
                    file_map[f"{cwd}/{object_name}"] = new_obj
            line_idx += 1
        cls._calc_sizes(file_map, file_map["/"])
        return file_map

    @classmethod
    def _part_one(cls, lines: List[str]) -> int:
        file_map = cls._build_sizes(lines)
        answer = 0
        for obj in file_map.items():
            if obj[1].children is not None:
                file_size = obj[1].size
                if file_size is not None and file_size <= 100000:
                    answer += file_size
        return answer

    @classmethod
    def _part_two(cls, lines: List[str]) -> int:
        file_map = cls._build_sizes(lines)
        answer = 70000000
        min_req = 0
        if file_map["/"].size is not None:
            min_req = file_map["/"].size - 40000000
        for obj in file_map.items():
            if obj[1].children is not None:
                file_size = obj[1].size
                if (
                    file_size is not None
                    and file_size >= min_req
                    and file_size <= answer
                ):
                    answer = file_size
        return answer


if __name__ == "__main__":
    print("===SAMPLE===")
    Day7Solution.do_solution()
    print("===ACTUAL===")
    Day7Solution.do_solution(False)
