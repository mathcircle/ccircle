import ccircle
import problem
import solution
import time

trader = solution.StockTrader()
account, market = problem.create(trader)

window = ccircle.Window('Scenario 2: Beating the Stock Market', 1600, 900, 32, 32)
window.toggleMaximized()
wx, wy = window.getSize()

fMenu = ccircle.Font('../res/NovaFlat.ttf')
fMono = ccircle.Font('../res/FiraMono.ttf')
day = 1

def lerp(x, y, t):
  return x + t * (y - x)

def panel(x, y, sx, sy, b, cInner, cOuter):
    global window
    window.drawRect(x, y, sx, sy, *cOuter)
    window.drawRect(x + b, y + b, sx - 2 * b, sy - 2 * b, *cInner)

def rect(x, y, sx, sy, r, g, b):
    global window
    window.drawRect(x, y, sx, sy, r, g, b)

def text(font, s, x, y, size = 16, color = (1, 1, 1)):
    global resX, resY
    font.draw(s, x, y + size, size, *color)

def accountPanel():
    global fMenu, fMono, account
    global wx, wy
    panel(0, 0, 400, wy, 8, (0.15, 0.15, 0.15), (0.2, 0.2, 0.2))
    text(fMenu, '- Account Info -', 64, 20, 30, (1, 1, 1))
    y = 80
    text(fMenu, 'BALANCE', 32, y, 20); y += 25
    text(fMono, '>', 64, y, 20);
    text(fMono, '$%.2f' % account.getBalance(), 90, y, 20, (0.5, 1.0, 0.5)); y += 25
    text(fMono, '>', 64, y, 20);
    text(fMono, '$%.2f PPD' % ((account.getBalance() - 1000) / day), 90, y, 20, (0.5, 1.0, 0.5)); y += 25

    y += 15
    text(fMenu, 'STOCKS', 32, y, 20); y += 25
    for sym, value in account._shares.items():
        text(fMono, '>', 64, y, 20)
        text(fMono, '%s : %d shares' % (sym, value), 90, y, 20, (0.5, 1.0, 0.5))
        y += 25
    y += 15

    text(fMenu, 'LOG', 32, y, 20); y += 30

    for line in reversed(account._log):
        c = (0.9, 0.9, 0.9)
        if 'BUY' in line:
          c = (0.9, 0.5, 0.5)
        elif 'SELL' in line:
          c = (0.5, 0.9, 0.5)
        text(fMono, line, 64, y, 12, c)
        y += 16
        if y > (wy - 16):
          break

def marketPanel():
    global fMenu, fMono, market
    global wx, wy, day
    panel(416, 0, wx - 416, wy, 8, (0.15, 0.15, 0.15), (0.2, 0.2, 0.2))
    text(fMono, 'Market (Day: %d)' % day, 870, 20, 30, (1, 1, 1))

    spacing = 8
    h = (wy - 64 - (16 - spacing)) / len(market._stocks)
    h -= spacing
    y = 64
    for sym, stock in market._stocks.items():
      panel(432, y, 96, h, 2, (0.2, 0.2, 0.2), (0.10, 0.10, 0.10))
      panel(540, y, wx - 540 - 16, h, 2, (0.2, 0.2, 0.2), (0.1, 0.1, 0.1))
      text(fMono, sym, 450, int(y) + 8, 32)
      text(fMono, '$%.2f' % stock.price, 442, int(y) + 54, 20)

      if len(stock.history) > 1:
        wsz = 128
        history = stock.history
        if len(history) > wsz:
          history = history[-wsz:]
        x = 548
        w = (wx - 548 - 16) / wsz
        vMin = min(history)
        vMax = max(history)
        for val in history:
          if vMin == vMax: vn = 0.5
          else: vn = (val - vMin) / (vMax - vMin)
          r = lerp(1.0, 0.1, vn)
          g = lerp(0.0, 0.4, vn)
          b = lerp(0.4, 1.0, vn)
          rect(x, y + 4 + (h - 8) * (1.0 - vn), 8, (h - 8) * vn, r, g, b)
          x += w

      y += h + spacing


last = time.time() - trader.getPauseTime()
while window.isOpen():
    resX, resY = window.getSize()
    window.clear(0.1, 0.1, 0.1)
    accountPanel()
    marketPanel()

    now = time.time()
    if (now - last) >= trader.getPauseTime():
      last = now
      trader.trade(account, market)
      market._update()
      day += 1
    window.update()
