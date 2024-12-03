''' Safe sequences are sequences of integers where the difference between each pair of adjacent integers is 1, 2, or 3.'''
def is_sequence_safe(sequence):
    ascending = sequence[1] > sequence[0]
    for i in range(1, len(sequence)):
        delta = sequence[i] - sequence[i - 1]
        if abs(delta) not in {1, 2, 3} or delta == 0:
            return False
        if ascending and delta < 0:
            return False
        if not ascending and delta > 0:
            return False
    return True

''' Count the number of safe reports
    @damper_enabled: If True, the dampener is enabled. The dampener allows a single bad level per line.'''
def count_safe_reports(input_file, dampener_enabled=False):
    num_safe = 0
    with open(input_file, 'r') as file:
        for line in file:
            levels = list(map(int, line.strip().split()))
            for i, _ in enumerate(levels):
                temp_levels = levels[:i] + levels[i+1:] if dampener_enabled else levels
                if is_sequence_safe(temp_levels):
                    num_safe += 1
                    break
    return num_safe

print(count_safe_reports('input.txt'))
print(count_safe_reports('input.txt', dampener_enabled=True))