import copy


class OthelloGame(object):
    def __init__(self, figura):
        self._tabla = [[" " for polje in range(8)] for polje in range(8)]
        self._tabla[3][3] = "B"
        self._tabla[4][4] = "B"
        self._tabla[3][4] = "W"
        self._tabla[4][3] = "W"
        self._figura = figura

    def prikazi_tablu(self, mogucnosti):
        print("  0 1 2 3 4 5 6 7")
        for potez in mogucnosti.keys():
            self._tabla[int(mogucnosti[potez][0])][int(mogucnosti[potez][2])] = potez
        for i in range(8):
            print(str(i)+"|" + "|".join(self._tabla[i])+"|")
        for potez in mogucnosti.keys():
            self._tabla[int(mogucnosti[potez][0])][int(mogucnosti[potez][2])] = " "

    def potencijalni_potezi(self,tabla, igrac):
        brojac = 1
        moguci_potezi = {}
        for i in range(8):
            for j in range(8):
                if self.provera_poteza(i, j,igrac, tabla):
                    if str(i) + " " + str(j) in moguci_potezi.values():
                        continue
                    else:
                        moguci_potezi[str(brojac)] = str(i) + " " + str(j)
                        brojac += 1
        return moguci_potezi

    def provera_poteza(self, red, kolona, igrac, tabla):
        smer_kretanja = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        if tabla[red][kolona] != " ":
            return False
        for smer in smer_kretanja:
            pot_red = red + smer[0]
            pot_kolona = kolona + smer[1]
            # provera ide sve dok je posmatrano polje unutar opsega table i dok je posmatrano polje jednako protivnickom
            if pot_red >= 0 and pot_red  < 8 and pot_kolona >=0 and pot_kolona < 8 and tabla[pot_red][pot_kolona] == self.protivnicka_figura(igrac):
                while pot_red >= 0 and pot_red  < 8 and pot_kolona >=0 and pot_kolona < 8 and tabla[pot_red][pot_kolona] == self.protivnicka_figura(igrac):
                    # smer kretanja je potencijalno dobar
                    pot_red = pot_red + smer[0]
                    pot_kolona = pot_kolona + smer[1]
                if pot_red >= 0 and pot_red  < 8 and pot_kolona >=0 and pot_kolona < 8 and tabla[pot_red][pot_kolona] == igrac:
                    # smer kretanja je dabr, posmatrano polje je validno
                    return True
        return False


    def odigraj_potez(self, red, kolona, igrac, tabla):
        nova_tabla = copy.deepcopy(tabla)
        nova_tabla[red][kolona] = igrac

        smer_kretanja = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for smer in smer_kretanja:
            pot_red = red + smer[0]
            pot_kolona = kolona + smer[1]
            # provera ide sve dok je posmatrano polje unutar opsega table i dok je posmatrano polje jednako protivnickom
            while pot_red >= 0 and pot_red  < 8 and pot_kolona >=0 and pot_kolona < 8 and nova_tabla[pot_red][pot_kolona] == self.protivnicka_figura(igrac):
                pot_red = pot_red + smer[0]
                pot_kolona = pot_kolona + smer[1]
                if pot_red >= 0 and pot_red  < 8 and pot_kolona >=0 and pot_kolona < 8 and nova_tabla[pot_red][pot_kolona] == igrac:
                    # smer kretanja je dobar
                    pot_red = pot_red - smer[0]
                    pot_kolona = pot_kolona - smer[1]
                    while  pot_red >= 0 and pot_red < 8 and pot_kolona >=0 and pot_kolona < 8 and nova_tabla[pot_red][pot_kolona] == self.protivnicka_figura(igrac):
                        # vraca je unazad i menja figure
                        nova_tabla[pot_red][pot_kolona] = igrac
                        pot_red = pot_red - smer[0]
                        pot_kolona = pot_kolona - smer[1]

        return nova_tabla

    def postavi_tablu(self, tabla):
        self._tabla = tabla
        self.zameni_igraca(self._figura)

    def zameni_igraca(self,igrac):
        self._figura = self.protivnicka_figura(igrac)

    def protivnicka_figura(self, igrac):
        if igrac == "B":
            return "W"
        return "B"

    def prebroj(self, tabla):
        brojBelih = 0
        brojCrnih = 0
        for i in range(8):
            for j in range(8):
                if tabla[i][j] == "B":
                    brojCrnih += 1
                elif tabla[i][j] == "W":
                    brojBelih += 1
        return brojCrnih, brojBelih

    def ima_pobednika(self, tabla):
        brojCrnih, brojBelih = self.prebroj(tabla)
        if brojBelih > brojCrnih:
            return 'Pobedio je beli (W)'
        elif brojBelih < brojCrnih:
            return 'Pobedio je crni (B)'
        else:
            return "Nereseno"


    def vrednost_table(self, tabla, igrac):

        bodovi = [[20, -3, 11, 8, 8, 11, -3, 20],
                  [-3, -7, -4, 1, 1, -4, -7, -3],
                  [11, -4, 2, 2, 2, 2, -4, 11],
                  [8, 1, 2, -3, -3, 2, 1, 8 ],
                  [8, 1, 2, -3, -3, 2, 1, 8 ],
                  [11, -4, 2, 2, 2, 2, -4, 11],
                  [-3, -7, -4, 1, 1, -4, -7, -3],
                  [20, -3, 11, 8, 8, 11, -3, 20]]
        moji_bodovi = 0
        protivnicki_bodovi = 0
        moje_figure = 0
        protivnicke_figure = 0
        for i in range(8):
            for j in range(8):
                if tabla[i][j] == igrac:
                    moji_bodovi += bodovi[i][j]
                    moje_figure += 1
                elif tabla[i][j] != " ":
                    protivnicki_bodovi += bodovi[i][j]
                    protivnicke_figure += 1

        bodovi_tabla = moji_bodovi - protivnicki_bodovi
        bodovi_figure = 0
        if moje_figure>protivnicke_figure:
            bodovi_figure = (100*moje_figure)/(moje_figure + protivnicke_figure)
        elif moje_figure < protivnicke_figure:
            bodovi_figure= -1* (100 * moje_figure) / (moje_figure + protivnicke_figure)

        moji_bodovi = 0
        protivnicki_bodovi = 0
        if tabla[0][7] == igrac:
            moji_bodovi += 1
        elif tabla[0][7] != " ":
            protivnicki_bodovi += 1
        if tabla[7][7] == igrac:
            moji_bodovi += 1
        elif tabla[7][7] != " ":
            protivnicki_bodovi += 1
        if tabla[0][0] == igrac:
            moji_bodovi += 1
        elif tabla[0][0] != " ":
            protivnicki_bodovi += 1
        if tabla[7][0] == igrac:
            moji_bodovi += 1
        elif tabla[7][0] != " ":
            protivnicki_bodovi += 1
        bodovi_uglovi = 25 *(moji_bodovi-protivnicki_bodovi)

        moji_bodovi = 0
        protivnicki_bodovi = 0
        if tabla[0][0] == " ":
            if tabla[0][1] == igrac:
                moji_bodovi += 1
            elif tabla[0][1] != " ":
                protivnicki_bodovi += 1
            if tabla[1][1] == igrac:
                moji_bodovi += 1
            elif tabla[1][1] != " ":
                protivnicki_bodovi += 1
            if tabla[1][0] == igrac:
                moji_bodovi += 1
            elif tabla[1][0] != " ":
                protivnicki_bodovi += 1
        if tabla[0][7] == " ":
            if tabla[0][6] == igrac:
                moji_bodovi += 1
            elif tabla[0][6] != " ":
                protivnicki_bodovi += 1
            if tabla[1][6] == igrac:
                moji_bodovi += 1
            elif tabla[1][6] != " ":
                protivnicki_bodovi += 1
            if tabla[1][7] == igrac:
                moji_bodovi += 1
            elif tabla[1][7] != " ":
                protivnicki_bodovi += 1
        if tabla[7][0] == " ":
            if tabla[6][0] == igrac:
                moji_bodovi += 1
            elif tabla[6][0] != " ":
                protivnicki_bodovi += 1
            if tabla[7][1] == igrac:
                moji_bodovi += 1
            elif tabla[7][1] != " ":
                protivnicki_bodovi += 1
            if tabla[6][1] == igrac:
                moji_bodovi += 1
            elif tabla[6][1] != " ":
                protivnicki_bodovi += 1
        if tabla[7][7] == " ":
            if tabla[7][6] == igrac:
                moji_bodovi += 1
            elif tabla[7][6] != " ":
                protivnicki_bodovi += 1
            if tabla[6][6] == igrac:
                moji_bodovi += 1
            elif tabla[6][6] != " ":
                protivnicki_bodovi += 1
            if tabla[6][7] == igrac:
                moji_bodovi += 1
            elif tabla[6][7] != " ":
                protivnicki_bodovi += 1
        bodovi_blizina_uglova = -12*(moji_bodovi-protivnicki_bodovi)

        moji_bodovi = len(self.potencijalni_potezi(tabla, igrac))
        protivnicki_bodovi = len(self.potencijalni_potezi(tabla, igrac))
        if (moji_bodovi - protivnicki_bodovi) != 0:
            bodovi_moguci_potezi = (100*moji_bodovi)/(moji_bodovi+protivnicki_bodovi)
            if moji_bodovi < protivnicki_bodovi:
                bodovi_moguci_potezi *= -1
        else:
            bodovi_moguci_potezi = 0

        return (10 * bodovi_figure) + (382 * bodovi_blizina_uglova) + (78 * bodovi_moguci_potezi) + (800 * bodovi_uglovi) + (10*bodovi_tabla)

    def igra_racunar(self, igrac):
        tabla = copy.deepcopy(self._tabla)
        mogucnosti = self.potencijalni_potezi(tabla, igrac)
        najbolja_opcija = None
        najbolji_skor = float('-inf')
        broj_poteza = 5
        if len(mogucnosti.keys()) < 4:
            broj_poteza = 6
        if len(mogucnosti.keys()) > 13:
            broj_poteza = 4
        for potez in mogucnosti.values():
            nova_tabla = self.odigraj_potez(int(potez[0]), int(potez[2]), igrac, tabla)
            skor = self.minimax(nova_tabla, broj_poteza-1, self._figura, float('-inf'), float('inf'), False)
            if skor > najbolji_skor:
                najbolji_skor = skor
                najbolja_opcija = potez
        if najbolja_opcija != None:
            red = int(najbolja_opcija[0])
            kolona = int(najbolja_opcija[2])
            self._tabla = self.odigraj_potez(red, kolona, igrac, self._tabla)

    def minimax(self, tabla, dubina, igrac, alfa_rez, beta_rez, maksimajzer: bool):
        if dubina == 0:
            return self.vrednost_table(tabla, igrac)

        potezi = self.potencijalni_potezi(tabla, igrac)
        if maksimajzer:
            maksimum = float('-inf')
            for potez in potezi.values():
                nova_tabla = self.odigraj_potez(int(potez[0]), int(potez[2]), igrac, tabla)
                bodovi = self.minimax(nova_tabla, dubina - 1, igrac, alfa_rez, beta_rez, False)
                maksimum = max(maksimum, bodovi)
                alfa_rez = max(alfa_rez, bodovi)
                if beta_rez <= alfa_rez:
                    break
            return maksimum
        else:
            minimum = float('inf')
            protivnik = self.protivnicka_figura(igrac)
            potezi = self.potencijalni_potezi(tabla, protivnik)
            for potez in potezi.values():
                nova_tabla = self.odigraj_potez(int(potez[0]), int(potez[2]), protivnik, tabla)
                bodovi = self.minimax(nova_tabla, dubina - 1, igrac, alfa_rez, beta_rez, True)
                minimum = min(minimum, bodovi)
                beta_rez = min(beta_rez, bodovi)
                if beta_rez <= alfa_rez:
                    break
            return minimum

    def tabla_trenutna(self):
        return self._tabla

    def trenutni_igrac(self):
        return self._figura


