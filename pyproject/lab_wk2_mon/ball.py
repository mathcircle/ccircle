from math import *

class Ball:
    def __init__(self, x, y, size):
        self.x, self.y, self.size = x, y, size
        self.mass = 1
        self.vx, self.vy, self.fx, self.fy = 0, 0, 0, 0

    def apply_force(self, fx, fy):
        self.fx += fx
        self.fy += fy

    def draw(self, window):
        window.drawCircle(self.x, self.y, self.size, 0, 0, 0, 0.25)
        window.drawCircle(self.x, self.y, self.size - 2, 1.0, 0, 0, 0.75)

    def update(self, dt):
        # Compute acceleration using a = F / m (Newton's second law)
        accel_x = self.fx / self.mass
        accel_y = self.fy / self.mass

        # Update velocity with acceleration
        # NOTE : It is important that we do this *before* we updating position!
        #        Updating velocity *first* gives us significantly more accurate
        #        results!
        self.vx += dt * accel_x
        self.vy += dt * accel_y

        # Update position with velocity
        self.x += dt * self.vx
        self.y += dt * self.vy

        # Reset force accumulators
        self.fx = 0
        self.fy = 0

        # Check for collision with ground
        if self.y + self.size > 700:
            self.y = 700 - self.size
            self.vy *= -0.9

        # Check for collision with right side
        if self.x + self.size > 800:
            self.x = 800 - self.size
            self.vx *= -0.9

        # Check for collision with left side
        if self.x - self.size < 0:
            self.x = self.size
            self.vx *= -0.9
