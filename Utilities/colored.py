import ctypes
import struct

class Colored:
    @staticmethod
    def initialize():
        Colored.STD_OUTPUT_HANDLE = -11
        Colored.RED = 0xC
        Colored.GREEN = 0xA

        Colored.handle = ctypes.windll.kernel32.GetStdHandle(Colored.STD_OUTPUT_HANDLE)
        Colored.reset = Colored.get_csbi_attributes(Colored.handle)

    @staticmethod
    def get_csbi_attributes(handle):
        csbi = ctypes.create_string_buffer(22)
        res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
        assert res

        (bufx, bufy, curx, cury, wattr,
        left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        return wattr

    @staticmethod
    def print(text, color):
        ctypes.windll.kernel32.SetConsoleTextAttribute(Colored.handle, color)
        print(text)
        ctypes.windll.kernel32.SetConsoleTextAttribute(Colored.handle, Colored.reset)

Colored.initialize()

def print_red(text):
    Colored.print(text, Colored.RED)

def print_green(text):
    Colored.print(text, Colored.GREEN)