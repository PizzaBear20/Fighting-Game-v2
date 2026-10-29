import math
import random
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

from core.character import (randomLook, randomColors, applyPreset, PRESETS, BUILDS, GLOVES, FACES, FACE_GEAR, HAIR_STYLES,
                            FACIAL_HAIR, HEADWEAR, OUTFITS, PANTS, SHOES, CAPES, AURAS, COLOR_CHOICES, SKIN_TONES,
                            HAIR_COLORS, EYE_COLORS)
from ui import theme
from ui.drawing import drawArena, drawFighter, darker, mix, readable


# Each tab: (tab name, [(label, look key, choices, tile zoom), ...])
# If the choices are colors, the row is a line of color swatches (and has no tile zoom).
# Otherwise each choice gets a picture tile, zoomed in on the part of the fighter it changes
TABS = [
    ("Body", [
        ("Build", "build", BUILDS, "body"),
        ("Body color", "bodyColor", COLOR_CHOICES),
        ("Skin", "skinColor", SKIN_TONES),
        ("Gloves", "gloveStyle", GLOVES, "hands"),
        ("Glove color", "gloveColor", COLOR_CHOICES),
    ]),
    ("Face", [
        ("Expression", "face", FACES, "head"),
        ("Eye color", "eyeColor", EYE_COLORS),
        ("Face gear", "faceGear", FACE_GEAR, "head"),
        ("Gear color", "faceGearColor", COLOR_CHOICES),
    ]),
    ("Hair", [
        ("Hair style", "hairStyle", HAIR_STYLES, "head"),
        ("Hair color", "hairColor", HAIR_COLORS + COLOR_CHOICES[:10]),
        ("Facial hair", "facialHair", FACIAL_HAIR, "head"),
    ]),
    ("Outfit", [
        ("Top", "outfit", OUTFITS, "body"),
        ("Top color", "outfitColor", COLOR_CHOICES),
        ("Pants", "pants", PANTS, "legs"),
        ("Pants color", "pantsColor", COLOR_CHOICES),
        ("Shoes", "shoes", SHOES, "feet"),
        ("Shoe color", "shoeColor", COLOR_CHOICES),
    ]),
    ("Gear", [
        ("Headwear", "headwear", HEADWEAR, "hat"),
        ("Headwear color", "headwearColor", COLOR_CHOICES),
        ("Back", "cape", CAPES, "body"),
        ("Back color", "capeColor", COLOR_CHOICES),
        ("Aura", "aura", AURAS, "aura"),
        ("Aura color", "auraColor", COLOR_CHOICES),
    ]),
]
PRESETS_TAB = "Presets"

# How tiles zoom in: (scale, the point on the fighter that goes in the middle of the tile, pose)
TILE_ZOOM = {
    "head": (1.35, (-4, -110), "stand"),
    "hat": (1.05, (0, -125), "stand"),
    "body": (0.5, (-4, -66), "stand"),
    "aura": (0.4, (0, -72), "stand"),
    "hands": (1.2, (58, -84), "punch"),
    "legs": (0.75, (0, -36), "stand"),
    "feet": (1.3, (4, -12), "stand"),
    "preset": (0.72, (-2, -70), "stand"),
}

# Color rows only matter while that part is worn. color key -> the part it colors
COLOR_OF = {
    "gloveColor": "gloveStyle",
    "faceGearColor": "faceGear",
    "outfitColor": "outfit",
    "pantsColor": "pants",
    "shoeColor": "shoes",
    "headwearColor": "headwear",
    "capeColor": "cape",
    "auraColor": "aura",
}
NOT_WORN = ("none", "bare")

# Things taken off in some tiles so you can see the part the tile is about (no hat over the hair styles)
HIDE_IN_TILES = {
    "hairStyle": {"headwear": "none"},
    "face": {"faceGear": "none"},
    "facialHair": {"faceGear": "none"},
}

# Option names that need more than a capital letter
OPTION_NAMES = {"tophat": "Top hat", "batwings": "Bat wings", "eyepatch": "Eye patch"}

