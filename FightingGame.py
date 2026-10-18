import random
import tkinter as tk
from tkinter import messagebox


class Character:
    def __init__(self, name):
        self.name = name
        self.specialMoves = []

    def stats(self):
        self.points = random.randrange(1, 21)
        self.health = 1
        self.strength = 1
        self.speed = 1
        self.mana = 1
        self.battleIQ = 1
        count = 1
        while count <= self.points:
            randomNum = random.randrange(1, 6)
            if randomNum == 1:
                self.health += 1
            elif randomNum == 2:
                self.strength += 1
            elif randomNum == 3:
                self.speed += 1
            elif randomNum == 4:
                self.mana += 1
            else:
                self.battleIQ += 1
            count += 1  # Increment count to avoid infinite loop

        
    def displayStats(self):
        specialMovesString = "\n".join(
            [f"Special Move: {move['name']}\n Type: {move['type']}\n Bonus Points: {move['bonus']}" for move in self.specialMoves]
        )
        
        return (
            f"Name: {self.name}\n"
            f"Health: {self.health}\n"
            f"Strength: {self.strength}\n"
            f"Speed: {self.speed}\n"
            f"Mana: {self.mana}\n"
            f"Battle IQ: {self.battleIQ}\n"
            f"{specialMovesString}\n"
        )
    
    def train(self, attribute):
        if self.mana < 10:
            range = 101
        elif self.mana < 20:
            range = 91
        elif self.mana < 30:
            range = 81
        elif self.mana < 40:
            range = 71
        elif self.mana < 50:
            range = 61
        else:
            range = 201
        specialAbilityChance = random.randrange(1,range)
        if specialAbilityChance == 1:

            prefixes = [
                "Shadow", "Fire", "Thunder", "Ice", "Mystic", "Solar", "Lunar", "Aqua", "Terra", "Wind",
                "Dark", "Light", "Storm", "Iron", "Steel", "Golden", "Crystal", "Arcane", "Divine", "Phantom",
                "Inferno", "Frost", "Electro", "Gravity", "Spectral", "Void", "Nebula", "Galactic", "Titan", "Venom",
                "Blazing", "Frozen", "Electric", "Mystical", "Celestial", "Enchanted", "Fiery", "Silent", "Ethereal", "Obsidian",
                "Radiant", "Corrupted", "Sacred", "Vengeful", "Ancient", "Eternal", "Shattered", "Omnipotent", "Astral", "Dread"
            ]

            elements = [
                "Dragon", "Phoenix", "Tiger", "Wolf", "Eagle", "Serpent", "Griffin", "Leviathan", "Basilisk", "Unicorn",
                "Flame", "Crystal", "Shadow", "Star", "Moon", "Sun", "Stone", "Storm", "Thunder", "Blizzard",
                "Inferno", "Glacier", "Tempest", "Hurricane", "Tornado", "Meteor", "Nebula", "Quasar", "Vortex", "Galaxy",
                "Mystic", "Arcane", "Celestial", "Ether", "Chaos", "Aura", "Spirit", "Void", "Illusion", "Mirage",
                "Specter", "Frost", "Volt", "Inferno", "Nebula", "Cosmos", "Phantom", "Aether", "Rift", "Oblivion",
                "Berserker", "Oracle", "Warrior", "Mage", "Sentinel", "Guardian", "Champion", "Knight", "Assassin", "Vanguard"
            ]

            suffixes = [
                "Blast", "Strike", "Wave", "Fury", "Roar", "Blade", "Storm", "Flare", "Punch", "Rage",
                "Slash", "Burst", "Beam", "Surge", "Claw", "Crash", "Dash", "Howl", "Shock", "Quake",
                "Vortex", "Torrent", "Bolt", "Gale", "Blaze", "Nova", "Slam", "Sting", "Wrath", "Pulse",
                "Inferno", "Eruption", "Cascade", "Maelstrom", "Explosion", "Onslaught", "Cataclysm", "Tempest", "Tornado", "Hurricane",
                "Blitz", "Frenzy", "Crush", "Rampage", "Strike", "Charge", "Assault", "Volley", "Sweep", "Crush"
            ]

            nameFormat = random.randrange(1,5) #1 = PE 2# =PS #3 = ES #4 = PES
            if nameFormat == 1:
                abilityName = random.choice(prefixes) + " " + random.choice(elements)
            elif nameFormat == 2:
                abilityName = random.choice(prefixes) + " " +  random.choice(suffixes)
            elif nameFormat == 3:
                abilityName = random.choice(elements) + " " +  random.choice(suffixes)
            else:
                abilityName = random.choice(prefixes) + " " +  random.choice(elements) + " " +  random.choice(suffixes)
        
            abilityTypeRoll = random.randrange(1,4) #1strength health speed
            if abilityTypeRoll == 1:
                abilityType = "Strength"
            elif abilityTypeRoll == 2:
                abilityType = "Health"
            else:
                abilityType = "Speed"

            bonusPoints = random.randrange(1,self.mana + 1)

            specialMove = {
                'name': abilityName,
                'type': abilityType,
                'bonus': bonusPoints
            }
            self.specialMoves.append(specialMove)
            message = f"{self.name} trained and created a special move called {abilityName} which is {abilityType} type move and has {bonusPoints} power!"

        else:
            if attribute == "random":
                attribute = random.choice(["health", "strength", "speed", "mana", "battleIQ"])

            statBoost = random.randrange(1, 21)
            if statBoost <= 5:
                increment = 0
                message = f"{self.name} trained but did not improve"
            elif statBoost <= 10:
                increment = 1
                message = f"{self.name} trained {attribute} by 1 point"
            elif statBoost <= 14:
                increment = 2
                message = f"{self.name} trained {attribute} by 2 points"
            elif statBoost <= 17:
                increment = 3
                message = f"{self.name} trained {attribute} by 3 points"
            elif statBoost <= 19:
                increment = 4
                message = f"{self.name} trained {attribute} by 4 points"
            else:
                increment = 5
                message = f"{self.name} trained {attribute} by 5 points"

            if attribute == "health":
                self.health += increment
            elif attribute == "strength":
                self.strength += increment
            elif attribute == "speed":
                self.speed += increment
            elif attribute == "mana":
                self.mana += increment
            elif attribute == "battleIQ":
                self.battleIQ += increment
        
        return message
        
