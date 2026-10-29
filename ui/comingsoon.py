import tkinter as tk
from tkinter import ttk

from ui import theme


# A stand-in screen for a game mode that isn't built yet. It just says "Coming soon" and has a Back button
class ComingSoonScreen:
    # onBack() is called when the Back button is clicked
    def __init__(self, parent, title, blurb, onBack):
        self.frame = tk.Frame(parent, bg=theme.BG)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        box, body = theme.panel(self.frame)
        box.grid(row=0, column=0, padx=16, pady=16)
        theme.label(body, title.upper(), font=theme.TITLE_FONT).pack(padx=40, pady=(24, 6))
        theme.label(body, blurb, fg=theme.MUTED, wraplength=380, justify="center").pack(padx=40)
        theme.label(body, "Coming soon", fg=theme.GOLD, font=(theme.FONT, 18, "bold")).pack(pady=24)
        ttk.Button(body, text="← Back to Menu", style="Accent.TButton", command=onBack).pack(pady=(0, 20))
