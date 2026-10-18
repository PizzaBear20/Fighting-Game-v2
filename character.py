import random

# ---------- how a character looks ----------

BUILDS = ["thin", "normal", "big"]
HAIR_STYLES = ["none", "short", "spiky", "mohawk", "long", "afro", "ponytail"]
HEADWEAR = ["none", "headband", "cap", "crown", "horns", "halo"]
FACES = ["normal", "happy", "angry", "shades"]
OUTFITS = ["none", "shirt", "gi", "armor"]
CAPES = ["none", "scarf", "cape"]

COLOR_CHOICES = [
    "#4da3ff", "#ff6b6b", "#4cd964", "#ffcc00", "#b47cff", "#ff9f43", "#00d2d3", "#ff6bcb",
    "#f5f6fa", "#a4b0be", "#2f3542", "#1e272e", "#8d6e63", "#c0392b", "#16a085", "#2c3e99",
]
SKIN_TONES = ["#ffe0bd", "#ffcd94", "#eac086", "#e0ac69", "#c68642", "#a5694f", "#8d5524", "#5c3a1e",
              "#8fd16a", "#7fb3ff", "#c7c7d1"]

def randomLook():
    return {
        "build": random.choice(BUILDS),
        "bodyColor": random.choice(COLOR_CHOICES[:8]),
        "skinColor": random.choice(SKIN_TONES[:8]),
        "gloveColor": random.choice(COLOR_CHOICES),
        "face": random.choice(FACES),
        "hairStyle": random.choice(HAIR_STYLES),
        "hairColor": random.choice(["#1e1e1e", "#4a2f1b", "#8d5524", "#e6c35c", "#d35400", "#f5f6fa"] + COLOR_CHOICES[:8]),
        "headwear": random.choice(HEADWEAR[:3] + ["none", "none"]),
        "headwearColor": random.choice(COLOR_CHOICES),
        "outfit": random.choice(OUTFITS),
        "outfitColor": random.choice(COLOR_CHOICES),
        "cape": random.choice(CAPES + ["none"]),
        "capeColor": random.choice(COLOR_CHOICES),
    }


class Character:
    def __init__(self, name):
        self.name = name
        self.specialMoves = []
        self.look = randomLook()

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

    def powerLevel(self):
        powerLevel = self.health + self.strength + self.speed + self.mana + self.battleIQ
        for move in self.specialMoves:
            powerLevel += move['bonus']
        return powerLevel

    # Trains several times in a row and sums up what changed
    def trainMany(self, attribute, times):
        statNames = {"health": "health", "strength": "strength", "speed": "speed", "mana": "mana", "battleIQ": "battle IQ"}
        before = {stat: getattr(self, stat) for stat in statNames}
        movesBefore = len(self.specialMoves)
        lastMessage = ""
        for count in range(times):
            lastMessage = self.train(attribute)
        if times == 1:
            return lastMessage

        gains = []
        for stat, label in statNames.items():
            gain = getattr(self, stat) - before[stat]
            if gain > 0:
                gains.append(f"+{gain} {label}")
        if gains:
            message = f"{self.name} trained {times} times: " + ", ".join(gains)
        else:
            message = f"{self.name} trained {times} times but did not improve"
        newMoves = [move['name'] for move in self.specialMoves[movesBefore:]]
        if newMoves:
            message += ". Learned " + ", ".join(newMoves) + "!"
        return message

    # Saving and loading
    def toDict(self):
        return {
            "name": self.name,
            "health": self.health,
            "strength": self.strength,
            "speed": self.speed,
            "mana": self.mana,
            "battleIQ": self.battleIQ,
            "specialMoves": self.specialMoves,
            "look": self.look,
        }

    @staticmethod
    def fromDict(data):
        character = Character(data["name"])
        character.health = data["health"]
        character.strength = data["strength"]
        character.speed = data["speed"]
        character.mana = data["mana"]
        character.battleIQ = data["battleIQ"]
        character.specialMoves = data.get("specialMoves", [])
        # start from a random look so anything missing from the save still has a value
        for key, value in data.get("look", {}).items():
            if key in character.look:
                character.look[key] = value
        return character


# Attribute names people can pick or type -> the real attribute name
ATTRIBUTE_CHOICES = ["Random", "Health", "Strength", "Speed", "Mana", "Battle IQ"]
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

# Turns text like "Battle IQ" into "battleIQ". Returns None if it isn't an attribute
def cleanAttribute(text):
    return attributeNames.get(text.strip().lower())
