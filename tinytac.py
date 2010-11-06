# -*- coding: latin-1 -*-

import operator, sys, random, time

def alleGleich(list):
    """liefert TRUE , wenn alle Elemente einer Liste sind gleich, oder wenn die Liste ist leer."""
    return not list or list == [list[0]] * len(list)

Leere = ' '
Spieler_X = 'x'
Spieler_O = 'o'

class Brett:
    """Diese Klasse stellt einen TinyTac Brett Zustand."""
    def __init__(self):
        """Initialisieren aller Mitglieder."""
        self.stucke = [Leere]*4
        self.feldnamen = '1234'

    def ausgang(self):
        """Zeigen Sie das Brett auf dem Bildschirm.."""
        for zeile in [self.stucke[0:2], self.stucke[2:]]:
            print ' '.join(zeile)

    def gewinner(self):
        """Bestimmen Sie, ob ein Spieler das Spiel gewonnen hat. Gibt Spieler_X, Spieler_O oder None"""
        gewinnerReihen = [[0,1],[2,3], # vertical
                        [0,2],[1,3], # horizontal
                        [0,3],[1,2]]         # diagonal
        for reihe in gewinnerReihen:
            if self.stucke[reihe[0]] != Leere and alleGleich([self.stucke[i] for i in reihe]):
                return self.stucke[reihe[0]]

    def bekommenGultigBewegt(self):
        """Gibt eine Liste von g�ltigen bewegt. Ein Umzug kann �bergeben werden sieBewegenNamen abrufen eines lesbaren Namen oder machen bewegen / r�ckg�ngig zu bewegen es zu spielen."""
        return [standpunkt for standpunkt in range(4) if self.stucke[standpunkt] == Leere]

    def spielEndete(self):
        """Liefert true, wenn ein Spieler gewonnen hat oder wenn es keine g�ltige bewegt sich nach links."""
        return self.gewinner() or not self.bekommenGultigBewegt()

    def bewegenNamen(self, bewegen):
        """Gibt einen lesbaren Namen f�r einen Umzug"""
        return self.feldnamen[bewegen]
    
    def machenBewegen(self, bewegen, spieler):
        """Spielt eine zu bewegen. Hinweis: Dieser �berpr�ft nicht, ob der Umzug ist legal!"""
        self.stucke[bewegen] = spieler
    
    def ruckgangigZuBewegen(self, bewegen):
        """Widerruft ein Schritt / l�scht ein St�ck der Platte."""
        self.machenBewegen(bewegen, Leere)

def menschSpieler(brett, spieler):
    """Funktion f�r den menschlichen Spieler"""
    brett.ausgang()
    moglichen_zuge = dict([(brett.bewegenNamen(bewegen), bewegen) for bewegen in brett.bekommenGultigBewegt()])
    bewegen = raw_input("Geben Sie Ihren Umzug (%s): " % (', '.join(sorted(moglichen_zuge))))
    while bewegen not in moglichen_zuge:
        print "Sorry, '%s' ist keine g�ltige bewegen. Bitte versuchen Sie es erneut." % bewegen
        bewegen = raw_input("Geben Sie Ihren Umzug (%s): " % (', '.join(sorted(moglichen_zuge))))
    brett.machenBewegen(moglichen_zuge[bewegen], spieler)

def computerSpieler(brett, spieler):
    """Funktion f�r die Computer-Spieler"""
    t0 = time.time()
    brett.ausgang()
    britisher = { Spieler_O : Spieler_X, Spieler_X : Spieler_O }

    def judge(gewinner):
        if gewinner == spieler:
            return +1
        if gewinner == None:
            return 0
        return -1

    def bewegenBewerten(bewegen, p=spieler):
        try:
            brett.machenBewegen(bewegen, p)
            if brett.spielEndete():
                return judge(brett.gewinner())
            ergebnisse = (bewegenBewerten(nachstenZug, britisher[p]) for nachstenZug in brett.bekommenGultigBewegt())

            if p == spieler:
                #return min(ergebnisse)
                minimale_element = 1
                for o in ergebnisse:
                    if o == -1:
                        return o
                    minimale_element = min(o,minimale_element)
                return minimale_element
            else:
                #return max(ergebnisse)
                maximale_element = -1
                for o in ergebnisse:
                    if o == +1:
                        return o
                    maximale_element = max(o,mmaximale_element)
                return maximale_element

        finally:
            brett.ruckgangigZuBewegen(bewegen)

    bewegenen = [(bewegen, bewegenBewerten(bewegen)) for bewegen in brett.bekommenGultigBewegt()]
    random.shuffle(bewegenen)
    bewegenen.sort(key = lambda (bewegen, gewinner): gewinner)
    brett.machenBewegen(bewegenen[-1][0], spieler)

def spiel():
    """Das Spiel Funktion"""
    b = Brett()
    reihe = 1
    while True:
        print "%i. reihe" % reihe
        computerSpieler(b, Spieler_X)
        if b.spielEndete(): 
            break
        menschSpieler(b, Spieler_O)
        if b.spielEndete(): 
            break
        reihe += 1

    b.ausgang()
    if b.gewinner():
        print 'Computer Spieler gewinnt!'
    else:
        print 'Das Spiel endet.'

if __name__ == "__main__":
    spiel()

