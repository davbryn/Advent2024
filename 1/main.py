from collections import Counter

''' Helper Function '''
def load_test_data(input_file):
    with open(input_file, 'r') as file:
        left_list, right_list = [], []
        for line in file:
            lhs, rhs = map(int, line.strip().split())
            left_list.append(lhs)
            right_list.append(rhs)
    return left_list, right_list

''' Distance between both destination lists '''
def total_distance(left_list, right_list):
    return sum(abs(a - b) for a, b in zip(sorted(left_list), sorted(right_list)))

''' Similarity between both destination lists '''
def similarity(left_list, right_list):
    right_counter = Counter(right_list)
    return sum(val * right_counter[val] for val in left_list)

left_list, right_list = load_test_data('input.txt')
print(total_distance(left_list, right_list))
print(similarity(left_list, right_list))