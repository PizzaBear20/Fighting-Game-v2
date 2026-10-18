import math

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


# Draws a fighter using their look (colors, hair, hat, outfit...).
# x, ground = where their feet are. facing: 1 = right, -1 = left.
# pose: stand, punch, hit, win, down. scale makes them bigger or smaller
def drawFighter(canvas, x, ground, look, facing=1, pose="stand", scale=1.0, tag="fighter", flash=False, shadow=SHADOW):
    f = facing
    limbWidth, headRadius, outfitWidth, fistRadius = BUILD_SIZES.get(look.get("build"), BUILD_SIZES["normal"])
    joints = fighterJoints(pose, f, headRadius)
    knockedOut = pose == "down"

    def paint(key):
        color = look[key]
        if flash:
            return "#ffffff"
        if knockedOut:
            return mix(color, "#6b6b7b", 0.55)
        return color

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
        centerX, centerY = point(center)
        r = radius * scale
        canvas.create_oval(centerX - r, centerY - r, centerX + r, centerY + r, fill=color, outline=outline,
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

    # shadow on the floor
    if shadow:
        canvas.create_oval(x - 38 * scale, ground - 6 * scale, x + 38 * scale, ground + 6 * scale,
                           fill=shadow, outline="", tags=tag)

    # cape goes behind everything
    if cape == "cape":
        spread = 0.3 if knockedOut else 1
        capeColor = paint("capeColor")
        polygon([offset(shoulder, 0, 3 * spread), offset(shoulder, bodyLength * 0.8, 18 * spread),
                 offset(shoulder, bodyLength * 1.8, 30 * spread), offset(shoulder, bodyLength * 1.9, 6 * spread),
                 offset(shoulder, bodyLength * 0.9, 0)],
                capeColor, outline=darker(capeColor), smooth=True, width=2)

    # hair that hangs behind the head
    if hairStyle == "afro":
        circle(onHead(-0.15, 0.3), r * 1.55, hairColor)
    elif hairStyle == "long":
        polygon([onHead(0.5, 1.0), onHead(-0.3, 1.2), onHead(-1.1, 0.75), onHead(-1.3, -0.4), onHead(-1.25, -1.7),
                 onHead(-0.7, -1.9), onHead(-0.45, -0.6)], hairColor, smooth=True)
    elif hairStyle == "ponytail":
        polygon([onHead(-0.8, 0.6), onHead(-1.5, 0.8), onHead(-2.2, 0.1), onHead(-2.1, -1.0), onHead(-1.7, -0.3),
                 onHead(-1.0, 0.1)], hairColor, smooth=True)

    def drawArm(arm, fistSize):
        elbow, fist = arm
        line([offset(shoulder, 4, 0), elbow, fist], bodyColor, limbWidth)
        circle(fist, fistSize, gloveColor, outline=darker(gloveColor), width=1.5)

    # back arm, legs, body
    drawArm(joints["arms"][1], fistRadius - 1)
    for knee, foot in joints["legs"]:
        line([hip, knee, foot], bodyColor, limbWidth)
    line([hip, shoulder], bodyColor, limbWidth)

    # outfit
    outfit = look.get("outfit", "none")
    if outfit != "none":
        outfitColor = paint("outfitColor")
        line([offset(hip, -4, 0), offset(shoulder, 4, 0)], outfitColor, outfitWidth)
        if outfit in ("gi", "armor"):
            if outfit == "gi":
                beltColor = "#20202a"
            else:
                beltColor = darker(outfitColor, 0.4)
            beltCenter = offset(hip, -8, 0)
            half = outfitWidth * 0.55
            line([offset(beltCenter, 0, -half), offset(beltCenter, 0, half)], beltColor, 4)
        if outfit == "armor":
            circle(offset(shoulder, 6, 0), outfitWidth * 0.5, lighter(outfitColor, 0.2), outline=darker(outfitColor, 0.4), width=2)

    # neck and scarf
    line([shoulder, onHead(0, -0.9)], skinColor, limbWidth * 0.8)
    if cape == "scarf":
        scarfColor = paint("capeColor")
        neck = offset(shoulder, -3, 0)
        line([offset(neck, 0, -6), offset(neck, 0, 6)], scarfColor, 8)
        line([offset(neck, 0, 4), offset(neck, 4, 18), offset(neck, 12, 32)], scarfColor, 6, smooth=True)

    # front arm
    drawArm(joints["arms"][0], fistRadius)

    # head and face
    circle(joints["head"], r, skinColor, outline=darker(skinColor, 0.35), width=1.5)
    face = look.get("face", "normal")
    mouthColor = darker(skinColor, 0.6)
    eyes = [0.62, 0.22]
    if knockedOut:
        for eye in eyes:
            line([onHead(eye - 0.13, 0.25), onHead(eye + 0.13, -0.01)], EYE_DARK, 2)
            line([onHead(eye - 0.13, -0.01), onHead(eye + 0.13, 0.25)], EYE_DARK, 2)
    elif face == "shades":
        line([onHead(-0.45, 0.2), onHead(0.1, 0.14)], "#111111", 1.5)
        line([onHead(0.05, 0.14), onHead(0.85, 0.14)], "#111111", r * 0.36)
        line([onHead(0.55, 0.2), onHead(0.7, 0.2)], "#ffffff", 1.5)
    elif pose == "hit":
        for eye in eyes:
            line([onHead(eye + 0.12, 0.22), onHead(eye - 0.04, 0.12), onHead(eye + 0.12, 0.02)], EYE_DARK, 2)
    else:
        for eye in eyes:
            circle(onHead(eye, 0.12), r * 0.18, EYE_WHITE)
            circle(onHead(eye + 0.06, 0.12), r * 0.1, EYE_DARK)

    if face == "angry" and not knockedOut:
        line([onHead(0.9, 0.45), onHead(0.48, 0.28)], EYE_DARK, 2)
        line([onHead(-0.04, 0.45), onHead(0.36, 0.28)], EYE_DARK, 2)
        line([onHead(0.68, -0.52), onHead(0.5, -0.42), onHead(0.3, -0.52)], mouthColor, 1.5, smooth=True)
    elif face == "happy" or pose == "win":
        line([onHead(0.75, -0.3), onHead(0.55, -0.55), onHead(0.28, -0.42)], mouthColor, 1.5, smooth=True)
    else:
        line([onHead(0.65, -0.45), onHead(0.35, -0.45)], mouthColor, 1.5)

    # hair on top of the head
    hairline = [onHead(-0.35, 0.35), onHead(0.35, 0.5)]
    if hairStyle in ("short", "long", "ponytail"):
        polygon(arc(1.12, 25, 215) + hairline, hairColor)
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

    # headwear
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
    elif headwear == "crown":
        polygon([onHead(-0.7, 0.65), onHead(-0.85, 1.65), onHead(-0.42, 1.12), onHead(0, 1.8), onHead(0.42, 1.12),
                 onHead(0.85, 1.65), onHead(0.7, 0.65)], hatColor, outline=darker(hatColor, 0.4), width=1.5)
        circle(onHead(0, 0.95), r * 0.14, "#ff3b30")
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
