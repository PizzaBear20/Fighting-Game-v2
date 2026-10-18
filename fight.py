import random
import tkinter as tk
from tkinter import ttk

import theme
from drawing import drawArena, drawFighter as drawLook, readable

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
            'look': dict(character.look),
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
    KO_COLOR = "#7d7d8c"
    SKY = "#20243a"

    # onFinish(historyEvent) is called once the fight has a result
    def __init__(self, parent, character1, character2, onFinish):
        self.result = simulateFight(character1, character2)
        self.fighters = self.result['fighters']
        self.events = self.result['events']
        self.onFinish = onFinish
        # text and aura colors come from each fighter's body color
        self.colors = [readable(fighter['look']['bodyColor']) for fighter in self.fighters]

        self.window = tk.Toplevel(parent)
        self.window.title(f"{character1.name} vs {character2.name}")
        self.window.resizable(False, False)
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.window.configure(bg=theme.BG)

        self.canvas = tk.Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, bg=self.SKY, highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.speedScale = tk.Scale(self.window, from_=1, to=5, orient=tk.HORIZONTAL, label="Speed", length=160,
                                   bg=theme.BG, fg=theme.TEXT, troughcolor=theme.PANEL_LIGHT, highlightthickness=0,
                                   activebackground=theme.BLUE, font=theme.SMALL_FONT, bd=0)
        self.speedScale.set(2)
        self.speedScale.grid(row=1, column=0, padx=12, pady=8, sticky="w")

        self.skipButton = ttk.Button(self.window, text="Skip to End", command=self.skip)
        self.skipButton.grid(row=1, column=1, padx=5, pady=8)

        closeButton = ttk.Button(self.window, text="Close", command=self.close)
        closeButton.grid(row=1, column=2, padx=12, pady=8, sticky="e")

        self.logText = theme.textBox(self.window, height=7, width=90)
        self.logText.config(font=theme.SMALL_FONT)
        self.logText.grid(row=2, column=0, columnspan=3, padx=12, pady=(0, 12), sticky="ew")

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
        drawArena(self.canvas, self.WIDTH, self.HEIGHT, self.GROUND)

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
                c.create_text(barLeft, 28, text=fighter['name'], anchor="w", fill=self.colors[i], font=("Helvetica", 15, "bold"), tags="hud")
                c.create_text(barRight, 28, text=hpText, anchor="e", fill="#cfd3e6", font=("Helvetica", 11), tags="hud")
            else:
                c.create_text(barRight, 28, text=fighter['name'], anchor="e", fill=self.colors[i], font=("Helvetica", 15, "bold"), tags="hud")
                c.create_text(barLeft, 28, text=hpText, anchor="w", fill="#cfd3e6", font=("Helvetica", 11), tags="hud")

    # Draws a fighter with their own look in their current pose
    def drawFighter(self, i):
        tag = f"fighter{i}"
        self.canvas.delete(tag)
        x = self.x[i]
        g = self.GROUND
        drawLook(self.canvas, x, g, self.fighters[i]['look'], self.facing[i], self.poses[i], tag=tag, flash=self.flash[i])
        if self.poses[i] == "down":
            self.canvas.create_text(x, g - 70, text=self.fighters[i]['name'], fill=self.KO_COLOR, font=("Helvetica", 12, "bold"), tags=tag)
        else:
            self.canvas.create_text(x, g - 168, text=self.fighters[i]['name'], fill=self.colors[i], font=("Helvetica", 12, "bold"), tags=tag)

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
        c.create_text(x, g - 214, text=move['name'], fill="#ffffff", font=("Helvetica", 14, "bold"), tags="temp")
        c.create_text(x, g - 195, text=f"+{move['bonus']} {move['type']}", fill="#ffd34d", font=("Helvetica", 12), tags="temp")
        for frame in range(16):
            c.delete("aura")
            size = 40 + (frame % 8) * 4
            c.create_oval(x - size, g - 140 - frame % 8, x + size, g + 8, outline=self.colors[i], width=3, tags=("aura", "temp"))
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
        damageText = c.create_text(self.x[defender], g - 190, text=f"-{event['damage']}", fill="#ffdd57", font=("Helvetica", 22, "bold"), tags="temp")
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
        self.onFinish(historyEvent)

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
