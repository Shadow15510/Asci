from asci_lib import *
from random import randint

maps = (
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
+------------------------------+
|                              |
|                              |
|   *                          |
|                              |
|                              |
+--|^|-------------------------+
""", (1, 3), (4, 6))
)


def get_dialogue(xp, current_map, x, y, stat):
    coords = (x, y)

    if current_map == 0:
        if coords == (16, 1): return {
            0: [1, "Hey, bienvenue dans la map de test d'Asci !", 0],
            1: [0, "Comment vas-tu aujourd'hui ? 1. Tres bien, merci ! Et vous-meme ? 2. La ferme le vieux ! ", 2],
                2: [4, "Je vais bien, merci ! Voici une epee et une cote de maille.", 0, 0, 10, 10],
                3: [0, "Oh, insultant personnage ! Pour la peine tu n'auras rien !", 0],

            6: [1, "Belle journée, n'est-ce pas ? Dommage que ce brigand un peu au sud soit la...", 0],

            8: [0, "Et bien je crois que c'est un test concluant !", 0],
            
            "base": [0, "Bonjour, besoin d'aide ?", 0],
            }

        elif coords == (24, 4):
            if stat[0] < 100: return [0, "Tsst, est-ce que je tape sur des gens moi ? Bah alors ? J'ai panse tes plaies, mais fait gaffe a toi...", 0, 50]
            else: return [0, "Tu es en pleine forme !", 0]

        # 
        elif coords == (4, 7): return {
            6: [2, "Tu as tue le brigand !", 0],
            "base": [0, "Il n'y a rien a faire par ici..."]
        }


    elif current_map == 1:
        if coords == (4, 3): return {
            3: [0, "Tsst, tu as encore insulte quelqu'un ? 1. Oui... 2. Hein ? Quoi ?", 2],
                4: [0, "C'est pas tres malin, tu sais ?", 0],
                5: [0, "Je n'aime pas les menteurs. Sort de chez moi.", 0],

            "base": [0, "Oui ?", False] 
            }

    return [0, "Hmmm ?", False]


def fight(xp, current_map, x, y, stat):
    coords = (x, y)

    if current_map == 0:
        if coords == (4, 7):
            if xp == 6:
                enemy = [75, randint(0, 10), 0]
            else:
                return True

    end = 1
    
    while stat[0] > 0 and enemy[0] > 0:
        player = stat[1] + randint(1, 5)
        adv = enemy[1] + randint(1, 5)

        if player > adv:
            enemy[0] -= (player - enemy[2])
        else:
            stat[0] -= (adv - stat[2])

    return stat[0] > 0



def display_stat(stat):
    print("<*> Statistiques <*>")
    print("Points de vie .: {}".format(stat[0]))
    print("Points attaque : {}".format(stat[1]))
    print("Points defense : {}".format(stat[2]))


def start():
    my_game = Asci(maps, get_dialogue, fight, display_stat, 10, [100, 0, 0])
    my_game.mainloop()