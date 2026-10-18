import tkinter as tk
from tkinter import ttk, colorchooser

import theme
from character import randomLook, BUILDS, HAIR_STYLES, HEADWEAR, FACES, OUTFITS, CAPES, COLOR_CHOICES, SKIN_TONES
from drawing import drawArena, drawFighter


# Each section of the customizer: (section title, [(label, look key, choices), ...])
# choices is a list of styles for a dropdown, or "colors"/"skin" for a row of color swatches
SECTIONS = [
    ("Body", [
        ("Build", "build", BUILDS),
        ("Body color", "bodyColor", "colors"),
        ("Skin", "skinColor", "skin"),
        ("Gloves", "gloveColor", "colors"),
    ]),
    ("Head", [
        ("Face", "face", FACES),
        ("Hair", "hairStyle", HAIR_STYLES),
        ("Hair color", "hairColor", "colors"),
        ("Headwear", "headwear", HEADWEAR),
        ("Headwear color", "headwearColor", "colors"),
    ]),
    ("Outfit", [
        ("Outfit", "outfit", OUTFITS),
        ("Outfit color", "outfitColor", "colors"),
        ("Cape", "cape", CAPES),
        ("Cape color", "capeColor", "colors"),
    ]),
]

HAIR_COLORS = ["#1e1e1e", "#4a2f1b", "#8d5524", "#e6c35c", "#d35400", "#f5f6fa"]
SWATCH = 18
SWATCH_GAP = 4