# List of names
names = []



# Dictionary to store power levels
powerLevels = {}

# List to store Character objects
characters = {}

#History list
history = []

# Loop through the names, create Character objects, set stats, and store in the list
for name in names:
    character = Character(name)
    character.stats()
    characters[name] = character

# train character call. attribute must be all lowercase or random
def trainCharacterCall(name, attribute):
    if name in characters:
        resultMessage = characters[name].train(attribute)
        messagebox.showinfo("Training Results", resultMessage)
        updateStats()
    else:
        messagebox.showerror("Error", f"Character '{name}' not found")

def trainAllCharactersCall(attribute):
    for character in characters.values():   
        character.train(attribute)
    updateStats()

def displayStatsCall(name):
    if name in characters:
        stats = characters[name].displayStats()
        messagebox.showinfo("Character Stats", stats)
    else:
        messagebox.showerror("Error", f"Character '{name}' not found")

#1v1 character fight
def oneVOne(character1_name, character2_name):
    character1 = characters[character1_name]
    character2 = characters[character2_name]

    # Initial stats
    character1Health = character1.health
    character2Health = character2.health
    character1Speed = character1.speed
    character2Speed = character2.speed
    character1BattleIQ = character1.battleIQ
    character2BattleIQ = character2.battleIQ
    character1AttackStrength = (0.25 * float(character1BattleIQ)) + float(character1.strength)
    character2AttackStrength = (0.25 * float(character2BattleIQ)) + float(character2.strength)
    number = character1Speed + character2Speed

    print(f"{character1_name} stats before special moves:")
    print(f"Health: {character1Health}, Speed: {character1Speed}, Strength: {character1AttackStrength}")
    print(f"{character2_name} stats before special moves:")
    print(f"Health: {character2Health}, Speed: {character2Speed}, Strength: {character2AttackStrength}")

    # Apply special moves
    for move in character1.specialMoves:
        if move['type'] == 'Speed':
            character1Speed += move['bonus']
        elif move['type'] == 'Strength':
            character1AttackStrength += move['bonus']
        elif move['type'] == 'Health':
            character1Health += move['bonus']

    for move in character2.specialMoves:
        if move['type'] == 'Speed':
            character2Speed += move['bonus']
        elif move['type'] == 'Strength':
            character2AttackStrength += move['bonus']
        elif move['type'] == 'Health':
            character2Health += move['bonus']

    print(f"{character1_name} stats after special moves:")
    print(f"Health: {character1Health}, Speed: {character1Speed}, Strength: {character1AttackStrength}")
    print(f"{character2_name} stats after special moves:")
    print(f"Health: {character2Health}, Speed: {character2Speed}, Strength: {character2AttackStrength}")

    maxIterations = 1000
    iteration = 0
    fighting = True
    while fighting and iteration < maxIterations:
        attackChance1 = random.randrange(1, number + 1)
        attackChance2 = random.randrange(1, number + 1)
        if character1Health <= 0 or character2Health <= 0:
            fighting = False
        else:
            if attackChance1 <= character1Speed:
                character2Health -= character1AttackStrength
            if attackChance2 > character1Speed:
                character1Health -= character2AttackStrength
        iteration += 1

    # Compare points
    if character1Health > character2Health:
        historyEvent = f"{character1_name} has won the fight against {character2_name}"
        messagebox.showinfo("Fight Results", historyEvent)
        documentFight(historyEvent)
    elif character2Health > character1Health:
        historyEvent = f"{character2_name} has won the fight against {character1_name}"
        messagebox.showinfo("Fight Results", historyEvent)
        documentFight(historyEvent)
    else:
        historyEvent = f"The fight between {character1_name} and {character2_name} ended in a draw"
        messagebox.showinfo("Fight Results", historyEvent)
        documentFight(historyEvent)

