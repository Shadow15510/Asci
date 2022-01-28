from asci import *


cartes = (
(r"""
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\

   


|==|==|==|==|==|==|==|""",
[
    (1, "*", 2, 5, "stand by")
],
(1, 3, 1, 5, 7)),

(r"""
+--+--+--------+--+--+
|  |  |        |  |  |
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/  \--------/  \--+
|                    |
+---|^|--------------+""",
[
    ("habitant", "?", 9, 1, "stand by"),
    ("voleur", "?", 20, 1, "stand by")
],
(5, 7, 0, 1, 3))
)


def pnj(data, stat, entites, identifiant):
    carte_actuelle = data[1]
    
    if carte_actuelle == 0:
        if identifiant == 1: return {
            0: [0, "Hey ! J'ai entendu du bruit dans la maison, mais je n'ose pas rentrer... 1. Rien entendu. 2. Je vais jeter un oeil.", 2],
                1: [3, "Etes-vous sourd ?"],
                2: [1, "J'etais sur que vous m'ecouteriez !"],

            3: [2, "C'est la maison juste au nord. Soyez prudent !"],
            4: [0, "Enfin, vous entendez bien du bruit la ? Et si c'etait un voleur ? 1. Bon ok j'y vais. 2. Mais foutez moi la paix !", 2],
                6: [0, "..."],

            5: [0, "Alors ?"],

            10: [1, "J'etais sur d'avoir entendu un truc !"],
            "base": [0, "Vous avez entendu quelque chose ?"]
            }

    elif carte_actuelle == 1:
        if identifiant == "habitant": return {
            5: [0, "Je crois que le voleur est dans la piece d'a cote... 1. Je vais regarder. 2. Debrouillez-vous !", 2],
                6: [2, "Merci !"],
                7: [0, "Pleutre ! Hors de ma vue !"],

            9: [1, "Ah, merci !"],
            "base": [0, "J'ai peur de sortir de cette piece"]
            }

        elif identifiant == "voleur": return {
                8: [1, "Ciel, je suis fait !"],
                9: [0, "Je pars, je pars !"],
                "base": [0, "File avant que je ne te detrousse !"]
            }

    return [0, "Hmm ?"]



def affichage_statistique(data, stat):
    print("Statistiques :")
    print("Points de Vie : {}".format(stat[0]))


evenements = {"?*": pnj}
touche = {8: affichage_statistique}


def mon_jeu():
    rpg_python = Asci(cartes, evenements, touche)
    rpg_python.mainloop(13, [100])