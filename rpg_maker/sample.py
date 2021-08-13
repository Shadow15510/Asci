from asci_lib import *

maps = (
r"""
 __                      
/  \___    ###  *        
|<>    \  #####    _     
|^|____|   ###    / \    
           /_\    |^|   *
                         
             __     __ 
        ##  /  \___/  \  ##   
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


def get_dialogue(xp, pv, current_map, x, y, stat):
    coords = (x, y)

    if current_map == 0:
        if coords == (16, 1): return {
            0: [1, 0, "Hey, bienvenue dans la map de test d'Asci !", False],
            1: [0, 0, "Comment vas-tu aujourd'hui ? 1. Tres bien, merci ! Et vous-meme ? 2. La ferme le vieux ! ", True],
                2: [4, 0, "Je vais bien ^.^", False],
                3: [0, 0, "Oh, insultant personnage !", False],

            6: [0, 0, "Belle journée, n'est-ce pas ?", False],
            
            "base": [0, 0, "Bonjour, besoin d'aide ?", False],
            }

        elif coords == (24, 4):
            if pv >= 100: return [0, 50, "Tsst, est-ce que je tape sur des gens moi ? Bah alors ? J'ai panse tes plaies, mais fait gaffe a toi...", False]
            else: return [0, 0, "Tu es en pleine forme !", False]

    elif current_map == 1:
        if coords == (4, 3): return {
            3: [0, 0, "Tsst, tu as encore insulte quelqu'un ? 1. Oui... 2. Hein ? Quoi ?", True],
                4: [0, 0, "C'est pas tres malin, tu sais ?", False],
                5: [0, 0, "Je n'aime pas les menteurs. Sort de chez moi.", False],

            "base": [0, 0, "Oui ?", False] 
            }

    return [0, 0, "Hmmm ?", False]
    


def start():
    my_game = Asci(maps, get_dialogue, 10, 0)
    my_game.mainloop()