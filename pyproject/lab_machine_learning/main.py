import markov
import util

words = util.readWords('text/spongebob_texas.txt')

chain = markov.Chain(1)
for word in words:
    chain.observe(word)

content = chain.chooseFirst()
for i in range(1000):
    next = chain.chooseNext()
    if not next: break
    content.append(next)

content = ' '.join(content)
util.writeFile('gen.txt', content)