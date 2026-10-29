import random

# ---------- how a character looks ----------

# The first choice in each list is the "plain" one
BUILDS = ["normal", "thin", "big"]
GLOVES = ["boxing", "wraps", "claws", "bare"]
FACES = ["normal", "happy", "angry", "smirk", "fierce", "calm"]
FACE_GEAR = ["none", "shades", "glasses", "visor", "eyepatch", "mask"]
HAIR_STYLES = ["none", "buzz", "short", "swoop", "spiky", "mohawk", "long", "ponytail", "bun", "afro"]
FACIAL_HAIR = ["none", "stubble", "mustache", "goatee", "beard"]
HEADWEAR = ["none", "headband", "cap", "tophat", "wizard", "helmet", "crown", "horns", "halo"]
OUTFITS = ["none", "shirt", "jacket", "gi", "armor", "robe"]
PANTS = ["none", "shorts", "pants"]
SHOES = ["none", "sneakers", "boots"]
CAPES = ["none", "scarf", "cape", "wings", "batwings"]
AURAS = ["none", "glow", "flame"]

COLOR_CHOICES = [
    "#4da3ff", "#ff6b6b", "#4cd964", "#ffcc00", "#b47cff", "#ff9f43", "#00d2d3", "#ff6bcb",
    "#f5f6fa", "#a4b0be", "#2f3542", "#1e272e", "#8d6e63", "#c0392b", "#16a085", "#2c3e99",
]
NEUTRALS = ["#f5f6fa", "#a4b0be", "#2f3542", "#1e272e"]
SKIN_TONES = ["#ffe0bd", "#ffcd94", "#eac086", "#e0ac69", "#c68642", "#a5694f", "#8d5524", "#5c3a1e",
              "#8fd16a", "#7fb3ff", "#c7c7d1", "#e05a4f"]
HAIR_COLORS = ["#1e1e1e", "#4a2f1b", "#8d5524", "#e6c35c", "#d35400", "#f5f6fa"]
EYE_COLORS = ["#1b1b24", "#4a2f1b", "#8d6e63", "#2e86de", "#16a085", "#7f8c8d", "#c0392b", "#8e44ad", "#ffcc00"]

# A fighter with nothing extra on. Old saves use this for parts that didn't exist yet
PLAIN_LOOK = {
    "build": "normal", "bodyColor": "#4da3ff", "skinColor": "#e0ac69",
    "gloveStyle": "boxing", "gloveColor": "#ff6b6b",
    "face": "normal", "eyeColor": "#1b1b24", "faceGear": "none", "faceGearColor": "#1e272e",
    "hairStyle": "short", "hairColor": "#4a2f1b", "facialHair": "none",
    "headwear": "none", "headwearColor": "#ff6b6b",
    "outfit": "none", "outfitColor": "#f5f6fa",
    "pants": "none", "pantsColor": "#2c3e99",
    "shoes": "none", "shoeColor": "#8d6e63",
    "cape": "none", "capeColor": "#c0392b",
    "aura": "none", "auraColor": "#4da3ff",
}

# Returns the plain choice (the first one) about plainChance of the time, otherwise one of the others
def pickStyle(options, plainChance):
    if random.random() < plainChance:
        return options[0]
    return random.choice(options[1:])

# Picks a color for every part from a small color scheme, so the whole outfit goes together
def randomColors(skinColor):
    main, accent = random.sample(COLOR_CHOICES[:8], 2)
    dark = random.choice(NEUTRALS)
    bodyColor = random.choice([main, dark, skinColor])
    # the clothes shouldn't be the same color as the body or they disappear
    clothes = [color for color in (main, accent, dark) if color != bodyColor]
    return {
        "bodyColor": bodyColor,
        "gloveColor": random.choice([main, accent, dark]),
        "eyeColor": random.choice(EYE_COLORS[:6]),
        "faceGearColor": random.choice([dark, main]),
        "hairColor": random.choice(HAIR_COLORS * 2 + [main, accent]),
        "headwearColor": random.choice([main, accent, dark]),
        "outfitColor": random.choice(clothes),
        "pantsColor": random.choice(clothes),
        "shoeColor": random.choice([dark, "#f5f6fa", accent]),
        "capeColor": random.choice([accent, main]),
        "auraColor": random.choice([main, accent]),
    }

