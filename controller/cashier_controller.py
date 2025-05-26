from model.product_model import ProductModel
from model.file_handler import FileHandler

class CashierController:
    def __init__(self, view):
        self.view = view
        self.model = ProductModel()

    def find_product(self, name):
        return self.model.find_price(name)

    def record_bill(self, total):
        existing = FileHandler.read_lines('data/bills.txt')
        FileHandler.append_to_file('data/bills.txt', f"Bill {len(existing)+1}: {total}")

    def get_categories(self):
        return sorted(set(self.model.get_all_categories()))

    def get_products_by_category(self):
        category_map = {}
        for line in self.model.get_all_products():
            if len(line) >= 4:
                name, category = line[0], line[1]
                if category not in category_map:
                    category_map[category] = []
                category_map[category].append(name)
        return category_map