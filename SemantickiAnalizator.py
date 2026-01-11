import fileinput
import node
import identifikacija
linije = []
for line in fileinput.input():
    linije.append(line.rstrip('\n'))

stablo = node.parse_tree(linije,identifikacija.identifikatori)
stablo.identifikator.provjera(stablo)
print()