def optionName(option):
    return OPTION_NAMES.get(option, option.capitalize())

TILE_WIDTH = 70
TILE_HEIGHT = 80
PRESET_WIDTH = 108
PRESET_HEIGHT = 128
CAPTION_HEIGHT = 18
TILES_PER_ROW = 6
PRESETS_PER_ROW = 4
TILE_SHADOW = darker(theme.PANEL_LIGHT, 0.25)
SWATCH = 18
SWATCH_GAP = 4


# A clickable picture of the fighter wearing one choice (or one preset)
class Tile:
    def __init__(self, parent, customizer, key, value, zoom, caption, width=TILE_WIDTH, height=TILE_HEIGHT):
        self.customizer = customizer
        self.key = key
        self.value = value
        self.zoom = zoom
        self.caption = caption
        self.width = width
        self.height = height
        self.hovered = False
        self.selected = False
        self.canvas = tk.Canvas(parent, width=width, height=height, bg=theme.PANEL_LIGHT, cursor="hand2",
                                highlightthickness=2, highlightbackground=theme.BORDER)
        self.canvas.bind("<Button-1>", lambda event: customizer.chooseTile(self))
        self.canvas.bind("<Enter>", lambda event: customizer.hoverTile(self, True))
        self.canvas.bind("<Leave>", lambda event: customizer.hoverTile(self, False))

    # The look you'd get by clicking this tile
    def lookWith(self, look):
        if self.key == "preset":
            return applyPreset(self.customizer.ownLook, self.value)
        newLook = dict(look)
        newLook[self.key] = self.value
        return newLook

    def draw(self, look):
        tileLook = self.lookWith(look)
        selected = tileLook == look
        tileLook.update(HIDE_IN_TILES.get(self.key, {}))
        canvas = self.canvas
        canvas.delete("all")
        scale, (centerX, centerY), pose = TILE_ZOOM[self.zoom]
        pictureHeight = self.height - CAPTION_HEIGHT
        drawFighter(canvas, self.width / 2 - centerX * scale, pictureHeight / 2 - centerY * scale, tileLook,
                    pose=pose, scale=scale, tag="tile", shadow=TILE_SHADOW)
        canvas.create_rectangle(0, pictureHeight, self.width + 4, self.height + 4,
                                fill=theme.BLUE if selected else theme.PANEL, outline="")
        canvas.create_text(self.width / 2 + 2, pictureHeight + CAPTION_HEIGHT / 2 + 1, text=self.caption,
                           fill="#ffffff" if selected else theme.MUTED,
                           font=(theme.FONT, 10, "bold" if selected else "normal"))
        self.selected = selected
        self.drawBorder()

    def drawBorder(self):
        if self.selected:
            color = theme.BLUE
        elif self.hovered:
            color = theme.MUTED
        else:
            color = theme.BORDER
        self.canvas.config(highlightbackground=color)


