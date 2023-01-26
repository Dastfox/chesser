from controllers.menu_controller import MainMenu
from utils import clear_console, set_debug


def main():
    clear_console()
    input_ = input(
        "Bienvenue dans Chesser ! Appuyez sur Entrée pour continuer..."
    )
    set_debug(input_)
    main_menu = MainMenu()
    main_menu.select(input("Entrez votre réponse : "))


if __name__ == "__main__":
    main()
