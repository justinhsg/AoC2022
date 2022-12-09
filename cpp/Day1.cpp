#include <bits/stdc++.h>
using namespace std;

list<string> readInput()
{
    list<string> lines = {};
    ifstream istream = ifstream("../input/1.input", ios_base::in);
    FILE *inputPtr = fopen("../input/1.input", "r");
    bool hasContent = true;
    while (!istream.eof())
    {
        string line;
        getline(istream, line);
        lines.push_back(line);
    }
    return lines;
}

int main()
{
    list<string> lines = readInput();
    list<int> calories = {};
    int calorie_acc = 0;
    for (list<string>::iterator it = lines.begin(); it != lines.end(); it++)
    {
        string line = *it;
        if (line.length() == 0)
        {
            if (calorie_acc)
            {
                calories.push_back(calorie_acc);
                calorie_acc = 0;
            }
        }
        else
        {
            calorie_acc += stoi(line);
        }
    }
    if (calorie_acc)
    {
        calories.push_back(calorie_acc);
    }
    calories.sort(greater<int>());

    int maxAmount = calories.front();
    int topThree = 0;
    for (int i = 0; i < 3; i++)
    {
        topThree += calories.front();
        calories.pop_front();
    }
    cout << maxAmount << endl;
    cout << topThree << endl;
}