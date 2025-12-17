import tkinter as tk
from app.services.auth_service import AuthService
from app.views.dashboard_view import DashboardView


class LoginView:
    def __init__(self, root):
        self.root = root
        root.title("Login")

        tk.Label(root, text="Username").pack()
        self.username = tk.Entry(root)
        self.username.pack()

        tk.Label(root, text="Password").pack()
        self.password = tk.Entry(root, show="*")
        self.password.pack()

        tk.Button(root, text="Login", command=self.login).pack()

    def login(self):
        user = AuthService.login(self.username.get(), self.password.get())
        if user:
            self.root.destroy()
            new_root = tk.Tk()
            DashboardView(new_root)
            new_root.mainloop()
        else:
            tk.Label(self.root, text="Invalid Credentials").pack()
