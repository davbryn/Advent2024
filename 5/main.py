import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from helpers.print_queue import PrintQueue


def load_instructions(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
        page_order = [tuple(line.strip().split('|')) for line in lines if '|' in line]
        page_updates = [list(line.strip().split(',')) for line in lines if ',' in line]
    return page_order, page_updates


page_rules, page_updates = load_instructions('input.txt')
queue = PrintQueue(page_rules)

# Fix the invalid updates
fixed_updates = queue.fix_updates(page_updates)
# Find the middle pages of the fixed updates
middle_pages = queue.find_middle_pages(fixed_updates)
result = sum(middle_pages)
print(result)