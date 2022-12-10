import { ISolution } from './ISolution'

export class Day0Solution extends ISolution<string, string> {
    protected parseRawInput(rawInput: string): string {
        return `${rawInput}-parsed`
    }
    protected solvePartOne(input: string): string {
        return `${input} ${input}`
    }
    protected solvePartTwo(input: string): string {
        let result: string = "";
        for (let i = input.length - 1; i >= 0; i--) {
            result += input[i];
        }
        return result
    }
}