import random
import util

class Chain:
    def __init__(self, degree=1):
        self.transitions = {}
        self.totals = {}
        self.history = []
        self.degree = degree

    def chooseFirst(self):
        state = util.samplePDF(self.totals)
        self.history = list(state)
        return self.history[:]

    def chooseNext(self):
        state = util.samplePDF(self.transitions.get(tuple(self.history), None))
        self.history.pop(0)
        self.history.append(state)
        return state

    def observe(self, state):
        if len(self.history) < self.degree:
            self.history.insert(0, state)
            return
        prev = tuple(self.history)
        if prev not in self.transitions:
            self.transitions[prev] = {}
        table = self.transitions[prev]
        table[state] = table.get(state, 0) + 1
        self.totals[prev] = self.totals.get(prev, 0) + 1
        self.history.pop(0)
        self.history.append(state)
