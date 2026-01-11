import sys

import node
from tabzn import TablicaZnakova
class Identifikator:
    def __init__(self, uvijet_identifikacije, svojstva:list, provjeri):
        self.uvijet_identifikacije_ = uvijet_identifikacije
        self.svojstva_ = svojstva.copy()
        self.provjeri_ = provjeri
    def provjera(self, n:node.Node):
        return self.provjeri_(n)
    def uvijet_identifikacije(self, n:node.Node):
        return self.uvijet_identifikacije_(n)
    def copy(self):
        return Identifikator(self.uvijet_identifikacije_,self.svojstva_,self.provjeri_)

def greska(n:node.Node):
    print(f"{n.vrijednost} ::=",end="")
    for dijete in n.djeca:
        if dijete.vrijednost.startswith("<"):
            print(f" {dijete.vrijednost}",end='')
        else:
            print(f" {dijete.vrijednost}({dijete.linija},{dijete.kod})",end='')
    print("")
    sys.exit(0)

tablica_znakova = TablicaZnakova()
main_postoji = False
identifikatori = []
ASCII = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789,./!?@#$%^&*()[]{}_+-?>=<:;`~| "
IDE_IZA_BACKSLASH = "tn0\'\"\\"
unutar = []

'''
[const_int , int, const_char, char] ~ [int, const_int]
[const_char, char] ~ [char, const_char]
[niz_char, niz_int] ~ [niz_int, niz_const_int]
[niz_char, niz_int, niz_const_char,niz_const_int] ~ [niz_const_int]
ima jos
'''


def check_impl(str1, str2):
    impl_konverzija = \
        {
            ('const_int', 'int'),
            ('int', 'const_int'),
            ('char', 'const_char'),
            ('const_char', 'char'),
            ('char', 'int'),
            ('char', 'const_int'),
            ('const_char', 'int'),
            ('const_char', 'const_int'),
            ('niz_int', 'niz_const_int'),
            ('niz_char', 'niz_const_char'),
            ('niz_char', 'niz_int'),
            ('niz_char', 'niz_const_char'),
         }
    if (str1, str2) in impl_konverzija:
        return True
    return str1 == str2

'''
<primarni_izraz> ::= IDN
tip ← IDN.tip
l-izraz ← IDN.l-izraz

1. IDN.ime je deklarirano
'''
def uvj_1(n:node.Node) -> bool:
    if n.vrijednost != '<primarni_izraz>':
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "IDN":
        return False
    return True
def prov_1(n:node.Node) -> bool:
    podaci = tablica_znakova.testiraj(n.djeca[0].kod)
    if not podaci:
        greska(n)
        return False
    n.svojstva["tip"]=podaci["tip"]
    n.svojstva["l-izraz"]=podaci["l-izraz"]
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
    if len(n.djeca) != 1:
        return False
    if not n.djeca[0].vrijednost =="BROJ":
        return False
    return True
def prov_2(n:node.Node) -> bool:
    try:
        if not (2147483648 > int(n.djeca[0].kod) >= -2147483648):
            greska(n)
            return False
    except ValueError:
        greska(n)
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
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost !="ZNAK":
        return False
    return True
def prov_3(n:node.Node) -> bool:
    znak = n.djeca[0].vrijednost
    if (znak[1] not in ASCII) and (not (znak[1] == "\\" and (znak[2] in IDE_IZA_BACKSLASH) and len(znak)==4)):
        greska(n)
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
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost !="NIZ_ZNAKOVA":
        return False
    return True
def prov_4(n:node.Node) -> bool:
    string = n.djeca[0].kod
    if not (string[0] == "\"" and string[-1] == "\""):
        greska(n)
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
                greska(n)
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
    if len(n.djeca) != 3:
        return False
    if not n.djeca[0].vrijednost =="L_ZAGRADA":
        return False
    if not n.djeca[1].vrijednost =="<izraz>":
        return False
    if not n.djeca[2].vrijednost =="D_ZAGRADA":
        return False
    return True
def prov_5(n:node.Node) -> bool:
    provjera = n.djeca[1].identifikator.provjera(n.djeca[1])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[1].svojstva["tip"]
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
    if n.vrijednost != '<postfiks_izraz>':
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<primarni_izraz>":
        return False
    return True
def prov_6(n:node.Node) -> bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_6,
    ["tip", "l-izraz"],
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
    elif len(n.djeca) != 4:
        return False
    elif n.djeca[0].vrijednost != "<postfiks_izraz>":
        return False
    elif n.djeca[1].vrijednost != "L_UGL_ZAGRADA":
        return False
    elif n.djeca[2].vrijednost != "<izraz>":
        return False
    elif n.djeca[3].vrijednost != "D_UGL_ZAGRADA":
        return False
    return True
def prov_7(n:node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[0].svojstva["tip"].startswith("niz_"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"][len("niz_"):]
    if not n.djeca[0].svojstva["tip"][len("niz_"):].startswith("const_"):
        n.svojstva["l-izraz"] = 1
    else:
        n.svojstva["l-izraz"] = 0
    return True
identifikatori.append(Identifikator(
    uvj_7,
    ["tip", "l-izraz"],
    prov_7
))



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
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<postfiks_izraz>":
        return False
    elif n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    elif n.djeca[2].vrijednost != "D_ZAGRADA":
        return False
    return True
def prov_8(n:node.Node) -> bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    '''
    funkcija void  int
    funkcija int char  int
    '''

    if not n.djeca[0].svojstva["tip"].startswith("funkcija void  "):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"][len("funkcija void  "):]
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_8,
    ["tip", "l-izraz"],
    prov_8
))

'''
 <postfiks_izraz> ::= <postfiks_izraz> L_ZAGRADA <lista_argumenata> D_ZAGRADA
tip ← pov
l-izraz ← 0
1. provjeri(<postfiks_izraz>)
2. provjeri(<lista_argumenata>)
3. <postfiks_izraz>.tip = funkcija(params → pov) i redom po elementima #
arg-tip iz <lista_argumenata>.tipovi i param-tip iz params vrijedi arg-tip
∼ param-tip
'''

def uvj_9(n:node.Node) -> bool:
    if n.vrijednost != '<postfiks_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<postfiks_izraz>":
        return False
    elif n.djeca[0].vrijednost != "L_ZAGRADA:":
        return False
    elif n.djeca[0].vrijednost != "<lista_argumentata>":
        return False
    elif n.djeca[0].vrijednost != "D_ZAGRADA:":
        return False
    return True
def prov_9(n:node.Node) -> bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    provjera = n.djeca[2].identifikator.provjera(n.djeca[2])
    if not provjera:
        greska(n)
        return False

    #<postfiks_izraz>.tip = funkcija(params → pov) i redom po elementima
    #arg-tip iz <lista_argumenata>.tipovi i param-tip iz params vrijedi
    #arg-tip ∼ param-tip
    lista_parametara = n.djeca[0].svojstva["tip"][len("funkcija "):].split()[:-1]
    lista_argumenata = n.djeca[2].svojstva["tipovi"]
    if len(lista_argumenata) == len(lista_parametara):
        for i in range(len(lista_parametara)):
            if not check_impl(lista_argumenata[i], lista_parametara[i]):
                greska(n)
                return False
    else:
        greska(n)
        return False

    pov = n.djeca[0].svojstva["tip"].split()[-1]
    n.svojstva["tip"] = pov
    n.svojstva["l-izraz"] = 0
    return True


identifikatori.append(Identifikator(
    uvj_9,
    ["tip", "l-izraz"],
    prov_9
))
'''
<postfiks_izraz> ::= <postfiks_izraz> (OP_INC | OP_DEC)
tip ← int
l-izraz ← 0
1. provjeri(<postfiks_izraz>)
2. <postfiks_izraz>.l-izraz = 1 i <postfiks_izraz>.tip ∼ int
'''
def uvj_10(n:node.Node) -> bool:
    if n.vrijednost != '<postfiks_izraz>':
        return False
    elif len(n.djeca)!= 2:
        return False
    elif n.djeca[0].vrijednost != "<postfiks_izraz>":
        return False
    elif n.djeca[1].vrijednost not in ["OP_INC", "OP_DEC"]:
        return False
    return True
def prov_10(n:node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["l-izraz"] != 1:
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_10,
    ["tip","l-izraz"],
    prov_10
))

