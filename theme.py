import tkinter as tk
from tkinter import ttk

from drawing import darker, lighter

# Colors
BG = "#151827"
PANEL = "#1f2336"
PANEL_LIGHT = "#2a2f47"
BORDER = "#343a58"
TEXT = "#e8eaf6"
MUTED = "#9aa0bf"
GOLD = "#ffd34d"
BLUE = "#5b8cff"
RED = "#ff5c5c"
GREEN = "#4cd964"

STAT_COLORS = {
    "health": "#4cd964",
    "strength": "#ff6b6b",
    "speed": "#00d2d3",
    "mana": "#b47cff",
    "battleIQ": "#ffcc00",
    "defense": "#ff9f43",
}
MOVE_COLORS = {"Health": "#4cd964", "Strength": "#ff6b6b", "Speed": "#00d2d3", "Defense": "#ff9f43"}

# Fonts
FONT = "Helvetica"
TITLE_FONT = (FONT, 24, "bold")
NAME_FONT = (FONT, 22, "bold")
HEADING_FONT = (FONT, 11, "bold")
BODY_FONT = (FONT, 13)
BOLD_FONT = (FONT, 13, "bold")
SMALL_FONT = (FONT, 11)


# Sets up the colors for ttk widgets (buttons, dropdowns, scrollbars)
def setupStyles(root):
    root.configure(bg=BG)
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure(".", background=PANEL, foreground=TEXT, font=BODY_FONT, bordercolor=BORDER,
                    lightcolor=PANEL_LIGHT, darkcolor=PANEL_LIGHT, troughcolor=BG, focuscolor=PANEL_LIGHT)

    style.configure("TButton", background=PANEL_LIGHT, foreground=TEXT, padding=(12, 6), borderwidth=0)
    style.map("TButton",
              background=[("disabled", PANEL), ("pressed", BORDER), ("active", "#353b5c")],
              foreground=[("disabled", MUTED)])
    for name, color, textColor in (("Accent", BLUE, "#ffffff"), ("Fight", RED, "#ffffff"), ("Gold", GOLD, "#1b1b24")):
        style.configure(f"{name}.TButton", background=color, foreground=textColor)
        style.map(f"{name}.TButton",
                  background=[("disabled", PANEL_LIGHT), ("pressed", darker(color, 0.2)), ("active", lighter(color, 0.15))],
                  foreground=[("disabled", MUTED)])
    style.configure("Fight.TButton", font=(FONT, 16, "bold"), padding=(18, 10))
    style.configure("Small.TButton", padding=(8, 3), font=SMALL_FONT)

    style.configure("TCombobox", fieldbackground=PANEL_LIGHT, background=PANEL_LIGHT, foreground=TEXT,
                    arrowcolor=TEXT, bordercolor=BORDER, padding=4)
    style.map("TCombobox",
              fieldbackground=[("readonly", PANEL_LIGHT)], foreground=[("readonly", TEXT)],
              selectbackground=[("readonly", PANEL_LIGHT)], selectforeground=[("readonly", TEXT)],
              background=[("active", BORDER)])
    root.option_add("*TCombobox*Listbox.background", PANEL_LIGHT)
    root.option_add("*TCombobox*Listbox.foreground", TEXT)
    root.option_add("*TCombobox*Listbox.selectBackground", BLUE)
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
    root.option_add("*TCombobox*Listbox.font", BODY_FONT)

    style.configure("TSpinbox", fieldbackground=PANEL_LIGHT, background=PANEL_LIGHT, foreground=TEXT,
                    arrowcolor=TEXT, bordercolor=BORDER, insertcolor=TEXT, padding=4)
    for scrollbarStyle in ("TScrollbar", "Vertical.TScrollbar"):
        style.configure(scrollbarStyle, background=PANEL_LIGHT, troughcolor=PANEL, arrowcolor=MUTED, bordercolor=PANEL, gripcount=0)


# A dark box with a small title at the top. Put widgets inside the returned "body" frame
def panel(parent, title=None):
    outer = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
    if title:
        tk.Label(outer, text=title.upper(), bg=PANEL, fg=MUTED, font=HEADING_FONT).pack(anchor="w", padx=14, pady=(12, 6))
    body = tk.Frame(outer, bg=PANEL)
    body.pack(fill="both", expand=True, padx=14, pady=(0 if title else 14, 14))
    return outer, body


def label(parent, text="", font=BODY_FONT, fg=TEXT, **options):
    return tk.Label(parent, text=text, bg=parent["bg"], fg=fg, font=font, **options)


def entry(parent, width=16):
    return tk.Entry(parent, width=width, bg=PANEL_LIGHT, fg=TEXT, insertbackground=TEXT, relief="flat",
                    highlightthickness=1, highlightbackground=BORDER, highlightcolor=BLUE, font=BODY_FONT)


# A read-only text box. Use setText() to change what it shows
def textBox(parent, height, width=30):
    box = tk.Text(parent, height=height, width=width, bg=PANEL_LIGHT, fg=TEXT, relief="flat", highlightthickness=0,
                  padx=10, pady=8, font=BODY_FONT, wrap="word", cursor="arrow", spacing1=2, spacing3=2)
    box.config(state=tk.DISABLED)
    return box


# lines is a list of (text, tagName) pairs. Tags let each line have its own color
def setText(box, lines):
    box.config(state=tk.NORMAL)
    box.delete("1.0", tk.END)
    for text, tagName in lines:
        box.insert(tk.END, text, tagName)
    box.config(state=tk.DISABLED)
