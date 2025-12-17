import tkinter as tk
from app.services.project_service import ProjectService
from app.views.task_view import TaskView


class ProjectView:
    def __init__(self, root):
        tk.Label(root, text="Projects").pack()

        self.name = tk.Entry(root)
        self.name.pack()

        tk.Button(root, text="Add Project",
                  command=lambda: ProjectService.create_project(
                      self.name.get(), "", "New", 1)).pack()

        for project in ProjectService.get_projects():
            tk.Label(root, text=project["name"]).pack()
            tk.Button(root, text="Tasks",
                      command=lambda p=project["id"]: TaskView(root, p)).pack()
