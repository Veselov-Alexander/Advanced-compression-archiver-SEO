import sys
import os
import filecmp
import colored

def load_files(input_path):
    input_files = []
    for dirname, dirnames, filenames in os.walk(input_path):
        for file in filenames:
            input_files.append(os.path.join(dirname, file)[len(input_path) + 1:])
    return input_files

def compare_files(input_path, output_path):
    input_files = load_files(input_path)
    for file in input_files:
        file_input_path = os.path.join(input_path, file)
        file_output_path = os.path.join(output_path, file)
        try:
            are_equal = filecmp.cmp(file_input_path, file_output_path)
            print(file, end=" - ")
            if are_equal:
                colored.print_green("OK")
            else:
                colored.print_red("ERROR")
        except FileNotFoundError:
            colored.print_red("No file to compare: " + file)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong parameters!")
        print("Example: py checker.py InputFolder OutputFolder")
    else:
        compare_files(sys.argv[1], sys.argv[2])
