import sys
import os
import subprocess
from config import *

def load_files(input_path):
    input_files = []
    for dirname, dirnames, filenames in os.walk(input_path):
        for file in filenames:
            filename, file_extension = os.path.splitext(file)
            input_files.append(os.path.join(dirname, file))
    return input_files

if __name__ == "__main__":
    input_files = load_files(INPUT_PATH)
    for file in input_files:
        subprocess.call(["py", "Source/seoanalysis.py", file])
        print("\nPress enter continue...")
        input()