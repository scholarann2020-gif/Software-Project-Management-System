import tkinter as tk
from tkinter import ttk
from app.Database.connection import DatabaseConnection
from app.utils.styles import header_label, styled_button
from tkinter import ttk
from app.utils.styles import card_frame


class DashboardView:
    def __init__(self, root, user=None):
        self.root = root
        self.user = user
        self.root.title("Project Management Dashboard")
        self.root.geometry("600x400")

        header_label(root, "Software Project Management System").pack(pady=10)

        # put table inside a card
        table_card = card_frame(root, padding=10)
        table_card.pack(expand=True, fill="both", padx=12, pady=10)

        self.table = ttk.Treeview(
            table_card,
            columns=("Client", "Project", "Status", "Budget", "Billed"),
            show="headings"
        )

        self.table.heading("Client", text="Client Name")
        self.table.heading("Project", text="Project Name")
        self.table.heading("Status", text="Status")
        self.table.heading("Budget", text="Budget")
        self.table.heading("Billed", text="Billed Amount")

        self.table.column("Client", width=160)
        self.table.column("Project", width=180)
        self.table.column("Status", width=100)
        self.table.column("Budget", width=80)
        self.table.column("Billed", width=80)

        self.table.pack(expand=True, fill="both", padx=20, pady=20)

        # status label and action buttons
        self.status_var = tk.StringVar(value="")
        status_frame = ttk.Frame(root)
        status_frame.pack(fill="x", padx=20)
        ttk.Label(status_frame, textvariable=self.status_var, foreground="red").pack(side="left")

        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill="x", padx=20, pady=(6, 12))
        styled_button(btn_frame, "Retry DB", self.retry_load).pack(side="left")
        styled_button(btn_frame, "Use Demo Data", self.use_demo_data).pack(side="left", padx=8)

        self.load_data()

    def load_data(self):
        try:
            conn = DatabaseConnection.get_connection()
            cursor = conn.cursor()

            # Prefer the view `vw_project_overview` if present; it should expose
            # client_name, project_name, status, budget, billed_amount
            try:
                cursor.execute("SELECT client_name, project_name, status, budget, billed_amount FROM vw_project_overview")
            except Exception:
                # fallback to a simple join if the view doesn't exist
                # Try to include billed_amount if present; if that column doesn't exist,
                # fall back to returning 0 for billed amount so the UI can still show rows.
                try:
                    cursor.execute("""
                        SELECT c.client_name, p.project_name, p.status, p.budget, COALESCE(p.billed_amount, 0)
                        FROM projects p
                        LEFT JOIN clients c ON p.client_id = c.client_id
                    """)
                except Exception:
                    cursor.execute("""
                        SELECT c.client_name, p.project_name, p.status, p.budget, 0 AS billed_amount
                        FROM projects p
                        LEFT JOIN clients c ON p.client_id = c.client_id
                    """)

            rows = cursor.fetchall()
            if not rows:
                self.table.insert("", tk.END, values=("No clients", "No projects", "-", "0", "0"))
            else:
                for row in rows:
                    # ensure row is a tuple/list in the expected order
                    self.table.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4]))
            # clear status on success
            self.status_var.set("")
            return True
        except Exception:
            # log full details to console for debugging
            import traceback

            traceback.print_exc()
            # set a friendly status and return False so callers can decide
            self.status_var.set("Could not load dashboard data from the database. Using demo data.")
            # populate placeholder so the UI isn't blank
            self.use_demo_data()
            return False

    def retry_load(self):
        # clear current rows
        for i in self.table.get_children():
            self.table.delete(i)
        success = self.load_data()
        if not success:
            # still failing; status_var already set and demo data shown
            pass

    def use_demo_data(self):
        # clear current rows
        for i in self.table.get_children():
            self.table.delete(i)
        demo_rows = [
            ("ABC Software House", "ERP System", "In Progress", "250000", "100000"),
            ("Tech Solutions", "Mobile Banking App", "In Progress", "400000", "200000"),
            ("Global IT Services", "Inventory Management", "Completed", "180000", "180000"),
        ]
        for r in demo_rows:
            self.table.insert("", tk.END, values=r)
        self.status_var.set("Showing demo data (DB unavailable)")
