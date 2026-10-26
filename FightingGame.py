import json
import math
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox

import theme
from character import Character, ATTRIBUTE_CHOICES, cleanAttribute
from customize import CustomizeWindow
from drawing import drawArena, drawFighter, darker, readable
from fight import FightWindow, describeMove, moveCost

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_data.json")
MAX_NAME_LENGTH = 16

# Dictionary of name -> Character
characters = {}

# History list (oldest first)
history = []

# Name of the character shown on the fighter card
selectedName = None


# ---------- saving and loading ----------

def saveGame():
    data = {
        "characters": [character.toDict() for character in characters.values()],
        "history": history,
    }
    # write to a temporary file first so a crash can't leave a half-written save
    tempFile = SAVE_FILE + ".tmp"
    with open(tempFile, "w") as file:
        json.dump(data, file, indent=2)
    os.replace(tempFile, SAVE_FILE)

def loadGame():
    if not os.path.exists(SAVE_FILE):
        return
    try:
        with open(SAVE_FILE) as file:
            data = json.load(file)
        for characterData in data["characters"]:
            character = Character.fromDict(characterData)
            characters[character.name] = character
        history.extend(data.get("history", []))
    except (ValueError, KeyError, TypeError) as error:
        characters.clear()
        history.clear()
        brokenFile = SAVE_FILE.replace(".json", "_broken.json")
        os.replace(SAVE_FILE, brokenFile)
        messagebox.showwarning("Save file problem", f"Your save file couldn't be read ({error}).\n\n"
                               f"It was renamed to {os.path.basename(brokenFile)} and a new game was started.")


# ---------- helpers ----------

# Names sorted from strongest to weakest
def rankedNames():
    return sorted(characters, key=lambda name: characters[name].powerLevel(), reverse=True)

def rankOf(name):
    return rankedNames().index(name) + 1

def setStatus(text, color=theme.TEXT):
    statusLabel.config(text=text, fg=color)

def selectedCharacter():
    if selectedName in characters:
        return characters[selectedName]
    return None

def selectCharacter(name):
    global selectedName
    selectedName = name
    drawRoster()
    updateCard()


# ---------- roster (left) ----------

ROW_HEIGHT = 76

def drawRoster():
    rosterCanvas.delete("all")
    width = int(rosterCanvas.cget("width"))
    names = rankedNames()
    if not names:
        rosterCanvas.create_text(width / 2, 60, text="No fighters yet.\nCreate one below!", fill=theme.MUTED,
                                 font=theme.BODY_FONT, justify="center")
    for index, name in enumerate(names):
        character = characters[name]
        top = index * ROW_HEIGHT
        selected = name == selectedName
        background = theme.PANEL_LIGHT if selected else theme.PANEL
        rosterCanvas.create_rectangle(0, top, width, top + ROW_HEIGHT - 2, fill=background, outline="")
        if selected:
            rosterCanvas.create_rectangle(0, top, 4, top + ROW_HEIGHT - 2, fill=readable(character.look["bodyColor"]), outline="")
        drawFighter(rosterCanvas, 44, top + 68, character.look, scale=0.42, tag="mini", shadow=darker(background, 0.25))
        rosterCanvas.create_text(86, top + 27, text=name, anchor="w", fill=theme.TEXT, font=theme.BOLD_FONT)
        details = f"#{index + 1}  ·  Power {character.powerLevel()}"
        if character.specialMoves:
            details += f"  ·  ★{len(character.specialMoves)}"
        rosterCanvas.create_text(86, top + 49, text=details, anchor="w", fill=theme.MUTED, font=theme.SMALL_FONT)
        rosterCanvas.create_line(12, top + ROW_HEIGHT - 1, width - 12, top + ROW_HEIGHT - 1, fill=theme.BORDER)
    rosterCanvas.config(scrollregion=(0, 0, width, max(len(names) * ROW_HEIGHT, 1)))

