from model.product_model import ProductModel
from model.file_handler import FileHandler

class AdminController:
    def __init__(self, view):
        self.view = view
        self.model = ProductModel()

    def add_product(self, name, category, price, stock):
        self.model.add_product(name, category, price, stock)
        self.view.show_message("Product added!")

    def get_all_products(self):
        return self.model.get_all_products()

    def delete_product(self, name):
        self.model.delete_product(name)
        self.view.show_message("Product deleted!")

    def update_product(self, name, category, price, stock):
        self.model.update_product(name, category, price, stock)
        self.view.show_message("Product updated!")

    def add_cashier(self, username, password):
        FileHandler.append_to_file("data/cashiers.txt", f"{username},{password}")
        self.view.show_message("Cashier added!")

    def get_all_cashiers(self):
        return FileHandler.read_lines("data/cashiers.txt")

    def delete_cashier(self, username):
        lines = FileHandler.read_lines("data/cashiers.txt")
        with open("data/cashiers.txt", "w") as f:
            for line in lines:
                if not line.startswith(username + ","):
                    f.write(line)
        self.view.show_message("Cashier deleted!")