import pytest
from unittest.mock import mock_open, patch
from model.file_handler import FileHandler
from model.product_model import ProductModel
from controller.cashier_controller import CashierController
from controller.admin_controller import AdminController


# ---------- FileHandler Tests ----------

def test_file_write_and_read(tmp_path):
    test_file = tmp_path / "test.txt"

    def temp_write_file(path, content):
        with open(path, 'w') as f:
            f.write(content)

    FileHandler.write_file = temp_write_file

    def temp_append_to_file(path, line):
        with open(path, 'a') as f:
            f.write('\n' + line)

    FileHandler.append_to_file = temp_append_to_file

    FileHandler.write_file(str(test_file), "line1\nline2")
    lines = FileHandler.read_lines(str(test_file))
    assert lines == ["line1\n", "line2"]

    FileHandler.append_to_file(str(test_file), "line3")
    lines = FileHandler.read_lines(str(test_file))
    assert lines[-1].strip() == "line3"


# ---------- ProductModel Tests ----------

def test_product_model_read(monkeypatch):
    sample_products = [
        ["Toothpaste", "Toiletries", "40", "100"],
        ["Shampoo", "Haircare", "350", "30"]
    ]

    # Patch get_all_products to return sample products directly
    monkeypatch.setattr(ProductModel, "get_all_products", lambda self: sample_products)

    model = ProductModel()
    products = model.get_all_products()
    assert len(products) == 2
    assert products[0][0] == "Toothpaste"
    assert model.find_price("Shampoo") == 350
    assert model.find_price("Unknown") is None


# ---------- CashierController Tests ----------

def test_cashier_controller(monkeypatch):
    monkeypatch.setattr(ProductModel, "get_all_products", lambda self: [["Soap", "Hygiene", "100", "50"]])
    monkeypatch.setattr(FileHandler, "append_to_file", lambda path, line: None)
    monkeypatch.setattr(FileHandler, "read_lines", lambda path: ["Bill 1: 200"])

    controller = CashierController(view=None)
    assert controller.find_product("Soap") == 100
    controller.record_bill(150)  # No error = pass
    assert controller.get_categories() == ["Hygiene"]
    assert controller.get_products_by_category() == {"Hygiene": ["Soap"]}


# ---------- AdminController Tests ----------

class MockView:
    def show_message(self, msg):
        pass  # or print(msg)


def test_admin_controller(monkeypatch):
    monkeypatch.setattr(FileHandler, "append_to_file", lambda path, line: None)
    monkeypatch.setattr(FileHandler, "read_lines", lambda path: ["admin,admin123"])
    FileHandler.write_file = lambda path, content: None

    mock_view = MockView()
    controller = AdminController(view=mock_view)

    # Patch built-in open to avoid FileNotFoundError when writing files
    m = mock_open(read_data="admin,admin123\n")
    with patch("builtins.open", m):
        controller.add_cashier("cashier1", "pass")  # Simulated add
        controller.delete_cashier("cashier1")  # Simulated delete

    controller.add_product("Juice", "Drinks", "50", "100")
    controller.update_product("Juice", "Drinks", "60", "80")
    controller.delete_product("Juice")
    assert controller.get_all_cashiers() == ["admin,admin123"]
    assert controller.get_all_products() == ["admin,admin123"]
