from config import get_database_path
from models.database import Database
from services.stock_service import StockService
import os
import platform

is_on_windows = platform.system() == "Windows"
width_columns = [10, 30, 30]
columns_names = ["ID", "Product", "Quantity"]

MENU_OPTIONS = (
    "1 - View stock",
    "2 - Create a product",
    "3 - Add to stock",
    "4 - Remove from stock",
    "5 - Exit",
)


def clear_screen(is_on_windows):
    if is_on_windows:
        os.system("cls")
    else:
        os.system("clear")


def display_menu():
    clear_screen(is_on_windows)
    print("\n=== Mini ERP - Stock Management ===")
    for option in MENU_OPTIONS:
        print(option)


def show_stock(service):
    products = service.list_stock()

    result = ""

    for col_index in range(len(columns_names)):
        result += columns_names[col_index] + "-" * (width_columns[col_index] - len(columns_names[col_index])) + "|"

    result += "\n"

    for product in products:
        result += (f"{product.id}{ " " * (width_columns[0] - len(str(product.id)))}|"
                   f"{product.name}{" " * (width_columns[1] - len(str(product.name)))}|"
                   f"{product.quantity}{" " * (width_columns[2] - len(str(product.quantity)))}|"
                   f"\n")

    for current_col_width in width_columns:
        result += "-" * current_col_width + "|"

    print(result)


def wait_for_user_exit():
    input("Continue ")


def ask_product_name():
    this_input = input("Product name: ")

    if len(this_input.strip()) == 0:
        print("Cannot be empty")
        return ask_product_name()

    return this_input


def ask_integer(input_string):
    this_input = input(input_string)

    if this_input.strip().isdigit():
        return int(this_input)

    print("Cannot be converted to integer")
    return ask_integer(input_string)


def ask_product_id():
    return ask_integer("Product ID : ")


def create_product(service):
    name = ask_product_name()
    quantity = ask_integer("Initial Quantity : ")
    product_creation_output = service.create_product(name, quantity)
    if product_creation_output["success"]:
        product = product_creation_output["product"]
        print(
            f"Product created: {product.name} (ID {product.id}, stock {product.quantity})."
        )
    else:
        print(f"Error : {product_creation_output['error']}")


def add_stock(service):
    product_id = ask_product_id()
    quantity = ask_integer("Quantity to add: ")
    stock_addition_output = service.add_to_stock(product_id, quantity)
    if stock_addition_output["success"]:
        product = stock_addition_output["product"]
        print(f"Stock updated: {product.name} now has {product.quantity} unit(s).")
    else:
        print(f"Error : {stock_addition_output['error']}")


def remove_stock(service):
    product_id = ask_product_id()
    quantity = ask_integer("Quantity to remove: ")
    stock_removal_output = service.remove_from_stock(product_id, quantity)
    if stock_removal_output["success"]:
        product = stock_removal_output["product"]
        print(f"Stock updated: {product.name} now has {product.quantity} unit(s).")
    else:
        print(f"Error : {stock_removal_output['error']}")


def run_cli():
    while True:
        service = StockService(Database(get_database_path()))
        display_menu()
        choice = input("Your choice: ").strip()

        if choice == "1":
            show_stock(service)
        elif choice == "2":
            create_product(service)
        elif choice == "3":
            add_stock(service)
        elif choice == "4":
            remove_stock(service)
        elif choice == "5":
            print("Goodbye")
            break
        wait_for_user_exit()



run_cli()