'''
<lista_argumenata> ::= <izraz_pridruzivanja>
tipovi ← [ <izraz_pridruzivanja>.tip ]
1. provjeri(<izraz_pridruzivanja>)
'''
def uvj_11(n:node.Node) -> bool:
    if n.vrijednost != "<lista_argumenata>":
        return False
    elif len(n.djeca)!=1:
        return False
    if n.djeca[0].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_11(n:node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tipovi"] = [n.djeca[0].svojstva["tip"]]
    return True

identifikatori.append(Identifikator(
    uvj_11,
    ["tipovi"],
    prov_11
))


'''
<lista_argumenata> ::= <lista_argumenata> ZAREZ <izraz_pridruzivanja>
tipovi ← <lista_argumenata>.tipovi + [ <izraz_pridruzivanja>.tip ]
1. provjeri(<lista_argumenata>)
2. provjeri(<izraz_pridruzivanja>)
'''
def uvj_12(n:node.Node)->bool:
    if n.vrijednost=="<lista_argumenata>":
        return False
    elif len(n.djeca)!=3:
        return False
    elif n.djeca[0].vrijednost!="<lista_argumenata>":
        return False
    elif n.djeca[1].vrijednost!="ZAREZ":
        return False
    elif n.djeca[2].vrijednost=="<izraz_pridruzivanja>":
        return False
    return True
def prov_12(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    n.svojstva["tipovi"] = n.djeca[0].svojstva["tipovi"] + [n.djeca[2].svojstva["tip"]]
    return True

identifikatori.append(Identifikator(
    uvj_12,
    ["tipovi"],
    prov_12
))

'''
<unarni_izraz> ::= <postfiks_izraz>
tip ← <postfiks_izraz>.tip
l-izraz ← <postfiks_izraz>.l-izraz
1. provjeri(<postfiks_izraz>)
'''

def uvj_13(n:node.Node)->bool:
    if n.vrijednost != "<unarni_izraz>":
        return False
    elif len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<postfiks_izraz>":
        return False
    return True
def prov_13(n:node.Node) -> bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_13,
    ["tip","l-izraz"],
    prov_13
))

'''
<unarni_izraz> ::= (OP_INC | OP_DEC) <unarni_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<unarni_izraz>)
2. <unarni_izraz>.l-izraz = 1 i <unarni_izraz>.tip ∼ int
'''

def uvj_14(n:node.Node) -> bool:
    if n.vrijednost != '<unarni_izraz>':
        return False
    elif len(n.djeca)!= 2:
        return False
    elif n.djeca[0].vrijednost not in ["OP_INC", "OP_DEC"]:
        return False
    elif n.djeca[1].vrijednost != "<unarni_izraz>":
        return False
    return True
def prov_14(n:node.Node)->bool:
    provjera = n.djeca[1].identifikator.provjera(n.djeca[1])
    if not provjera:
        greska(n)
        return False
    if not n.djeca[1].svojstva["l-izraz"] == 1:
        greska(n)
        return False
    if not check_impl(n.djeca[1].tip, "int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_14,
    ["tip","l-izraz"],
    prov_14
))

'''
<unarni_izraz> ::= <unarni_operator> <cast_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<cast_izraz>)
2. <cast_izraz>.tip ∼ int
'''

def uvj_15(n:node.Node) -> bool:
    if n.vrijednost != '<unarni_izraz>':
        return False
    elif len(n.djeca)!= 2:
        return False
    elif n.djeca[0].vrijednost != "<unarni_operator>":
        return False
    elif n.djeca[1].vrijednost != "<cast_izraz>":
        return False
    return True
def prov_15(n:node.Node)->bool:
    provjera = n.djeca[1].identifikator.provjera(n.djeca[1])
    if not provjera:
        greska(n)
        return False
    if not check_impl(n.djeca[1].svojstva["tip"], "int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_15,
    ["tip","l-izraz"],
    prov_15
))

'''
<unarni_operator>
'''
def uvj_16(n:node.Node)->bool:
    if n.vrijednost != '<unarni_operator>':
        return False
    return True
def prov_16(n:node.Node)->bool:
    return True

identifikatori.append(Identifikator(
    uvj_16,
    [],
    prov_16
))

'''
<cast_izraz> ::= <unarni_izraz>
tip ← <unarni_izraz>.tip
l-izraz ← <unarni_izraz>.l-izraz
1. provjeri(<unarni_izraz>)
'''

def uvj_17(n:node.Node)->bool:
    if n.vrijednost != '<cast_izraz>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "<unarni_izraz>":
        return False
    return True
def prov_17(n:node.Node)->bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True
identifikatori.append(Identifikator(
    uvj_17,
    ["tip", "l-izraz"],
    prov_17
))

'''
<cast_izraz> ::= L_ZAGRADA <ime_tipa> D_ZAGRADA <cast_izraz>
tip ← <ime_tipa>.tip
l-izraz ← 0
1. provjeri(<ime_tipa>)
2. provjeri(<cast_izraz>)
3. <cast_izraz>.tip se moˇze pretvoriti u <ime_tipa>.tip po poglavlju 4.3.1
'''
def uvj_18(n:node.Node)->bool:
    if n.vrijednost != '<cast_izraz>':
        return False
    elif len(n.djeca) != 4:
        return False
    elif n.djeca[0].vrijednost != "L_ZAGRADA":
        return False
    elif n.djeca[1].vrijednost != "<ime_tipa>":
        return False
    elif n.djeca[2].vrijednost != "D_ZAGRADA":
        return False
    elif n.djeca[3].vrijednost != "<cast_izraz>":
        return False
    return True
def prov_18(n:node.Node)->bool:
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    if not n.djeca[3].identifikator.provjera(n.djeca[3]):
        greska(n)
        return False
    if (not check_impl(n.djeca[3].svojstva["tip"],n.djeca[1].svojstva["tip"])) or (not n.djeca[1].svojstva["tip"]=='char' and n.djeca[3].svojstva["tip"]=='int') :
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[1].svojstva["tip"]
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_18,
    ["tip","l-izraz"],
    prov_18
))

'''
<ime_tipa> ::= <specifikator_tipa>
tip ← <specifikator_tipa>.tip
1. provjeri(<specifikator_tipa>)
'''

def uvj_19(n:node.Node)->bool:
    if n.vrijednost != '<ime_tipa>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "<specifikator_tipa>":
        return False
    return True
def prov_19(n:node.Node)->bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    return True
identifikatori.append(Identifikator(
    uvj_19,
    ["tip"],
    prov_19
))

'''
<ime_tipa> ::= KR_CONST <specifikator_tipa>
tip ← const(<specifikator_tipa>.tip)
1. provjeri(<specifikator_tipa>)
2. <specifikator_tipa>.tip 6= void
'''

def uvj_20(n:node.Node) -> bool:
    if n.vrijednost != '<ime_tipa>':
        return False
    elif len(n.djeca)!= 2:
        return False
    elif n.djeca[0].vrijednost != "KR_CONST":
        return False
    elif n.djeca[1].vrijednost != "<specifikator_tipa>":
        return False
    return True
def prov_20(n:node.Node)->bool:
    provjera = n.djeca[1].identifikator.provjera(n.djeca[1])
    if not provjera:
        greska(n)
        return False
    if n.djeca[1].svojstva["tip"] == "void":
        greska(n)
        return False
    n.svojstva["tip"] = "const" + n.djeca[1].svojstva["tip"]
    return True

identifikatori.append(Identifikator(
    uvj_20,
    ["tip","l-izraz"],
    prov_20
))

'''
<specifikator_tipa> ::= KR_VOID
tip ← void
'''

def uvj_21(n:node.Node)->bool:
    if n.vrijednost != '<specifikator_tipa>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "KR_VOID":
        return False
    return True
def prov_21(n:node.Node)->bool:
    n.svojstva["tip"] = "void"
    return True
identifikatori.append(Identifikator(
    uvj_21,
    ["tip"],
    prov_21
))

'''
<specifikator_tipa> ::= KR_CHAR
tip ← char
'''

def uvj_22(n:node.Node)->bool:
    if n.vrijednost != '<specifikator_tipa>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "KR_CHAR":
        return False
    return True
def prov_22(n:node.Node)->bool:
    n.svojstva["tip"] = "char"
    return True
identifikatori.append(Identifikator(
    uvj_22,
    ["tip"],
    prov_22
))

'''
<specifikator_tipa> ::= KR_INT
tip ← int
'''

def uvj_23(n:node.Node)->bool:
    if n.vrijednost != '<specifikator_tipa>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "KR_INT":
        return False
    return True
def prov_23(n:node.Node)->bool:
    n.svojstva["tip"] = "int"
    return True
identifikatori.append(Identifikator(
    uvj_23,
    ["tip"],
    prov_23
))

'''
<multiplikativni_izraz> ::= <cast_izraz>
tip ← <cast_izraz>.tip
l-izraz ← <cast_izraz>.l-izraz
1. provjeri(<cast_izraz>)
'''

def uvj_24(n:node.Node)->bool:
    if n.vrijednost != '<multiplikativni_izraz>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "<cast_izraz>":
        return False
    return True
def prov_24(n:node.Node)->bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True
identifikatori.append(Identifikator(
    uvj_24,
    ["tip", "l-izraz"],
    prov_24
))

'''
<multiplikativni_izraz> ::= <multiplikativni_izraz> (OP_PUTA |
OP_DIJELI | OP_MOD) <cast_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<multiplikativni_izraz>)
2. <multiplikativni_izraz>.tip ∼ int
3. provjeri(<cast_izraz>)
4. <cast_izraz>.tip ∼ int
'''
def uvj_25(n:node.Node)->bool:
    if n.vrijednost != '<multiplikativni_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<multiplikativni_izraz>":
        return False
    elif n.djeca[1].vrijednost not in ["OP_PUTA", "OP_DIJELI", "OP_MOD"]:
        return False
    elif n.djeca[2].vrijednost != "D_ZAGRADA":
        return False
    return True
