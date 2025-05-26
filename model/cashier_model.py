class CashierModel:
    def __init__(self, filepath='data/products.txt'):
        self.filepath = filepath

    def find_product(self, name):
        try:
            with open(self.filepath, 'r') as f:
                for line in f:
                    pname, price = line.strip().split(',')
                    if pname == name:
                        return int(price)
        except:
            return None
