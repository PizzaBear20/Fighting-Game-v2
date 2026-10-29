import json
import os

from core.character import Character, UNASSIGNED

# The save sits next to FightingGame.py
SAVE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "save_data.json")

# The version of the save format this game writes. Saves from before versions were added count as 1
SAVE_VERSION = 2


# Raised when the save can't be read. By then the broken file has been renamed to brokenFile
class SaveFileError(Exception):
    def __init__(self, error, brokenFile):
        super().__init__(str(error))
        self.brokenFile = brokenFile


# ---------- upgrading old saves ----------

# Each step upgrades the save data by one version. To change the save format, add 1 to
# SAVE_VERSION, write a step that turns the old version into the new one and add it to UPGRADES

# Version 2 added the list of players and gave every fighter an owner
def upgradeToVersion2(data):
    data["players"] = []
    for characterData in data["characters"]:
        characterData.setdefault("owner", UNASSIGNED)

# version a save is at -> the step that upgrades it to the next version
UPGRADES = {
    1: upgradeToVersion2,
}

# Runs the upgrade steps one at a time until the save data is at SAVE_VERSION
def upgradeSave(data):
    if not isinstance(data, dict):
        raise ValueError("the save isn't a JSON object")
    version = data.get("version", 1)
    if not isinstance(version, int) or version < 1:
        raise ValueError(f"unknown save version {version!r}")
    if version > SAVE_VERSION:
        raise ValueError(f"the save is from a newer version of the game (save version {version})")
    while version < SAVE_VERSION:
        UPGRADES[version](data)
        version += 1
        data["version"] = version
    return data


# ---------- saving and loading ----------

def saveGame(characters, players, history, saveFile=SAVE_FILE):
    data = {
        "version": SAVE_VERSION,
        "players": players,
        "characters": [character.toDict() for character in characters.values()],
        "history": history,
    }
    # write to a temporary file first so a crash can't leave a half-written save
    tempFile = saveFile + ".tmp"
    with open(tempFile, "w") as file:
        json.dump(data, file, indent=2)
    os.replace(tempFile, saveFile)

# Returns (characters, players, history). No save yet means an empty game
def loadGame(saveFile=SAVE_FILE):
    if not os.path.exists(saveFile):
        return {}, [], []
    try:
        with open(saveFile) as file:
            data = upgradeSave(json.load(file))
        characters = {}
        for characterData in data["characters"]:
            character = Character.fromDict(characterData)
            characters[character.name] = character
        players = list(data["players"])
        # every owner should be on the player list, even if the save was edited by hand
        for character in characters.values():
            if character.owner != UNASSIGNED and character.owner not in players:
                players.append(character.owner)
        history = list(data.get("history", []))
    except (ValueError, KeyError, TypeError) as error:
        # move the broken save out of the way so the next save doesn't overwrite it
        brokenFile = saveFile.replace(".json", "_broken.json")
        os.replace(saveFile, brokenFile)
        raise SaveFileError(error, brokenFile)
    return characters, players, history
