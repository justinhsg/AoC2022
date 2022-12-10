export default class Utils {
    static sum(arr: number[]) {
        return arr.reduce((acc, cur) => acc + cur, 0);
    }

    static sorted(arr: number[]) {
        return [...arr].sort((a, b) => a - b);
    }
}