def randomLook():
    skinColor = random.choice(SKIN_TONES[:8])
    look = {
        "build": random.choice(BUILDS),
        "skinColor": skinColor,
        "gloveStyle": pickStyle(GLOVES, 0.6),
        "face": random.choice(FACES),
        "faceGear": pickStyle(FACE_GEAR, 0.75),
        "hairStyle": pickStyle(HAIR_STYLES, 0.15),
        "facialHair": pickStyle(FACIAL_HAIR, 0.7),
        "headwear": pickStyle(HEADWEAR, 0.5),
        "outfit": pickStyle(OUTFITS, 0.2),
        "pants": pickStyle(PANTS, 0.3),
        "shoes": pickStyle(SHOES, 0.3),
        "cape": pickStyle(CAPES, 0.55),
        "aura": pickStyle(AURAS, 0.8),
    }
    look.update(randomColors(skinColor))
    return look


# Ready-made styles. Anything a preset doesn't list goes back to plain, except the fighter
# keeps their own skin, hair and eye color. A color of "skin" means "the same as the skin"
PRESETS = [
    ("Brawler", {"build": "big", "bodyColor": "skin", "face": "angry", "hairStyle": "buzz",
                 "headwear": "headband", "headwearColor": "#ff6b6b", "gloveColor": "#ff6b6b",
                 "pants": "shorts", "pantsColor": "#ff6b6b", "shoes": "sneakers", "shoeColor": "#f5f6fa"}),
    ("Ninja", {"build": "thin", "bodyColor": "#1e272e", "face": "fierce", "hairStyle": "none",
               "headwear": "headband", "headwearColor": "#c0392b", "faceGear": "mask", "faceGearColor": "#2f3542",
               "outfit": "gi", "outfitColor": "#2f3542", "pants": "pants", "pantsColor": "#2f3542",
               "gloveStyle": "wraps", "gloveColor": "#a4b0be", "cape": "scarf", "capeColor": "#c0392b"}),
    ("Knight", {"build": "big", "bodyColor": "#2f3542", "outfit": "armor", "outfitColor": "#a4b0be",
                "headwear": "helmet", "headwearColor": "#a4b0be", "gloveColor": "#a4b0be",
                "pants": "pants", "pantsColor": "#2f3542", "shoes": "boots", "shoeColor": "#a4b0be",
                "cape": "cape", "capeColor": "#2c3e99"}),
    ("Wizard", {"build": "thin", "bodyColor": "#2c3e99", "face": "calm", "hairStyle": "long", "hairColor": "#f5f6fa",
                "facialHair": "beard", "headwear": "wizard", "headwearColor": "#2c3e99",
                "outfit": "robe", "outfitColor": "#2c3e99", "gloveStyle": "bare",
                "aura": "glow", "auraColor": "#b47cff"}),
    ("King", {"build": "big", "bodyColor": "#c0392b", "face": "smirk", "facialHair": "beard",
              "headwear": "crown", "headwearColor": "#ffcc00", "outfit": "robe", "outfitColor": "#c0392b",
              "gloveStyle": "bare", "shoes": "boots", "shoeColor": "#8d6e63", "cape": "cape", "capeColor": "#ffcc00"}),
    ("Demon", {"skinColor": "#e05a4f", "bodyColor": "#1e272e", "face": "fierce", "eyeColor": "#ffcc00",
               "hairStyle": "none", "headwear": "horns", "headwearColor": "#2f3542",
               "gloveStyle": "claws", "gloveColor": "#1e272e", "pants": "pants", "pantsColor": "#1e272e",
               "cape": "batwings", "capeColor": "#2f3542", "aura": "flame", "auraColor": "#ff6b6b"}),
    ("Angel", {"bodyColor": "#f5f6fa", "face": "calm", "hairStyle": "long", "hairColor": "#e6c35c",
               "headwear": "halo", "headwearColor": "#ffcc00", "outfit": "robe", "outfitColor": "#f5f6fa",
               "gloveStyle": "bare", "cape": "wings", "capeColor": "#f5f6fa",
               "aura": "glow", "auraColor": "#ffcc00"}),
    ("Street", {"bodyColor": "skin", "face": "smirk", "hairStyle": "short", "faceGear": "shades",
                "headwear": "cap", "headwearColor": "#4da3ff", "outfit": "jacket", "outfitColor": "#ff9f43",
                "gloveStyle": "wraps", "gloveColor": "#f5f6fa", "pants": "pants", "pantsColor": "#2c3e99",
                "shoes": "sneakers", "shoeColor": "#f5f6fa"}),
]

