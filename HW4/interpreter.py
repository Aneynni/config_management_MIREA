import csv
from sys import argv
from os.path import exists
import yaml

class Interpreter:
    def __init__(self, path_to_bin, limit):
        self.registers = [0] * limit
        self.code = 0
        self.logs = []
        try:
            with open(path_to_bin, 'rb') as file:
                self.code = int.from_bytes(file.read(), byteorder='little', signed=True)
        except FileNotFoundError:
            print('Файл не найден')

    def interpret(self):
        while self.code != 0:
            a = self.code & ((1 << 8) - 1)
            match a:
                case 195:
                    self.load_constant()
                case 83:
                    self.read_memory()
                case 53:
                    self.write_memory()
                case 74:
                    self.OR()
                case _:
                    self.code >>= 1
        self.dump_result()

    def dump_result(self):
        with open('result.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(('Регистр', 'Значение'))
            for ind, val in enumerate(self.registers):
                if val > 2 ** 18 - 1:
                    val ^= (1 << 19) - 1
                    val = -val - 1
                writer.writerow((f'R{ind}', val))
        with open('result.yaml', 'w') as f:
            yaml.dump(self.logs, f)

    def load_constant(self):
        b = (self.code & ((1 << 35) - 1)) >> 8
        c = (self.code & ((1 << 60) - 1)) >> 35
        self.code >>= 60

        self.registers[b] = c

    def read_memory(self):
        b = (self.code & ((1 << 35) - 1)) >> 8
        c = (self.code & ((1 << 61) - 1)) >> 35
        self.code >>= 61

        self.registers[b] = self.registers[self.registers[c]]

    def write_memory(self):
        b = (self.code & ((1 << 35) - 1)) >> 8
        c = (self.code & ((1 << 44) - 1)) >> 35
        d = (self.code & ((1 << 70) - 1)) >> 44
        self.code >>= 70

        self.registers[b+c] = self.registers[d]

    def OR(self):
        b = (self.code & ((1 << 35) - 1)) >> 8
        c = (self.code & ((1 << 62) - 1)) >> 35
        d = (self.code & ((1 << 69) - 1)) >> 62
        self.code >>= 88
        val1 = self.registers[c]
        val2 = self.registers[d]
        val = val1 | val2
        self.registers[b] = val1 | val2
        (self.logs).append({"num": val1, "value from vector": val2, "result OR": val})
        #if val > 2 ** 18 - 1:
         #   val ^= (1 << 19) - 1
          #  val += 1
        #self.registers[c] = val

def interpret():
    if len(argv) < 3:
        print('Введены не все аргументы для корректной работы ассемблера')
        return

    path_to_bin = argv[1]
    limitation = argv[2]

    if not exists(path_to_bin):
        print('Файла с таким именем не существует')
        return

    try:
        limitation = int(limitation)
    except ValueError:
        print('Ограничение должно быть задано целым числом')
        return

    my_interpreter = Interpreter(path_to_bin, limitation)
    my_interpreter.interpret()


if __name__ == '__main__':
    interpret()
