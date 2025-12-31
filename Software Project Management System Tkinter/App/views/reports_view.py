import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from app.Database.connection import DatabaseConnection
from app.utils.styles import styled_button, header_label, card_frame


class ReportsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")

        top = card_frame(self, padding=8)
        top.pack(fill="x", pady=6)
        header_label(top, "Reports").pack(side="left")
        styled_button(top, "Export Projects CSV", self.export_projects).pack(side="right", padx=6)
        styled_button(top, "Export Tasks CSV", self.export_tasks).pack(side="right")

        ttk.Label(self, text="Use the buttons above to export basic CSV reports.").pack(padx=12, pady=12)

    def export_projects(self):
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            try:
                cur.execute("SELECT client_name, project_name, status, budget, billed_amount FROM vw_project_overview")
            except Exception:
                cur.execute("SELECT name, description, status, created_by FROM projects")
            rows = cur.fetchall()
        except Exception:
            messagebox.showerror("Error", "Could not fetch project data from DB")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for r in rows:
                writer.writerow(r)
        messagebox.showinfo("Exported", f"Projects exported to {path}")

    def export_tasks(self):
        try:
            conn = DatabaseConnection.get_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, title, status, project_id, assigned_to FROM tasks")
            rows = cur.fetchall()
        except Exception:
            messagebox.showerror("Error", "Could not fetch task data from DB")
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for r in rows:
                writer.writerow(r)
        messagebox.showinfo("Exported", f"Tasks exported to {path}")
