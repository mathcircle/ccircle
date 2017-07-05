import ccircle
import time

North = 0
East = 1
South = 2
West = 3

CellEmpty = 0
CellWall = 1
CellGoal = 2

class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tx = x
        self.ty = y
        self.image = [
            ccircle.Image('cat_n.png'),
            ccircle.Image('cat_e.png'),
            ccircle.Image('cat_s.png'),
            ccircle.Image('cat_w.png'),
        ]
        self.facing = West

    def draw(self, x, y, s, window):
        self.image[self.facing].draw(x, y, s, s)

    def getName(self):
        return 'pusheen'

    def update(self, dt):
        pass


class Handler:
    def __init__(self, world, cb):
        self.world = world
        self.cat = world.find('pusheen')
        self._success = False
        self._failure = False
        self._moved = False
        self._lastMove = time.time()
        self._cb = cb

    def _draw(self, window):
        self.world.draw(window)
        wx, wy = window.getSize()
        if self._success:
            window.drawRect(0, 0, wx, wy, 0, 1, 0, 0.5)
        elif self._failure:
            window.drawRect(0, 0, wx, wy, 1, 0, 0, 0.5)

    def _getFacingCell(self):
        if self.cat.facing == North:
            return self.cat.tx, self.cat.ty - 1
        if self.cat.facing == East:
            return self.cat.tx + 1, self.cat.ty
        if self.cat.facing == South:
            return self.cat.tx, self.cat.ty + 1
        if self.cat.facing == West:
            return self.cat.tx - 1, self.cat.ty
        return self.cat.tx, self.cat.ty

    def _update(self):
        now = time.time()
        elapsed = now - self._lastMove
        if elapsed > self._cb.getPauseTime() and not self._failure and not self._success:
            self._lastMove = now
            self._moved = False
            self._cb.moveTowardPizza(self)
            cell = self.world.getCell(self.cat.tx, self.cat.ty)
            if cell == None or cell == CellWall:
                self._failure = True
            if cell == CellGoal:
                self._success = True

    def hasPizza(self):
        return self.world.cells[self.cat.tx][self.cat.ty] == '!'

    def isBlocked(self):
        fx, fy = self._getFacingCell()
        result = self.world.getCell(fx, fy)
        return result == None or result == CellWall

    def isFacingN(self):
        return self.cat.facing == North

    def isFacingE(self):
        return self.cat.facing == East

    def isFacingS(self):
        return self.cat.facing == South

    def isFacingW(self):
        return self.cat.facing == West

    def smellsPizza(self):
        fx, fy = self._getFacingCell()
        result = self.world.getCell(fx, fy)
        return result == CellGoal

    def turnLeft(self):
        self.cat.facing = (self.cat.facing + 3) % 4

    def turnRight(self):
        self.cat.facing = (self.cat.facing + 1) % 4

    def walk(self):
        if not self._moved:
            self.cat.tx, self.cat.ty = self._getFacingCell()
            self.cat.x, self.cat.y = self.cat.tx, self.cat.ty
            self._moved = True

class World:
    def __init__(self, **kwargs):
        self.imageBG = ccircle.Image('space.png')
        self.imageGoal = ccircle.Image('pizza.png')

        if 'size' in kwargs:
            self.clear(kwargs['size'])
        elif 'layout' in kwargs:
            self.load(kwargs['layout'])
        else:
            raise Exception('Failed to create cat.World: keyword argument must be either size or layout')

    ''' Add a new free-standing object to the world '''
    def addObject(self, obj):
        self.objects.append(obj)

    ''' Clear the world to be size x size empty cells '''
    def clear(self, size):
        self.size = size
        self.cells = [[CellEmpty] * size for x in range(size)]
        self.objects = []

    ''' Draw the world to a window '''
    def draw(self, window):
        size = window.getSize()
        ms = min(size) - 64
        ox = (size[0] - ms) / 2
        oy = (size[1] - ms) / 2
        b = 4

        # Background
        self.imageBG.draw(0, 0, size[0], size[1])

        # Floor
        window.drawRect(ox, oy, ms, ms, 0.2, 0.2, 0.2)
        cs = (ms - 2*b) / self.size

        # Floor grid
        for i in range(1, self.size):
            px = ox + b + cs * i
            py = oy + b + cs * i
            window.drawLine(px, oy, px, oy + ms, 1, 0.3, 0.3, 0.3)
            window.drawLine(ox, py, ox + ms, py, 1, 0.3, 0.3, 0.3)

        # Border
        window.drawRect(ox, oy, ms, b)
        window.drawRect(ox, oy, b, ms)
        window.drawRect(size[0] - ox - b, oy, b, ms)
        window.drawRect(ox, size[1] - oy - b, ms, b)

        # Grid Objects
        for y in range(self.size):
            py = oy + b + y * cs
            for x in range(self.size):
                px = ox + b + x * cs
                cell = self.cells[x][y]
                if cell == CellWall:
                    window.drawRect(px, py, cs, cs, 1.0, 0.0, 0.3)
                elif cell == CellGoal:
                    self.imageGoal.draw(px, py, cs, cs)

        # Free-Standing Objects
        for obj in self.objects:
            px = ox + b + cs * obj.x
            py = oy + b + cs * obj.y
            obj.draw(px, py, cs, window)

    ''' Return the object in the world with the given name '''
    def find(self, name):
        for obj in self.objects:
            if hasattr(obj, 'getName') and obj.getName() == name:
                return obj
        return None

    def getCell(self, x, y):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return None
        return self.cells[x][y]

    ''' Load a world from a layout string
           X -> Main Character (a cat!)
           W -> Wall
           ! -> Goal (a pizza!) '''
    def load(self, layout):
        data = [x.strip() for x in layout.strip().split('\n')]
        self.clear(len(data[0]))
        for y, row in enumerate(data):
            for x, cell in enumerate(row):
                if cell == 'W' or cell == '|' or cell == '+':
                    self.cells[x][y] = CellWall
                elif cell == 'X' or cell == 'C':
                    self.addObject(Cat(x, y))
                elif cell == '!' or cell == 'P':
                    self.cells[x][y] = CellGoal
                else:
                    self.cells[x][y] = CellEmpty

    ''' Update the state of the world and the objects therein '''
    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)