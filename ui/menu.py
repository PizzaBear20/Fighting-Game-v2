import tkinter as tk
from tkinter import ttk

from ui import theme
from ui.drawing import drawArena, drawFighter, readable


# The first screen: the title and a big button for each game mode
class MainMenu:
    STAGE_WIDTH = 420
    STAGE_HEIGHT = 170
    STAGE_GROUND = 150

    # buttons is a list of (text, style, command). topFighters is up to 2 characters to show on the stage
    def __init__(self, parent, buttons, topFighters, subtitle):
        self.frame = tk.Frame(parent, bg=theme.BG)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        center = tk.Frame(self.frame, bg=theme.BG)
        center.grid(row=0, column=0, padx=16, pady=16)

        titleRow = tk.Frame(center, bg=theme.BG)
        titleRow.pack()
        tk.Label(titleRow, text="FIGHTING GAME", bg=theme.BG, fg=theme.TEXT, font=(theme.FONT, 40, "bold")).pack(side="left")
        tk.Label(titleRow, text="v2", bg=theme.BG, fg=theme.GOLD, font=(theme.FONT, 20, "bold")).pack(side="left", padx=(10, 0), pady=(14, 0))
        tk.Label(center, text=subtitle, bg=theme.BG, fg=theme.MUTED, font=theme.BODY_FONT).pack(pady=(2, 10))

        stage = tk.Canvas(center, width=self.STAGE_WIDTH, height=self.STAGE_HEIGHT, bg=theme.BG, highlightthickness=0)
        stage.pack(pady=(0, 18))
        drawArena(stage, self.STAGE_WIDTH, self.STAGE_HEIGHT, self.STAGE_GROUND)
        for character, x, facing in zip(topFighters, (120, self.STAGE_WIDTH - 120), (1, -1)):
            drawFighter(stage, x, self.STAGE_GROUND, character.look, facing, scale=0.7)
            stage.create_text(x, self.STAGE_GROUND + 12, text=character.name, fill=readable(character.look["bodyColor"]),
                              font=theme.SMALL_FONT)

        for text, style, command in buttons:
            ttk.Button(center, text=text, style=style, command=command, width=18).pack(pady=6)
