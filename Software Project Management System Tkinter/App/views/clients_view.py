import tkinter as tk
from tkinter import ttk, messagebox
from app.Database.connection import DatabaseConnection
from app.utils.styles import styled_button, card_frame, header_label


class ClientsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        top = card_frame(self, padding=8)
        top.pack(fill="x", pady=6)
        header_label(top, "Clients").pack(side="left")
        styled_button(top, "Refresh", self.load_clients).pack(side="right")

        cols = ("client_id", "client_name", "contact")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=160)
        self.tree.pack(expand=True, fill="both", padx=8, pady=8)

        self.load_clients()

    def load_clients(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT client_id, client_name, contact FROM clients")
            rows = cur.fetchall()
            if not rows:
                self.tree.insert("", tk.END, values=("-", "No clients", "-"))
                return
            for r in rows:
                if isinstance(r, dict):
                    vals = (r.get("client_id"), r.get("client_name"), r.get("contact"))
                else:
                    vals = (r[0], r[1], r[2])
                self.tree.insert("", tk.END, values=vals)
        except Exception:
            demo = [
                (1, "ABC Software House", "abc@example.com"),
                (2, "Global IT Services", "info@globalit.com"),
            ]
            for r in demo:
                self.tree.insert("", tk.END, values=r)
