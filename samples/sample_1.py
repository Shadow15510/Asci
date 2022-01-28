from asci import *

monde = (r"""
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\

   


|==|==|==|==|==|==|==|""",
# Entités
{
    "sdf": ["*", 2, 5]
},
# Portes
(1, 3, 1, 5, 7))


maison = (r"""
+--+--+--------+--+--+
|  |  |        |  |  |
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/  \--------/  \--+
|                    |
+---|^|--------------+""",
{},
(5, 7, 0, 1, 3))

carte_monde = (monde, maison)



def pnj(data, stat, identifiant):
    if identifiant == "sdf": return {
        0: [0, "Mon bon monsieur, vous n'auriez pas quelques sous pour moi ?\n1. He non mon brave...\n2. Mais si, bien sur, tenez.", 2],
            1: [6, "Radin !"],
            2: [1, "Merci !", 0, (1, -1)], # 0 réponse possibles, -1 Argent

        3: [0, "Hmm ?\n1. Arretez de me suivre !\n2. Non rien.", 2],
            4: [2, "Soit..."],
            5: [-2, "Bien"],

        "base": [0, "Hmm ?"]
    }

    return [0, "Hmm ?"]


def routine(data, stat):
    if data[0]["main"] == 3:
        if not "sdf" in carte_monde[data[1]][1]: carte_monde[data[1]][1]["sdf"] = ["*", data[2] + 1, data[3]]
        
        if data[4] == 1: carte_monde[data[1]][1]["sdf"] = ["*", data[2] + 1, data[3]]
        elif data[4] == 2: carte_monde[data[1]][1]["sdf"] = ["*", data[2], data[3] - 1]
        elif data[4] == 3: carte_monde[data[1]][1]["sdf"] = ["*", data[2] - 1, data[3]]
        elif data[4] == 5: carte_monde[data[1]][1]["sdf"] = ["*", data[2], data[3] + 1]

    elif data[0]["main"] == 6:
        for i in range(len(carte_monde)):
            if "sdf" in carte_monde[i][1]: carte_monde[i][1].pop("sdf")

        carte_monde[0][1]["sdf"] = ["*", 2, 5]

        data[0]["main"] = 0



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
    rpg_python.mainloop(7, stat=[100, 5], routine=routine)