def prov_25(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_25,
    ["tip","l-izraz"],
    prov_25
))


'''
<aditivni_izraz> ::= <multiplikativni_izraz>
tip ← <multiplikativni_izraz>.tip
l-izraz ← <multiplikativni_izraz>.l-izraz
1. provjeri(<multiplikativni_izraz>)
'''
def uvj_26(n:node.Node)->bool:
    if n.vrijednost != '<aditivni_izraz>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "<multiplikativni_izraz>":
        return False
    return True
def prov_26(n:node.Node)->bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True
identifikatori.append(Identifikator(
    uvj_26,
    ["tip", "l-izraz"],
    prov_26
))

'''
<aditivni_izraz> ::= <aditivni_izraz> (PLUS | MINUS) <multiplikativni_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<aditivni_izraz>)
2. <aditivni_izraz>.tip ∼ int
3. provjeri(<multiplikativni_izraz>)
4. <multiplikativni_izraz>.tip ∼ int
'''
def uvj_27(n:node.Node)->bool:
    if n.vrijednost != '<aditivni_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<aditivni_izraz>":
        return False
    elif n.djeca[1].vrijednost not in ["PLUS", "MINUS"]:
        return False
    elif n.djeca[2].vrijednost != "<multiplikativni_izraz>":
        return False
    return True
def prov_27(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_27,
    ["tip","l-izraz"],
    prov_27
))


'''
<odnosni_izraz> ::= <aditivni_izraz>
tip ← <aditivni_izraz>.tip
l-izraz ← <aditivni_izraz>.l-izraz
1. provjeri(<aditivni_izraz>)
'''
def uvj_28(n:node.Node)->bool:
    if n.vrijednost != '<odnosni_izraz>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "<aditivni_izraz>":
        return False
    return True
def prov_28(n:node.Node)->bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True
identifikatori.append(Identifikator(
    uvj_28,
    ["tip", "l-izraz"],
    prov_28
))

'''
<odnosni_izraz> ::= <odnosni_izraz> (OP_LT | OP_GT | OP_LTE | OP_GTE) <aditivni_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<odnosni_izraz>)
2. <odnosni_izraz>.tip ∼ int
3. provjeri(<aditivni_izraz>)
4. <aditivni_izraz>.tip ∼ int
TODO
'''
def uvj_29(n:node.Node)->bool:
    if n.vrijednost != '<odnosni_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<odnosni_izraz>":
        return False
    elif n.djeca[1].vrijednost not in ["OP_LT", "OP_GT", "OP_LTE", "OP_GTE"]:
        return False
    elif n.djeca[2].vrijednost != "<aditivni_izraz>":
        return False
    return True
def prov_29(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True
identifikatori.append(Identifikator(
    uvj_29,
    ["tip", "l-izraz"],
    prov_29
))


'''
<jednakosni_izraz> ::= <odnosni_izraz>
tip ← <odnosni_izraz>.tip
l-izraz ← <odnosni_izraz>.l-izraz
1. provjeri(<odnosni_izraz>)
'''
def uvj_30(n:node.Node)->bool:
    if n.vrijednost != '<jednakosni_izraz>':
        return False
    elif len(n.djeca)!= 1:
        return False
    elif n.djeca[0].vrijednost != "<odnosni_izraz>":
        return False
    return True
def prov_30(n:node.Node)->bool:
    provjera = n.djeca[0].identifikator.provjera(n.djeca[0])
    if not provjera:
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True
identifikatori.append(Identifikator(
    uvj_30,
    ["tip", "l-izraz"],
    prov_30
))

'''
<jednakosni_izraz> ::= <jednakosni_izraz> (OP_EQ | OP_NEQ) <odnosni_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<jednakosni_izraz>)
2. <jednakosni_izraz>.tip ∼ int
3. provjeri(<odnosni_izraz>)
4. <odnosni_izraz>.tip ∼ int
TODO
'''
def uvj_31(n:node.Node)->bool:
    if n.vrijednost != '<jednakosni_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<jednakosni_izraz>":
        return False
    elif n.djeca[1].vrijednost not in ["OP_EQ", "OP_NEQ"]:
        return False
    elif n.djeca[2].vrijednost != "<odnosni_izraz>":
        return False
    return True
def prov_31(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_31,
    ["tip","l-izraz"],
    prov_31
))

'''
<bin_i_izraz> ::= <jednakosni_izraz>
tip ← <jednakosni_izraz>.tip
l-izraz ← <jednakosni_izraz>.l-izraz
1. provjeri(<jednakosni_izraz>)
'''
def uvj_32(n:node.Node)->bool:
    if n.vrijednost != '<bin_i_izraz>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<jednakosni_izraz>":
        return False
    return True
def prov_32(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_32,
    ["tip","l-izraz"],
    prov_32
))

'''
<bin_i_izraz> ::= <bin_i_izraz> OP_BIN_I <jednakosni_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<bin_i_izraz>)
2. <bin_i_izraz>.tip ∼ int
3. provjeri(<jednakosni_izraz>)
4. <jednakosni_izraz>.tip ∼ int
'''

def uvj_33(n:node.Node)->bool:
    if n.vrijednost != '<bin_i_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<bin_i_izraz>":
        return False
    elif n.djeca[1].vrijednost != "OP_BIN_I":
        return False
    elif n.djeca[2].vrijednost != "<jednakosni_izraz>":
        return False
    return True
def prov_33(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_33,
    ["tip","l-izraz"],
    prov_33
))

'''
<bin_xili_izraz> ::= <bin_i_izraz>
tip ← <bin_i_izraz>.tip
l-izraz ← <bin_i_izraz>.l-izraz
1. provjeri(<bin_i_izraz>)
'''
def uvj_34(n:node.Node)->bool:
    if n.vrijednost != '<bin_xili_izraz>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<bin_i_izraz>":
        return False
    return True
def prov_34(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_34,
    ["tip","l-izraz"],
    prov_34
))
'''
<bin_xili_izraz> ::= <bin_xili_izraz> OP_BIN_XILI <bin_i_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<bin_xili_izraz>)
2. <bin_xili_izraz>.tip ∼ int
3. provjeri(<bin_i_izraz>)
4. <bin_i_izraz>.tip ∼ int
'''
def uvj_35(n:node.Node)->bool:
    if n.vrijednost != '<bin_xili_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<bin_xili_izraz>":
        return False
    elif n.djeca[1].vrijednost != "OP_BIN_XILI":
        return False
    elif n.djeca[2].vrijednost != "<bin_i_izraz>":
        return False
    return True
def prov_35(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_35,
    ["tip","l-izraz"],
    prov_35
))

'''
<bin_ili_izraz> ::= <bin_xili_izraz>
tip ← <bin_xili_izraz>.tip
l-izraz ← <bin_xili_izraz>.l-izraz
1. provjeri(<bin_xili_izraz>)
'''
def uvj_36(n:node.Node)->bool:
    if n.vrijednost != '<bin_ili_izraz>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<bin_xili_izraz>":
        return False
    return True
def prov_36(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_36,
    ["tip","l-izraz"],
    prov_36
))

'''
<bin_ili_izraz> ::= <bin_ili_izraz> OP_BIN_ILI <bin_xili_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<bin_ili_izraz>)
2. <bin_ili_izraz>.tip ∼ int
3. provjeri(<bin_xili_izraz>)
4. <bin_xili_izraz>.tip ∼ int
'''
def uvj_37(n:node.Node)->bool:
    if n.vrijednost != '<bin_ili_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<bin_ili_izraz>":
        return False
    elif n.djeca[1].vrijednost != "OP_BIN_ILI":
        return False
    elif n.djeca[2].vrijednost != "<bin_xili_izraz>":
        return False
    return True
def prov_37(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_37,
    ["tip","l-izraz"],
    prov_37
))

'''
<log_i_izraz> ::= <bin_ili_izraz>
tip ← <bin_ili_izraz>.tip
l-izraz ← <bin_ili_izraz>.l-izraz
1. provjeri(<bin_ili_izraz>)
'''
def uvj_38(n:node.Node)->bool:
    if n.vrijednost != '<log_i_izraz>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<bin_ili_izraz>":
        return False
    return True
def prov_38(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_38,
    ["tip","l-izraz"],
    prov_38
))

'''
<log_i_izraz> ::= <log_i_izraz> OP_I <bin_ili_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<log_i_izraz>)
2. <log_i_izraz>.tip ∼ int
3. provjeri(<bin_ili_izraz>)
4. <bin_ili_izraz>.tip ∼ int

'''
def uvj_39(n:node.Node)->bool:
    if n.vrijednost != '<log_i_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<log_i_izraz>":
        return False
    elif n.djeca[1].vrijednost != "OP_I":
        return False
    elif n.djeca[2].vrijednost != "<bin_ili_izraz>":
        return False
    return True
def prov_39(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_39,
    ["tip","l-izraz"],
    prov_39
))

'''
<log_ili_izraz> ::= <log_i_izraz>
tip ← <log_i_izraz>.tip
l-izraz ← <log_i_izraz>.l-izraz
1. provjeri(<log_i_izraz>)

'''
def uvj_40(n:node.Node)->bool:
    if n.vrijednost != '<log_ili_izraz>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<log_i_izraz>":
        return False
    return True
