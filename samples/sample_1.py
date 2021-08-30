from asci_lib import *

carte_monde = (
r"""
 _         ###
/o\__     #####
|  <>\     ###  
|____|     /_\

  *


|==|==|==|==|==|==|==|""",)


def pnj(data, stat):
    xp, carte_actuelle, x, y = data
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5): return {
            0: [0, "Mon bon monsieur, vous n'auriez pas quelques sous pour moi ? 1. He non mon brave... 2. Mais si, bien sur, tenez.", 2],
                1: [2, "Radin !"],
                # 0 réponse possibles, -1 Argent
                2: [1, "Merci !", 0, (0, -1)],

            "base": [0, "Hmm ?"]
        }

    return [0, "Hmm ?"]




def affichage_stat(data, stat):
    pv, argent = stat
    print("Statistiques")
    print("PV : {}".format(pv))
    print("Argent : {}".format(argent))
    input()


evenements = {"*": pnj}
touche = {6: affichage_stat}


def mon_jeu():
    rpg_python = Asci(carte_monde, evenements, touche)
    rpg_python.mainloop(4, [100, 5])