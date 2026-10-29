import random
import tkinter as tk
from tkinter import ttk

from core.fight import simulateFight, describeMove, moveCost
from ui import theme
from ui.drawing import drawArena, drawFighter as drawLook, readable

# A window that shows the fight happening
class FightWindow:
    WIDTH = 760
    HEIGHT = 420
    GROUND = 340
    BAR_WIDTH = 300
    KO_COLOR = "#7d7d8c"
    SKY = "#20243a"
    MP_COLOR = "#b47cff"
    SHIELD_COLOR = "#ff9f43"
    CRIT_COLOR = "#ff8c42"
    DODGE_COLOR = "#7fd6ff"
    HEAL_COLOR = "#4cd964"

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
        self.lift = [0, 0]               # how high off the ground (for dodging)
        self.shownHP = [self.fighters[0]['maxHP'], self.fighters[1]['maxHP']]
        self.shownMP = [0, 0]
        self.shownShield = [0, 0]

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

            # mana bar under the health bar
            c.create_rectangle(barLeft, 67, barRight, 75, fill="#111320", outline="#5a5f78", tags="hud")
            mpWidth = (self.BAR_WIDTH - 2) * self.shownMP[i] / fighter['maxMP']
            if mpWidth > 0:
                if i == 0:
                    c.create_rectangle(barLeft + 1, 68, barLeft + 1 + mpWidth, 74, fill=self.MP_COLOR, outline="", tags="hud")
                else:
                    c.create_rectangle(barRight - 1 - mpWidth, 68, barRight - 1, 74, fill=self.MP_COLOR, outline="", tags="hud")

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
        g = self.GROUND - self.lift[i]
        drawLook(self.canvas, x, g, self.fighters[i]['look'], self.facing[i], self.poses[i], tag=tag, flash=self.flash[i])
        if self.shownShield[i] > 0 and self.poses[i] != "down":
            self.canvas.create_oval(x - 62, g - 160, x + 62, g + 12, outline=self.SHIELD_COLOR, width=3, tags=tag)
            self.canvas.create_text(x, g + 22, text=f"Shield {self.shownShield[i]}", fill=self.SHIELD_COLOR, font=("Helvetica", 10, "bold"), tags=tag)
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
        move = event['move']
        if event['kind'] == 'dodge':
            text = f"{attacker} attacks but {defender} dodges!"
        elif move is not None and move['type'] == 'Health':
            text = f"{attacker} uses {move['name']} and heals {event['heal']} HP ({event['hp'][event['attacker']]} HP)"
        elif move is not None and move['type'] == 'Defense':
            text = f"{attacker} uses {move['name']} and raises a {event['shieldGain']} point shield"
        else:
            if move is not None:
                hits = f" in {len(event['hits'])} hits" if len(event['hits']) > 1 else ""
                text = f"{attacker} uses {move['name']}! {defender} takes {event['damage']} damage{hits}"
            elif event['kind'] == 'crit':
                text = f"CRITICAL HIT! {attacker} hits {defender} for {event['damage']} damage"
            else:
                text = f"{attacker} hits {defender} for {event['damage']} damage"
            if event['blocked']:
                text += f" ({event['blocked']} blocked by shield)"
            if hpLeft == 0:
                text += f". {defender} is knocked out!"
            else:
                text += f" ({hpLeft} HP left)"
        self.log(text)
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
            self.log(f"{fighter['name']}: {fighter['maxHP']} HP, {fighter['attack']} strength, {fighter['defense']} defense, "
                     f"{fighter['speed']} speed, {fighter['battleIQ']} battle IQ, {fighter['maxMP']} MP")
            for move in fighter['moves'][:3]:
                self.log(f"   ★ {move['name']} ({move['type']}, {moveCost(move)} MP): {describeMove(move)}")
            if len(fighter['moves']) > 3:
                self.log(f"   ...and {len(fighter['moves']) - 3} more special moves")
        yield 1000

        self.announce("FIGHT!", "#ff5c5c")
        yield 700
        self.canvas.delete("announce")

        for event in self.events:
            yield from self.playEvent(event)

        yield from self.playEnding()

    def playEvent(self, event):
        attacker = event['attacker']
        move = event['move']
        self.shownMP = list(event['mp'])
        self.drawHealthBars()
        if move is not None:
            yield from self.castMove(attacker, move)
        self.logEvent(event)

        if move is not None and move['type'] == 'Health':
            yield from self.playHeal(attacker, event)
        elif move is not None and move['type'] == 'Defense':
            yield from self.playShield(attacker, event)
        else:
            yield from self.playAttack(event)

        self.shownShield = list(event['shield'])
        for i in (0, 1):
            self.drawFighter(i)
        yield 150

    # The move's name flashes up and the fighter glows in the move's color
    def castMove(self, i, move):
        c = self.canvas
        x = self.x[i]
        g = self.GROUND
        color = theme.MOVE_COLORS.get(move['type'], self.colors[i])
        c.create_text(x + 2, g - 212, text=move['name'], fill="#000000", font=("Helvetica", 16, "bold"), tags="temp")
        c.create_text(x, g - 214, text=move['name'], fill=color, font=("Helvetica", 16, "bold"), tags="temp")
        for frame in range(12):
            c.delete("aura")
            size = 40 + (frame % 6) * 5
            c.create_oval(x - size, g - 140 - frame % 6, x + size, g + 8, outline=color, width=3, tags=("aura", "temp"))
            c.tag_lower("aura", f"fighter{i}")
            yield 45
        c.delete("temp")

    def playHeal(self, i, event):
        c = self.canvas
        x = self.x[i]
        g = self.GROUND
        healText = c.create_text(x, g - 190, text=f"+{event['heal']}", fill=self.HEAL_COLOR, font=("Helvetica", 22, "bold"), tags="temp")
        startHP = self.shownHP[i]
        endHP = event['hp'][i]
        frames = 14
        for frame in range(1, frames + 1):
            # little green sparkles float up
            sparkleX = x + random.randint(-40, 40)
            sparkleY = g - random.randint(10, 140)
            c.create_oval(sparkleX - 3, sparkleY - 3, sparkleX + 3, sparkleY + 3, fill=self.HEAL_COLOR, outline="", tags="temp")
            c.move(healText, 0, -2)
            self.shownHP[i] = startHP + (endHP - startHP) * frame / frames
            self.drawHealthBars()
            yield 35
        c.delete("temp")

    def playShield(self, i, event):
        c = self.canvas
        x = self.x[i]
        g = self.GROUND
        c.create_text(x, g - 190, text=f"+{event['shieldGain']} SHIELD", fill=self.SHIELD_COLOR, font=("Helvetica", 18, "bold"), tags="temp")
        # the shield grows out from the fighter
        for frame in range(1, 9):
            c.delete("ring")
            size = 62 * frame / 8
            c.create_oval(x - size, g - 74 - size * 1.4, x + size, g - 74 + size * 1.4, outline=self.SHIELD_COLOR, width=3, tags=("ring", "temp"))
            yield 35
        self.shownShield[i] = event['shield'][i]
        self.drawFighter(i)
        yield 300
        c.delete("temp")

    def playAttack(self, event):
        attacker = event['attacker']
        defender = 1 - attacker

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

        if event['kind'] == 'dodge':
            yield from self.playDodge(defender)
        else:
            for number, damage in enumerate(event['hits']):
                if number > 0:
                    # pull back and swing again
                    self.poses[attacker] = "stand"
                    self.drawFighter(attacker)
                    yield 60
                    self.poses[attacker] = "punch"
                    self.drawFighter(attacker)
                yield from self.playImpact(event, damage, showBlocked=(number == 0))
            self.shownHP[defender] = event['hp'][defender]
            self.drawHealthBars()

        # attacker goes back to their spot
        self.poses[attacker] = "stand"
        returnStart = self.x[attacker]
        frames = 8
        for frame in range(1, frames + 1):
            self.x[attacker] = returnStart + (self.homeX[attacker] - returnStart) * frame / frames
            self.drawFighter(attacker)
            yield 20

    # The defender hops back out of the way
    def playDodge(self, defender):
        c = self.canvas
        dodgeText = c.create_text(self.x[defender], self.GROUND - 190, text="DODGE!", fill=self.DODGE_COLOR, font=("Helvetica", 20, "bold"), tags="temp")
        defenderStart = self.x[defender]
        frames = 12
        for frame in range(1, frames + 1):
            if frame <= frames / 2:
                amount = frame
            else:
                amount = frames - frame
            self.x[defender] = defenderStart - self.facing[defender] * amount * 7
            self.lift[defender] = amount * 6
            c.move(dodgeText, 0, -2)
            self.drawFighter(defender)
            yield 30
        self.x[defender] = defenderStart
        self.lift[defender] = 0
        self.drawFighter(defender)
        c.delete("temp")

    def playImpact(self, event, damage, showBlocked):
        c = self.canvas
        defender = 1 - event['attacker']
        g = self.GROUND
        move = event['move']
        big = event['kind'] != 'hit'
        if event['kind'] == 'crit':
            color = self.CRIT_COLOR
            label = f"CRITICAL! -{damage}"
        elif move is not None:
            color = theme.MOVE_COLORS.get(move['type'], "#ffdd57")
            label = f"-{damage}"
        else:
            color = "#ffdd57"
            label = f"-{damage}"
        if showBlocked and event['blocked']:
            label += f"  ({event['blocked']} blocked)"

        self.poses[defender] = "hit"
        self.flash[defender] = True
        hitX = self.x[defender] + self.facing[defender] * 14
        hitY = g - 86
        sparkSize = 34 if big else 22
        for angle in range(8):
            dx = [1, 0.7, 0, -0.7, -1, -0.7, 0, 0.7][angle]
            dy = [0, 0.7, 1, 0.7, 0, -0.7, -1, -0.7][angle]
            c.create_line(hitX + dx * 8, hitY + dy * 8, hitX + dx * sparkSize, hitY + dy * sparkSize, fill=color, width=4 if big else 3, tags=("spark", "temp"))
        damageText = c.create_text(self.x[defender], g - 190, text=label, fill=color, font=("Helvetica", 24 if big else 22, "bold"), tags="temp")

        defenderStart = self.x[defender]
        startHP = self.shownHP[defender]
        endHP = max(0, startHP - damage)
        frames = 12
        for frame in range(1, frames + 1):
            if frame == 3:
                self.flash[defender] = False
            if frame == 4:
                c.delete("spark")
            # knocked back a little, then steps back in
            if frame <= frames / 2:
                knockback = frame * (5 if big else 3)
            else:
                knockback = (frames - frame) * (5 if big else 3)
            self.x[defender] = defenderStart - self.facing[defender] * knockback
            self.shownHP[defender] = startHP + (endHP - startHP) * frame / frames
            c.move(damageText, 0, -3)
            self.drawFighter(defender)
            self.drawHealthBars()
            yield 30
        c.delete("temp")
        self.x[defender] = defenderStart
        if event['hp'][defender] > 0:
            self.poses[defender] = "stand"
            self.drawFighter(defender)

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
            self.lift[i] = 0
            if self.events:
                self.shownHP[i] = self.events[-1]['hp'][i]
                self.shownMP[i] = self.events[-1]['mp'][i]
                self.shownShield[i] = self.events[-1]['shield'][i]
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