def prov_40(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_40,
    ["tip","l-izraz"],
    prov_40
))

'''
<log_ili_izraz> ::= <log_ili_izraz> OP_ILI <log_i_izraz>
tip ← int
l-izraz ← 0
1. provjeri(<log_ili_izraz>)
2. <log_ili_izraz>.tip ∼ int
3. provjeri(<log_i_izraz>)
4. <log_i_izraz>.tip ∼ int

'''
def uvj_41(n:node.Node)->bool:
    if n.vrijednost != '<log_ili_izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<log_ili_izraz>":
        return False
    elif n.djeca[1].vrijednost != "OP_ILI":
        return False
    elif n.djeca[2].vrijednost != "<log_i_izraz>":
        return False
    return True
def prov_41(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not check_impl(n.djeca[0].svojstva["tip"],"int"):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],"int"):
        greska(n)
        return False
    n.svojstva["tip"] = "int"
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_41,
    ["tip","l-izraz"],
    prov_41
))

'''
<izraz_pridruzivanja> ::= <log_ili_izraz>
tip ← <log_ili_izraz>.tip
l-izraz ← <log_ili_izraz>.l-izraz
1. provjeri(<log_ili_izraz>)
'''
def uvj_42(n:node.Node)->bool:
    if n.vrijednost != '<izraz_pridruzivanja>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<log_ili_izraz>":
        return False
    return True
def prov_42(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_42,
    ["tip","l-izraz"],
    prov_42
))

'''
<izraz_pridruzivanja> ::= <postfiks_izraz> OP_PRIDRUZI <izraz_pridruzivanja>
tip ← <postfiks_izraz>.tip
l-izraz ← 0
1. provjeri(<postfiks_izraz>)
2. <postfiks_izraz>.l-izraz = 1
3. provjeri(<izraz_pridruzivanja>)
4. <izraz_pridruzivanja>.tip ∼ <postfiks_izraz>.tip
'''
def uvj_43(n:node.Node)->bool:
    if n.vrijednost != '<izraz_pridruzivanja>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<postfiks_izraz>":
        return False
    elif n.djeca[1].vrijednost != "OP_PRIDRUZI":
        return False
    elif n.djeca[2].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_43(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[0].svojstva["l-izraz"] == 1:
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"],n.djeca[0].svojstva["tip"]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_43,
    ["tip","l-izraz"],
    prov_43
))

'''
<izraz> ::= <izraz_pridruzivanja>
tip ← <izraz_pridruzivanja>.tip
l-izraz ← <izraz_pridruzivanja>.l-izraz
1. provjeri(<izraz_pridruzivanja>)

'''
def uvj_44(n:node.Node)->bool:
    if n.vrijednost != '<izraz>':
        return False
    elif len(n.djeca) != 1:
        return False
    elif n.djeca[0].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_44(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    n.svojstva["l-izraz"] = n.djeca[0].svojstva["l-izraz"]
    return True

identifikatori.append(Identifikator(
    uvj_44,
    ["tip","l-izraz"],
    prov_44
))

'''
<izraz> ::= <izraz> ZAREZ <izraz_pridruzivanja>
tip ← <izraz_pridruzivanja>.tip
l-izraz ← 0
1. provjeri(<izraz>)
2. provjeri(<izraz_pridruzivanja>)
'''
def uvj_45(n:node.Node)->bool:
    if n.vrijednost != '<izraz>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "<izraz>":
        return False
    elif n.djeca[1].vrijednost != "ZAREZ":
        return False
    elif n.djeca[2].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_45(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[2].svojstva["tip"]
    n.svojstva["l-izraz"] = 0
    return True

identifikatori.append(Identifikator(
    uvj_45,
    ["tip","l-izraz"],
    prov_45
))



'''
<slozena_naredba> ::= L_VIT_ZAGRADA <lista_naredbi> D_VIT_ZAGRADA
1. provjeri(<lista_naredbi>)
'''
def uvj_100(n:node.Node)->bool:
    if n.vrijednost != '<slozena_naredba>':
        return False
    elif len(n.djeca) != 3:
        return False
    elif n.djeca[0].vrijednost != "L_VIT_ZAGRADA":
        return False
    elif n.djeca[1].vrijednost != "<lista_naredbi>":
        return False
    elif n.djeca[2].vrijednost != "D_VIT_ZAGRADA":
        return False
    return True
def prov_100(n:node.Node)->bool:
    global tablica_znakova
    tablica_znakova = tablica_znakova.otvori_blok()
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    tablica_znakova = tablica_znakova.zatvori_blok()
    return True
identifikatori.append(Identifikator(
    uvj_100,
    [],
    prov_100
))

'''
<slozena_naredba> ::= L_VIT_ZAGRADA <lista_deklaracija> <lista_naredbi> D_VIT_ZAGRADA
1. provjeri(<lista_deklaracija>)
2. provjeri(<lista_naredbi>)
'''
def uvj_101(n:node.Node)->bool:
    if n.vrijednost != '<slozena_naredba>':
        return False
    elif len(n.djeca) != 4:
        return False
    elif n.djeca[0].vrijednost != "L_VIT_ZAGRADA":
        return False
    elif n.djeca[1].vrijednost != "<lista_deklaracija>":
        return False
    elif n.djeca[2].vrijednost != "<lista_naredbi>":
        return False
    elif n.djeca[3].vrijednost != "D_VIT_ZAGRADA":
        return False
    return True
def prov_101(n:node.Node)->bool:
    global tablica_znakova
    tablica_znakova = tablica_znakova.otvori_blok()


    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    tablica_znakova = tablica_znakova.zatvori_blok()
    return True
identifikatori.append(Identifikator(
    uvj_101,
    [],
    prov_101
))


'''
<lista_naredbi> ::= <naredba>
1. provjeri(<naredba>)
'''
def uvj_102(n:node.Node) -> bool:
    if n.vrijednost != "<lista_naredbi>":
        return False
    elif len(n.djeca)!=1:
        return False
    if n.djeca[0].vrijednost != "<naredba>":
        return False
    return True
def prov_102(n:node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_102,
    [],
    prov_102
))

'''
<lista_naredbi> ::= <lista_naredbi> <naredba>
1. provjeri(<lista_naredbi>)
2. provjeri(<naredba>)
'''
def uvj_103(n:node.Node) -> bool:
    if n.vrijednost != "<lista_naredbi>":
        return False
    elif len(n.djeca)!=2:
        return False
    elif n.djeca[0].vrijednost != "<lista_naredbi>":
        return False
    elif n.djeca[1].vrijednost != "<naredba>":
        return False
    return True
def prov_103(n:node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_103,
    [],
    prov_103
))

'''
<naredba>
provjera(prvi)
'''
def uvj_104(n:node.Node)->bool:
    if n.vrijednost != "<naredba>":
        return False
    if len(n.djeca)!=1:
        return False
    if n.djeca[0].vrijednost not in ["<slozena_naredba>","<izraz_naredba>", "<naredba_grananja>", "<naredba_petlje>", "<naredba_skoka>"]:
        return False
    return True
def prov_104(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_104,
    [],
    prov_104
))


'''
<izraz_naredba> ::= TOCKAZAREZ
tip ← int
'''
def uvj_105(n:node.Node)->bool:
    if n.vrijednost != "<izraz_naredba>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "TOCKAZAREZ":
        return False
    return True
def prov_105(n:node.Node)->bool:
    n.svojstva["tip"] = "int"
    return True
identifikatori.append(Identifikator(
    uvj_105,
    ["tip"],
    prov_105
))

'''
<izraz_naredba> ::= <izraz> TOCKAZAREZ
tip ← <izraz>.tip
1. provjeri(<izraz>)
'''
def uvj_106(n:node.Node)->bool:
    if n.vrijednost != "<izraz_naredba>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "<izraz>":
        return False
    if n.djeca[1].vrijednost != "TOCKAZAREZ":
        return False
    return True
def prov_106(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    return True
identifikatori.append(Identifikator(
    uvj_106,
    ["tip"],
    prov_106
))

'''
<naredba_grananja> ::= KR_IF L_ZAGRADA <izraz> D_ZAGRADA <naredba>
1. provjeri(<izraz>)
2. <izraz>.tip ∼ int
3. provjeri(<naredba>)
'''
def uvj_107(n:node.Node)->bool:
    if n.vrijednost != "<naredba_grananja>":
        return False
    if len(n.djeca) != 5:
        return False
    if n.djeca[0].vrijednost != "KR_IF":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "<izraz>":
        return False
    if n.djeca[3].vrijednost != "D_ZAGRADA":
        return False
    if n.djeca[4].vrijednost != "<naredba>":
        return False
    return True
def prov_107(n:node.Node)->bool:
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"], "int"):
        return False
    if not n.djeca[4].identifikator.provjera(n.djeca[4]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_107,
    [],
    prov_107
))
'''
<naredba_grananja> ::= KR_IF L_ZAGRADA <izraz> D_ZAGRADA <naredba>1
KR_ELSE <naredba>2
1. provjeri(<izraz>)
2. <izraz>.tip ∼ int
3. provjeri(<naredba>1)
4. provjeri(<naredba>2)

'''
def uvj_108(n:node.Node)->bool:
    if n.vrijednost != "<naredba_grananja>":
        return False
    if len(n.djeca) != 7:
        return False
    if n.djeca[0].vrijednost != "KR_IF":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "<izraz>":
        return False
    if n.djeca[3].vrijednost != "D_ZAGRADA":
        return False
    if n.djeca[4].vrijednost != "<naredba>":
        return False
    if n.djeca[5].vrijednost != "KR_ELSE":
        return False
    if n.djeca[6].vrijednost != "<naredba>":
        return False
    return True
