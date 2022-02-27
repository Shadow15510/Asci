from asci import *
from random import randint


cartes = (
(r"""
 __                      
/  \___    ###           
|<>    \  #####    _     
|^|____|   ###    / \    
           /_\    |^|    
                         
             __     __ 
        ##  /  \___/  \  ##   
       #### |<>     <>| ####
        ##  |_________|  ##
        ||               ||""",
(1, 3, 1, 5, 7),
(19, 4, 2, 4, 4)),

(r"""
+--+--+--------+--+--+
|  |  |        |  |  |
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/  \--------/  \--+
|                    |
+---|^|--------------+""",
(5, 7, 0, 1, 3)),

(r"""
+-------+
|       |
|       |
|       |
+--|^|--+
""",
(4, 4, 0, 19, 4))
)

entites = (
    ["medecin", "*", 0, 24, 4, "stand by"],
    ["ami", "*", 0, 16, 1, "stand by"],
    ["bandit", "$", 0, 4, 7, "walk", 0, ((4, 7), (3, 7), (3, 6), (4, 6))],
    [0, "*", 1, 5, 5, "stand by"]
)

def pnj(data, stat, entites, identifiant):
    carte_actuelle = data[1]
    xp = data[0]["main"]

    if carte_actuelle == 0:
        if identifiant == "medecin":
            if stat[0] < 100: return [0, "Oh, mais tu es blesse !", 0, (0, 50)]
            else: return [0, "Reviens me voir quand tu seras blesse."]

        elif identifiant == "ami": return {
            "base": [0, "Alors ? T'en sorts-tu ?"],

            0: [0, "J'ai une quete pour toi ! Un ami a moi a des problemes : un personnage louche traine autour de sa maison... Si tu pouvais l'en debarasser, il t'en serai reconnaissant. 1. Je m'en charge ! 2. Trouve quelqu'un d'autre.", 2],
                1: [2, "J'etais sur que je pouvais compter sur toi ! Tiens, voila une dague et une petit bouclier.", 0, (1, 10), (2, 10)],
                2: [3, "Si un jour tu as besoin de moi, tu seras sympa de m'oublier."],

            3: [0, "Alors ? Il est mort ce bandit ?"],
            4: [1, "Merci, tu as rendu un grand service a mon ami !"]
        }

    return [0, "Hmm ?"]


def ennemi(data, stat, entites, identifiant):
    carte_actuelle = data[1]
    coords = data[2], data[3]
    xp = data[0]["main"]

    if carte_actuelle == 0:
        if identifiant == "bandit":
            # Bandit vivant
            if xp == 3:
                if combat(stat, [75, randint(5, 10), randint(5, 10)]):
                    return [1, "Vous avez reussi la quete !"]
            elif xp < 3: return [0, "Qu'est-ce tu regardes toi ? Casses-toi !"]
            else: return [0, "Vous regardez le cadavre froid du bandit."]


def combat(stat, ennemi_stat):
    defense_temporaire = defense_temporaire_ennemi = 0
    while stat[0] > 0 and ennemi_stat[0] > 0:

        print("Vos PV : {0}\nPV ennemi : {1}".format(stat[0], ennemi_stat[0]))
        print("<*> Actions <*>")
        print("1. Attaquer")
        print("2. Defendre")

        action = int(input(">"))

        defense_temporaire = 0
        if action == 1:
            pv = (stat[1] - ennemi_stat[2] - defense_temporaire_ennemi) + randint(-5, 10)
            if pv < 0: pv = 0
            ennemi_stat[0] -= pv
        elif action == 2:
            defense_temporaire = randint(1, 5)

        defense_temporaire_ennemi = 0
        if randint(1, 2) == 1:
            pv = (ennemi_stat[1] - stat[2] - defense_temporaire) + randint(-5, 10)
            if pv < 0: pv = 0
            stat[0] -= pv
        else:
            defense_temporaire_ennemi = randint(1, 5)

    return stat[0] > 0


def affichage_stat(data, stat):
    pv, pa, pd = stat

    print("<*> Statistiques <*>")
    print("Points de vie .: {}".format(pv))
    print("Points attaque : {}".format(pa))
    print("Points defense : {}".format(pd))
    input()

evenements = {"*": pnj, "$": ennemi}
touche = {7: affichage_stat}


def mon_jeu(stat=[100, 0, 0], data=[{"main": 0}, 0, 10, 3]):
    rpg_python = Asci(cartes, entites, evenements, touche)
    stat, data = rpg_python.mainloop(5, stat, data=data)
    print("Pour reprendre :")
    print("mon_jeu({}, {})".format(stat, data))