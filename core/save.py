import json
import os

from core.character import Character

# The save sits next to FightingGame.py
SAVE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "save_data.json")


# Raised when the save can't be read. By then the broken file has been renamed to brokenFile
class SaveFileError(Exception):
    def __init__(self, error, brokenFile):
        super().__init__(str(error))
        self.brokenFile = brokenFile


def saveGame(characters, history, saveFile=SAVE_FILE):
    data = {
        "characters": [character.toDict() for character in characters.values()],
        "history": history,
    }
    # write to a temporary file first so a crash can't leave a half-written save
    tempFile = saveFile + ".tmp"
    with open(tempFile, "w") as file:
        json.dump(data, file, indent=2)
    os.replace(tempFile, saveFile)

# Returns (characters, history). No save yet means an empty game
def loadGame(saveFile=SAVE_FILE):
    if not os.path.exists(saveFile):
        return {}, []
    try:
        with open(saveFile) as file:
            data = json.load(file)
        characters = {}
        for characterData in data["characters"]:
            character = Character.fromDict(characterData)
            characters[character.name] = character
        history = list(data.get("history", []))
    except (ValueError, KeyError, TypeError) as error:
        # move the broken save out of the way so the next save doesn't overwrite it
        brokenFile = saveFile.replace(".json", "_broken.json")
        os.replace(saveFile, brokenFile)
        raise SaveFileError(error, brokenFile)
    return characters, history
