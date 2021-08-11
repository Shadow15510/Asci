from Asci import *
print("Opus 2 (v1.0b):\n'Le Livre perdu'\nNouvelle partie:\nAsci([30,9,100])\nSinon entrez le code:\nAsci([,,])")
def Asci(liste):
  xp = liste[0]
  carte = liste[1]
  pv = liste[2]
  opus(2)
  liste = main([1,xp, carte, pv, 60])
  if liste[0] > 59:
    print("Quelqu'un a vole le\nlivre sur ordre de\nThyel.\nAvec des complicites\nle livre a ete...")
    input()
    return print("...cache\nchez le 'bourgeois'.\nMais dans quel but ?\nPourquoi un proche du\nRoi vole et cache ce\nlivre sensible ?")
  else:
    return print("Pour reprendre la\npartie entrez le code\nsuivant :\nAsci(",liste,")")