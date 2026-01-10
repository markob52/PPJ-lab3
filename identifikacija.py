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
ASCII = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789,./!?@#$%^&*()[]{}_+-?>=<:;`~| "
IDE_IZA_BACKSLASH = "tn0\'\"\\"
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

identifikatori.append(Identifikator(
    uvj_2,
    ["tip","l-izraz"],
    prov_2
))

'''
<primarni_izraz> ::= ZNAK
tip ← char
l-izraz ← 0
1. znak je ispravan po 4.3.2
'''
def uvj_3(n:node.Node) -> bool:
    if n.vrijednost != '<primarni_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost =="ZNAK"
    return False
def prov_3(n:node.Node) -> bool:
    znak = n.djeca[0].kod
    if (znak[1] not in ASCII) and (not (znak[1] == "\\" and (znak[2] in IDE_IZA_BACKSLASH) and len(znak)==4)):
                return False
    n.svojstva["tip"] = "char"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_3,
    ["tip","l-izraz"],
    prov_3
))

'''
<primarni_izraz> ::= NIZ_ZNAKOVA
tip ← niz (const(char))
l-izraz ← 0
1. konstantni niz znakova je ispravan po 4.3.2
'''

def uvj_4(n:node.Node) -> bool:
    if n.vrijednost != '<primarni_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost =="NIZ_ZNAKOVA"
    return False
def prov_4(n:node.Node) -> bool:
    string = n.dijeca[0].kod
    if not (string[0] == "\"" and string[-1] == "\""):
        return False
    i = 1
    while i < len(string) - 1:
        if string[i] in ASCII:
            #print(string[i], "je u ASCII")
            i += 1
        else:
            #print(string[i], "nije u ASCII")
            if string[i] == "\\" and string[i + 1] in IDE_IZA_BACKSLASH:
                #print(string[i:i + 2], "je u IDE_IZA_BACKSLASH")
                i += 2
            elif string[i] == "\'":
               #print(string[i], "je \'")
                i += 1
            else:
                #print(string[i], "je nevazeci znak")
                return False

    n.svojstva["tip"] = "niz_const_char"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_4,
    ["tip","l-izraz"],
    prov_4
))

'''
<primarni_izraz> ::= L_ZAGRADA <izraz> D_ZAGRADA
tip ← <izraz>.tip
l-izraz ← <izraz>.l-izraz
1. provjeri(<izraz>)
'''

def uvj_5(n:node.Node) -> bool:
    if n.vrijednost != '<primarni_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost =="L_ZAGRADA <izraz> D_ZAGRADA"
    return False
def prov_5(n:node.Node) -> bool:
    provjera = n.dijeca[1].identifikator.provjeri(n.dijeca[1])
    if not provjera:
        return False
    n.svojstva["tip"] = n.dijeca[1].svojstva["tip"]
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_5,
    ["tip","l-izraz"],
    prov_5
))

'''postfix izraz'''

'''
<postfiks_izraz> ::= <primarni_izraz>
tip ← <primarni_izraz>.tip
l-izraz ← <primarni_izraz>.l-izraz
1. provjeri(<primarni_izraz>)
'''

def uvj_6(n:node.Node) -> bool:
    if n.vrijednost != '<postfix_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost == "<primarni_izraz>"
    return False
def prov_6(n:node.Node) -> bool:
    provjera = n.dijeca[0].identifikator.provjeri(n.dijeca[0])
    if not provjera:
        return False
    n.svojstva["tip"] = n.dijeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.dijeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_6,
    ["tip"],
    prov_6
))

'''
<postfiks_izraz> ::= <postfiks_izraz> L_UGL_ZAGRADA <izraz> D_UGL_ZAGRADA
tip ← X
l-izraz ← X 6= const(T)
1. provjeri(<postfiks_izraz>)
2. <postfiks_izraz>.tip = niz (X )
3. provjeri(<izraz>)
4. <izraz>.tip ∼ int
'''
def uvj_7(n:node.Node) -> bool:
    if n.vrijednost != "<postfiks_izraz>":
        return False
    elif len(n.dijeca) != 4:
        return False
    elif n.dijeca[0].vrijednost != "<postfiks_izraz>":
        return False
    elif n.dijeca[1].vrijednost != "L_UGL_ZAGRADA":
        return False
    elif n.dijeca[2].vrijednost != "<izraz>":
        return False
    elif n.dijeca[3].vrijednost != "D_UGL_ZAGRADA":
        return False
    return True
def prov_7(n:node.Node) -> bool:
    if not n.dijeca[0].identifikator.provjeri(n.dijeca[0]):
        return False
    n.dijeca[0].identifikator[]
    return True




'''
<postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA D_ZAGRADA
tip ← pov
l-izraz ← 0
1. provjeri(<postfiks_izraz>)
2. <postfiks_izraz>.tip = funkcija(void → pov)
'''

def uvj_8(n:node.Node) -> bool:
    if n.vrijednost != '<postfiks_izraz>':
        return False
    if len(n.dijeca) == 1:
        return n.dijeca[0].vrijednost == "<postfiks_izraz> L_ZAGRADA D_ZAGRADA"
    return False # 'asd' ()
def prov_8(n:node.Node) -> bool:
    provjera = n.dijeca[0].identifikator.provjeri(n.dijeca[0])
    if not provjera:
        return False
    '''
    funkcija_void__int
    '''
    if not n.dijeca[0].svojstva["tip"].startswith("funkcija_void__"):
        return False

