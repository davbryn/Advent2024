
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from helpers.operator import add, multiply, concatenate

def load_questions(file):
    with open(file, 'r') as f:
        solutions = [(int(lhs), list(map(int, rhs.split())))
             for line in f for lhs, rhs in [line.strip().split(":")]]
    return solutions

def solve(solutions, operators):
    result = []
    
    for test_value, numbers in solutions:
        # Use a set rather than a list as this will not allow duplicates to be added to the possible values
        # and we don't have to check for duplicates in the list

        possibles = {numbers.pop(0)}
        for curr in numbers:
            possibles = {
                v for p in possibles
                    for op in operators
                        if (v := op(p, curr)) <= test_value
            }
        if test_value in possibles:
            result.append(test_value)
            
    return result


def puzzle1():
    solutions = load_questions('input.txt')
    result = solve(solutions, [add, multiply])
    return sum(result)

def puzzle2():
    solutions = load_questions('input.txt')
    result = solve(solutions, [add, multiply, concatenate])
    return sum(result)

print(puzzle1())
print(puzzle2())