from controllers.menu_controller import MainMenu


def main():
    main_menu = MainMenu()
    main_menu.select(input("Entrez votre réponse : "))


if __name__ == "__main__":
    main()

