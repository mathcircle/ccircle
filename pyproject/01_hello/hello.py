import random

hello_world = [
    'hello|world',
    'bonjour|monde',
    'hallo|welt',
    'halló|heimur',
    'ciao|mondo',
    'ahoj|světe',
    '你好|世界',
    'こんにちは|世界',
    '안녕|세상',
    'salve|mundi',
    'hei|verden',
    'witaj|świecie',
    'olá|mundo',
    'привет|мир',
    'hola|mundo',
]

hello = []
world = []

for greeting in hello_world:
    pieces = greeting.split('|')
    hello.append(pieces[0])
    world.append(pieces[1])


def make_greeting():
    return random.choice(hello).capitalize() + ' ' + random.choice(world) + '!'

for i in range(10):
    print(make_greeting())
