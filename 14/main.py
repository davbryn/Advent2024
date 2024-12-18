from enum import Enum

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
        operand = self.get_operand(self.instructions[self.IP + 1], combo=opcode in [0,2,5,6,7])
        return opcode, operand
    
    def decode(self, instruction):
        for i in instruction:
            self.instructions.append(i)

    def decompile(self):
        decompiled = []
        decompiled.append(f"a = {self.A}")
        decompiled.append("done = False")
        decompiled.append("While !done:")
        for i in range(0, len(self.instructions), 2):
            opcode = self.instructions[i]
            operand = self.instructions[i + 1]
            if opcode == self.Opcode.ADV.value:
                decompiled.append(f"\td = 2 ^ {operand}")
                decompiled.append(f"\ta = a // d")
            elif opcode == self.Opcode.BXL.value:
                decompiled.append(f"\tb = b xor {operand}")
            elif opcode == self.Opcode.BST.value:
                decompiled.append(f"\tb = b % {operand}")
            elif opcode == self.Opcode.JNZ.value:
                decompiled.append(f"\tif a != 0:")
                decompiled.append(f"\t\tGOTO {operand}")
            elif opcode == self.Opcode.BXC.value:
                decompiled.append(f"\tb = b xor c")
            elif opcode == self.Opcode.OUT.value:
                decompiled.append(f"\tprint({operand} % 8)")
            elif opcode == self.Opcode.BDV.value:
                decompiled.append(f"\td = 2 ^ {operand}")
                decompiled.append(f"\tb = a // {operand}")
            elif opcode == self.Opcode.CDV.value:
                decompiled.append(f"\td = 2 ^ {operand}")
                decompiled.append(f"\tc = a // {operand}")
        return decompiled
    
    def run_vtable(self):
        running = True
        print(f"Program: {self.instructions}")
        while running:
            opcode, operand = self.fetch()
            if opcode != None:
                opcode = self.Opcode(opcode)
                if self.debug_enabled:
                    print(f"Opcode: {opcode.name:<4} Operand: {operand:<3}")
            if opcode == None:
                running = False
            if opcode != None:
                self.call_fun(opcode.value, operand)

        
        print(f">> {self.std_io}")

    def run(self):
        running = True
        print(f"Program: {self.instructions}")
        while running:
            opcode, operand = self.fetch()
            if opcode != None:
                opcode = self.Opcode(opcode)
                if self.debug_enabled:
                    print(f"Opcode: {opcode.name:<4} Operand: {operand:<3}")
            if opcode == None:
                running = False
            if opcode == self.Opcode.ADV:
                self.adv_func(operand)
            elif opcode == self.Opcode.BXL:
                self.bxl_func(operand)
            elif opcode == self.Opcode.BST:
                self.bst_func(operand)
            elif opcode == self.Opcode.JNZ:
                self.jnz_func(operand)
            elif opcode == self.Opcode.BXC:
                self.bxc_func()
            elif opcode == self.Opcode.OUT:
                self.out_func(operand)
            elif opcode == self.Opcode.BDV:
                self.bdv_func(operand)
            elif opcode == self.Opcode.CDV:
                self.cdv_func(operand)
            else:
                if opcode != None:
                    print(f"Unknown opcode: {opcode.name:<4} :: {self.dump_state()}")
                running = False

        
        print(f">> {self.std_io}")

    def adv_func(self, operand):
        old_val = self.A
        d = 2 ** operand
        self.A = self.A // d
        if self.decompile_enabled:
            print(f"A   ADV  {operand:<3}: {old_val:<10} -> {self.A:<10} :: {self.dump_state()}")
        self.IP += 2

    def bxl_func(self, operand):
        old_val = self.B
        self.B = self.B ^ operand
        if self.decompile_enabled:
            print(f"B   BXL  {operand:<3}: {old_val:<10} -> {self.B:<10} :: {self.dump_state()}")
        self.IP += 2

    def bst_func(self, operand):
        old_val = self.B
        self.B = operand % 8
        if self.decompile_enabled:
            print(f"B   BST  {operand:<3}: {old_val:<10} -> {self.B:<10} :: {self.dump_state()}")
        self.IP += 2

    def jnz_func(self, operand):
        if self.A != 0:
            old_val = self.IP
            self.IP = operand
            if self.decompile_enabled:
                print(f"IP  JNZ  {operand:<3}: {old_val:<10} -> {self.IP:<10} :: {self.dump_state()}")
        else:
            self.IP += 2

    def bxc_func(self, operand=None): # Operand is not used
        old_val = self.B
        self.B = self.B ^ self.C
        if self.decompile_enabled:
            print(f"B   BXC  {self.C:<3}: {old_val:<10} -> {self.B:<10} :: {self.dump_state()}")
        self.IP += 2

    def out_func(self, operand):
        if len(self.std_io) > 0:
            self.std_io += ","
        self.std_io += str(operand % 8)
        if self.decompile_enabled:
            print(f"\t\t\t\t\t\t\t\t\t\t\t\t\t\tOUT {operand:<3}: -> {str(operand % 8):<10}")
        self.IP += 2

    def bdv_func(self, operand):
        old_val = self.B
        d = 2 ** operand
        self.B = self.A // d
        if self.decompile_enabled:
            print(f"B   BDV  {operand:<3}: {old_val:<10} -> {self.B:<10} :: {self.dump_state()}")
        self.IP += 2

    def cdv_func(self, operand):
        old_val = self.C
        d = 2 ** operand
        self.C = self.A // d
        if self.decompile_enabled:
            print(f"C   CDV  {operand:<3}: {old_val:<10} -> {self.C:<10} :: {self.dump_state()}")
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
    
def div_func(numerator, denominator):
    out = numerator // denominator % 8
    print(out)


cpu = Computer()
#cpu.load_state({"A": 0, "B": 0, "C": 9, "IP":0, "instructions":[2, 6]}).run()
#cpu.load_state({"A": 10, "B": 0, "C": 0, "IP":0, "instructions":[5,0,5,1,5,4]}).run()
#cpu.load_state({"A": 2024, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
#cpu.load_state({"A": 0, "B": 29, "C": 0, "IP":0, "instructions":[1,7]}).run()
#cpu.load_state({"A": 0, "B": 2024, "C": 43690, "IP":0, "instructions":[4,0]}).run()
#cpu.load_state({"A": 729, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
cpu.load_state({"A": 27334280, "B": 0, "C": 0, "IP":0, "instructions":[2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]}).set_decompile_enabled(True).run()
cpu.load_state({"A": 27334280, "B": 0, "C": 0, "IP":0, "instructions":[2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]}).set_decompile_enabled(True).run_vtable()

decompilation = cpu.load_state({"A": 117440, "B": 0, "C": 0, "IP":0, "instructions":[0,3,5,4,3,0]}).decompile()#set_decompile_enabled(True).run()
for line in decompilation:
    print(line)


v_table = []

def div_func(numerator, denominator):
    out = numerator // denominator % 8
    print(out)

v_table.append(div_func)

