from model.file_handler import FileHandler

class LoginController:
    def __init__(self, view):
        self.view = view

    def login(self, username, password, role):
        file = 'data/admin.txt' if role == 'Admin' else 'data/cashiers.txt'
        users = FileHandler.read_lines(file)
        for user in users:
            u, p = user.strip().split(',')
            if username == u and password == p:
                self.view.show_success(role)
                return
        self.view.show_error()