def prov_108(n:node.Node)->bool:
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"], "int"):
        greska(n)
        return False
    if not n.djeca[4].identifikator.provjera(n.djeca[4]):
        greska(n)
        return False
    if not n.djeca[6].identifikator.provjera(n.djeca[6]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_108,
    [],
    prov_108
))

'''
<naredba_petlje> ::= KR_WHILE L_ZAGRADA <izraz> D_ZAGRADA <naredba>
1. provjeri(<izraz>)
2. <izraz>.tip ∼ int
3. provjeri(<naredba>)

'''
def uvj_109(n:node.Node)->bool:
    if n.vrijednost != "<naredba_petlje>":
        return False
    if len(n.djeca) != 5:
        return False
    if n.djeca[0].vrijednost != "KR_WHILE":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "<izraz>":
        return False
    if n.djeca[3].vrijednost != "D_ZAGRADA":
        return False
    if n.djeca[4].vrijednost != "<naredba>":
        return False
    return True
def prov_109(n:node.Node)->bool:
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not check_impl(n.djeca[2].svojstva["tip"], "int"):
        greska(n)
        return False
    unutar.append('loop')
    if not n.djeca[4].identifikator.provjera(n.djeca[4]):
        greska(n)
        return False
    unutar.pop()
    return True
identifikatori.append(Identifikator(
    uvj_109,
    [],
    prov_109
))

'''
<naredba_petlje> ::= KR_FOR L_ZAGRADA <izraz_naredba>1 <izraz_naredba>2
D_ZAGRADA <naredba>
1. provjeri(<izraz_naredba>1)
2. provjeri(<izraz_naredba>2)
3. <izraz_naredba>2.tip ∼ int
4. provjeri(<naredba>)

'''
def uvj_110(n:node.Node)->bool:
    if n.vrijednost != "<naredba_petlje>":
        return False
    if len(n.djeca) != 7:
        return False
    if n.djeca[0].vrijednost != "KR_FOR":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "<izraz_naredba>":
        return False
    if n.djeca[3].vrijednost != "<izraz_naredba>":
        return False
    if n.djeca[4].vrijednost != "<izraz>":
        return False
    if n.djeca[5].vrijednost != "D_ZAGRADA":
        return False
    if n.djeca[6].vrijednost != "<naredba>":
        return False
    return True
def prov_110(n:node.Node)->bool:
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not n.djeca[3].identifikator.provjera(n.djeca[3]):
        greska(n)
        return False
    if not check_impl(n.djeca[3].svojstva["tip"], "int"):
        greska(n)
        return False
    unutar.append("loop")
    if not n.djeca[6].identifikator.provjera(n.djeca[6]):
        greska(n)
        return False
    unutar.pop()
    return True
identifikatori.append(Identifikator(
    uvj_110,
    [],
    prov_110
))

'''
<naredba_petlje> ::= KR_FOR L_ZAGRADA <izraz_naredba>1 <izraz_naredba>2
<izraz> D_ZAGRADA <naredba>
1. provjeri(<izraz_naredba>1)
2. provjeri(<izraz_naredba>2)
3. <izraz_naredba>2.tip ∼ int
4. provjeri(<izraz>)
5. provjeri(<naredba>)
'''
def uvj_110(n:node.Node)->bool:
    if n.vrijednost != "<naredba_petlje>":
        return False
    if len(n.djeca) != 7:
        return False
    if n.djeca[0].vrijednost != "KR_FOR":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "<izraz_naredba>":
        return False
    if n.djeca[3].vrijednost != "<izraz_naredba>":
        return False
    if n.djeca[4].vrijednost != "<izraz>":
        return False
    if n.djeca[5].vrijednost != "D_ZAGRADA":
        return False
    if n.djeca[6].vrijednost != "<naredba>":
        return False
    return True
def prov_110(n:node.Node)->bool:
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if not n.djeca[3].identifikator.provjera(n.djeca[3]):
        greska(n)
        return False
    if not check_impl(n.djeca[3].svojstva["tip"], "int"):
        greska(n)
        return False
    if not n.djeca[4].identifikator.provjera(n.djeca[4]):
        greska(n)
        return False
    unutar.append("loop")
    if n.djeca[6].identifikator.provjera(n.djeca[6]):
        greska(n)
        return False
    unutar.pop()
    return True
identifikatori.append(Identifikator(
    uvj_110,
    [],
    prov_110
))

'''
<naredba_skoka> ::= (KR_CONTINUE | KR_BREAK) TOCKAZAREZ
1. naredba se nalazi unutar petlje ili unutar bloka koji je ugnijeˇzden u petlji
'''
def uvj_111(n:node.Node)->bool:
    if n.vrijednost != "<naredba_skoka>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost not in ["KR_CONTINUE", "KR_BREAK"]:
        return False
    if n.djeca[1].vrijednost != "TOCKAZAREZ":
        return False
    return True
def prov_111(n:node.Node)->bool:
    if not unutar[-1] == "loop":
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_111,
    [],
    prov_111
))


'''
<naredba_skoka> ::= KR_RETURN TOCKAZAREZ
1. naredba se nalazi unutar funkcije tipa funkcija(params → void)
'''
def uvj_112(n:node.Node)->bool:
    if n.vrijednost != "<naredba_skoka>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "KR_RETURN":
        return False
    if n.djeca[1].vrijednost != "TOCKAZAREZ":
        return False
    return True
def prov_112(n:node.Node)->bool:
    if not unutar[-1] == "void":
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_112,
    [],
    prov_112
))
'''
<naredba_skoka> ::= KR_RETURN <izraz> TOCKAZAREZ
1. provjeri(<izraz>)
2. naredba se nalazi unutar funkcije tipa funkcija(params → pov) i vrijedi
<izraz>.tip ∼ pov
'''
def uvj_113(n:node.Node)->bool:
    if n.vrijednost != "<naredba_skoka>":
        return False
    if len(n.djeca) != 3:
        return False
    if n.djeca[0].vrijednost != "KR_RETURN":
        return False
    if n.djeca[1].vrijednost != "<izraz>":
        return False
    if n.djeca[2].vrijednost != "TOCKAZAREZ":
        return False
    return True
def prov_113(n:node.Node)->bool:
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    tren = len(unutar)-1
    while unutar[tren]=="loop":
        tren-=1
    if not (unutar[tren] != "void"):
        greska(n)
        return False
    if not check_impl(n.djeca[1].svojstva["tip"], unutar[-1]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_113,
    [],
    prov_113
))

'''
<prijevodna_jedinica> ::= <vanjska_deklaracija>
1. provjeri(<vanjska_deklaracija>)
'''
def uvj_114(n:node.Node)->bool:
    if n.vrijednost != "<prijevodna_jedinica>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<vanjska_deklaracija>":
        return False
    return True
def prov_114(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_114,
    [],
    prov_114
))

'''
<prijevodna_jedinica> ::= <prijevodna_jedinica> <vanjska_deklaracija>
1. provjeri(<prijevodna_jedinica>)
2. provjeri(<vanjska_deklaracija>)
'''
def uvj_115(n:node.Node)->bool:
    if n.vrijednost != "<prijevodna_jedinica>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "<prijevodna_jedinica>":
        return False
    if n.djeca[1].vrijednost != "<vanjska_deklaracija>":
        return False
    return True
def prov_115(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_115,
    [],
    prov_115
))

'''
<vanjska deklaracija>
Nezavrˇsni znak <vanjska_deklaracija> generira ili definiciju funkcije (znak <definicija_funkcije>)
ili deklaraciju varijable ili funkcije (znak <deklaracija>). Obje produkcije su jediniˇcne
i u obje se provjeravaju pravila u podstablu kojem je znak s desne strane korijen
'''

def uvj_116(n:node.Node)->bool:
    if n.vrijednost != "<vanjska_deklaracija>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost not in ["<definicija_funkcije>", "<vanjska_deklaracija>"]:
        return False
    return True
def prov_116(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_116,
    [],
    prov_116
))


#deklaracije i definicije
'''
<definicija_funkcije> ::= <ime_tipa> IDN L_ZAGRADA KR_VOID D_ZAGRADA
<slozena_naredba>
1. provjeri(<ime_tipa>)
2. <ime_tipa>.tip 6= const(T)
3. ne postoji prije definirana funkcija imena IDN.ime
4. ako postoji deklaracija imena IDN.ime u globalnom djelokrugu onda je pripadni
tip te deklaracije funkcija(void → <ime_tipa>.tip)
5. zabiljeˇzi definiciju i deklaraciju funkcije
6. provjeri(<slozena_naredba>)
'''

