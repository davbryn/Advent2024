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
    


    def __init__(self):
        # Registers
        self.A = 0
        self.B = 0
        self.C = 0
        self.IP = 0
        self.instructions = []

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
    
    def run(self):
        running = True
        output = ""
        while running:
            did_jump = False
            opcode, operand = self.fetch()
            if opcode != None:
                opcode = self.Opcode(opcode)
                print(f"Opcode: {opcode.name}, Operand: {operand}")
            if opcode == None:
                print("Halt")
                running = False
            if opcode == self.Opcode.ADV:
                d = 2 ** operand
                self.A = self.A // d
            elif opcode == self.Opcode.BXL:
                self.B = self.B ^ operand
            elif opcode == self.Opcode.BST:
                self.B = operand % 8
            elif opcode == self.Opcode.JNZ:
                if self.A != 0:
                    self.IP = operand
                    did_jump = True
            elif opcode == self.Opcode.BXC:
                self.B = self.B ^ self.C
            elif opcode == self.Opcode.OUT:
                output += str(operand % 8)
                print(output)
                if len(output) > 0:
                    output += ","
            elif opcode == self.Opcode.BDV:
                d = 2 ** operand
                self.B = self.A // d
            elif opcode == self.Opcode.CDV:
                d = 2 ** operand
                self.C = self.A // d
            else:
                print("Unknown opcode")
                running = False
            if not did_jump:
                self.IP += 2
        cpu.dump_state()
    
    def load_state(self, state):
        self.A = state["A"]
        self.B = state["B"]
        self.C = state["C"]
        self.IP = state["IP"]
        self.instructions = state["instructions"]
        return self

    def dump_state(self):
        print(f"Register: A={self.A}\nRegister B={self.B}\nRegister C={self.C}\nP={self.IP}")
    


cpu = Computer()
#cpu.load_state({"A": 0, "B": 0, "C": 9, "IP":0, "instructions":[2, 6]}).run()
#cpu.load_state({"A": 10, "B": 0, "C": 0, "IP":0, "instructions":[5,0,5,1,5,4]}).run()
#cpu.load_state({"A": 2024, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
#cpu.load_state({"A": 0, "B": 29, "C": 0, "IP":0, "instructions":[1,7]}).run()
#cpu.load_state({"A": 0, "B": 2024, "C": 43690, "IP":0, "instructions":[4,0]}).run()
#cpu.load_state({"A": 729, "B": 0, "C": 0, "IP":0, "instructions":[0,1,5,4,3,0]}).run()
cpu.load_state({"A": 27334280, "B": 0, "C": 0, "IP":0, "instructions":[2,4,1,2,7,5,0,3,1,7,4,1,5,5,3,0]}).run()

