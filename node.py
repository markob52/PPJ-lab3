import identifikacija

class Node:
    def __init__(self, vrijednost:str, jeNezavrsni:bool = True, linija:str=None, kod:str=None ):
        self.identifikator = None
        self.vrijednost = vrijednost
        if not jeNezavrsni:
            self.linija = linija
            self.kod = kod
        self.dijeca = []
        self.svojstva = {}

    def identificiraj(self):
        for i in range(len(self.dijeca)):
            self.dijeca[i].identificraj()
        for identifikator in identifikacija.identifikatori:
            if identifikator.uvijet_identifikacije(self):
                self.identifikator = identifikator
                break

    def dodaj_dijete(self,dijete:object):
        self.dijeca.append(dijete)
        dijete.roditelj = self


def parse_tree(linije: list[str]) -> Node:
    root = Node("<BEGIN>")
    tren = root
    indent = 0
    for linija in linije:
        tren_indent = len(linija)-len(linija.lstrip(' '))
        while tren_indent < indent:
            tren = tren.roditelj
            indent -=1
        while tren_indent > indent:
            tren = tren.dijeca[len(tren.dijeca)-1]
            indent +=1
        tren_izraz = linija.lstrip(' ').split(' ')
        if len(tren_izraz)==1:
            tren.dodaj_dijete(Node(tren_izraz[0]))
        else:
            tren.dodaj_dijete(Node(tren_izraz[0],False,tren_izraz[1],tren_izraz[2]))
    root.dijeca[0].identificraj()
    return root.dijeca[0]


'''


'''