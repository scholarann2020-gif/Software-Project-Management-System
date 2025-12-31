import tkinter as tk
from tkinter import ttk
from app.services.project_service import ProjectService
from app.views.task_view import TaskView
from app.utils.styles import styled_button, header_label, card_frame, styled_entry


class ProjectView:
    def __init__(self, root):
        frame = card_frame(root, padding=10)
        frame.pack(expand=True, fill="both", padx=12, pady=12)

        header_label(frame, "Projects").pack()

        self.name = styled_entry(frame, width=30)
        self.name.pack(pady=6)

        styled_button(frame, "Add Project", lambda: ProjectService.create_project(
            self.name.get(), "", "New", 1)).pack()

        for project in ProjectService.get_projects():
            ttk.Label(frame, text=project["name"]).pack()
            styled_button(frame, "Tasks", lambda p=project["id"]: TaskView(root, p)).pack()
