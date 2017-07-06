import random
import symbol

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def genSymbol():
  return (random.choice(letters)
        + random.choice(letters)
        + random.choice(letters))

def sign(x):
  if x < 0.0:
    return -1.0
  return 1.0

class Account:
    def __init__(self):
        self._balance = 0
        self._log = []
        self._shares = {}

    # --- Private --------------------------------------------------------------

    def _addShares(self, sym, quantity):
        self._shares[sym] = self.getShares(sym) + quantity

    def _logAction(self, action):
        self._log.append(action)
        print(action)

    def _removeShares(self, sym, quantity):
        self._shares[sym] -= quantity
        if self._shares[sym] <= 0:
            del self._shares[sym]

    # --- Public ---------------------------------------------------------------

    def getBalance(self):
      return self._balance

    def getShares(self, sym):
      return self._shares.get(sym, 0)


class Stock:
    def __init__(self, sym, chaos):
        self.sym, self.chaos = sym, chaos
        self.price = 100.0 * random.uniform(0, 1)
        self.history = [self.price]

    def _update(self):
        self.history.append(self.price)
        t = max(0.01, min(0.9, self.chaos))
        price = 100.0 * random.uniform(0, 1)
        self.price = (1.0 - t) * self.price + t * price


class StockMarket:
    def __init__(self):
        self._stocks = {}

    # --- Private --------------------------------------------------------------

    def _checkQuantity(self, quantity):
        if quantity < 0 or type(quantity) != int:
            raise Exception('Quantity must be a positive integer!')

    def _checkSym(self, sym):
        if not sym in self._stocks:
            raise Exception('There are no stocks with symbol %s!' % sym)

    def _update(self):
        for sym, stock in self._stocks.items():
            stock._update()

    # --- Public ---------------------------------------------------------------

    def buy(self, account, sym, quantity):
        self._checkSym(sym)
        self._checkQuantity(quantity)
        if quantity == 0:
            return
        stock = self._stocks[sym]
        total = stock.price * quantity
        if total > account.getBalance():
          raise Exception('Buying %d x %s costs $%.2f, but your account only has $%.2f') % (
            quantity, sym, total, account.getBalance())
        account._balance -= total
        account._addShares(sym, quantity)
        account._logAction('BUY  %d x %s @ $%.2f; total = $%.2f' % (quantity, sym, stock.price, total))

    def getPrice(self, sym):
        self._checkSym(sym)
        return self._stocks[sym].price

    def getHistory(self, sym):
        self._checkSym(sym)
        return self._stocks[sym].history

    def getStockSymbols(self):
        return list(self._stocks.keys())

    def sell(self, account, sym, quantity):
        self._checkSym(sym)
        self._checkQuantity(quantity)
        if quantity == 0:
            return 0
        stock = self._stocks[sym]
        total = stock.price * quantity
        if account.getShares(sym) < quantity:
          raise Exception('Selling %d x %s requires %d shares of %s, but your account only has %d') % (
            quantity, sym, quantity, sym, account.getShares(sym))
        account._balance += total
        account._removeShares(sym, quantity)
        account._logAction('SELL %d x %s @ $%.2f; total = $%.2f' % (quantity, sym, stock.price, total))


def create(solution):
    diff = solution.getDifficulty()
    # random.seed(solution.getSeed())

    account = Account()
    account._balance = 1000

    market = StockMarket()
    stockCount = 8
    for i in range(stockCount):
      stock = Stock(genSymbol(), diff)
      market._stocks[stock.sym] = stock

    return account, market
