import tkinter as tk
from tkinter import messagebox
from model.file_handler import FileHandler

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Mart 💗 Login")
        self.root.geometry("350x300")
        self.root.configure(bg="#fce4ec")

        tk.Label(root, text="💗 Smart Mart Login 💗", font=("Helvetica", 16, "bold"), bg="#fce4ec", fg="#880e4f").pack(pady=15)

        tk.Label(root, text="Username", bg="#fce4ec", fg="#6a1b9a").pack(pady=5)
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password", bg="#fce4ec", fg="#6a1b9a").pack(pady=5)
        self.password = tk.Entry(root, show='*')
        self.password.pack()

        tk.Button(root, text="Login", command=self.login, bg="#ce93d8", fg="white", width=20).pack(pady=20)

    def login(self):
        username = self.username.get()
        password = self.password.get()

        if self.validate_user('data/admin.txt', username, password):
            self.root.withdraw()
            from view.admin_view import AdminView
            AdminView(tk.Toplevel(self.root))
        elif self.validate_user('data/cashiers.txt', username, password):
            self.root.withdraw()
            from view.cashier_view import CashierView
            CashierView(tk.Toplevel(self.root))
        else:
            messagebox.showerror("Login Failed", "Invalid Credentials")

    def validate_user(self, filepath, username, password):
        for line in FileHandler.read_lines(filepath):
            u, p = line.strip().split(',')
            if u == username and p == password:
                return True
        return False