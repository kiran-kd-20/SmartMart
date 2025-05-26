class ProductModel:
    def __init__(self, filepath='data/products.txt'):
        self.filepath = filepath

    def add_product(self, name, category, price, stock):
        with open(self.filepath, 'a') as f:
            f.write(f"{name},{category},{price},{stock}\n")

    def get_all_products(self):
        try:
            with open(self.filepath, 'r') as f:
                return [line.strip().split(',') for line in f]
        except FileNotFoundError:
            return []

    def delete_product(self, name):
        lines = self.get_all_products()
        with open(self.filepath, 'w') as f:
            for line in lines:
                if line[0] != name:
                    f.write(','.join(line) + '\n')

    def update_product(self, name, new_category, new_price, new_stock):
        lines = self.get_all_products()
        with open(self.filepath, 'w') as f:
            for line in lines:
                if line[0] == name:
                    f.write(f"{name},{new_category},{new_price},{new_stock}\n")
                else:
                    f.write(','.join(line) + '\n')

    def find_price(self, name):
        for line in self.get_all_products():
            if line[0] == name:
                return int(line[2])
        return None

    def get_all_categories(self):
        return [line[1] for line in self.get_all_products() if len(line) >= 4]

