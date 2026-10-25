import math
import time

# ---------- color helpers ----------

def hexToRgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

def rgbToHex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(value))) for value in rgb)

# amount 0 = all color1, amount 1 = all color2
def mix(color1, color2, amount):
    rgb1 = hexToRgb(color1)
    rgb2 = hexToRgb(color2)
    return rgbToHex([rgb1[i] + (rgb2[i] - rgb1[i]) * amount for i in range(3)])

def darker(color, amount=0.3):
    return mix(color, "#000000", amount)

def lighter(color, amount=0.3):
    return mix(color, "#ffffff", amount)

def brightness(color):
    red, green, blue = hexToRgb(color)
    return (0.299 * red + 0.587 * green + 0.114 * blue) / 255

# Lightens dark colors so text in that color can be read on the dark background
def readable(color):
    while brightness(color) < 0.5:
        color = lighter(color, 0.2)
    return color


# ---------- arena background ----------

SKY_BANDS = ["#20243a", "#23283f", "#262c45", "#29304b", "#2c3451", "#2f3857"]
FLOOR = "#3b3b52"
SHADOW = "#2a2a3d"

def drawArena(canvas, width, height, ground, tag="arena"):
    bandHeight = ground / len(SKY_BANDS)
    for i, color in enumerate(SKY_BANDS):
        canvas.create_rectangle(0, i * bandHeight, width, (i + 1) * bandHeight + 1, fill=color, outline="", tags=tag)
    canvas.create_rectangle(0, ground, width, height, fill=FLOOR, outline="", tags=tag)
    canvas.create_line(0, ground, width, ground, fill="#5a5a7a", width=3, tags=tag)
    for lineX in range(0, width + 80, 80):
        canvas.create_line(lineX, ground + 10, lineX - 40, height, fill="#44445e", width=2, tags=tag)


# ---------- fighters ----------

# limb width, head radius, outfit width, fist radius
BUILD_SIZES = {
    "thin": (4, 14, 13, 6),
    "normal": (6, 15, 17, 7),
    "big": (9, 17, 24, 9),
}
EYE_WHITE = "#ffffff"
EYE_DARK = "#1b1b24"


# Where the hips, shoulders, head, arms and legs go for each pose.
# Numbers are measured from the fighter's feet: x goes right, y goes up (negative = higher)
def fighterJoints(pose, f, headRadius):
    if pose == "down":
        return {
            "hip": (f * 10, -12),
            "shoulder": (-f * 34, -12),
            "head": (-f * (34 + headRadius + 6), -14),
            "headAngle": -f * math.pi / 2,  # head is turned sideways, lying on the floor
            "legs": [((f * 30, -6), (f * 52, -4)), ((f * 28, -18), (f * 46, -26))],
            "arms": [((-f * 22, -28), (-f * 10, -38)), ((-f * 24, -2), (-f * 8, -3))],
        }

    if pose == "hit":
        lean = -f * 10
    elif pose == "punch":
        lean = f * 8
    else:
        lean = 0
    sx = lean  # shoulders move when leaning

    if pose == "punch":
        feet = [f * 30, -f * 28]
    else:
        feet = [f * 18, -f * 16]

    # each arm is (elbow, fist). The front arm comes first
    if pose == "punch":
        arms = [((sx + f * 30, -85), (sx + f * 62, -86)), ((sx + f * 8, -62), (sx + f * 21, -81))]
    elif pose == "win":
        arms = [((sx + f * 24, -102), (sx + f * 32, -132)), ((sx - f * 24, -102), (sx - f * 32, -132))]
    elif pose == "hit":
        arms = [((sx - f * 22, -70), (sx - f * 36, -88)), ((sx - f * 12, -58), (sx - f * 28, -54))]
    else:
        arms = [((sx + f * 18, -64), (sx + f * 30, -86)), ((sx + f * 6, -60), (sx + f * 20, -76))]

    return {
        "hip": (0, -50),
        "shoulder": (sx, -88),
        "head": (sx * 1.4, -88 - headRadius - 7),
        "headAngle": 0,
        "legs": [((footX / 2, -24), (footX, 0)) for footX in feet],
        "arms": arms,
    }



# The point that is "amount" of the way from p1 to p2 (0 = p1, 1 = p2)
def between(p1, p2, amount):
    return (p1[0] + (p2[0] - p1[0]) * amount, p1[1] + (p2[1] - p1[1]) * amount)