class CustomizeWindow:
    PREVIEW_WIDTH = 300
    PREVIEW_HEIGHT = 380
    PREVIEW_GROUND = 320

    # onSave() is called after the new look is saved onto the character
    def __init__(self, parent, character, onSave):
        self.character = character
        self.onSave = onSave
        self.look = dict(character.look)
        self.pose = "stand"
        self.facing = 1
        self.dropdowns = {}
        self.swatches = {}

        self.window = tk.Toplevel(parent)
        self.window.title(f"Customize {character.name}")
        self.window.configure(bg=theme.BG)
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)

        # ----- left: live preview -----
        previewPanel, previewBody = theme.panel(self.window, "Preview")
        previewPanel.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="ns")

        theme.label(previewBody, character.name, font=theme.NAME_FONT).pack(anchor="w", pady=(0, 8))
        self.preview = tk.Canvas(previewBody, width=self.PREVIEW_WIDTH, height=self.PREVIEW_HEIGHT,
                                 highlightthickness=0, bg=theme.PANEL)
        self.preview.pack()
        drawArena(self.preview, self.PREVIEW_WIDTH, self.PREVIEW_HEIGHT, self.PREVIEW_GROUND)

        poseRow = tk.Frame(previewBody, bg=theme.PANEL)
        poseRow.pack(fill="x", pady=(10, 0))
        for pose, text in (("stand", "Stand"), ("punch", "Punch"), ("hit", "Hit"), ("win", "Win"), ("down", "K.O.")):
            ttk.Button(poseRow, text=text, style="Small.TButton", width=5,
                       command=lambda pose=pose: self.setPose(pose)).pack(side="left", padx=(0, 4))
        ttk.Button(poseRow, text="⇄", style="Small.TButton", width=3, command=self.flip).pack(side="right")

        # ----- right: all the options -----
        optionsPanel, optionsBody = theme.panel(self.window, "Look")
        optionsPanel.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="nsew")

        row = 0
        for sectionTitle, options in SECTIONS:
            theme.label(optionsBody, sectionTitle, font=theme.BOLD_FONT, fg=theme.GOLD).grid(
                row=row, column=0, columnspan=2, sticky="w", pady=(10 if row else 0, 4))
            row += 1
            for text, key, choices in options:
                theme.label(optionsBody, text, fg=theme.MUTED, font=theme.SMALL_FONT).grid(row=row, column=0, sticky="w", padx=(0, 12), pady=3)
                if isinstance(choices, list):
                    self.addDropdown(optionsBody, row, key, choices)
                else:
                    self.addSwatches(optionsBody, row, key, choices)
                row += 1

        # ----- bottom buttons -----
        buttonRow = tk.Frame(self.window, bg=theme.BG)
        buttonRow.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))
        ttk.Button(buttonRow, text="🎲 Randomize", command=self.randomize).pack(side="left")
        ttk.Button(buttonRow, text="Reset", command=self.reset).pack(side="left", padx=8)
        ttk.Button(buttonRow, text="Save Look", style="Accent.TButton", command=self.save).pack(side="right")
        ttk.Button(buttonRow, text="Cancel", command=self.window.destroy).pack(side="right", padx=8)

        self.refresh()
        self.window.grab_set()  # finish customizing before going back to the main window

    def addDropdown(self, parent, row, key, choices):
        dropdown = ttk.Combobox(parent, values=[choice.capitalize() for choice in choices], state="readonly", width=14)
        dropdown.grid(row=row, column=1, sticky="w", pady=3)
        dropdown.bind("<<ComboboxSelected>>", lambda event, key=key, dropdown=dropdown: self.setValue(key, dropdown.get().lower()))
        self.dropdowns[key] = dropdown

    def addSwatches(self, parent, row, key, kind):
        if kind == "skin":
            colors = SKIN_TONES
        elif key == "hairColor":
            colors = HAIR_COLORS + COLOR_CHOICES[:10]
        else:
            colors = COLOR_CHOICES
        frame = tk.Frame(parent, bg=theme.PANEL)
        frame.grid(row=row, column=1, sticky="w", pady=3)
        width = len(colors) * (SWATCH + SWATCH_GAP)
        canvas = tk.Canvas(frame, width=width, height=SWATCH + 4, bg=theme.PANEL, highlightthickness=0, cursor="hand2")
        canvas.pack(side="left")
        canvas.bind("<Button-1>", lambda event, key=key, colors=colors: self.onSwatchClick(event, key, colors))
        ttk.Button(frame, text="+", style="Small.TButton", width=2,
                   command=lambda key=key: self.pickCustomColor(key)).pack(side="left", padx=(4, 0))
        self.swatches[key] = (canvas, colors)

    def drawSwatches(self, key):
        canvas, colors = self.swatches[key]
        canvas.delete("all")
        current = self.look[key].lower()
        for index, color in enumerate(colors):
            left = index * (SWATCH + SWATCH_GAP) + 2
            selected = color.lower() == current
            canvas.create_rectangle(left, 2, left + SWATCH, 2 + SWATCH, fill=color,
                                    outline="#ffffff" if selected else theme.BORDER, width=2 if selected else 1)

    def onSwatchClick(self, event, key, colors):
        index = int((event.x - 2) // (SWATCH + SWATCH_GAP))
        if 0 <= index < len(colors):
            self.setValue(key, colors[index])

    def pickCustomColor(self, key):
        rgb, color = colorchooser.askcolor(color=self.look[key], parent=self.window, title="Pick a color")
        if color:
            self.setValue(key, color)

    def setValue(self, key, value):
        self.look[key] = value
        self.refresh()

    def setPose(self, pose):
        self.pose = pose
        self.drawPreview()

    def flip(self):
        self.facing = -self.facing
        self.drawPreview()

    def randomize(self):
        self.look = randomLook()
        self.refresh()

    def reset(self):
        self.look = dict(self.character.look)
        self.refresh()

    # Makes every dropdown, swatch and the preview match self.look
    def refresh(self):
        for key, dropdown in self.dropdowns.items():
            dropdown.set(self.look[key].capitalize())
        for key in self.swatches:
            self.drawSwatches(key)
        self.drawPreview()

    def drawPreview(self):
        self.preview.delete("fighter")
        drawFighter(self.preview, self.PREVIEW_WIDTH / 2, self.PREVIEW_GROUND, self.look, self.facing, self.pose, scale=1.5)

    def save(self):
        self.character.look = dict(self.look)
        self.window.destroy()
        self.onSave()