def rosterNameAt(event):
    index = int(rosterCanvas.canvasy(event.y) // ROW_HEIGHT)
    names = rankedNames()
    if 0 <= index < len(names):
        return names[index]
    return None

def onRosterClick(event):
    name = rosterNameAt(event)
    if name:
        selectCharacter(name)

def onRosterDoubleClick(event):
    name = rosterNameAt(event)
    if name:
        selectCharacter(name)
        onCustomizeClick()

def onRosterScroll(event):
    rosterCanvas.yview_scroll(-1 * event.delta, "units")

def onCreateCharacterClick(event=None):
    name = createCharacterEntry.get().strip()
    if name == "":
        messagebox.showerror("Error", "Type a name for the new character")
        return
    if len(name) > MAX_NAME_LENGTH:
        messagebox.showerror("Error", f"Names can be at most {MAX_NAME_LENGTH} letters long")
        return
    if name in characters:
        messagebox.showerror("Error", f"There is already a character named '{name}'")
        return
    character = Character(name)
    character.stats()
    characters[name] = character
    createCharacterEntry.delete(0, tk.END)
    selectCharacter(name)
    refreshAll()
    setStatus(f"{name} joined the roster! Click Customize Look to change how they look.", theme.GREEN)


# ---------- fighter card (middle) ----------

PORTRAIT_WIDTH = 210
PORTRAIT_HEIGHT = 260
PORTRAIT_GROUND = 228
STATS = [("Health", "health"), ("Strength", "strength"), ("Speed", "speed"), ("Mana", "mana"), ("Battle IQ", "battleIQ"), ("Defense", "defense")]
portraitPhase = 0

def drawPortrait():
    portraitCanvas.delete("portrait")
    character = selectedCharacter()
    if character is None:
        portraitCanvas.create_text(PORTRAIT_WIDTH / 2, PORTRAIT_HEIGHT / 2 - 20, text="?", fill=theme.MUTED,
                                   font=(theme.FONT, 64, "bold"), tags="portrait")
        return
    # a gentle bounce so the fighter looks ready to go
    bounce = round(math.sin(portraitPhase / 4) * 2)
    drawFighter(portraitCanvas, PORTRAIT_WIDTH / 2, PORTRAIT_GROUND + bounce, character.look, scale=1.25, tag="portrait",
                shadow="#262a40")

def animatePortrait():
    global portraitPhase
    portraitPhase += 1
    drawPortrait()
    root.after(90, animatePortrait)

def drawStatBars():
    statsCanvas.delete("all")
    character = selectedCharacter()
    if character is None:
        return
    width = int(statsCanvas.cget("width"))
    biggest = 20
    for other in characters.values():
        for label, stat in STATS:
            biggest = max(biggest, getattr(other, stat))
    for index, (label, stat) in enumerate(STATS):
        y = 14 + index * 26
        value = getattr(character, stat)
        barLeft = 84
        barRight = width - 40
        statsCanvas.create_text(0, y, text=label, anchor="w", fill=theme.MUTED, font=theme.SMALL_FONT)
        statsCanvas.create_rectangle(barLeft, y - 5, barRight, y + 5, fill=theme.PANEL_LIGHT, outline="")
        fillRight = barLeft + (barRight - barLeft) * value / biggest
        statsCanvas.create_rectangle(barLeft, y - 5, fillRight, y + 5, fill=theme.STAT_COLORS[stat], outline="")
        statsCanvas.create_text(width, y, text=str(value), anchor="e", fill=theme.TEXT, font=theme.BOLD_FONT)

def updateCard():
    character = selectedCharacter()
    cardButtons = [customizeButton, trainButton, trainTenButton, deleteButton]
    if character is None:
        nameLabel.config(text="No fighter selected", fg=theme.TEXT)
        subtitleLabel.config(text="Create a fighter to get started")
        theme.setText(movesText, [])
        for button in cardButtons:
            button.state(["disabled"])
    else:
        nameLabel.config(text=character.name, fg=readable(character.look["bodyColor"]))
        subtitleLabel.config(text=f"Power Level {character.powerLevel()}  ·  Rank #{rankOf(character.name)} of {len(characters)}")
        if character.specialMoves:
            lines = []
            for move in character.specialMoves:
                lines.append((f"★ {move['name']}", "name"))
                lines.append((f"   {move['type']} · {moveCost(move)} MP · {describeMove(move)}\n", move['type']))
            theme.setText(movesText, lines)
        else:
            theme.setText(movesText, [("No special moves yet. Keep training to unlock them!", "muted")])
        for button in cardButtons:
            button.state(["!disabled"])
    drawPortrait()
    drawStatBars()

def onCustomizeClick():
    character = selectedCharacter()
    if character is None:
        return
    def onSave():
        refreshAll()
        setStatus(f"Saved {character.name}'s new look!", theme.GREEN)
    CustomizeWindow(root, character, onSave)

def onTrainClick(times):
    character = selectedCharacter()
    if character is None:
        return
    attribute = cleanAttribute(trainAttribute.get())
    movesBefore = len(character.specialMoves)
    message = character.trainMany(attribute, times)
    refreshAll()
    if len(character.specialMoves) > movesBefore:
        setStatus("★ " + message, theme.GOLD)
    else:
        setStatus(message)

def onDeleteClick():
    character = selectedCharacter()
    if character is None:
        return
    if not messagebox.askyesno("Delete fighter", f"Delete {character.name}? This can't be undone."):
        return
    del characters[character.name]
    names = rankedNames()
    selectCharacter(names[0] if names else None)
    refreshAll()
    setStatus(f"{character.name} left the roster.")


# ---------- fight and training (right) ----------

MATCHUP_WIDTH = 330
MATCHUP_HEIGHT = 150
MATCHUP_GROUND = 122

def updateFightChoices():
    names = list(characters)
    for dropdown in (fighter1Choice, fighter2Choice):
        dropdown.config(values=names)
    if fighter1Choice.get() not in characters:
        fighter1Choice.set(names[0] if names else "")
    if fighter2Choice.get() not in characters or fighter2Choice.get() == fighter1Choice.get():
        others = [name for name in names if name != fighter1Choice.get()]
        fighter2Choice.set(others[0] if others else "")
    drawMatchup()

def drawMatchup():
    matchupCanvas.delete("fighters")
    for dropdown, x, facing in ((fighter1Choice, 85, 1), (fighter2Choice, MATCHUP_WIDTH - 85, -1)):
        name = dropdown.get()
        if name in characters:
            look = characters[name].look
            drawFighter(matchupCanvas, x, MATCHUP_GROUND, look, facing, scale=0.62, tag="fighters")
            matchupCanvas.create_text(x, MATCHUP_GROUND + 16, text=name, fill=readable(look["bodyColor"]),
                                      font=theme.BOLD_FONT, tags="fighters")
        else:
            matchupCanvas.create_text(x, MATCHUP_GROUND - 40, text="?", fill=theme.MUTED, font=(theme.FONT, 36, "bold"), tags="fighters")
    matchupCanvas.create_text(MATCHUP_WIDTH / 2 + 2, 62, text="VS", fill="#000000", font=(theme.FONT, 26, "bold"), tags="fighters")
    matchupCanvas.create_text(MATCHUP_WIDTH / 2, 60, text="VS", fill=theme.GOLD, font=(theme.FONT, 26, "bold"), tags="fighters")

def onRandomMatchupClick():
    if len(characters) < 2:
        messagebox.showerror("Error", "You need at least 2 fighters for a fight")
        return
    name1, name2 = random.sample(list(characters), 2)
    fighter1Choice.set(name1)
    fighter2Choice.set(name2)
    drawMatchup()

def onFightButtonClick():
    name1 = fighter1Choice.get()
    name2 = fighter2Choice.get()
    if len(characters) < 2:
        messagebox.showerror("Error", "You need at least 2 fighters for a fight")
        return
    if name1 not in characters or name2 not in characters:
        messagebox.showerror("Error", "Pick two fighters")
        return
    if name1 == name2:
        messagebox.showerror("Error", "A character can't fight themselves")
        return
    FightWindow(root, characters[name1], characters[name2], onFightFinished)

def onFightFinished(historyEvent):
    history.append(historyEvent)
    refreshAll()
    setStatus(historyEvent, theme.GOLD)

def onTrainEveryoneClick():
    if not characters:
        messagebox.showerror("Error", "Create some fighters first")
        return
    try:
        times = int(trainEveryoneTimes.get())
    except ValueError:
        messagebox.showerror("Error", "Type how many times to train as a number")
        return
    if times < 1 or times > 100:
        messagebox.showerror("Error", "Train between 1 and 100 times")
        return
    attribute = cleanAttribute(trainEveryoneAttribute.get())
    learned = []
    for character in characters.values():
        movesBefore = len(character.specialMoves)
        character.trainMany(attribute, times)
        for move in character.specialMoves[movesBefore:]:
            learned.append(f"{character.name} ({move['name']})")
    refreshAll()
    message = f"Everyone trained {times} time{'s' if times > 1 else ''} in {trainEveryoneAttribute.get()}."
    if learned:
        setStatus(f"★ {message} New special moves: " + ", ".join(learned), theme.GOLD)
    else:
        setStatus(message)

def updateHistory():
    if history:
        lines = [(f"• {event}\n", "newest" if index == 0 else "") for index, event in enumerate(reversed(history))]
    else:
        lines = [("No fights yet.", "muted")]
    theme.setText(historyText, lines)


# Redraws everything after something changes, then saves the game
def refreshAll():
    fightCount = len(history)
    countsLabel.config(text=f"{len(characters)} fighters  ·  {fightCount} fight{'s' if fightCount != 1 else ''}")
    drawRoster()
    updateCard()
    updateFightChoices()
    updateHistory()
    saveGame()


# ---------- GUI ----------

root = tk.Tk()
root.title("Fighting Game")
theme.setupStyles(root)

# header
header = tk.Frame(root, bg=theme.BG)
header.grid(row=0, column=0, columnspan=3, sticky="ew", padx=16, pady=(14, 6))
tk.Label(header, text="FIGHTING GAME", bg=theme.BG, fg=theme.TEXT, font=theme.TITLE_FONT).pack(side="left")
tk.Label(header, text="v2", bg=theme.BG, fg=theme.GOLD, font=(theme.FONT, 14, "bold")).pack(side="left", padx=(8, 0), pady=(8, 0))
countsLabel = tk.Label(header, bg=theme.BG, fg=theme.MUTED, font=theme.BODY_FONT)
countsLabel.pack(side="right")

# roster
rosterPanel, rosterBody = theme.panel(root, "Roster  ·  ranked by power")
rosterPanel.grid(row=1, column=0, sticky="nsew", padx=(16, 8), pady=8)
rosterBody.rowconfigure(0, weight=1)
rosterCanvas = tk.Canvas(rosterBody, width=250, height=420, bg=theme.PANEL, highlightthickness=0, cursor="hand2")
rosterCanvas.grid(row=0, column=0, sticky="ns")
rosterScroll = ttk.Scrollbar(rosterBody, orient="vertical", command=rosterCanvas.yview)
rosterScroll.grid(row=0, column=1, sticky="ns")
rosterCanvas.config(yscrollcommand=rosterScroll.set)
rosterCanvas.bind("<Button-1>", onRosterClick)
rosterCanvas.bind("<Double-Button-1>", onRosterDoubleClick)
rosterCanvas.bind("<MouseWheel>", onRosterScroll)

theme.label(rosterBody, "NEW FIGHTER", fg=theme.MUTED, font=theme.HEADING_FONT).grid(row=1, column=0, columnspan=2, sticky="w", pady=(12, 4))
createRow = tk.Frame(rosterBody, bg=theme.PANEL)
createRow.grid(row=2, column=0, columnspan=2, sticky="ew")
createCharacterEntry = theme.entry(createRow, width=16)
createCharacterEntry.pack(side="left", fill="x", expand=True, ipady=4)
createCharacterEntry.bind("<Return>", onCreateCharacterClick)
ttk.Button(createRow, text="Create", style="Accent.TButton", command=onCreateCharacterClick).pack(side="left", padx=(8, 0))

# fighter card
cardPanel, cardBody = theme.panel(root, "Fighter")
cardPanel.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)

