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
|                              |
|                              |
|                              |
|                              |
|                              |
|                              |
|                              |
|                              |
+--|^|-------------------------+
""", (1, 4), (4, 10))
)



# line - 1 ; column - 1

# 4; 1

dialogue = {
    "base": [0, "Hmmm ?", False],

    "16:2": {
        0: [1, "Hey, bienvenue dans la map de test d'Asci !", False],
        1: [0, "Comment vas-tu aujourd'hui ? 1. Très bien, merci ! Et vous-même ? 2. La ferme le vieux ! ", True],
            2: [2, "Je vais bien ^.^", False],
            3: [0, "Oh, insultant personnage !", False],

        4: [0, "Belle journée, n'est-ce pas ?", False],
        "base": [0, "Bonjour, besoin d'aide ?", False],
    }
}

def start():
    my_game = Asci(maps, dialogue, 10, 0)
    my_game.mainloop()