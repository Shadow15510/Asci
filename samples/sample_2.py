from asci_lib import *


cartes = (
r"""
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\

  *


|==|==|==|==|==|==|==|""",

(r"""
+--+--+--------+--+--+
|  |  |  *     |  | *|
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/  \--------/  \--+
|                    |
+---|^|--------------+""",
(1, 3), (5, 7))
)


def evenements(xp, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5): return {
            0: [0, "Hey ! J'ai entendu du bruit dans la maison, mais je n'ose pas rentrer... 1. Rien entendu. 2. Je vais jeter un oeil.", 2],
                1: [3, "Etes-vous sourd ?"],
                2: [1, "J'etais sur que vous m'ecouteriez !"],

            3: [2, "C'est la maison juste au nord."],
            4: [0, "Enfin, vous entendez bien du bruit la ? Et si c'etait un voleur ? 1. Bon ok j'y vais. 2. Mais foutez moi la paix !", 2],
                6: [0, "..."],

            5: [2, "Soyez prudent !"],

            12: [1, "J'etais sur d'avoir entendu un truc !"],
            "base": [0, "Vous avez entendu quelque chose ?"]
            }

    elif carte_actuelle == 1:
        if coords == (9, 1): return {
            7: [0, "Je crois que le voleur est dans la piece d'a cote... 1. Je vais regarder. 2. Debrouillez-vous !", 2],
                8: [2, "Merci !"],
                9: [0, "Pleutre ! Hors de ma vue !"],

            11: [1, "Ah, merci !"],
            "base": [0, "J'ai peur de sortir de cette piece"]
            }

        elif coords == (20, 1): return {
                10: [1, "Ciel, je suis fait !"],
                "base": [0, "File avant que je ne te detrousse !"]
            }

    return [0, "Hmm ?"]


def combat(xp, carte_actuelle, x, y, stat):
    pass

def affichage_statistique(stat):
    print("Statistiques :")
    print("Points de Vie : {}".format(stat[0]))


def custom(stat):
    pass


def mon_jeu():
    rpg_python = Asci(cartes, evenements, combat, affichage_statistique, custom, 13, [100])
    rpg_python.mainloop()