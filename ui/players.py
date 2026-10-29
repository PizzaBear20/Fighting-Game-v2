import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from core.players import addPlayer, renamePlayer, removePlayer, fighterCount
from ui import theme


# A small window for adding, renaming and removing players. Changes happen right away
class PlayersWindow:
    # players and characters are changed in place. onChange(message) is called after each change
    def __init__(self, parent, players, characters, onChange):
        self.players = players
        self.characters = characters
        self.onChange = onChange

        self.window = tk.Toplevel(parent)
        self.window.title("Players")
        self.window.configure(bg=theme.BG)
        self.window.resizable(False, False)
        self.window.transient(parent)

        playersPanel, body = theme.panel(self.window, "Players")
        playersPanel.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")

        addRow = tk.Frame(body, bg=theme.PANEL)
        addRow.pack(fill="x")
        self.nameEntry = theme.entry(addRow, width=18)
        self.nameEntry.pack(side="left", fill="x", expand=True, ipady=4)
        self.nameEntry.bind("<Return>", lambda event: self.add())
        ttk.Button(addRow, text="Add", style="Accent.TButton", command=self.add).pack(side="left", padx=(8, 0))

        self.playerList = tk.Listbox(body, height=8, width=30, bg=theme.PANEL_LIGHT, fg=theme.TEXT, relief="flat",
                                     highlightthickness=0, selectbackground=theme.BLUE, selectforeground="#ffffff",
                                     font=theme.BODY_FONT, activestyle="none", exportselection=False)
        self.playerList.pack(fill="both", expand=True, pady=(12, 0))
        self.playerList.bind("<<ListboxSelect>>", lambda event: self.updateButtons())
        self.playerList.bind("<Double-Button-1>", lambda event: self.rename())

        buttonRow = tk.Frame(body, bg=theme.PANEL)
        buttonRow.pack(fill="x", pady=(12, 0))
        self.renameButton = ttk.Button(buttonRow, text="Rename", command=self.rename)
        self.renameButton.pack(side="left")
        self.removeButton = ttk.Button(buttonRow, text="Remove", style="Small.TButton", command=self.remove)
        self.removeButton.pack(side="left", padx=(8, 0))
        ttk.Button(buttonRow, text="Done", style="Accent.TButton", command=self.window.destroy).pack(side="right")

        theme.label(body, "Removing a player keeps their fighters as Unassigned.", fg=theme.MUTED,
                    font=theme.SMALL_FONT).pack(anchor="w", pady=(10, 0))

        self.window.bind("<Escape>", lambda event: self.window.destroy())
        self.refresh()
        self.nameEntry.focus_set()
        self.window.grab_set()

    def refresh(self, selected=None):
        self.playerList.delete(0, tk.END)
        for player in self.players:
            count = fighterCount(self.characters, player)
            self.playerList.insert(tk.END, f"{player}  ·  {count} fighter{'s' if count != 1 else ''}")
        if not self.players:
            self.playerList.insert(tk.END, "No players yet. Add one above!")
            self.playerList.itemconfig(0, fg=theme.MUTED, selectbackground=theme.PANEL_LIGHT, selectforeground=theme.MUTED)
        if selected in self.players:
            index = self.players.index(selected)
            self.playerList.selection_set(index)
            self.playerList.see(index)
        self.updateButtons()

    def selectedPlayer(self):
        selection = self.playerList.curselection()
        if selection and selection[0] < len(self.players):
            return self.players[selection[0]]
        return None

    def updateButtons(self):
        state = ["!disabled"] if self.selectedPlayer() else ["disabled"]
        self.renameButton.state(state)
        self.removeButton.state(state)

    def add(self):
        try:
            name = addPlayer(self.players, self.nameEntry.get())
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self.window)
            return
        self.nameEntry.delete(0, tk.END)
        self.refresh(name)
        self.onChange(f"{name} joined as a player!")

    def rename(self):
        oldName = self.selectedPlayer()
        if oldName is None:
            return
        newName = simpledialog.askstring("Rename player", f"New name for {oldName}:", initialvalue=oldName,
                                         parent=self.window)
        if newName is None or newName.strip() == oldName:
            return
        try:
            newName = renamePlayer(self.players, self.characters, oldName, newName)
        except ValueError as error:
            messagebox.showerror("Error", str(error), parent=self.window)
            return
        self.refresh(newName)
        self.onChange(f"{oldName} is now called {newName}.")

    def remove(self):
        name = self.selectedPlayer()
        if name is None:
            return
        count = fighterCount(self.characters, name)
        question = f"Remove {name} from the players?"
        if count:
            question += f"\n\nTheir {count} fighter{'s' if count != 1 else ''} will stay on the roster as Unassigned."
        if not messagebox.askyesno("Remove player", question, parent=self.window):
            return
        removePlayer(self.players, self.characters, name)
        self.refresh()
        self.onChange(f"{name} was removed from the players.")