portraitCanvas = tk.Canvas(cardBody, width=PORTRAIT_WIDTH, height=PORTRAIT_HEIGHT, bg=theme.PANEL, highlightthickness=0)
portraitCanvas.grid(row=0, column=0, sticky="n")
drawArena(portraitCanvas, PORTRAIT_WIDTH, PORTRAIT_HEIGHT, PORTRAIT_GROUND)

infoFrame = tk.Frame(cardBody, bg=theme.PANEL)
infoFrame.grid(row=0, column=1, sticky="nw", padx=(18, 0))
nameLabel = theme.label(infoFrame, font=theme.NAME_FONT)
nameLabel.pack(anchor="w")
subtitleLabel = theme.label(infoFrame, fg=theme.MUTED, font=theme.SMALL_FONT)
subtitleLabel.pack(anchor="w", pady=(0, 12))
statsCanvas = tk.Canvas(infoFrame, width=270, height=160, bg=theme.PANEL, highlightthickness=0)
statsCanvas.pack(anchor="w")

theme.label(cardBody, "SPECIAL MOVES", fg=theme.MUTED, font=theme.HEADING_FONT).grid(row=1, column=0, columnspan=2, sticky="w", pady=(14, 6))
movesText = theme.textBox(cardBody, height=5, width=40)
movesText.grid(row=2, column=0, columnspan=2, sticky="ew")
movesText.tag_config("name", foreground=theme.TEXT, font=theme.BOLD_FONT)
movesText.tag_config("muted", foreground=theme.MUTED)
for moveType, color in theme.MOVE_COLORS.items():
    movesText.tag_config(moveType, foreground=color)

