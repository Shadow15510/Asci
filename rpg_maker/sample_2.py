from asci_lib import *


carte_monde = (
r"""
 _         ###
/o\__     #####
|  <>\     ###  
|____|     /_\

  *


|==|==|==|==|==|==|==|""",)


def dialogue(xp, pv, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5): return {
            0: [0, "Coucou ! Comment ca va ? 1. Ca va, et toi ? 2. Bof... 3. Je t'emmerde.", True],
                1: [3, "Je vais bien, merci !", False],
                2: [3, "Ow, desole...", False],
                3: [4, "He, reviens quand tu sera de meilleure humeur !", False],

            4: [2, "Bon et bien, je crois bien que cette premiere carte s'est bien passee !", False],
            5: [1, "Je vais y aller, appelle moi si tu as besoin ;)", False],
            6: [1, "A pluche o/", False],

            "base": [0, "Oui ?", False]
            }

    return [0, "Hmm ?", False]


def mon_jeu():
    rpg_python = Asci(carte_monde, dialogue, 7, [])
    rpg_python.mainloop()