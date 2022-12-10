import { ISolution } from './ISolution'
import Utils from './utils';
type Day1Input = number[][]
type Day1Output = number
export class Day1Solution extends ISolution<Day1Input, Day1Output> {
    private totals: number[];
    protected parseRawInput(rawInput: string): Day1Input {
        let rawElves = rawInput.split("\n\n");
        let parsedInput = [];
        for (const elf of rawElves) {
            parsedInput.push(elf.split("\n").map(x => parseInt(x)));
        }
        return parsedInput;
    }

    private calcTotals(input: Day1Input) {
        this.totals = input.map(elf => Utils.sum(elf));
    }
    protected solvePartOne(input: Day1Input): Day1Output {
        this.calcTotals(input);
        return Math.max(...this.totals);
    }
    protected solvePartTwo(input: Day1Input): Day1Output {
        let topThree = Utils.sorted(this.totals).slice(-3);
        return Utils.sum(topThree);
    }
}