actionRow = tk.Frame(cardBody, bg=theme.PANEL)
actionRow.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(14, 0))
customizeButton = ttk.Button(actionRow, text="🎨 Customize Look", style="Gold.TButton", command=onCustomizeClick)
customizeButton.pack(side="left")
deleteButton = ttk.Button(actionRow, text="Delete", style="Small.TButton", command=onDeleteClick)
deleteButton.pack(side="right")

trainRow = tk.Frame(cardBody, bg=theme.PANEL)
trainRow.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))
theme.label(trainRow, "Train", fg=theme.MUTED, font=theme.SMALL_FONT).pack(side="left", padx=(0, 8))
trainAttribute = ttk.Combobox(trainRow, values=ATTRIBUTE_CHOICES, state="readonly", width=10)
trainAttribute.set("Random")
trainAttribute.pack(side="left")
trainButton = ttk.Button(trainRow, text="Train", style="Accent.TButton", command=lambda: onTrainClick(1))
trainButton.pack(side="left", padx=(8, 0))
trainTenButton = ttk.Button(trainRow, text="Train ×10", command=lambda: onTrainClick(10))
trainTenButton.pack(side="left", padx=(8, 0))

# right column
rightColumn = tk.Frame(root, bg=theme.BG)
rightColumn.grid(row=1, column=2, sticky="nsew", padx=(8, 16), pady=8)
rightColumn.rowconfigure(2, weight=1)

