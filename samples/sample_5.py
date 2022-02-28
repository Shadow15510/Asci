from asci import *

exterieur = (r"""
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\ 
 
                  


|==|==|==|==|==|==|==|""",
# Points de passage
(1, 3, 1, 3, 5))


interieur = (r"""
+----------+
|          |
|          |
|          |
|          |
+-|^|------+""",
# Points de passage
(3, 5, 0, 1, 3))


carte_monde = (exterieur, interieur)
entites = (
    ["pnj", "*", 0, 2, 5, "stand by"],
)


def pnj(data, stat, entites, identifiant):
    xp = data[0]["main"]

    if identifiant == "pnj":
        if xp == 1:
            entites["pnj"].change_behavior("follow by player")
            entites["pnj"].args = [0, ((3, 5), (16, 5), (16, 2))]

        return {
        "base": [0, "Moui ?"],
        0: [0, "Tu me suis ?\n1.Oui\n2.Non", 2],
        1: [2, "Parfait ! C'est parti !"],
        2: [-2, "Rhoo alleezz..."],

        3: [1, "Hehe"]
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
    rpg_python = Asci(carte_monde, entites, evenements, touche)
    rpg_python.mainloop(10, stat=[100, 5], data=[{"main": 0}, 0, 10, 3])
