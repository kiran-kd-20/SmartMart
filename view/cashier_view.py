import tkinter as tk
from tkinter import messagebox, ttk
from controller.cashier_controller import CashierController

class CashierView:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mart 💗 Cashier")
        self.root.geometry("500x650")
        self.root.configure(bg="#fce4ec")

        self.controller = CashierController(self)
        self.cart = []
        self.products_by_category = self.controller.get_products_by_category()

        tk.Label(root, text="💗 Cashier Panel 💗", font=("Helvetica", 18, "bold"), bg="#fce4ec", fg="#880e4f").pack(pady=10)

        # Category dropdown
        tk.Label(root, text="Select Category", bg="#fce4ec").pack()
        self.category_var = tk.StringVar()
        category_list = list(self.products_by_category.keys())
        self.category_box = ttk.Combobox(root, textvariable=self.category_var, values=category_list, state="readonly")
        self.category_box.set(category_list[0] if category_list else "No Categories")
        self.category_box.pack(pady=5)
        self.category_box.bind("<<ComboboxSelected>>", lambda e: self.update_product_menu(self.category_var.get()))

        # Product dropdown
        tk.Label(root, text="Select Product", bg="#fce4ec").pack()
        self.product_var = tk.StringVar()
        initial_products = self.products_by_category.get(self.category_var.get(), [])
        self.product_box = ttk.Combobox(root, textvariable=self.product_var, values=initial_products, state="readonly")
        self.product_box.set(initial_products[0] if initial_products else "No Products")
        self.product_box.pack(pady=5)
        self.product_box.bind("<<ComboboxSelected>>", lambda e: self.update_price_label(self.product_var.get()))

        # Live price label
        self.price_label = tk.Label(root, text="Price: --", bg="#fce4ec", fg="#4a148c", font=("Arial", 12))
        self.price_label.pack(pady=2)
        self.update_price_label(self.product_var.get())

        # Quantity input
        self.qty = tk.Entry(root)
        self.qty.insert(0, "Quantity")
        self.qty.pack(pady=5)

        tk.Button(root, text="Add to Cart", command=self.add_to_cart, bg="#ce93d8", fg="white", width=25).pack(pady=10)

        self.cart_display = tk.Text(root, height=10, width=55, bg="white")
        self.cart_display.pack(pady=5)

        self.payment_method = tk.StringVar(value="Cash")
        tk.Radiobutton(root, text="Cash", variable=self.payment_method, value="Cash", bg="#fce4ec").pack()
        tk.Radiobutton(root, text="Card (10% off)", variable=self.payment_method, value="Card", bg="#fce4ec").pack()

        tk.Button(root, text="Payment Received", command=self.checkout, bg="#f06292", fg="white", width=25).pack(pady=10)

    def update_product_menu(self, selected_category):
        products = self.products_by_category.get(selected_category, [])
        self.product_box['values'] = products
        self.product_var.set(products[0] if products else "No Products")
        self.update_price_label(self.product_var.get())

    def update_price_label(self, product_name):
        price = self.controller.find_product(product_name)
        if price:
            self.price_label.config(text=f"Price: Rs.{price}")
        else:
            self.price_label.config(text="Price: --")

    def add_to_cart(self):
        name = self.product_var.get()
        qty = self.qty.get().strip()

        if not qty.isdigit():
            messagebox.showerror("Invalid Input", "Quantity must be a number.")
            return

        price = self.controller.find_product(name)
        if price is None:
            messagebox.showerror("Not Found", "Product not found.")
            return

        quantity = int(qty)
        subtotal = price * quantity

        confirm = messagebox.askyesno("Confirm", f"Add {name} x {quantity} @ Rs.{price} = Rs.{subtotal}?")
        if not confirm:
            return

        self.cart.append((name, quantity, price, subtotal))
        self.cart_display.insert(tk.END, f"{name} x {quantity} @ Rs.{price} = Rs.{subtotal}\n")

    def checkout(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items before checkout.")
            return

        total = sum(item[3] for item in self.cart)
        method = self.payment_method.get()
        final_total = round(total * 0.9) if method == "Card" else total

        confirm = messagebox.askyesno("Confirm Checkout", f"Final Total ({method}): Rs.{final_total}\nProceed?")
        if not confirm:
            return

        self.controller.record_bill(final_total)
        self.cart_display.insert(tk.END, f"\nTotal ({method}): Rs.{final_total}\n")
        messagebox.showinfo("Payment Successful", f"Bill recorded: Rs.{final_total}")
        self.cart.clear()