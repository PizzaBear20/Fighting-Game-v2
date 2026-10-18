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
        # more mana = better chance of learning a special move
        if self.mana < 10:
            chanceRange = 101
        elif self.mana < 20:
            chanceRange = 91
        elif self.mana < 30:
            chanceRange = 81
        elif self.mana < 40:
            chanceRange = 71
        elif self.mana < 50:
            chanceRange = 61
        else:
            chanceRange = 51
        specialAbilityChance = random.randrange(1,chanceRange)
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

# Attribute names people can type -> the real attribute name
attributeNames = {
    "health": "health",
    "strength": "strength",
    "speed": "speed",
    "mana": "mana",
    "battleiq": "battleIQ",
    "battle iq": "battleIQ",
    "iq": "battleIQ",
    "random": "random",
}

# Turns typed text like "Battle IQ" into "battleIQ". Returns None if it isn't an attribute
def cleanAttribute(text):
    return attributeNames.get(text.strip().lower())

# train character call. attribute must already be cleaned with cleanAttribute
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

# Fight settings
HP_PER_HEALTH = 10  # each health point is worth 10 HP so fights last long enough to watch
MAX_ROUNDS = 300    # if nobody is knocked out by then, whoever has more HP wins

# Works out the whole fight ahead of time. The fight window then plays it back as an animation
def simulateFight(character1, character2):
    fighters = []
    for character in (character1, character2):
        health = character.health
        speed = character.speed
        attack = (0.25 * float(character.battleIQ)) + float(character.strength)

        # Apply special moves
        for move in character.specialMoves:
            if move['type'] == 'Speed':
                speed += move['bonus']
            elif move['type'] == 'Strength':
                attack += move['bonus']
            elif move['type'] == 'Health':
                health += move['bonus']

        fighters.append({
            'name': character.name,
            'maxHP': health * HP_PER_HEALTH,
            'attack': attack,
            'speed': speed,
            'moves': list(character.specialMoves),
        })

    hp = [fighters[0]['maxHP'], fighters[1]['maxHP']]
    totalSpeed = fighters[0]['speed'] + fighters[1]['speed']
    events = []

    # Each round one fighter attacks. The faster you are, the more often you get the attack
    while hp[0] > 0 and hp[1] > 0 and len(events) < MAX_ROUNDS:
        if random.randrange(1, totalSpeed + 1) <= fighters[0]['speed']:
            attacker = 0
        else:
            attacker = 1
        defender = 1 - attacker
        damage = max(1, round(fighters[attacker]['attack'] * random.uniform(0.8, 1.2)))
        hp[defender] = max(0, hp[defender] - damage)
        events.append({'attacker': attacker, 'damage': damage, 'hp': list(hp)})

    if hp[0] > hp[1]:
        winner = 0
    elif hp[1] > hp[0]:
        winner = 1
    else:
        winner = None

    return {
        'fighters': fighters,
        'events': events,
        'winner': winner,
        'knockout': hp[0] == 0 or hp[1] == 0,
    }

