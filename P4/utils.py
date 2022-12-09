import os
import platform


def clear_console():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux" or system == "Darwin":
        os.system("clear")
