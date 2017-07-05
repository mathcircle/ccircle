import ccircle
import cat
import worlds
import solution

solver = solution.Solution()

window = ccircle.Window("Scenario 1: Space Cat Pizza Party!")
window.toggleMaximized()
world = cat.World(layout=solver.getLevel())
handler = cat.Handler(world, solver)

while window.isOpen():
    handler._update()
    handler._draw(window)
    window.update()