# A darker or lighter version of a color that shows up on top of it
def contrast(color, amount=0.45):
    if brightness(color) > 0.35:
        return darker(color, amount)
    return lighter(color, amount)


# Wing shapes as (along the body, behind the fighter) from the shoulder. Negative "along" is higher up.
# Feathered wings are a row of feathers hanging off the wing's arm: (where it starts, where it ends)
WING_ARM = [(4, 2), (-14, 12), (-30, 26)]
WING_FEATHERS = [((-30, 26), (-50, 42)), ((-26, 24), (-38, 50)), ((-20, 20), (-24, 56)), ((-14, 16), (-9, 56)),
                 ((-8, 12), (4, 51)), ((-2, 8), (14, 42))]
BAT_WING_SHAPE = [(0, 2), (-22, 18), (-42, 40), (-26, 38), (-16, 54), (-6, 40), (8, 50), (8, 34), (20, 30), (14, 8)]

AURA_BACKGROUND = "#272c44"  # auras fade into this, since every background in the game is about this dark
CLAW_COLOR = "#e8e8f0"
PLUME_COLOR = "#d63031"
STAR_COLOR = "#ffcc00"


# Draws a fighter using their look (colors, hair, hat, outfit...).
# x, ground = where their feet are. facing: 1 = right, -1 = left.
# pose: stand, punch, hit, win, down. scale makes them bigger or smaller
def drawFighter(canvas, x, ground, look, facing=1, pose="stand", scale=1.0, tag="fighter", flash=False, shadow=SHADOW):
    f = facing
    limbWidth, headRadius, outfitWidth, fistRadius = BUILD_SIZES.get(look.get("build"), BUILD_SIZES["normal"])
    joints = fighterJoints(pose, f, headRadius)
    knockedOut = pose == "down"

    # fighters flash white when they get hit and go gray when they're knocked out
    def tone(color):
        if flash:
            return "#ffffff"
        if knockedOut:
            return mix(color, "#6b6b7b", 0.55)
        return color

    def paint(key):
        return tone(look.get(key, "#888888"))

    # turns fighter coordinates into canvas coordinates
    def point(p):
        return (x + p[0] * scale, ground + p[1] * scale)

    def flat(points):
        result = []
        for p in points:
            result.extend(point(p))
        return result

    def line(points, color, width, smooth=False):
        canvas.create_line(*flat(points), fill=color, width=max(1, width * scale), capstyle="round",
                           joinstyle="round", smooth=smooth, tags=tag)

    def polygon(points, color, outline="", smooth=False, width=1):
        canvas.create_polygon(*flat(points), fill=color, outline=outline, width=max(1, width * scale),
                              smooth=smooth, tags=tag)

    def circle(center, radius, color, outline="", width=1):
        oval(center, radius, radius, color, outline, width)

    def oval(center, radiusX, radiusY, color, outline="", width=1):
        centerX, centerY = point(center)
        canvas.create_oval(centerX - radiusX * scale, centerY - radiusY * scale, centerX + radiusX * scale,
                           centerY + radiusY * scale, fill=color, outline=outline,
                           width=max(1, width * scale) if outline else 0, tags=tag)

    # Head helpers: "forward" and "up" are measured in head sizes, so hair and hats
    # stay on the head even when the fighter is lying down
    headX, headY = joints["head"]
    cosA = math.cos(joints["headAngle"])
    sinA = math.sin(joints["headAngle"])
    r = headRadius

    def onHead(forward, up):
        localX = forward * f * r
        localY = -up * r
        return (headX + localX * cosA - localY * sinA, headY + localX * sinA + localY * cosA)

    def around(radius, degrees):
        angle = math.radians(degrees)
        return onHead(radius * math.cos(angle), radius * math.sin(angle))

    def arc(radius, startDegrees, endDegrees, steps=12):
        return [around(radius, startDegrees + (endDegrees - startDegrees) * k / steps) for k in range(steps + 1)]

    # Body helpers: move a point along the body (towards the hips) or behind the fighter
    hip = joints["hip"]
    shoulder = joints["shoulder"]
    bodyLength = math.hypot(hip[0] - shoulder[0], hip[1] - shoulder[1])
    downX = (hip[0] - shoulder[0]) / bodyLength
    downY = (hip[1] - shoulder[1]) / bodyLength
    backPoint = onHead(-1, 0)
    backX = (backPoint[0] - headX) / r
    backY = (backPoint[1] - headY) / r

    def offset(base, alongBody, behind):
        return (base[0] + downX * alongBody + backX * behind, base[1] + downY * alongBody + backY * behind)

    bodyColor = paint("bodyColor")
    skinColor = paint("skinColor")
    gloveColor = paint("gloveColor")
    hairColor = paint("hairColor")
    hairStyle = look.get("hairStyle", "none")
    cape = look.get("cape", "none")

    # ----- behind the fighter: aura, shadow, cape or wings, long hair -----

    # the aura goes out when the fighter is knocked out
    aura = look.get("aura", "none")
    if aura != "none" and not knockedOut and not flash:
        auraColor = look.get("auraColor", "#4da3ff")
        center = (shoulder[0] * 0.6, -70)
        wiggle = time.monotonic() * 6  # different every time it's drawn, so animated fighters flicker
        if aura == "glow":
            pulse = 1 + 0.04 * math.sin(wiggle / 2)
            for size, fade in ((1.0, 0.86), (0.85, 0.74), (0.7, 0.62), (0.55, 0.5)):
                oval(center, 44 * size * pulse, 76 * size * pulse, mix(auraColor, AURA_BACKGROUND, fade))
        elif aura == "flame":
            for size, fade in ((1.0, 0.68), (0.74, 0.42)):
                points = []
                for k in range(16):
                    angle = 2 * math.pi * k / 16
                    pointX = math.cos(angle) * 40 * size
                    pointY = math.sin(angle) * 66 * size
                    upness = -math.sin(angle)  # 1 at the top, 0 at the sides
                    if upness > 0 and k % 2 == 0:
                        # flame tongues lick upwards
                        pointY -= (26 + 7 * math.sin(wiggle + k)) * size * upness
                        pointX *= 0.75
                    points.append((center[0] + pointX, center[1] + 6 + pointY))
                polygon(points, mix(auraColor, AURA_BACKGROUND, fade), smooth=True)

    if shadow:
        canvas.create_oval(x - 38 * scale, ground - 6 * scale, x + 38 * scale, ground + 6 * scale,
                           fill=shadow, outline="", tags=tag)

    spread = 0.3 if knockedOut else 1
    if cape == "cape":
        capeColor = paint("capeColor")
        polygon([offset(shoulder, 0, 3 * spread), offset(shoulder, bodyLength * 0.8, 18 * spread),
                 offset(shoulder, bodyLength * 1.8, 30 * spread), offset(shoulder, bodyLength * 1.9, 6 * spread),
                 offset(shoulder, bodyLength * 0.9, 0)],
                capeColor, outline=darker(capeColor), smooth=True, width=2)
    elif cape in ("wings", "batwings"):
        capeColor = paint("capeColor")
        # the far wing peeks out a little higher than the near one
        for lift, shift, color in ((-7, -8, darker(capeColor, 0.25)), (0, 0, capeColor)):
            def wingPoint(p):
                return offset(shoulder, (p[0] + lift) * spread, (p[1] + shift) * spread)
            if cape == "wings":
                for start, end in WING_FEATHERS:
                    line([wingPoint(start), wingPoint(end)], darker(color, 0.3), 9)
                    line([wingPoint(start), wingPoint(end)], color, 6.5)
                line([wingPoint(p) for p in WING_ARM], darker(color, 0.3), 10)
                line([wingPoint(p) for p in WING_ARM], color, 7.5)
            else:
                polygon([wingPoint(p) for p in BAT_WING_SHAPE], color, outline=darker(capeColor, 0.4), width=1.5)

    if hairStyle == "afro":
        circle(onHead(-0.15, 0.3), r * 1.55, hairColor)
    elif hairStyle == "long":
        polygon([onHead(0.5, 1.0), onHead(-0.3, 1.2), onHead(-1.1, 0.75), onHead(-1.3, -0.4), onHead(-1.25, -1.7),
                 onHead(-0.7, -1.9), onHead(-0.45, -0.6)], hairColor, smooth=True)
    elif hairStyle == "ponytail":
        polygon([onHead(-0.8, 0.6), onHead(-1.5, 0.8), onHead(-2.2, 0.1), onHead(-2.1, -1.0), onHead(-1.7, -0.3),
                 onHead(-1.0, 0.1)], hairColor, smooth=True)

    # ----- arms, legs and body -----

    gloveStyle = look.get("gloveStyle", "boxing")

    def drawArm(arm, fistSize):
        elbow, fist = arm
        line([offset(shoulder, 4, 0), elbow, fist], bodyColor, limbWidth)
        if gloveStyle == "bare":
            circle(fist, fistSize * 0.75, skinColor, outline=darker(skinColor, 0.35), width=1)
        elif gloveStyle == "wraps":
            line([between(fist, elbow, 0.45), fist], gloveColor, limbWidth + 1.5)
            circle(fist, fistSize * 0.8, skinColor, outline=gloveColor, width=2.5)
        elif gloveStyle == "claws":
            length = math.hypot(fist[0] - elbow[0], fist[1] - elbow[1])
            dirX = (fist[0] - elbow[0]) / length
            dirY = (fist[1] - elbow[1]) / length
            for side in (-1, 0, 1):
                base = (fist[0] - dirY * side * fistSize * 0.6, fist[1] + dirX * side * fistSize * 0.6)
                tip = (base[0] + dirX * fistSize * 1.9 - dirY * side * fistSize * 0.3,
                       base[1] + dirY * fistSize * 1.9 + dirX * side * fistSize * 0.3)
                line([base, tip], tone(CLAW_COLOR), 1.6)
            circle(fist, fistSize * 0.9, gloveColor, outline=darker(gloveColor), width=1.5)
        else:
            circle(fist, fistSize, gloveColor, outline=darker(gloveColor), width=1.5)

    shoes = look.get("shoes", "none")
    shoeColor = paint("shoeColor")
    shoeWidth = limbWidth * 0.6 + 4

    def drawShoe(knee, foot):
        length = math.hypot(foot[0] - knee[0], foot[1] - knee[1])
        shinX = (foot[0] - knee[0]) / length
        shinY = (foot[1] - knee[1]) / length
        # toes point the way the fighter is facing (or up, when they're lying down)
        toeX = f * shinY
        toeY = -f * shinX
        sole = (foot[0] - shinX * 2, foot[1] - shinY * 2)
        heel = (sole[0] - toeX * 3, sole[1] - toeY * 3)
        toe = (sole[0] + toeX * (6 + limbWidth * 0.3), sole[1] + toeY * (6 + limbWidth * 0.3))
        if shoes == "boots":
            line([between(foot, knee, 0.45), sole], shoeColor, limbWidth + 3)
            line([heel, toe], shoeColor, shoeWidth + 1)
        else:
            line([heel, toe], shoeColor, shoeWidth)
            if brightness(shoeColor) < 0.7:
                soleColor = tone("#f5f6fa")
            else:
                soleColor = tone("#a4b0be")
            edge = shoeWidth * 0.4
            line([(heel[0] + shinX * edge, heel[1] + shinY * edge), (toe[0] + shinX * edge, toe[1] + shinY * edge)],
                 soleColor, 1.6)

    pants = look.get("pants", "none")
    pantsColor = paint("pantsColor")

    drawArm(joints["arms"][1], fistRadius - 1)
    for knee, foot in joints["legs"]:
        line([hip, knee, foot], bodyColor, limbWidth)
        if pants == "shorts":
            line([hip, between(hip, knee, 0.85)], pantsColor, limbWidth + 4)
        elif pants == "pants":
            line([hip, knee, between(foot, knee, 0.12)], pantsColor, limbWidth + 3)
        if shoes != "none":
            drawShoe(knee, foot)
    line([hip, shoulder], bodyColor, limbWidth)

    outfit = look.get("outfit", "none")
    if outfit != "none":
        outfitColor = paint("outfitColor")
        half = outfitWidth * 0.55
        if outfit == "robe":
            # a long skirt that hangs down past the knees
            polygon([offset(hip, -6, -half), offset(hip, -6, half), offset(hip, 32, half * 1.9),
                     offset(hip, 34, 0), offset(hip, 32, -half * 1.9)], outfitColor, outline=darker(outfitColor, 0.25))
        line([offset(hip, -4, 0), offset(shoulder, 4, 0)], outfitColor, outfitWidth)
        if outfit in ("gi", "armor", "robe"):
            if outfit == "gi":
                beltColor = "#20202a"
            elif outfit == "robe":
                beltColor = contrast(outfitColor, 0.35)
            else:
                beltColor = darker(outfitColor, 0.4)
            beltCenter = offset(hip, -8, 0)
            line([offset(beltCenter, 0, -half), offset(beltCenter, 0, half)], beltColor, 4)
        if outfit == "armor":
            circle(offset(shoulder, 6, 0), outfitWidth * 0.5, lighter(outfitColor, 0.2), outline=darker(outfitColor, 0.4), width=2)
        elif outfit == "jacket":
            # the open front shows the body underneath, and the collar sticks up behind the neck
            line([offset(shoulder, 7, -half * 0.55), offset(hip, -6, -half * 0.55)], bodyColor, 2.5)
            polygon([offset(shoulder, 4, half * 1.0), offset(shoulder, -5, half * 0.55), offset(shoulder, 3, -half * 0.1)],
                    darker(outfitColor, 0.25))

    # neck and scarf
    line([shoulder, onHead(0, -0.9)], skinColor, limbWidth * 0.8)
    if cape == "scarf":
        scarfColor = paint("capeColor")
        neck = offset(shoulder, -3, 0)
        line([offset(neck, 0, -6), offset(neck, 0, 6)], scarfColor, 8)
        line([offset(neck, 0, 4), offset(neck, 4, 18), offset(neck, 12, 32)], scarfColor, 6, smooth=True)

    drawArm(joints["arms"][0], fistRadius)

    # ----- head and face -----

    circle(joints["head"], r, skinColor, outline=darker(skinColor, 0.35), width=1.5)
    face = look.get("face", "normal")
    facialHair = look.get("facialHair", "none")
    mouthColor = darker(skinColor, 0.6)

    # stubble and beards go under the mouth
    if facialHair == "stubble":
        polygon(arc(1.0, -15, -125) + [onHead(-0.42, -0.3), onHead(-0.28, 0.25), onHead(-0.05, 0.25), onHead(0.15, -0.12),
                                       onHead(0.6, -0.22)], mix(skinColor, hairColor, 0.35), smooth=True)
    elif facialHair == "beard":
        # from the sideburn, along the jaw, down to a pointy chin, then back up under the mouth
        polygon([onHead(-0.05, 0.3), onHead(-0.32, 0.25), onHead(-0.5, -0.3), onHead(-0.45, -0.95), onHead(0.05, -1.25),
                 onHead(0.55, -1.55), onHead(0.95, -1.0), onHead(1.06, -0.45), onHead(0.86, -0.55), onHead(0.55, -0.68),
                 onHead(0.28, -0.45), onHead(0.16, -0.1)], hairColor, smooth=True)

    eyes = [0.62, 0.22]
    if knockedOut:
        for eye in eyes:
            line([onHead(eye - 0.13, 0.25), onHead(eye + 0.13, -0.01)], EYE_DARK, 2)
            line([onHead(eye - 0.13, -0.01), onHead(eye + 0.13, 0.25)], EYE_DARK, 2)
    elif pose == "hit":
        for eye in eyes:
            line([onHead(eye + 0.12, 0.22), onHead(eye - 0.04, 0.12), onHead(eye + 0.12, 0.02)], EYE_DARK, 2)
    elif face == "calm":
        for eye in eyes:
            line([onHead(eye - 0.1, 0.17), onHead(eye, 0.1), onHead(eye + 0.1, 0.17)], EYE_DARK, 1.5, smooth=True)
    else:
        eyeColor = paint("eyeColor")
        for eye in eyes:
            circle(onHead(eye, 0.12), r * 0.18, EYE_WHITE)
            circle(onHead(eye + 0.06, 0.12), r * 0.11, eyeColor)

    if not knockedOut:
        if face in ("angry", "fierce"):
            line([onHead(0.9, 0.45), onHead(0.48, 0.28)], EYE_DARK, 2)
            line([onHead(-0.04, 0.45), onHead(0.36, 0.28)], EYE_DARK, 2)
        elif face == "smirk":
            line([onHead(0.86, 0.36), onHead(0.62, 0.48), onHead(0.4, 0.4)], EYE_DARK, 2, smooth=True)

    if face == "fierce" and not knockedOut:
        # wide open, shouting
        polygon([onHead(0.86, -0.3), onHead(0.32, -0.34), onHead(0.4, -0.62), onHead(0.62, -0.74), onHead(0.82, -0.6)],
                mix(mouthColor, "#7a1f1f", 0.5), outline=mouthColor, smooth=True)
        line([onHead(0.42, -0.38), onHead(0.8, -0.35)], EYE_WHITE, 1.5)
    elif face == "angry" and not knockedOut:
        line([onHead(0.68, -0.52), onHead(0.5, -0.42), onHead(0.3, -0.52)], mouthColor, 1.5, smooth=True)
    elif face == "happy" or pose == "win":
        line([onHead(0.75, -0.3), onHead(0.55, -0.55), onHead(0.28, -0.42)], mouthColor, 1.5, smooth=True)
    elif face == "smirk":
        line([onHead(0.74, -0.32), onHead(0.55, -0.48), onHead(0.3, -0.48)], mouthColor, 1.5, smooth=True)
    elif face == "calm":
        line([onHead(0.68, -0.42), onHead(0.52, -0.5), onHead(0.36, -0.45)], mouthColor, 1.5, smooth=True)
    else:
        line([onHead(0.65, -0.45), onHead(0.35, -0.45)], mouthColor, 1.5)

    # mustaches go over the mouth
    if facialHair in ("mustache", "goatee", "beard"):
        line([onHead(0.88, -0.4), onHead(0.62, -0.27), onHead(0.32, -0.36)], hairColor, r * 0.16, smooth=True)
    if facialHair == "goatee":
        polygon([onHead(0.72, -0.62), onHead(0.4, -0.62), onHead(0.5, -1.2), onHead(0.66, -1.05)], hairColor, smooth=True)

    faceGear = look.get("faceGear", "none")
    gearColor = paint("faceGearColor")
    if faceGear == "mask":
        polygon(arc(1.04, -4, -128) + [onHead(-0.62, -0.08)], gearColor)
        line([onHead(0.92, -0.32), onHead(0.25, -0.36)], darker(gearColor, 0.35), 1)
    elif faceGear == "glasses":
        for eye in eyes:
            circle(onHead(eye + 0.03, 0.12), r * 0.24, "", outline=gearColor, width=1.5)
        line([onHead(0.36, 0.14), onHead(0.48, 0.14)], gearColor, 1.5)
        line([onHead(-0.02, 0.14), onHead(-0.7, 0.24)], gearColor, 1.5)
    elif faceGear == "eyepatch":
        line([onHead(0.95, 0.42), onHead(-0.9, 0.55)], darker(gearColor, 0.2), 1.5)
        circle(onHead(0.64, 0.12), r * 0.25, gearColor)
    elif faceGear == "shades" and not knockedOut:
        line([onHead(-0.45, 0.2), onHead(0.1, 0.14)], gearColor, 1.5)
        line([onHead(0.05, 0.14), onHead(0.85, 0.14)], gearColor, r * 0.36)
        line([onHead(0.55, 0.2), onHead(0.7, 0.2)], "#ffffff", 1.5)
    elif faceGear == "visor" and not knockedOut:
        line([onHead(-0.95, 0.24), onHead(-0.1, 0.16)], darker(gearColor, 0.4), 2)
        line([onHead(-0.15, 0.14), onHead(1.0, 0.14)], gearColor, r * 0.44)
        line([onHead(0.1, 0.24), onHead(0.85, 0.24)], lighter(gearColor, 0.5), 1.5)

    # ----- hair on top of the head -----

    hairline = [onHead(-0.35, 0.35), onHead(0.35, 0.5)]
    if hairStyle in ("short", "long", "ponytail", "bun", "swoop"):
        polygon(arc(1.12, 25, 215) + hairline, hairColor)
    if hairStyle == "buzz":
        polygon(arc(1.05, 35, 205) + [onHead(-0.4, 0.4), onHead(0.4, 0.62)], mix(hairColor, skinColor, 0.35))
    elif hairStyle == "bun":
        circle(onHead(-0.62, 0.95), r * 0.45, hairColor)
    elif hairStyle == "swoop":
        polygon([onHead(-0.8, 0.9), onHead(0.1, 1.35), onHead(0.95, 1.0), onHead(1.25, 0.35), onHead(0.85, 0.62),
                 onHead(0.2, 0.62)], hairColor, smooth=True)
    elif hairStyle == "spiky":
        spikes = []
        for k in range(13):
            angle = 25 + 190 * k / 12
            if k % 2 == 1:
                spikes.append(around(1.8, angle + 8))
            else:
                spikes.append(around(1.05, angle))
        polygon(spikes + hairline, hairColor)
    elif hairStyle == "mohawk":
        crest = []
        for k in range(9):
            angle = 50 + 120 * k / 8
            if k % 2 == 1:
                crest.append(around(1.95, angle + 6))
            else:
                crest.append(around(1.0, angle))
        polygon(crest + arc(0.9, 170, 50, steps=6), hairColor)

    # ----- headwear -----

    headwear = look.get("headwear", "none")
    hatColor = paint("headwearColor")
    if headwear == "headband":
        line([onHead(-0.92, 0.45), onHead(0.92, 0.45)], hatColor, r * 0.3)
        line([onHead(-0.95, 0.45), onHead(-1.7, 0.6), onHead(-2.3, 0.3)], hatColor, r * 0.2, smooth=True)
        line([onHead(-0.95, 0.45), onHead(-1.6, 0.2), onHead(-2.1, -0.25)], hatColor, r * 0.2, smooth=True)
    elif headwear == "cap":
        polygon(arc(1.1, 25, 190) + [onHead(-0.2, 0.42), onHead(0.6, 0.45)], hatColor)
        line([onHead(0.75, 0.42), onHead(1.7, 0.32)], hatColor, r * 0.28)
        circle(onHead(0, 1.08), r * 0.12, darker(hatColor))
    elif headwear == "tophat":
        polygon([onHead(-0.78, 0.7), onHead(-0.84, 2.1), onHead(0.84, 2.1), onHead(0.78, 0.7)], hatColor,
                outline=darker(hatColor, 0.3))
        line([onHead(-0.8, 0.95), onHead(0.8, 0.95)], contrast(hatColor), r * 0.22)
        line([onHead(-1.3, 0.72), onHead(1.3, 0.72)], hatColor, r * 0.2)
    elif headwear == "wizard":
        polygon([onHead(-0.95, 0.72), onHead(-0.35, 1.55), onHead(-0.85, 2.3), onHead(0.15, 1.75), onHead(0.95, 0.72)],
                hatColor, outline=darker(hatColor, 0.3), width=1.5)
        line([onHead(-1.55, 0.66), onHead(1.6, 0.66)], hatColor, r * 0.22)
        circle(onHead(0.15, 1.12), r * 0.15, tone(STAR_COLOR))
    elif headwear == "helmet":
        polygon([onHead(0.4, 1.1), onHead(0.15, 1.6), onHead(-0.6, 1.75), onHead(-1.35, 1.25), onHead(-0.9, 1.05),
                 onHead(-0.3, 1.2)], tone(PLUME_COLOR), smooth=True)
        polygon(arc(1.16, 12, 212, steps=14) + [onHead(-0.55, -0.4), onHead(-0.3, 0.36), onHead(1.0, 0.36)], hatColor,
                outline=darker(hatColor, 0.35), width=1.5)
        line([onHead(0.86, 0.38), onHead(0.9, -0.12)], hatColor, r * 0.14)
    elif headwear == "crown":
        polygon([onHead(-0.7, 0.65), onHead(-0.85, 1.65), onHead(-0.42, 1.12), onHead(0, 1.8), onHead(0.42, 1.12),
                 onHead(0.85, 1.65), onHead(0.7, 0.65)], hatColor, outline=darker(hatColor, 0.4), width=1.5)
        circle(onHead(0, 0.95), r * 0.14, tone("#ff3b30"))
    elif headwear == "horns":
        for side in (1, -1):
            polygon([onHead(side * 0.15, 0.97), onHead(side * 0.68, 0.74), onHead(side * 1.05, 1.3),
                     onHead(side * 1.1, 2.05), onHead(side * 0.62, 1.3)],
                    hatColor, outline=darker(hatColor, 0.4), smooth=True)
    elif headwear == "halo":
        ring = []
        for k in range(13):
            angle = math.radians(k * 30)
            ring.append(onHead(0.85 * math.cos(angle), 1.8 + 0.28 * math.sin(angle)))
        line(ring, hatColor, r * 0.16, smooth=True)
