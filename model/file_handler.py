import os
import sys

def get_base_path():
    if getattr(sys, 'frozen', False):  # .exe run
        return sys._MEIPASS
    return os.path.abspath(".")
class FileHandler:

    @staticmethod
    def read_lines(filename):
        full_path = os.path.join(get_base_path(), filename)
        try:
            with open(full_path, 'r') as f:
                return f.readlines()
        except FileNotFoundError:
            print(f"[ERROR] File not found: {full_path}")
            return []

    @staticmethod
    def append_to_file(filename, line):
        full_path = os.path.join(get_base_path(), filename)
        with open(full_path, 'a') as f:
            f.write(f"{line}\n")

    @staticmethod
    def write_file(filename, content):
        full_path = os.path.join(get_base_path(), filename)
        with open(full_path, 'w') as f:
            f.write(content)
