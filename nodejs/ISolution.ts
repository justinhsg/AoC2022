import * as fs from "fs";
import { performance } from 'perf_hooks';

export abstract class ISolution<InputType, OutputType> {
    private inputSuffix: string = ".input";
    private sampleSuffix: string = ".sample";
    private fileName: string;
    private useSample: boolean;

    constructor(fileName: string, useSample: boolean) {
        this.fileName = fileName;
        this.useSample = useSample;
    }

    private readInput(): string {
        return fs.readFileSync(`../input/${this.fileName}${this.useSample ? this.sampleSuffix : this.inputSuffix}`, 'utf8')
    }

    protected abstract parseRawInput(rawInput: string): InputType;
    protected abstract solvePartOne(input: InputType): OutputType;
    protected abstract solvePartTwo(input: InputType): OutputType;

    public solve() {
        const startTime = performance.now();
        let rawInput: string = this.readInput();
        let parsedInput: InputType = this.parseRawInput(rawInput);
        let partOne = this.solvePartOne(parsedInput);
        let partTwo = this.solvePartTwo(parsedInput);
        const endTime = performance.now();
        console.log(`Solving Day ${this.fileName} ${this.useSample ? "with sample input" : "with real input"}:`);
        console.log("Part One:");
        console.log(partOne);
        console.log("Part Two:");
        console.log(partTwo);
        console.log(`Total execution time: ${(endTime - startTime).toFixed(3)}ms`);
    }
}

