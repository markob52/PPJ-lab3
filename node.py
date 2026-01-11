import sys

class Node:
    def __init__(self, vrijednost:str, jeNezavrsni:bool = True, linija:str=None, kod:str=None ):
        self.identifikator = None
        self.vrijednost = vrijednost
        if not jeNezavrsni:
            self.linija = linija
            self.kod = kod
        self.djeca = []
        self.svojstva = {}

    def identificiraj(self,identifikatori):
        for i in range(len(self.djeca)):
            if not self.djeca[i].vrijednost.startswith("<"):
                continue
            self.djeca[i].identificiraj(identifikatori)
        for i in range(len(identifikatori)):
            if identifikatori[i].uvijet_identifikacije(self):
                self.identifikator = identifikatori[i].copy()
                sys.stderr.write(f"identificiran: {i+1}\n")
                self.identifikator.id = i
                return
        sys.stderr.write(f"greska tijekom identifikacije\n")
        print(f"{self.vrijednost} ::=", end="")
        for dijete in self.djeca:
            if dijete.vrijednost.startswith("<"):
                print(f" {dijete.vrijednost}",end='')
            else:
                print(f" {dijete.vrijednost}({dijete.linija},{dijete.kod})",end='')
        print("")
        sys.exit(0)

    def dodaj_djete(self,dijete:object):
        self.djeca.append(dijete)
        dijete.roditelj = self


def parse_tree(linije: list[str],identifikatori) -> Node:
    root = Node("<BEGIN>")
    tren = root
    indent = 0
    for linija in linije:
        tren_indent = len(linija)-len(linija.lstrip(' '))
        while tren_indent < indent:
            tren = tren.roditelj
            indent -=1
        while tren_indent > indent:
            tren = tren.djeca[len(tren.djeca)-1]
            indent +=1
        tren_izraz = linija.lstrip(' ').split(' ')
        if len(tren_izraz)==1:
            tren.dodaj_dijete(Node(tren_izraz[0]))
        else:
            tren.dodaj_djete(Node(tren_izraz[0],False,tren_izraz[1],tren_izraz[2]))
    root.djeca[0].roditelj = None
    root.djeca[0].identificiraj(identifikatori)
    return root.djeca[0]


'''


'''