import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from app.services.task_service import TaskService
from app.utils.styles import styled_button, card_frame, header_label


class TasksView(tk.Frame):
    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user or {}
        self.pack(expand=True, fill="both")

        top = card_frame(self, padding=8)
        top.pack(fill="x", pady=6)
        header_label(top, "Tasks").pack(side="left")
        styled_button(top, "New Task", self.new_task).pack(side="right", padx=6)
        styled_button(top, "Edit Task", self.edit_task).pack(side="right")
        styled_button(top, "Delete Task", self.delete_task).pack(side="right", padx=6)
        styled_button(top, "Refresh", self.load_tasks).pack(side="right")

        cols = ("id", "title", "status", "project_id", "assigned_to")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120)
        self.tree.pack(expand=True, fill="both", padx=8, pady=8)

        self.load_tasks()

    def load_tasks(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        try:
            rows = TaskService.get_tasks(None)  # service expects project_id; None -> all
            if not rows:
                self.tree.insert("", tk.END, values=("-", "No tasks", "-", "-", "-"))
                return
            for r in rows:
                if isinstance(r, dict):
                    vals = (r.get("id"), r.get("title"), r.get("status"), r.get("project_id"), r.get("assigned_to"))
                else:
                    vals = (r[0], r[1], r[2], r[3], r[4])
                self.tree.insert("", tk.END, values=vals)
        except Exception:
            demo = [
                (1, "Design UI", "Pending", 1, "alice"),
                (2, "Build API", "In Progress", 1, "bob"),
            ]
            for r in demo:
                self.tree.insert("", tk.END, values=r)

    def new_task(self):
        dlg = TaskDialog(self, title="New Task")
        if dlg.result:
            title, status, project_id, assigned_to = dlg.result
            try:
                TaskService.create_task(title, status, project_id, assigned_to)
                messagebox.showinfo("Success", "Task created")
                self.load_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Could not create task: {e}")

    def edit_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a task to edit")
            return
        vals = self.tree.item(sel[0])['values']
        task_id = vals[0]
        dlg = TaskDialog(self, title="Edit Task", initial=(vals[1], vals[2], vals[3], vals[4]))
        if dlg.result:
            title, status, project_id, assigned_to = dlg.result
            try:
                TaskService.update_task(task_id, status)
                messagebox.showinfo("Success", "Task updated")
                self.load_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Could not update task: {e}")

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a task to delete")
            return
        vals = self.tree.item(sel[0])['values']
        task_id = vals[0]
        if messagebox.askyesno("Confirm", "Delete selected task?"):
            try:
                TaskService.delete_task(task_id)
                messagebox.showinfo("Deleted", "Task deleted")
                self.load_tasks()
            except Exception as e:
                messagebox.showerror("Error", f"Could not delete task: {e}")


class TaskDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial=None):
        self.initial = initial or ("", "Pending", "", "")
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Title:").grid(row=0, column=0, sticky="w")
        self.e_title = ttk.Entry(master, width=40)
        self.e_title.grid(row=0, column=1)
        tk.Label(master, text="Status:").grid(row=1, column=0, sticky="w")
        self.e_status = ttk.Entry(master, width=20)
        self.e_status.grid(row=1, column=1, sticky="w")
        tk.Label(master, text="Project ID:").grid(row=2, column=0, sticky="w")
        self.e_project = ttk.Entry(master, width=10)
        self.e_project.grid(row=2, column=1, sticky="w")
        tk.Label(master, text="Assigned to:").grid(row=3, column=0, sticky="w")
        self.e_assigned = ttk.Entry(master, width=20)
        self.e_assigned.grid(row=3, column=1, sticky="w")

        self.e_title.insert(0, self.initial[0])
        self.e_status.insert(0, self.initial[1])
        self.e_project.insert(0, self.initial[2])
        self.e_assigned.insert(0, self.initial[3])
        return self.e_title

    def apply(self):
        title = self.e_title.get().strip()
        status = self.e_status.get().strip() or "Pending"
        project_id = self.e_project.get().strip() or None
        assigned_to = self.e_assigned.get().strip() or None
        self.result = (title, status, project_id, assigned_to)
