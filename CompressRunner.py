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

def compress(file):
    filename = file.split("\\")[-1]
    subprocess.call(["py", "Source/arithmetic.py", "c", file, os.path.join(COMPRESS_PATH, filename)])
    print("{} is compressed".format(filename))

def decompress(file):
    filename = file.split("\\")[-1]
    subprocess.call(["py", "Source/arithmetic.py", "d", file, os.path.join(DECOMPRESS_PATH, filename)])
    print("{} is decompressed".format(filename))

def compress_files(input_files):
    for file in input_files:
        compress(file)
    print()

def decompress_files(compressed_files):
    for file in compressed_files:
        decompress(file)
    print()

if __name__ == "__main__":
    subprocess.call(["py", "clear.py"])
	
    input_files = load_files(INPUT_PATH)
    compress_files(input_files)

    compressed_files = load_files(COMPRESS_PATH)
    decompress_files(compressed_files)
    
    subprocess.call(["py", "Utilities/checker.py", INPUT_PATH, DECOMPRESS_PATH])

    print("\nPress enter continue...")
    input()