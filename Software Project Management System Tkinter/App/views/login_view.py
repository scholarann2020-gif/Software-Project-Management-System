import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import AuthService
from app.views.dashboard_view import DashboardView
from app.views.main_window import MainWindow
from app.utils.styles import style_root, styled_button, FONT_TITLE, header_label, styled_entry, card_frame
from tkinter import ttk


class LoginView:
    def __init__(self, root):
        self.root = root
        root.title("SPMS - Login")
        style_root(root)

        frame = card_frame(root, padding=14)
        frame.pack(expand=True, padx=20, pady=12)

        header_label(frame, "Software Project Management System").pack(pady=12)

        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username = styled_entry(frame, width=30)
        self.username.pack(pady=5)

        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password = styled_entry(frame, width=30)
        self.password.config(show="*")
        self.password.pack(pady=5)

        # role selection
        tk.Label(frame, text="Role", bg="#f4f6f8").pack(anchor="w", pady=(6, 0))
        self.role_var = tk.StringVar(value="Any")
        role_combo = ttk.Combobox(frame, textvariable=self.role_var, values=["Any", "Admin", "User"], state="readonly", width=28)
        role_combo.pack(pady=4)

        styled_button(frame, "Login", self.login).pack(pady=12)

    def login(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        user = AuthService.login(username, password)
        if user:
            # if a role is selected, ensure it matches the returned user's role
            selected_role = self.role_var.get()
            if selected_role != "Any":
                user_role = (user.get("role") or "").lower()
                if user_role != selected_role.lower():
                    messagebox.showerror("Login Failed", "Role does not match user account.")
                    return

            self.root.destroy()
            new_root = tk.Tk()
            MainWindow(new_root, user)
            new_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