def uvj_200(n:node.Node)-> bool:
    if n.vrijednost != '<definicija_funkcije>':
        return False
    elif len(n.djeca) != 6:
        return False
    elif n.djeca[0].vrijednost != "<ime_tipa>":
        return False
    elif n.djeca[1].vrijednost != "IDN":
        return False
    elif n.djeca[2].vrijednost != "L_ZAGRADA":
        return False
    elif n.djeca[3].vrijednost != "KR_VOID":
        return False
    elif n.djeca[4].vrijednost != "D_ZAGRADA":
        return False
    elif n.djeca[5].vrijednost != "<slozena_naredba>":
        return False
    return True
def prov_200(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"].startswith("const_"):
        greska(n)
        return False
    podaci = tablica_znakova.testiraj(n.djeca[1].kod)
    if podaci:
        if podaci.get("isDefined",False):
            greska(n)
            return False
    podaci_globalnog = tablica_znakova.get_root().testiraj(n.djeca[1].kod)
    if podaci_globalnog:
        globalni_tip = podaci.get("tip")
        if not globalni_tip.startswith("funkcija void  "):
            greska(n)
            return False
        if globalni_tip.split()[-1] != n.djeca[0].svojstva["tip"]:
            greska(n)
            return False
        podaci_globalnog["isDefined"] = True
        tablica_znakova.get_root().promjena(n.djeca[1].kod,podaci_globalnog)
    else:
        if not podaci:
            tablica_znakova.dodajZnak(n.djeca[1].kod, {
                "tip": "funkcija void  " + n.djeca[0].svojstva["tip"],
                "l-izraz": 0,
                "isDefined": True
            })
        else:
            tablica_znakova.dodajZnak(n.djeca[1].kod, {
                "tip": "funkcija void  " + n.djeca[0].svojstva["tip"],
                "l-izraz": 0,
                "isDefined": True
            })
    unutar.append(n.djeca[0].svojstva["tip"])
    if not n.djeca[5].identifikator.provjera(n.djeca[5]):
        greska(n)
        return False
    unutar.pop()
    return True
identifikatori.append(Identifikator(
    uvj_200,
    [],
    prov_200
))

'''
<definicija_funkcije> ::= <ime_tipa> IDN L_ZAGRADA <lista_parametara> D_ZAGRADA
<slozena_naredba>
1. provjeri(<ime_tipa>)
2. <ime_tipa>.tip 6= const(T)
3. ne postoji prije definirana funkcija imena IDN.ime
4. provjeri(<lista_parametara>)
5. ako postoji deklaracija imena IDN.ime u globalnom djelokrugu onda je pripadni
tip te deklaracije funkcija(<lista_parametara>.tipovi → <ime_tipa>.tip)
6. zabiljeˇzi definiciju i deklaraciju funkcije
7. provjeri(<slozena_naredba>) uz parametre funkcije koriste´ci <lista_parametara>.tipovi
i <lista_parametara>.imena.
'''
def uvj_200(n:node.Node)-> bool:
    if n.vrijednost != '<definicija_funkcije>':
        return False
    elif len(n.djeca) != 6:
        return False
    elif n.djeca[0].vrijednost != "<ime_tipa>":
        return False
    elif n.djeca[1].vrijednost != "IDN":
        return False
    elif n.djeca[2].vrijednost != "L_ZAGRADA":
        return False
    elif n.djeca[3].vrijednost != "<lista_parametara>":
        return False
    elif n.djeca[4].vrijednost != "D_ZAGRADA":
        return False
    elif n.djeca[5].vrijednost != "<slozena_naredba>":
        return False
    return True
def prov_200(n:node.Node)->bool:
    global tablica_znakova
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"].startswith("const_"):
        greska(n)
        return False
    podaci = tablica_znakova.testiraj(n.djeca[1].kod)
    if podaci:
        if podaci.get("isDefined",False):
            greska(n)
            return False
        lista_parametara = podaci["tip"].strip("funkcija ").split()[:-1]
        lista_argumenata = n.djeca[2].svojstva["tipovi"]
        if len(lista_argumenata) == len(lista_parametara):
            for i in range(len(lista_parametara)):
                if lista_argumenata[i] != lista_parametara[i]:
                    greska(n)
                    return False
        else:
            greska(n)
            return False

        ret = podaci["tip"].strip("funkcija ").split()[-1]
    if not n.djeca[3].identifikator.provjera(n.djeca[3]):
        greska(n)
        return False

    podaci_globalnog = tablica_znakova.get_root().testiraj(n.djeca[1].kod)
    if podaci_globalnog:
        globalni_tip = podaci.get("tip")
        if not globalni_tip.startswith("funkcija void  "):
            greska(n)
            return False
        if globalni_tip.split()[-1] != n.djeca[0].svojstva["tip"]:
            greska(n)
            return False
        podaci_globalnog["isDefined"] = True
        tablica_znakova.get_root().promjena(n.djeca[1].kod,podaci_globalnog)
    else:
        if not podaci:
            tablica_znakova.dodajZnak(n.djeca[1].kod, {
                "tip": "funkcija void  " + n.djeca[0].svojstva["tip"],
                "l-izraz": 0,
                "isDefined": True
            })
        else:
            tablica_znakova.dodajZnak(n.djeca[1].kod, {
                "tip": "funkcija void  " + n.djeca[0].svojstva["tip"],
                "l-izraz": 0,
                "isDefined": True
            })
    unutar.append(n.djeca[0].svojstva["tip"])
    tablica_znakova = tablica_znakova.otvori_blok()


    for i in range(len(n.djeca[3].svojstva["imena"])):
        tablica_znakova.dodajZnak(n.djeca[3].svojstva["imena"][i], {
            "tip":n.djeca[3].svojstva["tipovi"][i],
            "l-izraz": 0,
            "jeArgument": True,
        })
    if not n.djeca[5].identifikator.provjera(n.djeca[5]):
        greska(n)
        return False
    tablica_znakova = tablica_znakova.zatvori_blok()
    unutar.pop()
    return True
identifikatori.append(Identifikator(
    uvj_200,
    [],
    prov_200
))



'''
<lista_parametara> ::= <deklaracija_parametra>
tipovi ← [ <deklaracija_parametra>.tip ]
imena ← [ <deklaracija_parametra>.ime ]
1. provjeri(<deklaracija_parametra>)
'''
def uvj_201(n:node.Node):
    if n.vrijednost != "<lista_parametara>":
        return False
    elif len(n.djeca) !=1:
        return False
    elif n.djeca[0].vrijednost != "<deklaracija_parametra>":
        return False
    return True
def prov_201(n:node.Node):
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tipovi"] = [ n.djeca[0].svojstva["tip"] ]
    n.svojstva["imena"] = [ n.djeca[0].svojstva["ime"] ]
    return True
identifikatori.append(Identifikator(
    uvj_201,
    ["tipovi","imena"],
    prov_201
))

'''
<lista_parametara> ::= <lista_parametara> ZAREZ <deklaracija_parametra>
tipovi ← <lista_parametara>.tipovi + [ <deklaracija_parametra>.tip ]
imena ← <lista_parametara>.imena + [ <deklaracija_parametra>.ime ]
1. provjeri(<lista_parametara>)
2. provjeri(<deklaracija_parametra>)
3. <deklaracija_parametra>.ime ne postoji u <lista_parametara>.imena
'''
def uvj_201(n:node.Node):
    if n.vrijednost != "<lista_parametara>":
        return False
    elif len(n.djeca) !=3:
        return False
    elif n.djeca[0].vrijednost != "<lista_parametara>":
        return False
    elif n.djeca[1].vrijednost != "ZAREZ":
        return False
    elif n.djeca[2].vrijednost != "<deklaracija_parametra>":
        return False
    return True
def prov_201(n:node.Node):
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if n.djeca[2].svojstva["ime"] in n.djeca[0].svojstva["imena"]:
        greska(n)
        return False
    n.svojstva["tipovi"] = n.djeca[0].svojstva["tipovi"] + [ n.djeca[2].svojstva["tip"] ]
    n.svojstva["imena"] = n.djeca[0].svojstva["imena"] + [ n.djeca[2].svojstva["ime"] ]
    return True
identifikatori.append(Identifikator(
    uvj_201,
    ["tipovi","imena"],
    prov_201
))


'''
<deklaracija_parametra> ::= <ime_tipa> IDN
tip ← <ime_tipa>.tip
ime ← IDN.ime
1. provjeri(<ime_tipa>)
2. <ime_tipa>.tip 6= void
'''
def uvj_202(n:node.Node)->bool:
    if n.vrijednost != "<deklaracija_parametra>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "<ime_tipa>":
        return False
    if n.djeca[1].vrijednost != "IDN":
        return False
    return True
def prov_202(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"] == "void":
        return False
    n.svojstva["ime"] = n.djeca[1].kod
    n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
    return True
identifikatori.append(Identifikator(
    uvj_202,
    ["tipovi","imena"],
    prov_202
))


'''
<deklaracija_parametra> ::= <ime_tipa> IDN L_UGL_ZAGRADA D_UGL_ZAGRADA
tip ← niz (<ime_tipa>.tip)
ime ← IDN.ime
1. provjeri(<ime_tipa>)
2. <ime_tipa>.tip 6= void
'''
def uvj_203(n:node.Node)->bool:
    if n.vrijednost != "<deklaracija_parametra>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "<ime_tipa>":
        return False
    if n.djeca[1].vrijednost != "IDN":
        return False
    if n.djeca[2].vrijednost != "L_UGL_ZAGRADA":
        return False
    if n.djeca[3].vrijednost != "D_UGL_ZAGRADA":
        return False
    return True
def prov_203(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"] == "void":
        return False
    n.svojstva["ime"] = n.djeca[1].kod
    n.svojstva["tip"] = "niz_"+n.djeca[0].svojstva["tip"]
    return True
identifikatori.append(Identifikator(
    uvj_203,
    ["tip","ime"],
    prov_203
))

'''
<lista_deklaracija> ::= <deklaracija>
1. provjeri(<deklaracija>)
'''
def uvj_204(n:node.Node)->bool:
    if n.vrijednost != "<lista_deklaracija>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<deklaracija>":
        return False
    return True
def prov_204(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_204,
    [],
    prov_204
))

'''
<lista_deklaracija> ::= <lista_deklaracija> <deklaracija>
1. provjeri(<lista_deklaracija>)
2. provjeri(<deklaracija>)
'''
def uvj_205(n:node.Node)->bool:
    if n.vrijednost != "<lista_deklaracija>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "<lista_deklaracija>":
        return False
    if n.djeca[1].vrijednost != "<deklaracija>":
        return False
    return True
def prov_205(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_205,
    [],
    prov_205
))

'''
<deklaracija> ::= <ime_tipa> <lista_init_deklaratora> TOCKAZAREZ
1. provjeri(<ime_tipa>)
2. provjeri(<lista_init_deklaratora>) uz nasljedno svojstvo
<lista_init_deklaratora>.ntip ← <ime_tipa>.tip
'''
def uvj_206(n:node.Node)->bool:
    if n.vrijednost != "<deklaracija>":
        return False
    if len(n.djeca) != 3:
        return False
    if n.djeca[0].vrijednost != "<ime_tipa>":
        return False
    if n.djeca[1].vrijednost != "<lista_init_deklaratora>":
        return False
    if n.djeca[2].vrijednost != "TOCKAZAREZ":
        return False
    return True
def prov_206(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.djeca[1].svojstva["ntip"] = n.djeca[0].svojstva["tip"]
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_206,
    [],
    prov_206
))