# Returns a copy of look dressed up as the preset
def applyPreset(look, preset):
    newLook = dict(PLAIN_LOOK)
    for key in ("skinColor", "hairColor", "eyeColor"):
        newLook[key] = look[key]
    newLook.update(preset)
    for key, value in newLook.items():
        if value == "skin":
            newLook[key] = newLook["skinColor"]
    return newLook


# Owner of fighters that don't belong to a player yet
UNASSIGNED = "Unassigned"


class Character:
    def __init__(self, name, owner=UNASSIGNED):
        self.name = name
        self.owner = owner
        self.specialMoves = []
        self.look = randomLook()

    def stats(self):
        self.points = random.randrange(1, 21)
        self.health = 1
        self.strength = 1
        self.speed = 1
        self.mana = 1
        self.battleIQ = 1
        self.defense = 1
        count = 1
        while count <= self.points:
            randomNum = random.randrange(1, 7)
            if randomNum == 1:
                self.health += 1
            elif randomNum == 2:
                self.strength += 1
            elif randomNum == 3:
                self.speed += 1
            elif randomNum == 4:
                self.mana += 1
            elif randomNum == 5:
                self.defense += 1
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
            f"Defense: {self.defense}\n"
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
        
            abilityTypeRoll = random.randrange(1,5) #1strength health speed defense
            if abilityTypeRoll == 1:
                abilityType = "Strength"
            elif abilityTypeRoll == 2:
                abilityType = "Health"
            elif abilityTypeRoll == 3:
                abilityType = "Speed"
            else:
                abilityType = "Defense"

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
                attribute = random.choice(["health", "strength", "speed", "mana", "battleIQ", "defense"])

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
            elif attribute == "defense":
                self.defense += increment
        
        return message

    def powerLevel(self):
        powerLevel = self.health + self.strength + self.speed + self.mana + self.battleIQ + self.defense
        for move in self.specialMoves:
            powerLevel += move['bonus']
        return powerLevel

    # Trains several times in a row and sums up what changed
    def trainMany(self, attribute, times):
        statNames = {"health": "health", "strength": "strength", "speed": "speed", "mana": "mana", "battleIQ": "battle IQ", "defense": "defense"}
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
            "owner": self.owner,
            "health": self.health,
            "strength": self.strength,
            "speed": self.speed,
            "mana": self.mana,
            "battleIQ": self.battleIQ,
            "defense": self.defense,
            "specialMoves": self.specialMoves,
            "look": self.look,
        }

    @staticmethod
    def fromDict(data):
        character = Character(data["name"], data.get("owner", UNASSIGNED))
        character.health = data["health"]
        character.strength = data["strength"]
        character.speed = data["speed"]
        character.mana = data["mana"]
        character.battleIQ = data["battleIQ"]
        character.defense = data.get("defense", 1)  # older saves didn't have defense
        character.specialMoves = data.get("specialMoves", [])
        savedLook = data.get("look")
        if savedLook:
            # parts that were added after this fighter was saved start out plain
            character.look = dict(PLAIN_LOOK)
            for key, value in savedLook.items():
                if key in character.look:
                    character.look[key] = value
            # shades used to be a face. Now they're face gear
            if character.look["face"] == "shades":
                character.look["face"] = "normal"
                character.look["faceGear"] = "shades"
        return character


# Attribute names people can pick or type -> the real attribute name
ATTRIBUTE_CHOICES = ["Random", "Health", "Strength", "Speed", "Mana", "Battle IQ", "Defense"]
attributeNames = {
    "health": "health",
    "strength": "strength",
    "speed": "speed",
    "mana": "mana",
    "battleiq": "battleIQ",
    "battle iq": "battleIQ",
    "iq": "battleIQ",
    "defense": "defense",
    "random": "random",
}

# Turns text like "Battle IQ" into "battleIQ". Returns None if it isn't an attribute
def cleanAttribute(text):
    return attributeNames.get(text.strip().lower())
