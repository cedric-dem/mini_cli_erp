MENU_OPTIONS = (
    "1 - View stock",
    "2 - Create a product",
    "3 - Add to stock",
    "4 - Remove from stock",
    "5 - Exit",
)


def display_menu():
    print("\n=== Mini ERP - Stock Management ===")
    for option in MENU_OPTIONS:
        print(option)


def show_stock():
    # TODO
    return None


def create_product():
    # TODO
    return None


def add_stock():
    # TODO
    return None


def remove_stock():
    # TODO
    return None


def run_cli():
    while True:
        display_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            show_stock()
        elif choice == "2":
            create_product()
        elif choice == "3":
            add_stock()
        elif choice == "4":
            remove_stock()
        elif choice == "5":
            print("Goodbye")
            break


run_cli()
