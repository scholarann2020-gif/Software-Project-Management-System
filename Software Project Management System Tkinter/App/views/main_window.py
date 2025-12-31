import tkinter as tk
from tkinter import ttk
from app.Database.connection import DatabaseConnection
from app.views.projects_view import ProjectsView


class MainWindow:
    def __init__(self, root, user):
        self.root = root
        self.user = user
        root.title("SPMS - Main")
        root.geometry("900x600")
        # Apply theme (modern colors)
        try:
            from app.utils.styles import apply_theme

            apply_theme()
        except Exception:
            pass

        # Top bar
        top = tk.Frame(root)
        top.pack(fill="x")
        try:
            from app.utils.styles import header_label

            header_label(top, text=f"Logged in: {user.get('username')}").pack(side="left", padx=8, pady=6)
        except Exception:
            tk.Label(top, text=f"Logged in: {user.get('username')}", anchor="w").pack(side="left", padx=8, pady=6)

        # Notebook tabs
        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill="both")

        # Dashboard tab
        dash_frame = tk.Frame(notebook)
        notebook.add(dash_frame, text="Dashboard")
        self._init_dashboard(dash_frame)

        # Projects tab
        proj_frame = tk.Frame(notebook)
        notebook.add(proj_frame, text="Projects")
        ProjectsView(proj_frame, user)

        # Tasks tab
        tasks_frame = tk.Frame(notebook)
        notebook.add(tasks_frame, text="Tasks")
        from app.views.tasks_view import TasksView
        TasksView(tasks_frame, user)

        # Clients tab
        clients_frame = tk.Frame(notebook)
        notebook.add(clients_frame, text="Clients")
        from app.views.clients_view import ClientsView
        ClientsView(clients_frame)

        # Billing tab
        billing_frame = tk.Frame(notebook)
        notebook.add(billing_frame, text="Billing")
        from app.views.billing_tab import BillingTab
        BillingTab(billing_frame)

        # Reports tab
        reports_frame = tk.Frame(notebook)
        notebook.add(reports_frame, text="Reports")
        from app.views.reports_view import ReportsView
        ReportsView(reports_frame)

    def _init_dashboard(self, parent):
        # Simple project overview table similar to DashboardView
        cols = ("Client", "Project", "Status", "Budget", "Billed")
        tree = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120)
        tree.pack(expand=True, fill="both", padx=12, pady=12)

        status_var = tk.StringVar(value="")
        tk.Label(parent, textvariable=status_var, fg="red").pack(anchor="w", padx=12)

        # load rows
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            try:
                cur.execute("SELECT client_name, project_name, status, budget, billed_amount FROM vw_project_overview")
            except Exception:
                try:
                    cur.execute("""
                        SELECT c.client_name, p.project_name, p.status, p.budget, COALESCE(p.billed_amount, 0)
                        FROM projects p
                        LEFT JOIN clients c ON p.client_id = c.client_id
                    """)
                except Exception:
                    cur.execute("""
                        SELECT c.client_name, p.project_name, p.status, p.budget, 0 AS billed_amount
                        FROM projects p
                        LEFT JOIN clients c ON p.client_id = c.client_id
                    """)

            rows = cur.fetchall()
            if not rows:
                tree.insert("", tk.END, values=("No clients", "No projects", "-", "0", "0"))
            else:
                for r in rows:
                    tree.insert("", tk.END, values=(r[0], r[1], r[2], r[3], r[4]))
            status_var.set("")
        except Exception:
            status_var.set("Could not load live data — showing demo rows.")
            demo_rows = [
                ("ABC Software House", "ERP System", "In Progress", "250000", "100000"),
                ("Tech Solutions", "Mobile Banking App", "In Progress", "400000", "200000"),
                ("Global IT Services", "Inventory Management", "Completed", "180000", "180000"),
            ]
            for r in demo_rows:
                tree.insert("", tk.END, values=r)