def updatePowerLevels():
    powerLevelsText.config(state=tk.NORMAL)
    powerLevelsText.delete('1.0', tk.END)
    sortedPowerLevels = sorted(powerLevels.items(), key=lambda item: item[1], reverse=True)#need to research how this works
    rank = 0
    for name, powerLevel in sortedPowerLevels:
        rank += 1
        powerLevelsText.insert(tk.END, f"{rank}. {name}: {powerLevel}\n")
    powerLevelsText.config(state=tk.DISABLED)    

def updateStats():
    statsText.config(state=tk.NORMAL)
    statsText.delete('1.0',tk.END)
    for name, character in characters.items():
        statsText.insert(tk.END,character.displayStats() + "\n\n")
        powerLevel = character.health + character.strength + character.speed + character.mana + character.battleIQ
        for move in character.specialMoves:
            powerLevel += move['bonus']
        powerLevels[name] = powerLevel
    statsText.config(state=tk.DISABLED)
    updatePowerLevels()

def documentFight(historyEvent):
    history.append(historyEvent)
    historyText.config(state=tk.NORMAL)
    historyText.delete('1.0',tk.END)
    for event in history:
        historyText.insert(tk.END,event + "\n\n")
    historyText.config(state=tk.DISABLED)

def onTrainButtonClick():
    name = charNameEntry.get()
    attribute = attributeEntry.get()
    trainCharacterCall(name,attribute)
    updateStats()

def onShowStatsButtonClick():
    name = charNameEntry.get()
    displayStatsCall(name)
    updateStats()

def createCharacter(name):
    character = Character(name)
    character.stats()
    characters[name] = character
    updateStats()

def onCreateCharacterClick():
    name = createCharacterEntry.get()
    createCharacter(name)

