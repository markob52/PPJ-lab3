import fileinput
import node

linije = []
for line in fileinput.input():
    linije.append(line.rstrip('\n'))

stablo = node.parseTree(linije)
print()