# A window that shows the fight happening
class FightWindow:
    WIDTH = 760
    HEIGHT = 420
    GROUND = 340
    BAR_WIDTH = 300
    COLORS = ["#4da3ff", "#ff6b6b"]
    KO_COLOR = "#7d7d8c"
    SKY = "#20243a"

    def __init__(self, parent, character1, character2):
        self.result = simulateFight(character1, character2)
        self.fighters = self.result['fighters']
        self.events = self.result['events']

        self.window = tk.Toplevel(parent)
        self.window.title(f"{character1.name} vs {character2.name}")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, bg=self.SKY, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.speedScale = tk.Scale(self.window, from_=1, to=5, orient=tk.HORIZONTAL, label="Speed")
        self.speedScale.set(2)
        self.speedScale.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.skipButton = tk.Button(self.window, text="Skip to End", command=self.skip)
        self.skipButton.grid(row=1, column=1, padx=5, pady=5)

        closeButton = tk.Button(self.window, text="Close", command=self.close)
        closeButton.grid(row=1, column=2, padx=5, pady=5, sticky="e")

        self.logText = tk.Text(self.window, width=90, height=8)
        self.logText.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.logText.config(state=tk.DISABLED)

        # Where each fighter is and what they are doing
        self.homeX = [270, 490]
        self.x = [-60, self.WIDTH + 60]  # start off screen and walk in
        self.facing = [1, -1]            # 1 = facing right, -1 = facing left
        self.poses = ["stand", "stand"]  # stand, punch, hit, down, win
        self.flash = [False, False]
        self.shownHP = [self.fighters[0]['maxHP'], self.fighters[1]['maxHP']]

        self.eventsLogged = 0
        self.recorded = False
        self.afterId = None

        self.drawArena()
        self.drawHealthBars()
        self.drawFighter(0)
        self.drawFighter(1)

        self.animation = self.playFight()
        self.step()

    # Runs the next frame of the animation. playFight "yields" how many milliseconds to wait
    def step(self):
        try:
            delay = next(self.animation)
        except StopIteration:
            self.afterId = None
            return
        self.afterId = self.window.after(max(1, int(delay / self.speedScale.get())), self.step)

    def stopAnimation(self):
        if self.afterId is not None:
            self.window.after_cancel(self.afterId)
            self.afterId = None
        self.animation.close()

    # ---------- drawing ----------

    def drawArena(self):
        c = self.canvas
        # sky fades a little lighter towards the floor
        bands = ["#20243a", "#23283f", "#262c45", "#29304b", "#2c3451", "#2f3857"]
        bandHeight = self.GROUND / len(bands)
        for i, color in enumerate(bands):
            c.create_rectangle(0, i * bandHeight, self.WIDTH, (i + 1) * bandHeight + 1, fill=color, outline="")
        c.create_rectangle(0, self.GROUND, self.WIDTH, self.HEIGHT, fill="#3b3b52", outline="")
        c.create_line(0, self.GROUND, self.WIDTH, self.GROUND, fill="#5a5a7a", width=3)
        for lineX in range(0, self.WIDTH, 80):
            c.create_line(lineX, self.GROUND + 10, lineX - 40, self.HEIGHT, fill="#44445e", width=2)

    def drawHealthBars(self):
        c = self.canvas
        c.delete("hud")
        for i in (0, 1):
            fighter = self.fighters[i]
            if i == 0:
                barLeft = 30
            else:
                barLeft = self.WIDTH - 30 - self.BAR_WIDTH
            barRight = barLeft + self.BAR_WIDTH
            percent = max(0, self.shownHP[i]) / fighter['maxHP']

            if percent > 0.5:
                barColor = "#4cd964"
            elif percent > 0.25:
                barColor = "#ffcc00"
            else:
                barColor = "#ff3b30"

            c.create_rectangle(barLeft, 40, barRight, 62, fill="#111320", outline="#cfd3e6", width=2, tags="hud")
            fillWidth = (self.BAR_WIDTH - 4) * percent
            if fillWidth > 0:
                # player 1's bar drains towards the left, player 2's towards the right
                if i == 0:
                    c.create_rectangle(barLeft + 2, 42, barLeft + 2 + fillWidth, 60, fill=barColor, outline="", tags="hud")
                else:
                    c.create_rectangle(barRight - 2 - fillWidth, 42, barRight - 2, 60, fill=barColor, outline="", tags="hud")

            hpText = f"HP {round(max(0, self.shownHP[i]))} / {fighter['maxHP']}"
            if i == 0:
                c.create_text(barLeft, 28, text=fighter['name'], anchor="w", fill=self.COLORS[i], font=("Helvetica", 15, "bold"), tags="hud")
                c.create_text(barRight, 28, text=hpText, anchor="e", fill="#cfd3e6", font=("Helvetica", 11), tags="hud")
            else:
                c.create_text(barRight, 28, text=fighter['name'], anchor="e", fill=self.COLORS[i], font=("Helvetica", 15, "bold"), tags="hud")
                c.create_text(barLeft, 28, text=hpText, anchor="w", fill="#cfd3e6", font=("Helvetica", 11), tags="hud")

    # Draws a stick figure fighter in their current pose
    def drawFighter(self, i):
        c = self.canvas
        tag = f"fighter{i}"
        c.delete(tag)

        x = self.x[i]
        g = self.GROUND
        f = self.facing[i]
        pose = self.poses[i]

        color = self.COLORS[i]
        if pose == "down":
            color = self.KO_COLOR
        if self.flash[i]:
            color = "#ffffff"

        def line(*points):
            c.create_line(*points, fill=color, width=6, capstyle=tk.ROUND, joinstyle=tk.ROUND, tags=tag)

        def circle(centerX, centerY, radius):
            c.create_oval(centerX - radius, centerY - radius, centerX + radius, centerY + radius, fill=color, outline=color, tags=tag)

        # shadow on the floor
        c.create_oval(x - 38, g - 6, x + 38, g + 6, fill="#2a2a3d", outline="", tags=tag)

        if pose == "down":
            line(x - f * 40, g - 12, x + f * 10, g - 12)    # body
            line(x + f * 10, g - 12, x + f * 52, g - 4)     # legs
            line(x + f * 10, g - 12, x + f * 46, g - 24)
            line(x - f * 28, g - 12, x - f * 12, g - 32)    # arm
            circle(x - f * 56, g - 15, 15)                  # head
            c.create_text(x, g - 60, text=self.fighters[i]['name'], fill=self.KO_COLOR, font=("Helvetica", 12, "bold"), tags=tag)
            return

        if pose == "hit":
            lean = -f * 10
        elif pose == "punch":
            lean = f * 8
        else:
            lean = 0

        hipY = g - 50
        shoulderX = x + lean
        shoulderY = g - 88
        armY = shoulderY + 4

        # legs
        if pose == "punch":
            feet = [x + f * 30, x - f * 28]
        else:
            feet = [x + f * 18, x - f * 16]
        for footX in feet:
            line(x, hipY, (x + footX) / 2, hipY + 26, footX, g)

        # body and head
        line(x, hipY, shoulderX, shoulderY)
        circle(shoulderX + lean * 0.4, shoulderY - 22, 15)

        # arms
        if pose == "punch":
            line(shoulderX, armY, shoulderX + f * 60, armY - 2)
            circle(shoulderX + f * 62, armY - 2, 8)
            line(shoulderX, armY, shoulderX + f * 8, armY + 22, shoulderX + f * 20, armY + 4)
            circle(shoulderX + f * 21, armY + 3, 6)
        elif pose == "win":
            line(shoulderX, armY, shoulderX + 24, armY - 18, shoulderX + 32, armY - 46)
            circle(shoulderX + 32, armY - 48, 7)
            line(shoulderX, armY, shoulderX - 24, armY - 18, shoulderX - 32, armY - 46)
            circle(shoulderX - 32, armY - 48, 7)
        elif pose == "hit":
            line(shoulderX, armY, shoulderX - f * 22, armY + 14, shoulderX - f * 36, armY - 4)
            line(shoulderX, armY, shoulderX - f * 12, armY + 26, shoulderX - f * 28, armY + 30)
        else:
            line(shoulderX, armY, shoulderX + f * 18, armY + 20, shoulderX + f * 30, armY - 2)
            circle(shoulderX + f * 31, armY - 3, 7)
            line(shoulderX, armY, shoulderX + f * 6, armY + 24, shoulderX + f * 20, armY + 8)
            circle(shoulderX + f * 21, armY + 7, 6)

        c.create_text(x, g - 150, text=self.fighters[i]['name'], fill=self.COLORS[i], font=("Helvetica", 12, "bold"), tags=tag)

    def announce(self, text, color="#ffd34d"):
        c = self.canvas
        c.delete("announce")
        c.create_text(self.WIDTH / 2 + 3, 98, text=text, fill="#000000", font=("Helvetica", 34, "bold"), tags="announce")
        c.create_text(self.WIDTH / 2, 95, text=text, fill=color, font=("Helvetica", 34, "bold"), tags="announce")

    def log(self, text):
        self.logText.config(state=tk.NORMAL)
        self.logText.insert(tk.END, text + "\n")
        self.logText.see(tk.END)
        self.logText.config(state=tk.DISABLED)

    def logEvent(self, event):
        attacker = self.fighters[event['attacker']]['name']
        defenderIndex = 1 - event['attacker']
        defender = self.fighters[defenderIndex]['name']
        hpLeft = event['hp'][defenderIndex]
        if hpLeft == 0:
            self.log(f"{attacker} hits {defender} for {event['damage']} damage. {defender} is knocked out!")
        else:
            self.log(f"{attacker} hits {defender} for {event['damage']} damage ({hpLeft} HP left)")
        self.eventsLogged += 1

    # ---------- animation ----------

    # The whole fight, start to finish. Each "yield" is a pause in milliseconds between frames
    def playFight(self):
        name1 = self.fighters[0]['name']
        name2 = self.fighters[1]['name']

        # fighters walk in
        startX = list(self.x)
        frames = 30
        for frame in range(1, frames + 1):
            for i in (0, 1):
                self.x[i] = startX[i] + (self.homeX[i] - startX[i]) * frame / frames
                self.drawFighter(i)
            yield 25

        self.announce(f"{name1}  VS  {name2}")
        for fighter in self.fighters:
            self.log(f"{fighter['name']}: {fighter['maxHP']} HP, {fighter['attack']:.1f} attack, {fighter['speed']} speed")
        yield 1000

        # special moves power up
        for i in (0, 1):
            moves = self.fighters[i]['moves']
            for move in moves[:3]:
                yield from self.powerUp(i, move)
            if len(moves) > 3:
                self.log(f"...and {len(moves) - 3} more special moves")

        self.announce("FIGHT!", "#ff5c5c")
        yield 700
        self.canvas.delete("announce")

        for event in self.events:
            yield from self.playEvent(event)

        yield from self.playEnding()

    def powerUp(self, i, move):
        c = self.canvas
        x = self.x[i]
        g = self.GROUND
        self.log(f"{self.fighters[i]['name']} powers up with {move['name']} (+{move['bonus']} {move['type']})")
        c.create_text(x, g - 198, text=move['name'], fill="#ffffff", font=("Helvetica", 14, "bold"), tags="temp")
        c.create_text(x, g - 180, text=f"+{move['bonus']} {move['type']}", fill="#ffd34d", font=("Helvetica", 12), tags="temp")
        for frame in range(16):
            c.delete("aura")
            size = 40 + (frame % 8) * 4
            c.create_oval(x - size, g - 140 - frame % 8, x + size, g + 8, outline=self.COLORS[i], width=3, tags=("aura", "temp"))
            c.tag_lower("aura", f"fighter{i}")
            yield 45
        c.delete("temp")

    def playEvent(self, event):
        c = self.canvas
        attacker = event['attacker']
        defender = 1 - attacker
        g = self.GROUND

        # attacker dashes in and throws a punch
        attackStart = self.x[attacker]
        target = self.x[defender] - self.facing[attacker] * 80
        frames = 7
        for frame in range(1, frames + 1):
            self.x[attacker] = attackStart + (target - attackStart) * frame / frames
            if frame >= 4:
                self.poses[attacker] = "punch"
            self.drawFighter(attacker)
            yield 25

        # impact
        self.poses[defender] = "hit"
        self.flash[defender] = True
        hitX = self.x[defender] + self.facing[defender] * 14
        hitY = g - 86
        for angle in range(8):
            dx = [1, 0.7, 0, -0.7, -1, -0.7, 0, 0.7][angle]
            dy = [0, 0.7, 1, 0.7, 0, -0.7, -1, -0.7][angle]
            c.create_line(hitX + dx * 8, hitY + dy * 8, hitX + dx * 22, hitY + dy * 22, fill="#ffdd57", width=3, tags=("spark", "temp"))
        damageText = c.create_text(self.x[defender], g - 165, text=f"-{event['damage']}", fill="#ffdd57", font=("Helvetica", 22, "bold"), tags="temp")
        self.logEvent(event)

        defenderStart = self.x[defender]
        startHP = self.shownHP[defender]
        endHP = event['hp'][defender]
        frames = 12
        for frame in range(1, frames + 1):
            if frame == 3:
                self.flash[defender] = False
            if frame == 4:
                c.delete("spark")
            # knocked back a little, then steps back in
            if frame <= frames / 2:
                knockback = frame * 3
            else:
                knockback = (frames - frame) * 3
            self.x[defender] = defenderStart - self.facing[defender] * knockback
            self.shownHP[defender] = startHP + (endHP - startHP) * frame / frames
            c.move(damageText, 0, -3)
            self.drawFighter(defender)
            self.drawHealthBars()
            yield 30
        c.delete("temp")
        self.x[defender] = defenderStart
        if endHP > 0:
            self.poses[defender] = "stand"
            self.drawFighter(defender)

        # attacker goes back to their spot
        self.poses[attacker] = "stand"
        returnStart = self.x[attacker]
        frames = 8
        for frame in range(1, frames + 1):
            self.x[attacker] = returnStart + (self.homeX[attacker] - returnStart) * frame / frames
            self.drawFighter(attacker)
            yield 20
        yield 150

    def playEnding(self):
        winner = self.result['winner']
        if self.result['knockout']:
            loser = 1 - winner
            self.poses[loser] = "hit"
            self.drawFighter(loser)
            yield 250
            self.poses[loser] = "down"
            self.drawFighter(loser)
            self.announce("K.O.!", "#ff5c5c")
            yield 900
        else:
            self.announce("TIME!", "#ff5c5c")
            yield 900
        self.showResult()

    # Puts everything in its final position, shows the winner and saves the result to history
    def showResult(self):
        self.canvas.delete("temp")
        winner = self.result['winner']
        for i in (0, 1):
            self.x[i] = self.homeX[i]
            self.flash[i] = False
            self.shownHP[i] = self.events[-1]['hp'][i] if self.events else self.fighters[i]['maxHP']
            if winner is None:
                self.poses[i] = "stand"
            elif i == winner:
                self.poses[i] = "win"
            elif self.result['knockout']:
                self.poses[i] = "down"
            else:
                self.poses[i] = "stand"
            self.drawFighter(i)
        self.drawHealthBars()

        if winner is None:
            self.announce("DRAW!", "#cfd3e6")
        else:
            self.announce(f"{self.fighters[winner]['name']} WINS!")
        self.skipButton.config(state=tk.DISABLED)
        self.recordResult()

    def recordResult(self):
        if self.recorded:
            return
        self.recorded = True
        name1 = self.fighters[0]['name']
        name2 = self.fighters[1]['name']
        winner = self.result['winner']
        if winner == 0:
            historyEvent = f"{name1} has won the fight against {name2}"
        elif winner == 1:
            historyEvent = f"{name2} has won the fight against {name1}"
        else:
            historyEvent = f"The fight between {name1} and {name2} ended in a draw"
        if winner is not None:
            if self.result['knockout']:
                historyEvent += " by knockout"
            else:
                historyEvent += " on points"
        self.log(historyEvent)
        documentFight(historyEvent)

    def skip(self):
        if self.recorded:
            return
        self.stopAnimation()
        for event in self.events[self.eventsLogged:]:
            self.logEvent(event)
        self.showResult()

    def close(self):
        # closing early still counts the fight
        self.stopAnimation()
        self.recordResult()
        self.window.destroy()

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
    name = charNameEntry.get().strip()
    attribute = cleanAttribute(attributeEntry.get())
    if attribute is None:
        messagebox.showerror("Error", "Attribute must be health, strength, speed, mana, battleIQ, or random")
        return
    trainCharacterCall(name,attribute)

