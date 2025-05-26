import tkinter as tk
from tkinter import messagebox
from controller.admin_controller import AdminController

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mart 💗 Admin")
        self.root.geometry("700x600")
        self.root.configure(bg="#fce4ec")

        self.controller = AdminController(self)

        title = tk.Label(root, text="💗 Smart Mart Admin Panel 💗", font=("Helvetica", 20, "bold"), bg="#fce4ec", fg="#880e4f")
        title.pack(pady=20)

        section = tk.Frame(root, bg="#fce4ec")
        section.pack(pady=10)

        # Product Buttons
        tk.Label(section, text="Product Management", font=("Arial", 14, "bold"), bg="#fce4ec", fg="#6a1b9a").grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(section, text="Add Product", command=self.add_product, bg="#ce93d8", fg="white", width=25).grid(row=1, column=0, padx=10, pady=5)
        tk.Button(section, text="View Products", command=self.view_products, bg="#ce93d8", fg="white", width=25).grid(row=1, column=1, padx=10, pady=5)
        tk.Button(section, text="Delete Product", command=self.delete_product, bg="#ce93d8", fg="white", width=25).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(section, text="Update Product", command=self.update_product, bg="#ce93d8", fg="white", width=25).grid(row=2, column=1, padx=10, pady=5)

        # Divider
        tk.Label(section, text="", bg="#fce4ec").grid(row=3, columnspan=2, pady=10)

        # Cashier Buttons
        tk.Label(section, text="Cashier Management", font=("Arial", 14, "bold"), bg="#fce4ec", fg="#6a1b9a").grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(section, text="Add Cashier", command=self.add_cashier, bg="#ce93d8", fg="white", width=25).grid(row=5, column=0, padx=10, pady=5)
        tk.Button(section, text="View Cashiers", command=self.view_cashiers, bg="#ce93d8", fg="white", width=25).grid(row=5, column=1, padx=10, pady=5)
        tk.Button(section, text="Delete Cashier", command=self.delete_cashier, bg="#ce93d8", fg="white", width=25).grid(row=6, column=0, padx=10, pady=5)

    def add_product(self):
        win = tk.Toplevel(self.root)
        win.title("Add Product")
        win.geometry("350x350")
        win.configure(bg="#fce4ec")

        for label in ["Name", "Category", "Price", "Stock"]:
            tk.Label(win, text=label, bg="#fce4ec", fg="#6a1b9a").pack(pady=2)
            setattr(self, f"entry_{label.lower()}", tk.Entry(win))
            getattr(self, f"entry_{label.lower()}").pack()

        tk.Button(win, text="Save", command=lambda: self.controller.add_product(
            self.entry_name.get(), self.entry_category.get(), self.entry_price.get(), self.entry_stock.get()
        ), bg="#ce93d8", fg="white").pack(pady=10)

    def view_products(self):
        win = tk.Toplevel(self.root)
        win.title("Product List")
        win.geometry("500x400")
        win.configure(bg="#fce4ec")
        products = self.controller.get_all_products()
        for line in products:
            if len(line) == 4:
                name, category, price, stock = line
                tk.Label(win, text=f"{name} ({category}) - Rs.{price} - Stock: {stock}", bg="#fce4ec", fg="#4a148c", anchor="w").pack(fill=tk.X, padx=10)

    def delete_product(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Product")
        win.geometry("300x150")
        win.configure(bg="#fce4ec")

        tk.Label(win, text="Product Name to Delete", bg="#fce4ec", fg="#6a1b9a").pack(pady=5)
        name = tk.Entry(win)
        name.pack()
        tk.Button(win, text="Delete", command=lambda: self.controller.delete_product(name.get()), bg="#ce93d8", fg="white").pack(pady=10)

    def update_product(self):
        win = tk.Toplevel(self.root)
        win.title("Update Product")
        win.geometry("350x350")
        win.configure(bg="#fce4ec")

        for label in ["Product Name to Update", "New Category", "New Price", "New Stock"]:
            tk.Label(win, text=label, bg="#fce4ec", fg="#6a1b9a").pack(pady=2)
            setattr(self, f"entry_{label.lower().replace(' ', '_')}", tk.Entry(win))
            getattr(self, f"entry_{label.lower().replace(' ', '_')}").pack()

        tk.Button(win, text="Update", command=lambda: self.controller.update_product(
            self.entry_product_name_to_update.get(),
            self.entry_new_category.get(),
            self.entry_new_price.get(),
            self.entry_new_stock.get()
        ), bg="#ce93d8", fg="white").pack(pady=10)

    def add_cashier(self):
        win = tk.Toplevel(self.root)
        win.title("Add Cashier")
        win.geometry("300x200")
        win.configure(bg="#fce4ec")

        tk.Label(win, text="Username", bg="#fce4ec", fg="#6a1b9a").pack()
        username = tk.Entry(win)
        username.pack()

        tk.Label(win, text="Password", bg="#fce4ec", fg="#6a1b9a").pack()
        password = tk.Entry(win)
        password.pack()

        tk.Button(win, text="Save", command=lambda: self.controller.add_cashier(username.get(), password.get()), bg="#ce93d8", fg="white").pack(pady=10)

    def view_cashiers(self):
        win = tk.Toplevel(self.root)
        win.title("Cashier List")
        win.geometry("300x300")
        win.configure(bg="#fce4ec")
        for line in self.controller.get_all_cashiers():
            tk.Label(win, text=line.strip(), bg="#fce4ec", fg="#4a148c").pack(anchor="w")

    def delete_cashier(self):
        win = tk.Toplevel(self.root)
        win.title("Delete Cashier")
        win.geometry("300x150")
        win.configure(bg="#fce4ec")

        tk.Label(win, text="Username to Delete", bg="#fce4ec", fg="#6a1b9a").pack()
        username = tk.Entry(win)
        username.pack()

        tk.Button(win, text="Delete", command=lambda: self.controller.delete_cashier(username.get()), bg="#ce93d8", fg="white").pack(pady=10)

    def show_message(self, msg):
        messagebox.showinfo("Message", msg)