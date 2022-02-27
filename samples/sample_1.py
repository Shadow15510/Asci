from asci import *

exterieur = (r"""
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\
 
   


|==|==|==|==|==|==|==|""",
# Entités
[
    ("sdf", "*", 2, 5, "stand by")
],

# Points de passage
(1, 3, 1, 3, 5))


interieur = (r"""
+----------+
|          |
|          |
|          |
|          |
+-|^|------+
""",
# Entités
[],

# Points de passage
(3, 5, 0, 1, 3))



carte_monde = (exterieur, interieur)


def pnj(data, stat, entites, identifiant):
    xp = data[0]["main"]

    if identifiant == "sdf":
        if xp in (2, 7): entites["sdf"].change_behavior("follow")
        elif xp == 4: entites["sdf"].change_behavior("stand by")
        elif xp == 6:
            entites["sdf"].change_behavior("stand by")
            entites["sdf"].teleport(1, 2, 2)

        return {
            0: [0, "Mon bon monsieur, vous n'auriez pas quelques sous pour moi ?\n1. He non mon brave...\n2. Mais si, bien sur, tenez.", 2],
                1: [5, "Radin !"],
                2: [1, "Merci !", 0, (1, -1)], # 0 réponse possibles, -1 Argent

            3: [0, "Hmm ?\n1.Arretez de me suivre !\n2.Non rien.\n3.Attendez-moi a l'intérieur, j'en ai pour une minute.", 3],
                4: [2, "Soit..."],
                5: [-2, "Bien."],
                6: [1, "Soit."],
            7: [-4, "Je vous suis !"],

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
    rpg_python.mainloop(10, stat=[100, 5], data=[{"main": 0}, 0, 10, 3])
