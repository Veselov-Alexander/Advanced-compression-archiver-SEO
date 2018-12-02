import math
import sys
import itertools

from filemanager import FileManager
from collections import Counter


def previous_value(dictionary, current_key):
    keys = list(dictionary.keys())
    index = keys.index(current_key) - 1
    return keys[index]


class Arithmetic:
    def __init__(self, bits=16):
        self.bits = bits
        self.max_range = (2 ** bits) - 1
        self.first_quarter = self.max_range // 4 + 1
        self.second_quarter = 2 * self.first_quarter
        self.third_quarter = 3 * self.first_quarter

        self.EOF_symbol = "__EOF__"
        self.break_symbol = "\0"
        self.separator = "__separator__"

    def build_intervals(self, string):
        letters = Counter()
        letters[self.EOF_symbol] = 0
        for line in string:
            for word in line:
                for letter in word:
                    letters[letter] += 1
        letters = dict(letters)
        for i in range(len(letters) - 1):
            current_key = list(letters.items())[i + 1][0]
            prev_key = list(letters.items())[i][0]
            letters[current_key] += letters[prev_key]
        return letters

    def write_bits(self, bit, bits_to_delete):
        bits = str(bit)
        while bits_to_delete > 0:
            bits += str(int(not bit))
            bits_to_delete -= 1
        return bits

    def encode(self, inputfile, outputfile=None):       
        string = FileManager.load_text(inputfile) + \
                 self.break_symbol * (self.bits // 8)

        table = self.build_intervals(string)
        encoded = self._encode(string, table)

        if outputfile:
            data = FileManager.merge_data(table, self.separator, encoded)
            FileManager.export(data, outputfile, "wb")
        
        return encoded

    def decode(self, inputfile, outputfile=None):
        byte_array = FileManager.load_bytes(inputfile)
        
        freq, code = FileManager.parse_bytes(byte_array, self.separator)
        decoded = self._decode(code, freq)

        if outputfile:
            FileManager.export(decoded, outputfile, "w")

        return decoded

    def _encode(self, string, freq):
        length = len(string) + 1
        low = [0] * length
        high = [0] * length

        low[0] = 0
        high[0] = self.max_range

        delta = freq[list(freq.items())[-1][0]]
        bits_to_delete = 0
        code = ""

        for i in range(1, length):
            current_symbol = string[i - 1]
            prev_symbol = previous_value(freq, current_symbol)

            current_range = high[i - 1] - low[i - 1] + 1
            low[i] = low[i - 1] + (current_range * freq[prev_symbol]) // delta
            high[i] = low[i - 1] + (current_range * freq[current_symbol]) // delta - 1

            while True:
                if high[i] < self.second_quarter:
                    code += self.write_bits(0, bits_to_delete)
                    bits_to_delete = 0
                elif low[i] >= self.second_quarter:
                    code += self.write_bits(1, bits_to_delete)
                    bits_to_delete = 0
                    low[i] -= self.second_quarter
                    high[i] -= self.second_quarter
                elif low[i] >= self.first_quarter and high[i] < self.third_quarter:
                    bits_to_delete += 1
                    low[i] -= self.first_quarter
                    high[i] -= self.first_quarter
                else:
                    break

                low[i] = low[i] * 2
                high[i] = high[i] * 2 + 1

        return code

    def _decode(self, code, freq):
        decoded = ""
        low = [0]
        high = [0]

        low[0] = 0
        high[0] = self.max_range

        sum = 0
        delta = freq[list(freq.items())[-1][0]]

        value = 0
        for i in range(self.bits):
            value <<= 1
            value |= int(code[i])

        count = self.bits

        process = False

        for i in itertools.count(1):
            current_range = high[i - 1] - low[i - 1] + 1
            sum = (((value - low[i - 1]) + 1) * delta - 1) // current_range
            current_symbol = -1
            for char in freq:
                if freq[char] > sum:
                    current_symbol = char
                    break
            if current_symbol == self.break_symbol:
                return decoded

            prev_symbol = previous_value(freq, current_symbol)

            low.append([None])
            high.append([None])

            low[i] = low[i - 1] + (current_range * freq[prev_symbol]) // delta
            high[i] = low[i - 1] + (current_range * freq[current_symbol]) // delta - 1

            decoded += current_symbol

            while True:
                if high[i] >= self.second_quarter:
                    if low[i] >= self.second_quarter:
                        value -= self.second_quarter
                        low[i] -= self.second_quarter
                        high[i] -= self.second_quarter
                    elif low[i] >= self.first_quarter and high[i] < self.third_quarter:
                        value -= self.first_quarter
                        low[i] -= self.first_quarter
                        high[i] -= self.first_quarter
                    else:
                        break

                low[i] = low[i] * 2
                high[i] = high[i] * 2 + 1
                value = 2 * value

                if process:
                    value = value & (~1)
                elif count >= len(code):
                    value = value | 1
                    process = True
                elif code[count] == "1":
                    value = value | 1
                elif code[count] == "0":
                    value = value & (~1)

                count += 1

def test_module():
    from config import config

    INPUT_PATH = config["InputPath"]

    INPUT_FILES = [None] * 3

    INPUT_FILES[0] = INPUT_PATH + "/" + "Ershow_Konyok-gorbunok.txt"    # 82 kb
    INPUT_FILES[1] = INPUT_PATH + "/" + "Chehow_Tolstiy i tonkiy.txt"   # 4 kb
    INPUT_FILES[2] = INPUT_PATH + "/" +"Pushkin_Evgeniy Onegin.txt"     # 148 kb

    OUTPUT_FILE = "output.txt"
    EXTRACT_FILE = "extract.txt"

    arithmetic = Arithmetic(32)

    INPUT_FILE = INPUT_FILES[2]
    
    encoded = arithmetic.encode(INPUT_FILE, OUTPUT_FILE)
    decoded = arithmetic.decode(OUTPUT_FILE, EXTRACT_FILE)

    text = FileManager.load_text(INPUT_FILE)

    initial_length = len(text)
    compressed_length = round(len(encoded) / 8)
    percent = compressed_length / initial_length

    print(encoded, "\n")
    print(decoded, "\n")
    print("Compressed is equal: {}".format(text == decoded))
    print("Compress percent: {:f}%".format((1 - percent) * 100))

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong parameters!")
        print("Example: py arithmetic.py c input.txt output.txt")
    else:
        arithmetic = Arithmetic(32)
        if sys.argv[1] == "c":
            arithmetic.encode(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "d":
            arithmetic.decode(sys.argv[2], sys.argv[3])
        else:
            print("First parameter should be \'c\' or \'d\'")