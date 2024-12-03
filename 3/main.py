import re

''' Helper Function '''
def load_test_data(input_file):
    pattern = r"mul\((\d+),(\d+)\)"
    with open(input_file, 'r') as file:
        content = file.read()
    content = parse_conditionals(content)
    matches = re.findall(pattern, content)
    multiplacation_args = [[int(a), int(b)] for a, b in matches]
    return multiplacation_args

''' Parse conditionals'''
def parse_conditionals(input_string):
    tokens = re.split(r"(don't\(\)|do\(\))", input_string)
    result = ''
    capture = True

    # Don't consume on conditionals but if we haven't found a conditional we might want to treat the 
    # input as tokens we are interested in (mul() in our case)
    for token in tokens:
        if token == "don't()":
            capture = False
        elif token == "do()":
            capture = True
        elif capture:
            result += token
    
    return result

''' Distance between both destination lists '''
def sum_of_multiplications(multiplication_list):
    return sum(a * b for a, b in multiplication_list)


multiplication_list = load_test_data('input.txt')
print(sum_of_multiplications(multiplication_list))
