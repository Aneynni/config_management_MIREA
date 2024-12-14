import csv
import yaml
from sys import argv
from os.path import exists

class Assembler:
    def __init__(self, path_to_code, path_to_log):
        self.path_to_log = path_to_log
        self.logs = []
        self.commands = []
        try:
            with open(path_to_code, 'rt') as file:
                self.commands = file.readlines()
        except FileNotFoundError:
            print('Файл не найден')
        except:
            print('Ошибка работы с файлом')

    def assemble(self, path_to_bin):
        with open(path_to_bin, 'wb') as file:
            for command in self.commands:
                if command.strip().startswith('#'):
                    continue
                try:
                    name, body = command.split(' ', 1)
                except ValueError:
                    continue
                print(name)
                body = tuple(map(int, body.split()))
                print(body)
                number = None
                bits = None
                match name:
                    case 'LOAD_CONSTANT':
                        number = 195
                        bits = Assembler.load_constant(self, *body)
                    case 'READ':
                        number = 83
                        bits = Assembler.read_memory(self, *body)
                    case 'WRITE':
                        number = 53
                        bits = Assembler.write_memory(self, *body)
                    case 'OR':
                        number = 74
                        bits = Assembler.OR(self, *body)
                file.write(bits)
        self.make_log()

    def make_log(self):
        with open(path_to_log, 'w') as f:
            yaml.dump(self.logs, f)

    @staticmethod
    def load_constant(self, b, c):
        bits = (c << 35) | (b << 8) | 195
        (self.logs).append({'A': 195, 'B': b, 'C': c, 'bits': str(bits.to_bytes(12, byteorder='little'))})
        print(self.logs)
        return bits.to_bytes(12, byteorder='little', signed=True)

    @staticmethod
    def read_memory(self, b, c):
        bits = (c << 35) | (b << 8) | 83
        (self.logs).append({'A': 83, 'B': b, 'C': c, 'bits': str(bits.to_bytes(12, byteorder='little'))})
        #(self.logs).append({'A': 83, 'B': b, 'C': c})
        return bits.to_bytes(12, byteorder='little', signed=True)

    @staticmethod
    def write_memory(self, b, c, d):
        bits = (d << 44) | (c << 35) | (b << 8) | 53
        (self.logs).append({'A': 53, 'B': b, 'C': c, 'D': d, 'bits': str(bits.to_bytes(12, byteorder='little'))})
        #self.logs.append({'A': 53, 'B': b, 'C': c, 'D': d})
        return bits.to_bytes(12, byteorder='little', signed=True)

    @staticmethod
    def OR(self, b, c, d):
        bits = (d << 62) | (c << 35) | (b << 8) | 74
        (self.logs).append({'A': 74, 'B': b, 'C': c, 'D': d, 'bits': str(bits.to_bytes(12, byteorder='little'))})
        #self.logs.append({'A': 74, 'B': b, 'C': c, 'D': d})
        return bits.to_bytes(12, byteorder='little', signed=True)
if __name__ == '__main__':
    path_to_code = argv[1]
    path_to_bin = argv[2]
    path_to_log = argv[3]

    if not exists(path_to_code):
        print('Файла с таким именем не существует')

    my_assembler = Assembler(path_to_code, path_to_log)
    my_assembler.assemble(path_to_bin)
