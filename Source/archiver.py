import os
import sys
import subprocess

NEWFILE_SEPARATOR = "__newfile__"
COMPRESSED_EXTENSION = ".compressed"
DECOMPRESSED_EXTENSION = ".decompressed"

def append_archive(dir_path, dirname, filename, archive_file):
    full_dir = os.path.join(dirname, filename)
    with open(full_dir, "r") as file:
        archive_file.write(NEWFILE_SEPARATOR + "\n")
        archive_file.write(full_dir[len(dir_path) + 1:] + "\n")
        for line in file:
            archive_file.write(line)
        archive_file.write("\n")


def archive(dir_path, archive_path):
    with open(archive_path, "w") as archive_file:
        for dirname, dirnames, filenames in os.walk(dir_path):
            for file in filenames:
                filename, file_extension = os.path.splitext(file)
                append_archive(dir_path, dirname, file, archive_file)
    arithmetic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arithmetic.py")
    subprocess.call(["py", arithmetic_path, "c", archive_path, archive_path + COMPRESSED_EXTENSION])


def extract(archive_path, extract_path):
    arithmetic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "arithmetic.py")
    subprocess.call(["py", arithmetic_path, "d", archive_path + COMPRESSED_EXTENSION, archive_path + DECOMPRESSED_EXTENSION])
    archive = ""
    with open(archive_path + DECOMPRESSED_EXTENSION, "r") as archive_file:
        for line in archive_file:
            archive += line
    files = archive.split(NEWFILE_SEPARATOR)[1:]
    for file in files:
        path = file.split("\n")[1]
        data = file[len(path) + 2:-1]
        path = os.path.join(extract_path, path)
        dir = os.path.split(path)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, "w") as extract_file:
            extract_file.write(data)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong parameters!")
        print("Example: py archiver.py a Folder/Subfolder archivefilename")
        print("Example: py archiver.py e archivefilename Folder/Extractdir")
    else:
        if sys.argv[1] == "a":
            archive(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == "e":
            extract(sys.argv[2], sys.argv[3])
        else:
            print("First parameter should be \'a\' or \'e\'")