def onShowStatsButtonClick():
    name = charNameEntry.get().strip()
    displayStatsCall(name)

def createCharacter(name):
    character = Character(name)
    character.stats()
    characters[name] = character
    updateStats()

def onCreateCharacterClick():
    name = createCharacterEntry.get().strip()
    if name == "":
        messagebox.showerror("Error", "Type a name for the new character")
        return
    if name in characters:
        messagebox.showerror("Error", f"There is already a character named '{name}'")
        return
    createCharacter(name)
    createCharacterEntry.delete(0, tk.END)

def onFightButtonClick():
    character1 = oneVOneEntry1.get().strip()
    character2 = oneVOneEntry2.get().strip()
    for name in (character1, character2):
        if name not in characters:
            messagebox.showerror("Error", f"Character '{name}' not found")
            return
    if character1 == character2:
        messagebox.showerror("Error", "A character can't fight themselves")
        return
    FightWindow(root, characters[character1], characters[character2])

def trainAllCharacters():
    try:
        times = int(trainAllEntry1.get())
    except ValueError:
        messagebox.showerror("Error", "Type how many times to train as a number")
        return
    if times < 1:
        messagebox.showerror("Error", "Train at least 1 time")
        return
    attribute = cleanAttribute(trainAllEntry2.get())
    if attribute is None:
        messagebox.showerror("Error", "Attribute must be health, strength, speed, mana, battleIQ, or random")
        return
    count = 1
    while count <= times:
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

