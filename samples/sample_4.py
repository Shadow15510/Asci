from asci import *


cartes = (
(r"""
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\

  ?


|==|==|==|==|==|==|==|""",
(1, 3, 1, 5, 7)),

(r"""
+--+--+--------+--+--+
|  |  |  ?     |  | ?|
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/  \--------/  \--+
|                    |
+---|^|--------------+""",
(5, 7, 0, 1, 3))
)


def pnj(data, stat):
    xp, carte_actuelle, x, y = data
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5):
            # Si les deux quêtes annexes sont terminées, on incrémente la quête principale
            if "pain" in xp and "journal" in xp and xp["pain"] == 3 and xp["journal"] == 3:
                data[0]["main"] += 1

            # Si le joueur accepte la quête, on initialise les deux quêtes annexes
            if xp["main"] == 1:
                data[0]["pain"] = 1
                data[0]["journal"] = 1
                return [2, "Tu es un ange !"] # data[0]["main"] = 3

            elif "pain" in xp and xp["pain"] == 2: return "pain", [1, "Ah merci pour le pain."] # Si joueur a été chercher le pain
            elif "journal" in xp and xp["journal"] == 2: return "journal", [1, "Aha enfin de la lecture !"]  # Si le joueur a été chercher le journal

            else:
                return {
                    0: [0, "J'ai que tu ailles m'acheter un journal et du pain.\n1. J'y vais m'sieur !\n2. Humm... Non.", 2],
                    2: [-2, "Vilain garnement !"], # Si le joueur refuse la quête
                    3: [0, "Alors ? J'attend moi !"], # Si le joueur a accepté la quête, mais n'a été cherché ni le pain, ni le journal
                    4: [1, "Merci, pour ces commissions !"] # Si le joueur a terminé la quête
                }


    elif carte_actuelle == 1:
        if coords == (9, 1):
            if "pain" in xp and xp["pain"] == 1: return "pain", [1, "Tient voila pour toi ! [+PAIN]"]
            else: return [0, "Je suis boulanger mon jeune ami !"]

        elif coords == (20, 1):
            if "journal" in xp and xp["journal"] == 1: return "journal", [1, "Voila ton journal"]
            else: return [0, "Ce kiosque est dans la famille depuis plusieurs générations !"]


    return [0, "Hmm ?"]



def affichage_statistique(data, stat):
    print("Statistiques :")
    print("Points de Vie : {}".format(stat[0]))


evenements = {"?*": pnj}
touche = {8: affichage_statistique}


def mon_jeu():
    rpg_python = Asci(cartes, evenements, touche)
    stat, data = rpg_python.mainloop(5, [100])
    print(stat, data)