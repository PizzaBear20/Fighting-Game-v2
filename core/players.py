from core.character import UNASSIGNED

MAX_PLAYER_NAME_LENGTH = 16

# players is the list of player names, in the order they were added.
# Every fighter's owner is one of those names or UNASSIGNED


# Raises ValueError saying what's wrong with the name. oldName is the player being renamed
def checkPlayerName(name, players, oldName=None):
    if name == "":
        raise ValueError("Type a name for the player")
    if len(name) > MAX_PLAYER_NAME_LENGTH:
        raise ValueError(f"Player names can be at most {MAX_PLAYER_NAME_LENGTH} letters long")
    if name.lower() == UNASSIGNED.lower():
        raise ValueError(f"'{UNASSIGNED}' is for fighters with no owner. Pick another name")
    for player in players:
        if player.lower() == name.lower() and player != oldName:
            raise ValueError(f"There is already a player named '{player}'")

# Returns the cleaned up name that was added
def addPlayer(players, name):
    name = name.strip()
    checkPlayerName(name, players)
    players.append(name)
    return name

# Renames the player and moves their fighters over to the new name. Returns the new name
def renamePlayer(players, characters, oldName, newName):
    newName = newName.strip()
    checkPlayerName(newName, players, oldName)
    players[players.index(oldName)] = newName
    for character in characters.values():
        if character.owner == oldName:
            character.owner = newName
    return newName

# Removes the player. Their fighters stay on the roster as UNASSIGNED. Returns how many fighters that was
def removePlayer(players, characters, name):
    players.remove(name)
    count = 0
    for character in characters.values():
        if character.owner == name:
            character.owner = UNASSIGNED
            count += 1
    return count

# Everyone a fighter can belong to
def ownerChoices(players):
    return players + [UNASSIGNED]

# How many fighters the owner has
def fighterCount(characters, owner):
    return sum(1 for character in characters.values() if character.owner == owner)