def onFightButtonClick():
    character1 = oneVOneEntry1.get()
    character2 = oneVOneEntry2.get()
    oneVOne(character1,character2)

def trainAllCharacters():
    times = int(trainAllEntry1.get())
    count = 1
    while count <= times:
        attribute = trainAllEntry2.get()
        trainAllCharactersCall(attribute)
        count += 1

#GUI
root = tk.Tk()
root.title("Fighting Game")

labelCharName = tk.Label(root, text = "Character Name:")
labelCharName.grid(row=0,column=0,padx=5,pady=5)

charNameEntry = tk.Entry(root)
charNameEntry.grid(row=0,column=1,padx=5,pady=5)

labelAttribute = tk.Label(root, text = "Attribute:")
labelAttribute.grid(row=1,column=0,padx=5,pady=5)

attributeEntry = tk.Entry(root)
attributeEntry.grid(row=1,column=1,padx=5,pady=5)

createCharacterLabel = tk.Label(root, text = "Create Character")
createCharacterLabel.grid(row=3,column=0,padx=5,pady=5)

createCharacterEntry = tk.Entry(root)
createCharacterEntry.grid(row=3,column=1,padx=5,pady=5)

oneVOneLabel = tk.Label(root, text="Hold a one vs one fight")
oneVOneLabel.grid(row=0,column=3,padx=5,pady=5)

oneVOneEntry1 = tk.Entry(root)
oneVOneEntry1.grid(row=0,column=4,padx=5,pady=5)

vsLabel = tk.Label(root, text="vs")
vsLabel.grid(row=0,column=5)

powerLevelLabel = tk.Label(root, text="Power Level Rankings")
powerLevelLabel.grid(row=5,column=0,padx=5,pady=5)

oneVOneEntry2 = tk.Entry(root)
oneVOneEntry2.grid(row=0,column=6,padx=5,pady=5)

showStatsButton = tk.Button(root, text = "Show Character Stats", command=onShowStatsButtonClick)
showStatsButton.grid(row=0,column=2,padx=5,pady=5)

fightButton = tk.Button(root, text="Simulate Fight", command=onFightButtonClick)
fightButton.grid(row=0,column=7,padx=5,pady=5)

trainButton = tk.Button(root, text = "Train", command=onTrainButtonClick)
trainButton.grid(row=1,column=2,padx=5,pady=5)

createCharacterButton = tk.Button(root, text = "Create", command=onCreateCharacterClick)
createCharacterButton.grid(row=3,column=2,padx=5,pady=5)

statsText = tk.Text(root, width=40, height=15)
statsText.grid(row=4,column=0,columnspan=2,padx=5,pady=5)
statsText.config(state=tk.DISABLED)

historyText = tk.Text(root,width=40,height=24)
historyText.grid(row=1,column=4,rowspan=4,columnspan=3,padx=5,pady=5)
historyText.config(state=tk.DISABLED)

powerLevelsText = tk.Text(root,width=40,height=21)
powerLevelsText.grid(row=6,column=0,columnspan=2,padx=5,pady=5)
powerLevelsText.config(state=tk.DISABLED)

spaceLabel = tk.Label(root)
spaceLabel.grid(row=2,column=1)

trainAllLabel1 = tk.Label(root, text="Train all characters")
trainAllLabel1.grid(row=7,column=0,padx=5,pady=5)

trainAllEntry1 = tk.Entry(root)
trainAllEntry1.grid(row=7,column=1,padx=5,pady=5)

trainAllLabel2 = tk.Label(root,text="times for")
trainAllLabel2.grid(row=7,column=2,padx=5,pady=5)

trainAllEntry2 = tk.Entry(root)
trainAllEntry2.grid(row=7,column=3,padx=5,pady=5)

trainAllButton = tk.Button(root,text="Train All", command=trainAllCharacters)
trainAllButton.grid(row=7,column=4,padx=5,pady=5)
updateStats()

root.mainloop()

