"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8  load 'immediate'; next value is the register number, subsequent number is the value to add to that register
        #     0b00000000, # register number
        #     0b00001000, # value to store in register
        #     0b01000111, # PRN R0 print value from register
        #     0b00000000, # register number
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        try:
            with open(filename) as f:
                for line in f:
                    split_line = line.split('#')

                    code_value = split_line[0].strip()
                    if code_value == '':
                        continue
                    
                    num = int(code_value, 2)
                    self.ram[address] = num
                    address += 1

        except FileNotFoundError:
            print(f'{sys.argv[1]} file not found')
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # MAR = memory address register, contains the address that is being read or written to
    # MDR = memory data register, contains the data that was read or the data to write

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        return self.ram[mar]

    def ldi(self, mar, mdr):
        self.reg[mar] = mdr

    def prn(self, mar):
        print(self.reg[mar])

    def mul(self, a1, a2):
        self.alu('MUL', a1, a2)

    def run(self):
        """Run the CPU."""
        running = True
        HLT = 0b00000001


        while running:
            ir = self.ram_read(self.pc)

            if ir == 162:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.mul(operand_a, operand_b)
                self.pc += 3

            elif ir == 130:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.ldi(operand_a, operand_b)
                self.pc += 3

            elif ir == 71:
                operand_a = self.ram_read(self.pc + 1)
                self.prn(operand_a)
                self.pc += 2

            elif ir == HLT:
                running = False
                self.pc += 1

            else:
                print(f'unknown')
                

