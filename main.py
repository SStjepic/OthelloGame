import time

from OthelloGame import  OthelloGame


if __name__ == '__main__':
    igra = OthelloGame("B")
    x = ""
    while x != "x":
        mogucnosti = igra.potencijalni_potezi(igra.tabla_trenutna(), igra.trenutni_igrac())
        igra.prikazi_tablu(mogucnosti)
        crni, beli = igra.prebroj(igra.tabla_trenutna())
        print("CRNI: "+ str(crni)+", BELI: " + str(beli))

        if len(mogucnosti) == 0:
            print(igra.ima_pobednika(igra.tabla_trenutna()))
            x = "x"
            continue

        for k in mogucnosti:
            print(k + " --> " + mogucnosti[k])

        x = input(">> ")
        if x in mogucnosti.keys():
            red = int(mogucnosti[x][0])
            kolona = int(mogucnosti[x][2])
            igra.postavi_tablu(igra.odigraj_potez(red, kolona,igra.trenutni_igrac(),igra.tabla_trenutna()))
            print("Vaš potez")
            igra.prikazi_tablu({})
            igra.igra_racunar(igra.trenutni_igrac())
            igra.zameni_igraca(igra.trenutni_igrac())
            print("Potez računara")
        else:
            continue