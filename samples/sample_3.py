from asci_lib import *
from random import randint


cartes = (
r"""
 __                      
/  \___    ###  *        
|<>    \  #####    _     
|^|____|   ###    / \    
           /_\    |^|   *
                         
             __     __ 
    $   ##  /  \___/  \  ##   
       #### |<>     <>| ####
        ##  |___|^|___|  ##
        ||               ||""",

(r"""
+--+--+--------+--+--+
|  |  |        |  |  |
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/ *\--------/  \--+
|                    |
+---|^|--------------+""",
(1, 3), (5, 7)),

(r"""
+-------+
|       |
|       |
|       |
+--|^|--+
""",
(19, 4), (4, 4))
)


def evenements(xp, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (24, 4):
            if stat[0] < 100: return [0, "Oh, mais tu es blesse !", 0, 50]
            else: return [0, "Reviens me voir quand tu seras blesse."]

        elif coords == (16, 1): return {
            "base": [0, "Alors ? T'en sorts-tu ?"],

            0: [0, "J'ai une quete pour toi ! Un ami a moi a des problemes : un personnage louche traine autour de sa maison... Si tu pouvais l'en debarasser, il t'en serai reconnaissant. 1. Je m'en charge ! 2. Trouve quelqu'un d'autre.", 2],
                1: [2, "J'etais sur que je pouvais compter sur toi ! Tiens, voila une dague et une petit bouclier.", 0, 0, 10, 10],
                2: [2, "Si un jour tu as besoin de moi, tu seras sympa de m'oublier."],

            3: [0, "Alors ? Il est mort ce bandit ?"],
            4: [1, "Merci, tu as rendu un grand service a mon ami !"]
        }

        elif coords == (4, 7):
            # Si le bandit vient d'être tué
            if xp == 3: return [1, "Vous avez reussi la quete !"]

            # Si le bandit est encore vivant
            elif xp < 3: return [0, "Qu'est-ce que tu regardes toi ? Casses-toi !"]

            # Si le bandit est déjà mort
            else: return [0, "Vous regardez le cadavre froid du bandit."]

    return [0, "Hmm ?"]


def combats(xp, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (4, 7):
            if xp == 3: ennemi_stat = [75, randint(5, 10), randint(5, 10)]
            else: return True

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


def affichage_stat(stat):
    pv, pa, pd = stat

    print("<*> Statistiques <*>")
    print("Points de vie .: {}".format(pv))
    print("Points attaque : {}".format(pa))
    print("Points defense : {}".format(pd))


def custom(stat):
    pass


def mon_jeu(stat=[100, 0, 0], data=[0, 0, 0, 0]):
    rpg_python = Asci(cartes, evenements, combats, affichage_stat, custom 5, stat, data)
    stat, data = rpg_python.mainloop()
    print("Pour reprendre :")
    print("mon_jeu({}, {})".format(stat, data))