import random

# Fight settings
HP_PER_HEALTH = 10      # each health point is worth 10 HP so fights last long enough to watch
MAX_ROUNDS = 300        # if nobody is knocked out by then, whoever has more HP wins
CRIT_MULTIPLIER = 1.75  # critical hits do this much more damage
DEFENSE_SOFTENER = 15   # a fighter with this much defense takes half damage
MOVE_CHANCE = 0.7       # chance of using a special move when one is ready

# ---------- special moves ----------

# Stronger moves cost more mana
def moveCost(move):
    return 15 + move['bonus']

# How much mana a fighter can hold, and how much they get back each time they attack
def maxMana(mana):
    return 30 + mana * 4

def manaGain(mana):
    return 4 + mana // 3

# A short line saying what a move does in a fight
def describeMove(move):
    bonus = move['bonus']
    if move['type'] == 'Strength':
        return f"+{bonus * 3} damage"
    elif move['type'] == 'Speed':
        return "2 hits, can't be dodged"
    elif move['type'] == 'Health':
        return f"heals {bonus * 8} HP"
    else:
        return f"shield blocks {bonus * 6} damage"

# ---------- battle IQ ----------

# A number from 0 to 1 for how much smarter one fighter is than the other
def iqEdge(mine, theirs):
    return mine / (mine + theirs + 10)

def dodgeChance(defender, attacker):
    return 0.03 + 0.3 * iqEdge(defender['battleIQ'], attacker['battleIQ'])

def critChance(attacker, defender):
    return 0.05 + 0.3 * iqEdge(attacker['battleIQ'], defender['battleIQ'])

# Works out the whole fight ahead of time. The fight window then plays it back as an animation
def simulateFight(character1, character2):
    fighters = []
    for character in (character1, character2):
        fighters.append({
            'name': character.name,
            'maxHP': character.health * HP_PER_HEALTH,
            'attack': character.strength,
            'defense': character.defense,
            'speed': character.speed,
            'battleIQ': character.battleIQ,
            'mana': character.mana,
            'maxMP': maxMana(character.mana),
            'moves': list(character.specialMoves),
            'look': dict(character.look),
        })

    hp = [fighters[0]['maxHP'], fighters[1]['maxHP']]
    mp = [0, 0]
    shield = [0, 0]
    totalSpeed = fighters[0]['speed'] + fighters[1]['speed']
    events = []

    # Lands one hit on the defender. Defense makes it smaller and a shield soaks it up first
    def strike(event, rawDamage):
        defender = 1 - event['attacker']
        softened = DEFENSE_SOFTENER / (DEFENSE_SOFTENER + fighters[defender]['defense'])
        damage = max(1, round(rawDamage * random.uniform(0.8, 1.2) * softened))
        blocked = min(shield[defender], damage)
        shield[defender] -= blocked
        hp[defender] = max(0, hp[defender] - (damage - blocked))
        event['hits'].append(damage - blocked)
        event['blocked'] += blocked

    # Picks a special move the fighter can afford and that makes sense right now, or None
    def chooseMove(i):
        fighter = fighters[i]
        usable = []
        for move in fighter['moves']:
            if moveCost(move) > mp[i]:
                continue
            if move['type'] == 'Health' and hp[i] > fighter['maxHP'] * 0.6:
                continue
            if move['type'] == 'Defense' and shield[i] > 0:
                continue
            usable.append(move)
        if usable and random.random() < MOVE_CHANCE:
            return random.choice(usable)
        return None

    # Each round one fighter attacks. The faster you are, the more often you get the attack
    while hp[0] > 0 and hp[1] > 0 and len(events) < MAX_ROUNDS:
        if random.randrange(1, totalSpeed + 1) <= fighters[0]['speed']:
            attacker = 0
        else:
            attacker = 1
        defender = 1 - attacker
        me = fighters[attacker]
        them = fighters[defender]
        mp[attacker] = min(me['maxMP'], mp[attacker] + manaGain(me['mana']))
        event = {'attacker': attacker, 'kind': 'hit', 'move': None, 'hits': [], 'blocked': 0, 'heal': 0, 'shieldGain': 0}

        move = chooseMove(attacker)
        if move is not None:
            mp[attacker] -= moveCost(move)
            event['kind'] = 'move'
            event['move'] = move
            bonus = move['bonus']
            if move['type'] == 'Strength':
                strike(event, me['attack'] + bonus * 3)
            elif move['type'] == 'Speed':
                for count in range(2):
                    if hp[defender] > 0:
                        strike(event, me['attack'] * 0.7 + bonus * 1.5)
            elif move['type'] == 'Health':
                event['heal'] = min(bonus * 8, me['maxHP'] - hp[attacker])
                hp[attacker] += event['heal']
            else:
                event['shieldGain'] = bonus * 6
                shield[attacker] += event['shieldGain']
        elif random.random() < dodgeChance(them, me):
            event['kind'] = 'dodge'
        elif random.random() < critChance(me, them):
            event['kind'] = 'crit'
            strike(event, me['attack'] * CRIT_MULTIPLIER)
        else:
            strike(event, me['attack'])

        # getting hit builds a little mana too
        if event['hits']:
            mp[defender] = min(them['maxMP'], mp[defender] + 2)
        event['damage'] = sum(event['hits'])
        event['hp'] = list(hp)
        event['mp'] = list(mp)
        event['shield'] = list(shield)
        events.append(event)

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
