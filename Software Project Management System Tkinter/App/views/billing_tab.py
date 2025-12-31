import tkinter as tk
from tkinter import ttk, messagebox
from app.Database.connection import DatabaseConnection
from app.utils.styles import styled_button, card_frame, header_label


class BillingTab(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        top = card_frame(self, padding=8)
        top.pack(fill="x", pady=8)
        header_label(top, "Invoices").pack(side="left")
        styled_button(top, "New Invoice", self.new_invoice).pack(side="right", padx=6)
        styled_button(top, "Refresh", self.load_invoices, ).pack(side="right")

        cols = ("invoice_id", "client", "project", "amount", "status")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.replace("_", " ").title())
            self.tree.column(c, width=140)
        self.tree.pack(expand=True, fill="both", padx=8, pady=8)

        self.load_invoices()

    def load_invoices(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT invoice_id, client_name, project_name, amount, status FROM invoices")
            rows = cur.fetchall()
            if not rows:
                self.tree.insert("", tk.END, values=("-", "No invoices", "-", "0", "-"))
                return
            for r in rows:
                if isinstance(r, dict):
                    vals = (r.get("invoice_id"), r.get("client_name"), r.get("project_name"), r.get("amount"), r.get("status"))
                else:
                    vals = (r[0], r[1], r[2], r[3], r[4])
                self.tree.insert("", tk.END, values=vals)
        except Exception:
            demo = [
                (1, "ABC Software House", "ERP System", "15000", "Paid"),
                (2, "Tech Solutions", "Mobile App", "25000", "Pending"),
            ]
            for r in demo:
                self.tree.insert("", tk.END, values=r)

    def new_invoice(self):
        messagebox.showinfo("Not Implemented", "Invoice creation not implemented yet.")
