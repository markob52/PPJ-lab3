
class TablicaZnakova:
    def __init__(self,parent:object=None):
        self.parent = parent
        self.content = {}
    def dodajZnak(self,kljuc, podaci):
        self.content[kljuc] = podaci
    def testiraj(self,kljuc):
        if kljuc in self.content.keys():
            return self.content[kljuc]
        if self.parent:
            return self.parent.testiraj(kljuc)
        return None
    def promjena(self,kljuc,podaci):
        if not self.testiraj(kljuc):
            return False
        tren = self
        while not kljuc in tren.content.keys():
            tren = tren.parent
        tren.content[kljuc] = podaci
        return True
    def otvori_blok(self) -> object:
        return TablicaZnakova(self)
    def zatvori_blok(self) -> object:

        return self.parent

    def get_root(self) -> object:
        tren:TablicaZnakova = self
        while tren.parent:
            tren = tren.parent
        return tren

'''
Upute za korištenje:
    Kada se otvara novi blok:
        tablicaZnakova = tablicaZnakova.otvori_blok()
    Kada se zatvara novi blok:
        tablicaZnakova = tablicaZnakova.zatvori_blok()
    Kada se dodaje deklaracija:
        tablicaZnakova.dodajZnak(deklarirani_znak, podaci_potrebni_iz_deklaracije_u_dictu)
    Kada se testira postoji li znak i ako postoji doći do podataka o njemu:
        podaci = tablicaZnakova.testiraj(znak)
        if not podaci:
            # nije pronadjen
    Promjena podataka:
        podaci = tablicaZnakova.testiraj(znak)
        # promijeni podatke
        tablicaZnakova.promjena(znak,podaci)
'''

