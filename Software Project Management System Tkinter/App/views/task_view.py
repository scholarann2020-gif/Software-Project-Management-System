import tkinter as tk
from tkinter import ttk
from app.services.task_service import TaskService
from app.utils.styles import header_label, styled_entry, styled_button, card_frame


class TaskView:
    def __init__(self, root, project_id):
        frame = card_frame(root, padding=10)
        frame.pack(expand=True, fill="both", padx=12, pady=12)

        header_label(frame, "Tasks").pack()

        self.title = styled_entry(frame, width=30)
        self.title.pack(pady=6)

        styled_button(frame, "Add Task",
                      lambda: TaskService.create_task(
                          self.title.get(), "Pending", project_id, 1)).pack()

        for task in TaskService.get_tasks(project_id):
            ttk.Label(frame, text=task["title"]).pack()