fightPanel, fightBody = theme.panel(rightColumn, "Fight")
fightPanel.grid(row=0, column=0, sticky="ew")
matchupCanvas = tk.Canvas(fightBody, width=MATCHUP_WIDTH, height=MATCHUP_HEIGHT, bg=theme.PANEL, highlightthickness=0)
matchupCanvas.pack()
drawArena(matchupCanvas, MATCHUP_WIDTH, MATCHUP_HEIGHT, MATCHUP_GROUND)
chooseRow = tk.Frame(fightBody, bg=theme.PANEL)
chooseRow.pack(fill="x", pady=(10, 0))
fighter1Choice = ttk.Combobox(chooseRow, state="readonly", width=12)
fighter1Choice.pack(side="left")
theme.label(chooseRow, "vs", fg=theme.MUTED).pack(side="left", expand=True)
fighter2Choice = ttk.Combobox(chooseRow, state="readonly", width=12)
fighter2Choice.pack(side="right")
for dropdown in (fighter1Choice, fighter2Choice):
    dropdown.bind("<<ComboboxSelected>>", lambda event: drawMatchup())
fightButtons = tk.Frame(fightBody, bg=theme.PANEL)
fightButtons.pack(fill="x", pady=(10, 0))
ttk.Button(fightButtons, text="🎲 Random", command=onRandomMatchupClick).pack(side="left")
ttk.Button(fightButtons, text="FIGHT!", style="Fight.TButton", command=onFightButtonClick).pack(side="right")

trainEveryonePanel, trainEveryoneBody = theme.panel(rightColumn, "Train Everyone")
trainEveryonePanel.grid(row=1, column=0, sticky="ew", pady=16)
trainEveryoneTimes = ttk.Spinbox(trainEveryoneBody, from_=1, to=100, width=4)
trainEveryoneTimes.set(5)
trainEveryoneTimes.pack(side="left")
theme.label(trainEveryoneBody, "times in", fg=theme.MUTED, font=theme.SMALL_FONT).pack(side="left", padx=8)
trainEveryoneAttribute = ttk.Combobox(trainEveryoneBody, values=ATTRIBUTE_CHOICES, state="readonly", width=9)
trainEveryoneAttribute.set("Random")
trainEveryoneAttribute.pack(side="left")
ttk.Button(trainEveryoneBody, text="Go", style="Accent.TButton", command=onTrainEveryoneClick).pack(side="right")

historyPanel, historyBody = theme.panel(rightColumn, "Fight History")
historyPanel.grid(row=2, column=0, sticky="nsew")
historyText = theme.textBox(historyBody, height=6, width=36)
historyText.pack(fill="both", expand=True)
historyText.config(font=theme.SMALL_FONT)
historyText.tag_config("newest", foreground=theme.GOLD)
historyText.tag_config("muted", foreground=theme.MUTED)

# status bar
statusBar = tk.Frame(root, bg=theme.PANEL, highlightbackground=theme.BORDER, highlightthickness=1)
statusBar.grid(row=2, column=0, columnspan=3, sticky="ew", padx=16, pady=(8, 16))
statusLabel = tk.Label(statusBar, text="Welcome! Create fighters, customize them, train them, and make them fight.",
                       bg=theme.PANEL, fg=theme.MUTED, font=theme.SMALL_FONT, anchor="w")
statusLabel.pack(fill="x", padx=12, pady=8)

root.rowconfigure(1, weight=1)

loadGame()
names = rankedNames()
selectedName = names[0] if names else None
refreshAll()
animatePortrait()

root.mainloop()
