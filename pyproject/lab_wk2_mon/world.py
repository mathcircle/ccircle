class World:
    def __init__(self, name):
        self.name = name
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def draw(self, window):
        window.drawRect(0, 0, 800, 600, 0.3, 0.5, 1.0)
        window.drawRect(0, 600, 800, 200, 0.25, 0.5, 0.25)
        for i in range(100):
            window.drawCircle(0, 0, 50 + i, 1.0, 1.0, 0.25, 0.05)
        for obj in self.objects:
            obj.draw(window)

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)
