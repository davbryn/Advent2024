from math import gcd
from collections import namedtuple

def read_claw_machines(file_path):
    machines = []  
    machine = {}   
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:  
                if machine:  
                    machines.append(machine)
                    machine = {}
                continue
            
            # Parse Button A
            if line.startswith("Button A"):
                parts = line.split(", ")
                xa = int(parts[0].split("+")[1])
                ya = int(parts[1].split("+")[1])
                machine["A"] = (xa, ya)
            
            # Parse Button B
            elif line.startswith("Button B"):
                parts = line.split(", ")
                xb = int(parts[0].split("+")[1])
                yb = int(parts[1].split("+")[1])
                machine["B"] = (xb, yb)
            
            # Parse Prize
            elif line.startswith("Prize"):
                parts = line.split(", ")
                xp = int(parts[0].split("=")[1])
                yp = int(parts[1].split("=")[1])
                machine["Prize"] = (xp, yp)
        
        # Add the last machine if it exists
        if machine:
            machines.append(machine)
    
    return machines


def solve_claw_machine(xa, ya, xb, yb, xp, yp, max_presses=100):
    min_cost = float('inf')  # Start with a very high cost
    
    for a in range(max_presses + 1):
        for b in range(max_presses + 1):
            if a * xa + b * xb == xp and a * ya + b * yb == yp:
                cost = 3 * a + b  #
                min_cost = min(min_cost, cost)
                found_solution = True
    
    return min_cost if found_solution else None


if __name__ == "__main__":
    file_path = "input.txt"  
    machines = read_claw_machines(file_path)

    total_min_cost = 0
    
    for i, machine in enumerate(machines, start=1):
        xa, ya = machine["A"]
        xb, yb = machine["B"]
        xp, yp = machine["Prize"]
        
        min_cost = solve_claw_machine(xa, ya, xb, yb, xp, yp)
        
        if min_cost is not None:
            print(f"Machine {i}: Minimum tokens = {min_cost}")
            total_min_cost += min_cost

        else:
            print(f"Machine {i}: No solution found")
    
    print(f"Minimum tokens required: {total_min_cost}")