'''
<lista_init_deklaratora> ::= <init_deklarator>
1. provjeri(<init_deklarator>) uz nasljedno svojstvo
<init_deklarator>.ntip ← <lista_init_deklaratora>.ntip
'''
def uvj_207(n:node.Node)->bool:
    if n.vrijednost != "<lista_init_deklaratora>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<init_deklarator>":
        return False
    return True
def prov_207(n:node.Node)->bool:
    n.djeca[0].svojstva["ntip"] = n.svojstva["ntip"]
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_207,
    ["ntip"],
    prov_207
))


'''
<lista_init_deklaratora>1 ::= <lista_init_deklaratora>2 ZAREZ <init_deklarator>
1. provjeri(<lista_init_deklaratora>2) uz nasljedno svojstvo
<lista_init_deklaratora>2.ntip ← <lista_init_deklaratora>1.ntip
2. provjeri(<init_deklarator>) uz nasljedno svojstvo
<init_deklarator>.ntip ← <lista_init_deklaratora>1.ntip
'''
def uvj_208(n:node.Node):
    if n.vrijednost != "<lista_parametara>":
        return False
    elif len(n.djeca) !=3:
        return False
    elif n.djeca[0].vrijednost != "<lista_init_deklaratora>":
        return False
    elif n.djeca[1].vrijednost != "ZAREZ":
        return False
    elif n.djeca[2].vrijednost != "<init_deklarator>":
        return False
    return True
def prov_208(n:node.Node):
    n.djeca[0].svojstva["ntip"] = n.svojstva["ntip"]
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.djeca[2].svojstva["ntip"] = n.svojstva["ntip"]
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_208,
    ["ntip"],
    prov_208
))

'''
<init_deklarator> ::= <izravni_deklarator>
1. provjeri(<izravni_deklarator>) uz nasljedno svojstvo
<izravni_deklarator>.ntip ← <init_deklarator>.ntip
2. <izravni_deklarator>.tip 6= const(T)
i
<izravni_deklarator>.tip 6= niz (const(T))
'''
def uvj_209(n:node.Node)->bool:
    if n.vrijednost != "<init_deklarator>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<izravni_deklarator>":
        return False
    return True
def prov_209(n:node.Node)->bool:
    n.djeca[0].svojstva["ntip"] = n.svojstva["ntip"]
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"].startswith("const") or n.djeca[0].svojstva["tip"].startswith("niz_const"):
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_209,
    ["ntip"],
    prov_209
))


'''
<init_deklarator> ::= <izravni_deklarator> OP_PRIDRUZI <inicijalizator>
1. provjeri(<izravni_deklarator>) uz nasljedno svojstvo
<izravni_deklarator>.ntip ← <init_deklarator>.ntip
2. provjeri(<incijalizator>)
3. ako je <izravni_deklarator>.tip T ili const(T)
<inicijalizator>.tip ∼ T
inaˇce ako je <izravni_deklarator>.tip niz (T) ili niz (const(T))
<inicijalizator>.br-elem ≤ <izravni_deklarator>.br-elem
za svaki U iz <inicijalizator>.tipovi vrijedi U ∼ T
inaˇce greˇska
'''
def uvj_210(n:node.Node)->bool:
    if n.vrijednost != "<init_deklarator>":
        return False
    if len(n.djeca) != 3:
        return False
    if n.djeca[0].vrijednost != "<izravni_deklarator>":
        return False
    if n.djeca[1].vrijednost != "OP_PRIDRUZI":
        return False
    if n.djeca[2].vrijednost != "<inicijalizator>":
        return False
    return True
def prov_210(n:node.Node)->bool:
    n.djeca[0].svojstva["ntip"] = n.svojstva["ntip"]
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"].startswith("niz"):
        if n.djeca[2].svojstva["br-elem"] > n.djeca[0].svojstva["br-elem"]:
            greska(n)
            return False
        for U in n.djeca[2].svojstva["tipovi"]:
            T:str
            if n.djeca[0].svojstva["tip"].startswith("niz_const"):
                T = n.djeca[0].svojstva["tip"].strip("niz_const_")
            else:
                T = n.djeca[0].svojstva["tip"].strip("niz_")
            if not check_impl(U,T):
                greska(n)
                return False
    elif n.djeca[0].svojstva["tip"] in ["char","int","const_char","const_int"]:
        T = n.djeca[0].svojstva["tip"]
        if n.djeca[0].svojstva["tip"].startswith("const"):
            T = T.strip("const_")
        if not check_impl(n.djeca[2].svojstva["tip"],T):
            greska(n)
            return False
    else:
        greska(n)
        return False
    return True
identifikatori.append(Identifikator(
    uvj_210,
    ["ntip"],
    prov_210
))


'''
<izravni_deklarator> ::= IDN
tip ← ntip
1. ntip 6= void
2. IDN.ime nije deklarirano u lokalnom djelokrugu
3. zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom
'''
def uvj_211(n:node.Node)->bool:
    if n.vrijednost != "<izravni_deklarator>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "IDN":
        return False
    return True
def prov_211(n:node.Node)->bool:
    if n.svojstva["ntip"] == "void":
        greska(n)
        return False
    if n.djeca[0].kod in tablica_znakova.content.keys():
        greska(n)
        return False
    tablica_znakova.dodajZnak(n.djeca[0].kod,{
        "tip": n.svojstva["ntip"],
        "l-izraz": 1
    })
    n.svojstva["tip"] = n.svojstva["ntip"]
    return True
identifikatori.append(Identifikator(
    uvj_211,
    ["ntip","tip"],
    prov_211
))

'''
<izravni_deklarator> ::= IDN L_UGL_ZAGRADA BROJ D_UGL_ZAGRADA
tip ← niz (ntip)
br-elem ← BROJ.vrijednost
1. ntip 6= void
2. IDN.ime nije deklarirano u lokalnom djelokrugu
3. BROJ.vrijednost je pozitivan broj (> 0) ne ve´ci od 1024
4. zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom
'''
def uvj_212(n:node.Node)->bool:
    if n.vrijednost != "<izravni_deklarator>":
        return False
    if len(n.djeca) != 4:
        return False
    if n.djeca[0].vrijednost != "IDN":
        return False
    if n.djeca[1].vrijednost != "L_UGL_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "BROJ":
        return False
    if n.djeca[3].vrijednost != "D_UGL_ZAGRADA":
        return False
    return True
