import node
from tabzn import TablicaZnakova
class Identifikator:
    def __init__(self, uvijet_identifikacije, svojstva:list, provjeri):
        self.uvijet_identifikacije = uvijet_identifikacije
        self.svojstva = svojstva
        self.provjeri = provjeri


tablica_znakova = TablicaZnakova()
main_postoji = False
identifikatori = []

'''
<primarni_izraz> ::= IDN
tip ← IDN.tip
l-izraz ← IDN.l-izraz

1. IDN.ime je deklarirano
'''
def uvj_1(n:node.Node) -> bool:
    if n.vrijednost != '<primarni_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost =="IDN"
    return False
def prov_1(n:node.Node) -> bool:
    if not tablica_znakova.testiraj(n.dijeca[0].svojstva["ime"]):
        return False
    n.svojstva["tip"]=n.dijeca[0].svojstva["tip"]
    n.svojstva["l-izraz"]=n.dijeca[0].svojstva["l-izraz"]
    return True
identifikatori.append(Identifikator(
    uvj_1,
    ["tip","l-izraz"],
    prov_1
))

'''
<primarni_izraz> ::= BROJ
tip ← int
l-izraz ← 0

1. vrijednost je u rasponu tipa int
'''
def uvj_2(n:node.Node) -> bool:
    if n.vrijednost != '<primarni_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost =="BROJ"
    return False
def prov_2(n:node.Node) -> bool:
    try:
        if not (2147483648 > int(n.dijeca[0].kod) >= -2147483648):
            return False
    except:
        return False
    if n.svojstva["vrijednost"] :
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

'''
IDN
tip
'''


identifikatori.append(Identifikator(
    uvj_2,
    ["tip","l-izraz"],
    prov_2
))