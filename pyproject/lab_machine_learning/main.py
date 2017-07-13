import markov
import util

elems = util.readWords('text/spongebob_texas.txt')
chain = markov.Chain(2)
for x in elems:
    chain.observe(x)

content = chain.chooseFirst()
for i in range(100):
    next = chain.chooseNext()
    if not next: break
    content.append(next)

content = ' '.join(content)
print(content)
input()