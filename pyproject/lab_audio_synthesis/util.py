import ccircle

def generateSound(fn, duration):
    sound = ccircle.Sound()
    duration = int(duration * 44100)
    for i in range(duration):
        sound.addSample(fn(i / 44100))
    return sound

# 0 is actualy 60 (Middle C)
frequencyMap = {
    0:  261.6255653006,
    1:  277.1826309769,
    2:  293.6647679174,
    3:  311.1269837221,
    4:  329.6275569129,
    5:  349.2282314330,
    6:  369.9944227116,
    7:  391.9954359817,
    8:  415.3046975799,
    9:  440.0000000000,
   10:  466.1637615181,
   11:  493.8833012561,
}

def getNoteFrequency(midiNote):
    mult = 1
    while midiNote < 60:
        midiNote += 12
        mult /= 2
    while midiNote > 71:
        midiNote -= 12
        mult *= 2
    return frequencyMap[midiNote - 60] * mult