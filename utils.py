import os
import platform

debug = False


def yes_or_no(question: str) -> bool:
    """Ask a yes or no question.
    Args:
        question (str): The yes or no question to be asked.
    Returns:
        bool: True if the answer is "yes"
        or if the user press enter, False if the answer is "no".
    """
    answer = input(question + " ([O]/n): ").lower().strip()
    print("")
    while not (
        answer == "o"
        or answer == "oui"
        or answer == "n"
        or answer == "non"
        or answer == ""
    ):
        print("Entrez oui ou non ou appuyez sur entrée")
        answer = input(question + "([O]/n):").lower().strip()
        print("")
    if answer == "":
        return True
    elif answer[0] == "o":
        return True
    else:
        return False


def clear_console():
    global debug
    if debug:
        return
    else:
        system = platform.system()
        if system == "Windows":
            os.system("cls")
        elif system == "Linux" or system == "Darwin":
            os.system("clear")


def set_debug(input: str):
    global debug
    if input == "debug":
        debug = True
