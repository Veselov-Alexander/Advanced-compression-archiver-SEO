import shutil
import os
from config import *

def clear():
    ARCHIVE_PATH = os.path.split(ARCHIVE_FILE)[0]

    if os.path.exists(DECOMPRESS_PATH):
        shutil.rmtree(DECOMPRESS_PATH)
    if os.path.exists(COMPRESS_PATH):
        shutil.rmtree(COMPRESS_PATH)
    if os.path.exists(ARCHIVE_EXTRACT_DIRECTORY):
        shutil.rmtree(ARCHIVE_EXTRACT_DIRECTORY)
    if os.path.exists(ARCHIVE_PATH):
        shutil.rmtree(ARCHIVE_PATH)

    os.makedirs(DECOMPRESS_PATH)
    os.makedirs(COMPRESS_PATH)
    os.makedirs(ARCHIVE_EXTRACT_DIRECTORY)
    os.makedirs(ARCHIVE_PATH)

if __name__ == "__main__":
    clear()