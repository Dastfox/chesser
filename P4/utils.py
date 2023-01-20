import os
import platform


def clear_console():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux" or system == "Darwin":
        os.system("clear")

def yes_or_no(question):
    """Ask a yes or no question.

    Args:
        question (str): The yes or no question to be asked.

    Returns:
        bool: True if the answer is "yes", False if the answer is "no".

    Raises:
        ValueError: If the answer is not "yes" or "no".
    """
    answer = input(question + "(O/n): ").lower().strip()
    print("")
    while not (answer == "o" or answer == "oui" or answer == "n" or answer == "non"):
        print("Entrez oui ou non")
        answer = input(question + "(O/n):").lower().strip()
        print("")
    if answer[0] == "o":
        return True
    else:
        return False