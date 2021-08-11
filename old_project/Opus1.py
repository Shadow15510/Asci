from Asci import *
print("Opus 1 (v1.1b):\n'Le Secret d'Asci'\nNouvelle partie:\nAsci([0,1,100])\nSinon entrez le code:\nAsci([,,])")
def Asci(liste):
    xp = liste[0]
    carte = liste[1]
    pv = liste[2]
    opus(1)
    liste = main([1,xp, carte, pv, 30])
    if liste[0] > 29:
        return print("Tu as trouve le code\n! (15510) Mais les\nennuis arrivent qui\na vole ce livre et\nsurtout pourquoi ?")
    else:
        return print("Pour reprendre la\npartie entrez le code\nsuivant :\nAsci(",liste,")")