import zlib

class FileManager:
    @staticmethod
    def load_text(filename):
        string = ""
        with open(filename) as file:
            for line in file:
                string += line
        return string

    @staticmethod
    def load_bytes(filename):
        byte_array = []
        with open(filename, "rb") as file:
            for line in file:
                byte_array += line
        return byte_array

    @staticmethod
    def byte_string_to_bytes(byte_string):
        byte = 8
        bytes_array = []
        for i in range(len(byte_string) // byte):
            number = byte_string[i * byte : (i + 1) * byte]
            bytes_array.append(int(number, 2))
        return bytes(bytes_array)

    @staticmethod
    def byte_array_to_string(byte_array):
        code = ""
        for byte in byte_array:
            code += "{:08b}".format(byte)
        return code

    @staticmethod
    def encode_table(data):
        return zlib.compress(str.encode(str(data)))

    @staticmethod
    def decode_table(data):
        return zlib.decompress(bytes(data))

    @staticmethod
    def export(data, outputfile, mode):
        with open(outputfile, mode) as file:
            file.write(data)

    @staticmethod
    def parse_bytes(byte_array, separator):
        separator = list(separator.encode())
        split_index = FileManager._find_sublist(byte_array, separator)
        freq = eval(FileManager.decode_table(byte_array[:split_index]).decode())
        code = FileManager.byte_array_to_string((byte_array[split_index + len(separator):]))
        return freq, code

    @staticmethod
    def merge_data(table, separator, byte_string):
        data = FileManager.encode_table(table) + \
               bytes(separator.encode()) + \
               FileManager.byte_string_to_bytes(byte_string)
        return data

    @staticmethod
    def _find_sublist(input_list, sublist):
        size = len(sublist)
        for i in range(len(input_list) - size):
            if input_list[i : i + size] == sublist:
                return i
        return -1