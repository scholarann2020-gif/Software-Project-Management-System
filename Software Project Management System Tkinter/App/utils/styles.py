import tkinter as tk
from tkinter import ttk

# Modern theme palette
BG_COLOR = "#0f1724"          # deep navy
SURFACE = "#0b2238"           # panel background
ACCENT = "#7b61ff"            # vibrant purple accent
ACCENT_2 = "#00c2a8"          # teal secondary accent
ACCENT_DARK = "#5a3dd6"
TEXT = "#f1f5f9"
MUTED = "#93a4b6"

FONT_MAIN = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_BOLD = ("Segoe UI", 11, "bold")


def style_root(root, geometry: str = "420x380"):
    """Apply window background and run ttk theme setup.
    Pass geometry=None to skip resizing."""
    try:
        root.configure(bg=BG_COLOR)
    except Exception:
        pass
    if geometry:
        try:
            root.geometry(geometry)
            root.resizable(False, False)
        except Exception:
            pass
    apply_theme()


def apply_theme():
    """Configure ttk styles for a colorful modern look. Safe to call multiple times."""
    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        try:
            style.theme_use(style.theme_names()[0])
        except Exception:
            pass

    # Generic labels
    style.configure("TLabel", background=BG_COLOR, foreground=TEXT, font=FONT_MAIN)
    style.configure("Header.TLabel", font=FONT_TITLE, foreground=TEXT, background=BG_COLOR)
    style.configure("Muted.TLabel", foreground=MUTED, background=BG_COLOR, font=FONT_MAIN)

    # Frames as cards
    style.configure("Card.TFrame", background=SURFACE, relief="flat")
    style.configure("TFrame", background=BG_COLOR)

    # Notebook / Tabs
    style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
    style.configure("TNotebook.Tab", background=SURFACE, foreground=TEXT, padding=[12, 8], font=FONT_BOLD)
    style.map("TNotebook.Tab", background=[("selected", ACCENT)])

    # Treeview
    style.configure("Treeview", background=SURFACE, fieldbackground=SURFACE, foreground=TEXT, rowheight=26, font=FONT_MAIN)
    style.configure("Treeview.Heading", background=ACCENT_DARK, foreground=TEXT, relief="flat", font=FONT_BOLD)

    # Buttons
    style.configure("Accent.TButton", font=FONT_MAIN, foreground=TEXT, background=ACCENT, padding=8)
    style.map("Accent.TButton",
                background=[("active", ACCENT_DARK), ("pressed", ACCENT_DARK)],
                foreground=[("active", TEXT)])

    style.configure("Secondary.TButton", font=FONT_MAIN, foreground=BG_COLOR, background=ACCENT_2, padding=6)
    style.map("Secondary.TButton", background=[("active", ACCENT)])

    style.configure("Outline.TButton", font=FONT_MAIN, foreground=TEXT, background=SURFACE, padding=6)
    style.map("Outline.TButton", relief=[("pressed", "sunken")])


def styled_button(parent, text, command, style_name="Accent.TButton"):
    """Return a styled ttk.Button. Default uses the colorful accent."""
    btn = ttk.Button(parent, text=text, command=command, style=style_name)
    return btn


def header_label(parent, text):
    lbl = ttk.Label(parent, text=text, style="Header.TLabel")
    return lbl


def card_frame(parent, padding=12):
    frm = ttk.Frame(parent, style="Card.TFrame", padding=padding)
    return frm


def styled_entry(parent, width=30):
    e = ttk.Entry(parent, width=width)
    return e
