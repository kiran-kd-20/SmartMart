import tkinter as tk
from view.login_view import LoginView

if __name__ == "__main__":
    root = tk.Tk()
    LoginView(root)
    root.mainloop()