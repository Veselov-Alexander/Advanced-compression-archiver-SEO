import subprocess
from config import *

if __name__ == "__main__":
    subprocess.call(["py", "Source/archiver.py", "a", ARCHIVE_INPUT_DIRECTORY, ARCHIVE_FILE])
    print("Archived.")
    subprocess.call(["py", "Source/archiver.py", "e", ARCHIVE_FILE, ARCHIVE_EXTRACT_DIRECTORY])
    print("Extracted.")
    subprocess.call(["py", "Utilities/checker.py", ARCHIVE_INPUT_DIRECTORY, ARCHIVE_EXTRACT_DIRECTORY])
    
    print("\nPress enter continue...")
    input()