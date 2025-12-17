import tkinter as tk
from app.services.task_service import TaskService


class TaskView:
    def __init__(self, root, project_id):
        tk.Label(root, text="Tasks").pack()

        self.title = tk.Entry(root)
        self.title.pack()

        tk.Button(root, text="Add Task",
                  command=lambda: TaskService.create_task(
                      self.title.get(), "Pending", project_id, 1)).pack()

        for task in TaskService.get_tasks(project_id):
            tk.Label(root, text=task["title"]).pack()
