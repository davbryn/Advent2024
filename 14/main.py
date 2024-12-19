from enum import Enum
from datetime import datetime

class Computer():
    
    class Opcode(Enum):
        ADV = 0
        BXL = 1
        BST = 2
        JNZ = 3
        BXC = 4
        OUT = 5
        BDV = 6
        CDV = 7
    
    v_table = []

    def __init__(self):
        # Registers
        self.A = 0
        self.B = 0
        self.C = 0
        self.IP = 0
        self.instructions = []
        self.debug_enabled = False
        self.decompile_enabled = False
        self.std_io = "" # Standard IO
        self._build_v_table()
        self.decompilation = []

    def set_decompile_enabled(self, enabled):
        self.decompile_enabled = enabled
        return self
    
    def set_debug_enabled(self, enabled):
        self.debug_enabled = enabled
        return self
    
    def _build_v_table(self):
        self.v_table.append(self.adv_func)
        self.v_table.append(self.bxl_func)
        self.v_table.append(self.bst_func)
        self.v_table.append(self.jnz_func)
        self.v_table.append(self.bxc_func)
        self.v_table.append(self.out_func)
        self.v_table.append(self.bdv_func)
        self.v_table.append(self.cdv_func)
    
    def call_fun(self, index, operand=None, arg=None):
        if arg is not None:
            return self.v_table[index](operand, arg)
        else:
            self.v_table[index](operand)

    def get_operand(self, operand, combo=False):
        if not combo:
            return operand
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            return self.C
        else:
            return None
        
    def fetch(self):
        if len(self.instructions) < 2 or self.IP > len(self.instructions) - 2:
            return None, None
        opcode = self.instructions[self.IP]
        operand = self.get_operand(
            self.instructions[self.IP + 1],
            combo=self.Opcode(opcode) in [
                self.Opcode.ADV, self.Opcode.BST, 
                self.Opcode.OUT, self.Opcode.BDV, self.Opcode.CDV
            ]
        )
        return opcode, operand
    
    def decode(self, instruction):
        for i in instruction:
            self.instructions.append(i)

    def decompile(self, opcode=None, operand=None):
        decompilation = []
        if opcode == self.Opcode.ADV.value:
            decompilation.append(f"\td = 2 ** {operand}\n")
            decompilation.append(f"\ta = a // d")
        elif opcode == self.Opcode.BXL.value:
            decompilation.append(f"\tb = b ^ {operand}")
        elif opcode == self.Opcode.BST.value:
            decompilation.append(f"\tb = get_operand(a, b, c, {self.instructions[self.IP + 1]}, combo=True) % 8)")
        elif opcode == self.Opcode.BXC.value:
            decompilation.append(f"\tb = b ^ c")
        elif opcode == self.Opcode.OUT.value:
            decompilation.append(f"\toutputs.append(get_operand(a, b, c, {self.instructions[self.IP + 1]}, combo=True) % 8)")
        elif opcode == self.Opcode.BDV.value:
            decompilation.append(f"\td = 2 ** {operand}\n")
            decompilation.append(f"\tb = a // d")
        elif opcode == self.Opcode.CDV.value:
            decompilation.append(f"\td = 2 ** {operand}\n")
            decompilation.append(f"\tc = a // d")
        return decompilation
            
    def run(self):
        running = True
        # Decompilation is optional, we keep it but do not print if not needed
        decompilation = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        decompilation.append(f"''' Decompilation of Program {self.instructions} - DateTime: {current_time} '''")
        decompilation.append(f"def decompliation():\n")
        combo_helper = """
        def get_operand(a, b, c, operand, combo=False):
            if not combo:
                return operand
            if operand >= 0 and operand <= 3:
                return operand
            elif operand == 4:
                return a
            elif operand == 5:
                return b
            elif operand == 6:
                return c
            elif operand == 7:
                return c
            else:
                return None
        """
        decompilation.append(f"{combo_helper}\n")
        decompilation.append(f"\toutputs = [] \n")
        decompilation.append(f"\ta = {self.A}")
        decompilation.append(f"\tb = 0\n")
        decompilation.append(f"\tc = 0\n")
        decompilation.append(f"\td = 0\n")

        if self.debug_enabled:
            print(f"Program: {self.instructions}")
        while running:
            opcode, operand = self.fetch()
            
            if opcode is not None:
                decompilation.append(self.decompile(opcode, operand))
                self.call_fun(opcode, operand)
            else:
                running = False
        decompilation.append(f"\treturn outputs")
        self.decompilation = decompilation
        return self.std_io
    

    def adv_func(self, operand):
        d = 2 ** operand
        self.A = self.A // d
        self.IP += 2

    def bxl_func(self, operand):
        self.B = self.B ^ operand
        self.IP += 2

    def bst_func(self, operand):
        self.B = operand % 8
        self.IP += 2

    def jnz_func(self, operand):
        if self.A != 0:
            self.IP = operand
        else:
            self.IP += 2

    def bxc_func(self, operand=None):
        self.B = self.B ^ self.C
        self.IP += 2

    def out_func(self, operand):
        if len(self.std_io) > 0:
            self.std_io += ","
        self.std_io += str(operand % 8)
        self.IP += 2

    def bdv_func(self, operand):
        d = 2 ** operand
        self.B = self.A // d
        self.IP += 2

    def cdv_func(self, operand):
        d = 2 ** operand
        self.C = self.A // d
        self.IP += 2
    
    def load_state(self, state):
        self.A = state["A"]
        self.B = state["B"]
        self.C = state["C"]
        self.IP = state["IP"]
        self.instructions = state["instructions"]
        self.std_io = ""
        return self

    def dump_state(self):
        return f"A={self.A:<10} B={self.B:<10} C={self.C:<10}"


def search_initial_value(computer):
    """
    Search for the lowest initial value of register A that causes the
    program to output a copy of its own instructions.
    """

    def _search_at_position(position, current_value=0):
        if position < 0:
            return current_value

        # Try all possible values for this 'digit'
        for i in range(8):
            candidate_value = current_value + i * (8 ** position)
            
            computer.load_state({
                "A": candidate_value,
                "B": 0,
                "C": 0,
                "IP": 0,
                "instructions": computer.instructions[:]
            })

            out_str = computer.run().strip()
            if out_str == "":
                out_list = []
            else:
                out_list = out_str.split(",")

            # Check if we can compare the position-th output to the instructions
            if position >= len(out_list):
                continue

            digit_str = out_list[position]
            # Ensure it's a valid digit
            if not digit_str.isdigit():
                continue

            output_digit = int(digit_str)
            if output_digit != computer.instructions[position]:
                continue

            # If it matches, go one position deeper
            result = _search_at_position(position - 1, candidate_value)
            if result is not None:
                return result

        return None

    return _search_at_position(len(computer.instructions) - 1)





cpu = Computer()
outputs = cpu.load_state({"A": 27334280, "B": 0, "C": 0, "IP":0, "instructions":[2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]}).run()
print(f"CPU output is {outputs}")

result = search_initial_value(cpu)
print(f"Quine seed is {result}")

for decompilation in cpu.decompilation:
    print("".join(decompilation))
