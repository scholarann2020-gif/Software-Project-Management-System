import tkinter as tk
from app.views.project_view import ProjectView


class DashboardView:
    def __init__(self, root):
        root.title("Dashboard")
        tk.Label(root, text="Dashboard").pack()
        tk.Button(root, text="Manage Projects", command=lambda: ProjectView(root)).pack()
