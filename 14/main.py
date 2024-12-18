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
        if arg != None:
            return self.v_table[index](operand, arg)
        else:
            self.v_table[index](operand)

    def get_operand(self, operand, combo=False):
        if not combo:
            return operand
        if operand >= 0 and operand <= 3:
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
            return
        
        
    def fetch(self):
        if len(self.instructions) < 2 or self.IP > len(self.instructions) - 2:
            return None, None
        opcode = self.instructions[self.IP]
        operand = self.get_operand(self.instructions[self.IP + 1], combo=self.Opcode(opcode) in [self.Opcode.ADV, self.Opcode.BST, self.Opcode.OUT, self.Opcode.BDV, self.Opcode.CDV])
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
            decompilation.append(f"\tb = a % 8")
        # We don't have to decompile JNZ since it's a control flow instruction
        elif opcode == self.Opcode.BXC.value:
            decompilation.append(f"\tb = b ^ c")
        elif opcode == self.Opcode.OUT.value:
            decompilation.append(f"\toutputs.append(a % 8)")
        elif opcode == self.Opcode.BDV.value:
            decompilation.append(f"\td = 2 ** {operand}\n")
            decompilation.append(f"\tb = a // d")
        elif opcode == self.Opcode.CDV.value:
            decompilation.append(f"\td = 2 ** {operand}\n")
            decompilation.append(f"\tc = a // d")
        return decompilation
            
    
    def run(self):
        running = True
        decompilation = []
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        decompilation.append(f"''' Decompilation of Program {self.instructions} - DateTime: {current_time} '''")
        decompilation.append(f"def decompliation():\n")
        decompilation.append(f"\toutputs = [] \n")
        decompilation.append(f"\ta = {self.A}")
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
        for line in decompilation:
            print("".join(line))
        
        return self.std_io
    

    def adv_func(self, operand):
        old_val = self.A
        d = 2 ** operand
        self.A = self.A // d
        self.IP += 2

    def bxl_func(self, operand):
        old_val = self.B
        self.B = self.B ^ operand
        self.IP += 2

    def bst_func(self, operand):
        old_val = self.B
        self.B = operand % 8
        self.IP += 2

    def jnz_func(self, operand):
        if self.A != 0:
            old_val = self.IP
            self.IP = operand
        else:
            self.IP += 2

    def bxc_func(self, operand=None): # Operand is not used
        old_val = self.B
        self.B = self.B ^ self.C
        self.IP += 2

    def out_func(self, operand):
        if len(self.std_io) > 0:
            self.std_io += ","
        self.std_io += str(operand % 8)
        self.IP += 2

    def bdv_func(self, operand):
        old_val = self.B
        d = 2 ** operand
        self.B = self.A // d
        self.IP += 2

    def cdv_func(self, operand):
        old_val = self.C
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
    



cpu = Computer()
#cpu.load_state({"A": 0, "B": 0, "C": 9, "IP":0, "instructions":[2, 6]}).run()
#cpu.load_state({"A": 10, "B": 0, "C": 0, "IP":0, "instructions":[5,0,5,1,5,4]}).run()
#cpu.load_state({"A": 2024, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
#cpu.load_state({"A": 0, "B": 29, "C": 0, "IP":0, "instructions":[1,7]}).run()
#cpu.load_state({"A": 0, "B": 2024, "C": 43690, "IP":0, "instructions":[4,0]}).run()
#cpu.load_state({"A": 729, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
#cpu.load_state({"A": 130402909397776, "B": 0, "C": 0, "IP":0, "instructions":[2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]}).set_decompile_enabled(False).run()
#cpu.load_state({"A": ≈, "B": 0, "C": 0, "IP":0, "instructions":[0,3,5,4,3,0]}).set_decompile_enabled(False).run()
#cpu.load_state({"A": 729, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).set_decompile_enabled(True).run()


# Run the CPU, it will generate a new decompilation function
#std_io = cpu.load_state({"A": 729, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
std_io = cpu.load_state({"A": 27334280, "B": 0, "C": 0, "IP":0, "instructions":[2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]}).run()

# Replace the below function with the generated decompilation function

''' Decompilation of Program [2, 4, 1, 2, 7, 5, 0, 3, 1, 7, 4, 1, 5, 5, 3, 0] - DateTime: 2024-12-18 18:47:52 '''
def decompliation():

        outputs = [] 

        a = 27334280
        d = 0

        b = a % 8
        b = b ^ 2
        d = 2 ** 2
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 3
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 0
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 1
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 3
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 0
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 2
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 7
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        b = a % 8
        b = b ^ 2
        d = 2 ** 3
        c = a // d
        d = 2 ** 3
        a = a // d
        b = b ^ 7
        b = b ^ c
        outputs.append(a % 8)

        return outputs


#print(reconstruct_a_from_outputs(outputs))
print("std_io: ", std_io)
outputs = decompliation()
print("decomp: ",outputs)


