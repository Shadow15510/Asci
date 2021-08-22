from asci_lib import *

carte_monde = (
r"""
 _         ###
/o\__     #####
|  <>\     ###  
|____|     /_\

  *


|==|==|==|==|==|==|==|""",)


def evenements(xp, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5): return {
            0: [0, "Mon bon monsieur, vous n'auriez pas quelques sous pour moi ? 1. He non mon brave... 2. Mais si, bien sur, tenez.", 2],
                1: [2, "Radin !"],
                # 0 réponse possibles, +0 PV, -1 Argent
                2: [1, "Merci !", 0, 0, -1],

            "base": [0, "Hmm ?"]
        }

    return [0, "Hmm ?"]


def combat(xp, carte_actuelle, x, y, stat): 
    pass


def affichage_stat(stat):
    pv, argent = stat
    print("Statistiques")
    print("PV : {}".format(pv))
    print("Argent : {}".format(argent))

def custom(xp, carte_actuelle, x, y, stat):
    pass


def mon_jeu():
    rpg_python = Asci(carte_monde, evenements, combat, affichage_stat, custom)
    rpg_python.mainloop(4, [100, 5])