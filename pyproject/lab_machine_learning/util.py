import os.path
import random

def readLetters(filename):
    if not os.path.isfile(filename):
        raise Exception('Could not find file <%s>' % filename)
    data = open(filename, 'r').read().strip().replace('\n', ' ').replace('\r', '')
    while '  ' in data: data = data.replace('  ', ' ')
    return list(data)

def readWords(filename):
    if not os.path.isfile(filename):
        raise Exception('Could not find file <%s>' % filename)
    data = open(filename, 'r').read().strip().replace('\n', ' ').replace('\r', '')
    while '  ' in data: data = data.replace('  ', ' ')
    return data.split(' ')

def samplePDF(self):
    if not self or len(self) == 0:
        return None
    total = sum(self.values())
    if total == 0:
        return None
    choice = random.randint(0, total - 1)
    partial = 0
    for key, value in self.items():
        partial += value
        if choice < partial:
            return key
    return self.keys()[0]

def writeFile(name, content):
    open(name, 'w').write(content)