def prov_212(n:node.Node)->bool:
    if n.svojstva["ntip"] == "void":
        greska(n)
        return False
    if tablica_znakova.testiraj(n.djeca[0].kod):
        greska(n)
        return False
    try:
        if not (0 < int(n.djeca[2].kod) <= 1024):
            greska(n)
            return False
    except ValueError:
        greska(n)
        return False

    tablica_znakova.dodajZnak(n.djeca[0].kod,{
        "tip": "niz_"+n.svojstva["ntip"],
        "l-izraz": 1
    })
    n.svojstva["tip"] = "niz_"+n.svojstva["ntip"]
    return True
identifikatori.append(Identifikator(
    uvj_212,
    ["ntip","tip"],
    prov_212
))

'''
<izravni_deklarator> ::= IDN L_ZAGRADA KR_VOID D_ZAGRADA
tip ← funkcija(void → ntip)
1. ako je IDN.ime deklarirano u lokalnom djelokrugu, tip prethodne deklaracije
je jednak funkcija(void → ntip)
2. zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom ako ista funkcija ve´c nije
deklarirana u lokalnom djelokrugu
'''
def uvj_213(n:node.Node)->bool:
    if n.vrijednost != "<izravni_deklarator>":
        return False
    if len(n.djeca) != 4:
        return False
    if n.djeca[0].vrijednost != "IDN":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "KR_VOID":
        return False
    if n.djeca[3].vrijednost != "D_ZAGRADA":
        return False
    return True
def prov_213(n:node.Node)->bool:
    if n.djeca[0].kod in tablica_znakova.content.keys():
       if tablica_znakova.content[n.djeca[0].kod]["tip"] != "funkcija void  "+n.svojstva["ntip"]:
           greska(n)
           return False
    else:
        tablica_znakova.dodajZnak(n.djeca[0].kod,{
            "tip": "funkcija void  "+n.svojstva["ntip"],
            "l-izraz": 1
        })
    n.svojstva["tip"]="funkcija void  "+n.svojstva["ntip"]
    return True
identifikatori.append(Identifikator(
    uvj_213,
    ["ntip","tip"],
    prov_213
))


'''
<izravni_deklarator> ::= IDN L_ZAGRADA <lista_parametara> D_ZAGRADA
tip ← funkcija(<lista_parametara>.tipovi → ntip)
1. provjeri(<lista_parametara>)
2. ako je IDN.ime deklarirano u lokalnom djelokrugu, tip prethodne deklaracije
je jednak funkcija(<lista_parametara>.tipovi → ntip)
3. zabiljeˇzi deklaraciju IDN.ime s odgovaraju´cim tipom ako ista funkcija ve´c nije
deklarirana u lokalnom djelokrugu
'''
def uvj_214(n:node.Node)->bool:
    if n.vrijednost != "<izravni_deklarator>":
        return False
    if len(n.djeca) != 4:
        return False
    if n.djeca[0].vrijednost != "IDN":
        return False
    if n.djeca[1].vrijednost != "L_ZAGRADA":
        return False
    if n.djeca[2].vrijednost != "<lista_parametara>":
        return False
    if n.djeca[3].vrijednost != "D_ZAGRADA":
        return False
    return True
def prov_214(n:node.Node)->bool:
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    if n.djeca[0].kod in tablica_znakova.content.keys():
       if tablica_znakova.content[n.djeca[0].kod]["tip"] != "funkcija "+" ".join(n.djeca[2].svojstva["tipovi"])+"  "+n.svojstva["ntip"]:
           greska(n)
           return False
    else:
        tablica_znakova.dodajZnak(n.djeca[0].kod,{
            "tip": "funkcija "+" ".join(n.djeca[2].svojstva["tipovi"])+"  "+n.svojstva["ntip"],
            "l-izraz": 1
        })
    n.svojstva["tip"]="funkcija "+" ".join(n.djeca[2].svojstva["tipovi"])+"  "+n.svojstva["ntip"]
    return True
identifikatori.append(Identifikator(
    uvj_214,
    ["ntip","tip"],
    prov_214
))

'''
TODO - ovo ne znam kako napravit
<inicijalizator> ::= <izraz_pridruzivanja>
ako je <izraz_pridruzivanja> ∗⇒ NIZ_ZNAKOVA
    br-elem ← duljina niza znakova + 1
    tipovi ← lista duljine br-elem, svi elementi su char
inaˇce
    tip ← <izraz_pridruzivanja>.tip
1. provjeri(<izraz_pridruzivanja>)
'''
def uvj_215(n:node.Node)->bool:
    if n.vrijednost != "<inicijalizator>":
        return False
    if len(n.djeca)!=1:
        return False
    if n.djeca[0].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_215(n:node.Node)->bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if n.djeca[0].svojstva["tip"] == "niz_const_char": #je_li_niz(n.djeca[0])
        n.svojstva["br-elem"] = n.djeca[0].svojstva["length"] + 1
        n.svojstva["tipovi"] = ["char" for i in range(n.djeca[0].svojstva["length"] + 1)]
        identifikatori.append(Identifikator(
            uvj_215,
            ["br-elem", "tipovi"],
            prov_215
        ))
    else:
        n.svojstva["tip"] = n.djeca[0].svojstva["tip"]
        identifikatori.append(Identifikator(
            uvj_215,
            ["tip"],
            prov_215
        ))
    #TODO
    return True
identifikatori.append(Identifikator(
    uvj_215,
    ["br-elem", "tipovi","tip"],
    prov_215
))
'''
<inicijalizator> ::= L_VIT_ZAGRADA <lista_izraza_pridruzivanja> D_VIT_ZAGRADA
br-elem ← <lista_izraza_pridruzivanja>.br-elem
tipovi ← <lista_izraza_pridruzivanja>.tipovi
1. provjeri(<lista_izraza_pridruzivanja>)
'''
def uvj_216(n:node.Node) -> bool:
    if n.vrijednost != "<inicijalizator>":
        return False
    if len(n.djeca) != 3:
        return False
    if n.djeca[0].vrijednost != "L_VIT_ZAGRADA":
        return False
    if n.djeca[1].vrijednost != "<izraz_pridruzivanja>":
        return False
    if n.djeca[2].vrijednost != "D_VIT_ZAGRADA":
        return False
    return True
def prov_216(n: node.Node) -> bool:
    if not n.djeca[1].identifikator.provjera(n.djeca[1]):
        greska(n)
        return False
    n.svojstva["tipovi"] = n.djeca[1].svojstva["tipovi"]
    n.svojstva["br-elem"] = n.djeca[1].svojstva["br-elem"]
    return True
identifikatori.append(Identifikator(
    uvj_216,
    [],
    prov_216
))


'''
<lista_izraza_pridruzivanja> ::= <izraz_pridruzivanja>
tipovi ← [ <izraz_pridruzivanja>.tip ]
br-elem ← 1
1. provjeri(<izraz_pridruzivanja>)
'''
def uvj_217(n:node.Node) -> bool:
    if n.vrijednost != "<inicijalizator>":
        return False
    if len(n.djeca) != 1:
        return False
    if n.djeca[0].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_217(n: node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    n.svojstva["tipovi"] = [n.djeca[0].svojstva["tip"]]
    n.svojstva["br-elem"] = 1
    return True
identifikatori.append(Identifikator(
    uvj_217,
    [],
    prov_217
))

'''
<lista_izraza_pridruzivanja> ::= <lista_izraza_pridruzivanja> ZAREZ <izraz_pridruzivanja>
tipovi ← <lista_izraza_pridruzivanja>.tipovi + [ <izraz_pridruzivanja>.tip ]
br-elem ← <lista_izraza_pridruzivanja>.br-elem+ 1
1. provjeri(<lista_izraza_pridruzivanja>)
2. provjeri(<izraz_pridruzivanja>)
'''

def uvj_218(n:node.Node) -> bool:
    if n.vrijednost != "<inicijalizator>":
        return False
    if len(n.djeca) != 2:
        return False
    if n.djeca[0].vrijednost != "<lista_izraza_pridruzivanja>":
        return False
    if n.djeca[0].vrijednost != "ZAREZ":
        return False
    if n.djeca[0].vrijednost != "<izraz_pridruzivanja>":
        return False
    return True
def prov_218(n: node.Node) -> bool:
    if not n.djeca[0].identifikator.provjera(n.djeca[0]):
        greska(n)
        return False
    if not n.djeca[2].identifikator.provjera(n.djeca[2]):
        greska(n)
        return False
    n.svojstva["tipovi"] = n.djeca[0].svojstva["tipovi"] + [n.djeca[2].svojstva["tip"]]
    n.svojstva["br-elem"] = n.djeca[0].svojstva["br-elem"] + 1
    return True
identifikatori.append(Identifikator(
    uvj_218,
    [],
    prov_218
))

def finalna_provjera():
    # 1 provjera
    podaci = tablica_znakova.get_root().testiraj("main")
    if not podaci:
        print("main")
        sys.exit(0)
    if podaci.content["tip"] != "funkcija void  int":
        print("main")
        sys.exit(0)

    # 2 provjera
    root = tablica_znakova.get_root()
    tren
    for key in root.content.keys():
        if root.content[key]["tip"].startswith("funkcija"):
            if "isDefined" in root.content