class CustomizeWindow:
    PREVIEW_WIDTH = 300
    PREVIEW_HEIGHT = 380
    PREVIEW_GROUND = 330
    lastTab = PRESETS_TAB  # the window opens on whichever tab you used last time

    # onSave() is called after the new look is saved onto the character
    def __init__(self, parent, character, onSave):
        self.character = character
        self.onSave = onSave
        self.look = dict(character.look)
        # Presets keep the skin, hair and eye colors from this look: the last one picked without a preset.
        # That way trying the Demon preset doesn't leave every other preset with red skin
        self.ownLook = self.look
        self.undoStack = []
        self.redoStack = []
        self.pose = "stand"
        self.facing = 1
        self.phase = 0
        self.hovered = None
        self.tiles = {}       # tab name -> list of tiles on that tab
        self.swatches = {}    # look key -> (canvas, colors, row label)
        self.tabFrames = {}
        self.tabButtons = {}

        self.window = tk.Toplevel(parent)
        self.window.title(f"Customize {character.name}")
        self.window.configure(bg=theme.BG)
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)

        # ----- left: live preview -----
        previewPanel, previewBody = theme.panel(self.window, "Preview")
        previewPanel.grid(row=0, column=0, padx=(16, 8), pady=16, sticky="ns")

        self.nameLabel = theme.label(previewBody, character.name, font=theme.NAME_FONT)
        self.nameLabel.pack(anchor="w", pady=(0, 8))
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
        theme.label(previewBody, "Point at a tile to try it on, click to pick it.", fg=theme.MUTED,
                    font=theme.SMALL_FONT).pack(anchor="w", pady=(10, 0))

        # ----- right: tabs full of options -----
        optionsPanel, optionsBody = theme.panel(self.window)
        optionsPanel.grid(row=0, column=1, padx=(8, 16), pady=16, sticky="nsew")

        tabBar = tk.Frame(optionsBody, bg=theme.PANEL)
        tabBar.grid(row=0, column=0, sticky="ew")
        for tabName in [PRESETS_TAB] + [tab[0] for tab in TABS]:
            button = tk.Label(tabBar, text=tabName, bg=theme.PANEL, fg=theme.MUTED, font=theme.BOLD_FONT,
                              padx=12, pady=6, cursor="hand2")
            button.pack(side="left")
            button.bind("<Button-1>", lambda event, tabName=tabName: self.showTab(tabName))
            self.tabButtons[tabName] = button
        ttk.Button(tabBar, text="🎲 Shuffle tab", style="Small.TButton", command=self.shuffleTab).pack(side="right")
        tk.Frame(optionsBody, bg=theme.BORDER, height=1).grid(row=1, column=0, sticky="ew", pady=(0, 12))

        pages = tk.Frame(optionsBody, bg=theme.PANEL)
        pages.grid(row=2, column=0, sticky="nsew")
        self.buildPresetsTab(pages)
        for tabName, rows in TABS:
            self.buildTab(pages, tabName, rows)

        # ----- bottom buttons -----
        buttonRow = tk.Frame(self.window, bg=theme.BG)
        buttonRow.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 16))
        ttk.Button(buttonRow, text="🎲 Randomize", command=self.randomize).pack(side="left")
        ttk.Button(buttonRow, text="🎨 New Colors", command=self.newColors).pack(side="left", padx=(8, 0))
        self.undoButton = ttk.Button(buttonRow, text="↶ Undo", command=self.undo)
        self.undoButton.pack(side="left", padx=(16, 0))
        self.redoButton = ttk.Button(buttonRow, text="↷ Redo", command=self.redo)
        self.redoButton.pack(side="left", padx=(8, 0))
        ttk.Button(buttonRow, text="Reset", command=self.reset).pack(side="left", padx=(8, 0))
        ttk.Button(buttonRow, text="Save Look", style="Accent.TButton", command=self.save).pack(side="right")
        ttk.Button(buttonRow, text="Cancel", command=self.cancel).pack(side="right", padx=8)

        # keyboard shortcuts: Cmd+Z / Cmd+Shift+Z on a Mac, Ctrl+Z / Ctrl+Shift+Z everywhere else
        if self.window.tk.call("tk", "windowingsystem") == "aqua":
            modifier = "Command"
        else:
            modifier = "Control"
        self.window.bind(f"<{modifier}-z>", lambda event: self.undo())
        self.window.bind(f"<{modifier}-Z>", lambda event: self.redo())
        self.window.bind("<Escape>", lambda event: self.cancel())

        self.showTab(CustomizeWindow.lastTab)
        self.refresh()
        self.animate()
        self.window.focus_set()
        self.window.grab_set()  # finish customizing before going back to the main window

    # ---------- building the tabs ----------

    def buildPresetsTab(self, pages):
        frame = tk.Frame(pages, bg=theme.PANEL)
        frame.grid(row=0, column=0, sticky="nsew")
        self.tabFrames[PRESETS_TAB] = frame
        theme.label(frame, "Start from a ready-made style, then change anything you like.", fg=theme.MUTED,
                    font=theme.SMALL_FONT).grid(row=0, column=0, columnspan=PRESETS_PER_ROW, sticky="w", pady=(0, 10))
        tiles = []
        for index, (name, preset) in enumerate(PRESETS):
            tile = Tile(frame, self, "preset", preset, "preset", name, PRESET_WIDTH, PRESET_HEIGHT)
            tile.canvas.grid(row=1 + index // PRESETS_PER_ROW, column=index % PRESETS_PER_ROW, padx=(0, 8), pady=(0, 8))
            tiles.append(tile)
        self.tiles[PRESETS_TAB] = tiles

    def buildTab(self, pages, tabName, rows):
        frame = tk.Frame(pages, bg=theme.PANEL)
        frame.grid(row=0, column=0, sticky="nsew")
        self.tabFrames[tabName] = frame
        tiles = []
        for row, (text, key, choices, *zoom) in enumerate(rows):
            rowLabel = theme.label(frame, text, fg=theme.MUTED, font=theme.SMALL_FONT)
            rowLabel.grid(row=row, column=0, sticky="nw", padx=(0, 12), pady=(4, 8))
            if choices[0].startswith("#"):
                self.addSwatches(frame, row, key, choices, rowLabel)
            else:
                tileFrame = tk.Frame(frame, bg=theme.PANEL)
                tileFrame.grid(row=row, column=1, sticky="w", pady=(0, 8))
                for index, choice in enumerate(choices):
                    tile = Tile(tileFrame, self, key, choice, zoom[0], optionName(choice))
                    tile.canvas.grid(row=index // TILES_PER_ROW, column=index % TILES_PER_ROW, padx=(0, 6), pady=(0, 6))
                    tiles.append(tile)
        self.tiles[tabName] = tiles

    def addSwatches(self, parent, row, key, colors, rowLabel):
        frame = tk.Frame(parent, bg=theme.PANEL)
        frame.grid(row=row, column=1, sticky="w", pady=(0, 12))
        # one extra space at the end shows a custom color picked with "+"
        width = (len(colors) + 1) * (SWATCH + SWATCH_GAP)
        canvas = tk.Canvas(frame, width=width, height=SWATCH + 4, bg=theme.PANEL, highlightthickness=0, cursor="hand2")
        canvas.pack(side="left")
        canvas.bind("<Button-1>", lambda event: self.onSwatchClick(event, key, colors))
        ttk.Button(frame, text="+", style="Small.TButton", width=2,
                   command=lambda: self.pickCustomColor(key)).pack(side="left", padx=(4, 0))
        self.swatches[key] = (canvas, colors, rowLabel)

    # ---------- drawing ----------

    def drawSwatches(self, key):
        canvas, colors, rowLabel = self.swatches[key]
        canvas.delete("all")
        current = self.look[key].lower()
        # grayed out while the part it colors isn't being worn
        worn = key not in COLOR_OF or self.look[COLOR_OF[key]] not in NOT_WORN
        rowLabel.config(fg=theme.MUTED if worn else theme.BORDER)
        shownColors = list(colors)
        if current not in [color.lower() for color in colors]:
            shownColors.append(current)
        for index, color in enumerate(shownColors):
            left = index * (SWATCH + SWATCH_GAP) + 2
            selected = color.lower() == current
            if not worn:
                color = mix(color, theme.PANEL, 0.7)
            canvas.create_rectangle(left, 2, left + SWATCH, 2 + SWATCH, fill=color,
                                    outline="#ffffff" if selected else theme.BORDER, width=2 if selected else 1)

    def drawPreview(self):
        self.preview.delete("fighter")
        look = self.look
        if self.hovered:
            look = self.hovered.lookWith(self.look)
        bounce = 0
        if self.pose != "down":
            bounce = round(math.sin(self.phase / 4) * 2)  # a gentle bounce, like on the fighter card
        drawFighter(self.preview, self.PREVIEW_WIDTH / 2, self.PREVIEW_GROUND + bounce, look, self.facing, self.pose, scale=1.5)

    def animate(self):
        self.phase += 1
        self.drawPreview()
        self.animationId = self.window.after(90, self.animate)

    # Makes the tiles, swatches, buttons and preview match self.look
    def refresh(self):
        for tile in self.tiles[self.currentTab]:
            tile.draw(self.look)
        for key in self.swatches:
            self.drawSwatches(key)
        self.nameLabel.config(fg=readable(self.look["bodyColor"]))
        self.undoButton.state(["!disabled"] if self.undoStack else ["disabled"])
        self.redoButton.state(["!disabled"] if self.redoStack else ["disabled"])
        self.drawPreview()

    # ---------- tabs and tiles ----------

    def showTab(self, tabName):
        self.currentTab = tabName
        CustomizeWindow.lastTab = tabName
        self.hovered = None
        self.tabFrames[tabName].tkraise()
        for name, button in self.tabButtons.items():
            if name == tabName:
                button.config(bg=theme.PANEL_LIGHT, fg=theme.TEXT)
            else:
                button.config(bg=theme.PANEL, fg=theme.MUTED)
        for tile in self.tiles[tabName]:
            tile.draw(self.look)

    def chooseTile(self, tile):
        self.setLook(tile.lookWith(self.look), fromPreset=tile.key == "preset")

    # Pointing at a tile shows it on the preview without picking it
    def hoverTile(self, tile, isOver):
        tile.hovered = isOver
        tile.drawBorder()
        if isOver:
            self.hovered = tile
        elif self.hovered is tile:
            self.hovered = None
        self.drawPreview()

    # ---------- changing the look ----------

    # Every change goes through here so it can be undone
    def setLook(self, newLook, fromPreset=False):
        if newLook == self.look:
            return
        self.undoStack.append(self.look)
        self.redoStack.clear()
        self.look = newLook
        if not fromPreset:
            self.ownLook = newLook
        self.refresh()

    def onSwatchClick(self, event, key, colors):
        index = int((event.x - 2) // (SWATCH + SWATCH_GAP))
        if 0 <= index < len(colors):
            self.setValue(key, colors[index])

    def pickCustomColor(self, key):
        rgb, color = colorchooser.askcolor(color=self.look[key], parent=self.window, title="Pick a color")
        if color:
            self.setValue(key, color)

    def setValue(self, key, value):
        newLook = dict(self.look)
        newLook[key] = value
        self.setLook(newLook)

    def randomize(self):
        self.setLook(randomLook())

    # Keeps every style but picks a new set of matching colors (the skin stays the same)
    def newColors(self):
        newLook = dict(self.look)
        newLook.update(randomColors(self.look["skinColor"]))
        self.setLook(newLook)

    # Randomizes only the things on the tab you're looking at
    def shuffleTab(self):
        tiles = self.tiles[self.currentTab]
        if self.currentTab == PRESETS_TAB:
            others = [tile for tile in tiles if not tile.selected]
            self.chooseTile(random.choice(others))
            return
        rows = dict(TABS)[self.currentTab]
        randomOne = randomLook()
        newLook = dict(self.look)
        for text, key, *rest in rows:
            newLook[key] = randomOne[key]
        self.setLook(newLook)

    def undo(self):
        if self.undoStack:
            self.redoStack.append(self.look)
            self.look = self.undoStack.pop()
            self.refresh()

    def redo(self):
        if self.redoStack:
            self.undoStack.append(self.look)
            self.look = self.redoStack.pop()
            self.refresh()

    def reset(self):
        self.setLook(dict(self.character.look))

    def setPose(self, pose):
        self.pose = pose
        self.drawPreview()

    def flip(self):
        self.facing = -self.facing
        self.drawPreview()

    # ---------- closing ----------

    def close(self):
        self.window.after_cancel(self.animationId)
        self.window.destroy()

    def cancel(self):
        if self.look != self.character.look:
            if not messagebox.askyesno("Discard changes?", f"Close without saving {self.character.name}'s new look?",
                                       parent=self.window):
                return
        self.close()

    def save(self):
        self.character.look = dict(self.look)
        self.close()
        self.onSave()
