import { Day0Solution } from './day0';
import { Day1Solution } from './day1';

const solutions = [Day0Solution, Day1Solution]
const args: string[] = process.argv;
const solutionDay = parseInt(args[2]);
const useSample = args.length == 4 && args[3].toLowerCase() === "true"
const solution = new solutions[solutionDay](args[2], useSample);
solution.solve();


