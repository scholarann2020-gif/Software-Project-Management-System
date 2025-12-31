import tkinter as tk
from tkinter import messagebox
from app.utils.styles import style_root, styled_button, FONT_TITLE, header_label
from tkinter import ttk


class BillingView:
    def __init__(self, root):
        self.root = root
        root.title("SPMS - Billing Module")
        style_root(root)
        root.geometry("450x420")

        main_frame = ttk.Frame(root)
        main_frame.pack(expand=True, padx=20, pady=20)

        # Title
        header_label(main_frame, "Billing Module").pack(pady=8)

        # Client Name
        ttk.Label(main_frame, text="Client Name").pack(anchor="w")
        self.client_name = ttk.Entry(main_frame, width=35)
        self.client_name.pack(pady=5)

        # Project Name
        ttk.Label(main_frame, text="Project Name").pack(anchor="w")
        self.project_name = ttk.Entry(main_frame, width=35)
        self.project_name.pack(pady=5)

        # Amount
        ttk.Label(main_frame, text="Amount").pack(anchor="w")
        self.amount = ttk.Entry(main_frame, width=35)
        self.amount.pack(pady=5)

        # Buttons
        styled_button(main_frame, "Generate Bill", self.generate_bill).pack(pady=15)
        styled_button(main_frame, "Back to Dashboard", self.back_to_dashboard).pack()

    def generate_bill(self):
        client = self.client_name.get().strip()
        project = self.project_name.get().strip()
        amount = self.amount.get().strip()

        if not client or not project or not amount:
            messagebox.showwarning("Validation Error", "All fields are required.")
            return

        if not amount.isdigit():
            messagebox.showerror("Invalid Amount", "Amount must be numeric.")
            return

        messagebox.showinfo(
            "Billing Success",
            f"Bill Generated Successfully!\n\nClient: {client}\nProject: {project}\nAmount: {amount}"
        )

        self.clear_fields()

    def clear_fields(self):
        self.client_name.delete(0, tk.END)
        self.project_name.delete(0, tk.END)
        self.amount.delete(0, tk.END)

    def back_to_dashboard(self):
        self.root.destroy()
