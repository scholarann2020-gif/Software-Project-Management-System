import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from app.services.project_service import ProjectService
from app.utils.styles import styled_button, card_frame, header_label


class ProjectsView(tk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user or {}
        self.pack(expand=True, fill="both")

        top = card_frame(self, padding=8)
        top.pack(fill="x", pady=6)
        header_label(top, "Projects").pack(side="left")
        styled_button(top, "New Project", self.new_project).pack(side="right", padx=6)
        styled_button(top, "Edit Project", self.edit_project).pack(side="right")
        styled_button(top, "Delete Project", self.delete_project).pack(side="right", padx=6)
        styled_button(top, "Refresh", self.load_projects).pack(side="right")

        cols = ("id", "name", "description", "status", "created_by")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120)
        self.tree.pack(expand=True, fill="both", padx=8, pady=8)

        self.load_projects()

    def load_projects(self):
        # Clear
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            rows = ProjectService.get_projects()
            if not rows:
                self.tree.insert("", tk.END, values=("-", "No projects", "-", "-", "-"))
                return
            for r in rows:
                # project_service may return dicts
                if isinstance(r, dict):
                    vals = (r.get("id"), r.get("name"), r.get("description"), r.get("status"), r.get("created_by"))
                else:
                    vals = (r[0], r[1], r[2], r[3], r[4])
                self.tree.insert("", tk.END, values=vals)
        except Exception:
            # fallback demo rows
            demo = [
                (1, "ERP System", "Enterprise ERP", "In Progress", "admin"),
                (2, "Mobile Banking App", "iOS/Android app", "In Progress", "user"),
            ]
            for r in demo:
                self.tree.insert("", tk.END, values=r)

    def new_project(self):
        dlg = ProjectDialog(self, title="New Project")
        if dlg.result:
            name, desc, status = dlg.result
            try:
                user_id = self.user.get("id", 0)
                ProjectService.create_project(name, desc, status, user_id)
                messagebox.showinfo("Success", "Project created")
                self.load_projects()
            except Exception as e:
                messagebox.showerror("Error", f"Could not create project: {e}")

    def edit_project(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a project to edit")
            return
        vals = self.tree.item(sel[0])['values']
        project_id = vals[0]
        dlg = ProjectDialog(self, title="Edit Project", initial=(vals[1], vals[2], vals[3]))
        if dlg.result:
            name, desc, status = dlg.result
            try:
                ProjectService.update_project(project_id, status)
                messagebox.showinfo("Success", "Project updated")
                self.load_projects()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update project: {e}")

    def delete_project(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a project to delete")
            return
        vals = self.tree.item(sel[0])['values']
        project_id = vals[0]
        if messagebox.askyesno("Confirm", "Delete selected project?"):
            try:
                ProjectService.delete_project(project_id)
                messagebox.showinfo("Deleted", "Project deleted")
                self.load_projects()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete project: {e}")


class ProjectDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial=None):
        self.initial = initial or ("", "", "Planned")
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Name:").grid(row=0, column=0, sticky="w")
        self.e_name = ttk.Entry(master, width=40)
        self.e_name.grid(row=0, column=1)
        tk.Label(master, text="Description:").grid(row=1, column=0, sticky="w")
        self.e_desc = ttk.Entry(master, width=40)
        self.e_desc.grid(row=1, column=1)
        tk.Label(master, text="Status:").grid(row=2, column=0, sticky="w")
        self.e_status = ttk.Entry(master, width=20)
        self.e_status.grid(row=2, column=1, sticky="w")

        self.e_name.insert(0, self.initial[0])
        self.e_desc.insert(0, self.initial[1])
        self.e_status.insert(0, self.initial[2])
        return self.e_name

    def apply(self):
        name = self.e_name.get().strip()
        desc = self.e_desc.get().strip()
        status = self.e_status.get().strip() or "Planned"
        self.result = (name, desc, status)
