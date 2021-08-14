# Asci

## Présentation

### Le projet

À l'origine, Asci est un jeu de rôle en Python pour Graph 90. Le jeu est aujourd'hui accompagné d'un moteur pour que vous puissiez réaliser vos jeux de rôles en Python avec un minimum d'effort.

### Principe

Le moteur repose sur l'évolution de points d'expérience pour déterminer votre avancée dans le jeu. Ces points d'expériences sont donnés au joueur à l'issu d'évènements.

### Licence

Tout le projet est soumis à la licence GNU General Public Licence v3.0.

## Utilisation

### Les statistiques

Les statistiques sont une liste de variables dont le premier élément est nécessairement les points de vie. Cette liste est donnée au moteur lors de l'initialisation, néanmoins, le moteur ne *modifie en aucun cas* cette variable. Il la stocke pour vous et la modifie sur votre demande, lors des évènements. Il s'agit donc d'une variable maîtresse dans les mécaniques de votre jeu.

Les statistiques ne peuvent être modifées que lors d'évènements. Comme vous le verrez dans la suite, les évènements sont des listes dont les derniers éléments ne sont pas déterminés : il s'agit des points que vous pouvez ajouter ou enlever à vos statistiques.

### Structure du programme

Votre jeu va se diviser en grandes partie :
 - création de la carte
 - création des évènements
 - gestion des combats
 - affichage des statistiques
 - finalisation

Vous aurez à plusieurs reprise des fonctions à programmer, ces fonctions auront accès à des variables du moteurs, elles sont toutes en lecture seule, exceptée les statistiques qui peuvent être modifiée par effet de bord. 

#### Création de la carte

Vous allez devoir créer une carte du monde, mais aussi les intérieurs des maisons. Pour cela vous allez avoir besoin d'un tuple qui va devoir remplir quelques conditions :
 - toutes les cartes sont des r-docstrings `r""" ... """`
 - le premier élément du tuple est la carte du monde
 - les autres éléments sont eux-même des tuples de la forme : `(carte, (x_entree, y_entree), (x_sortie, y_sortie))` où `(x_entree, y_entree)` sont les coordonnées de la porte de la maison *dans la carte du monde* et où `(x_sortie, y_sortie)` sont les coordonnées de la porte de la maison *dans la carte de la maison*

#### Création des évènements

Les évènements sont des listes formatées qui ont cette forme : `[xp_gagnee, "Texte de l'évènement", nb, ...]`.
 - `xp_gagnee` : correspond à l'expérience que le joueur gagne lors de l'évènement.
 - le texte est ce qui est affiché à l'écran lors de l'évènement.
 - `nb` : est une variable utilisée lors de dialogues. C'est une manipulation un peu plus délicate sur laquelle je reviens juste après.
 - les `...` correspondent à des modificateurs sur les statistiques. J'y reviendrais également.

Les dialogues permettent au joueur de choisir sa réponse. Si le joueur ne peux pas choisir de réponse, mettez `nb` à 0, sinon mettez `nb` sur le nombre de réponse possible. Les différentes réponses sont à afficher avec un numéro dans le corps du message. Par exemple : `[0, "Ceci est une question ? 1.Première réponse. 2.Seconde réponse.", 2]`. Le numéro de la question correspond alors au nombre de points d'expérience gagnée par le joueur (il est, de se fait, conseillé de ne pas donner de points d'expérience au joueur lors d'un dialogue). Si il n'y a pas de réponses possible, vous pouvez omettre cet argument. Attention, cette astuce n'est valable que si vous ne comptez pas modifier les statistiques.

Ces évènements sont stockés dans des dictionnaires dont les clefs correspondent aux points d'expériences, c'est peut-être pas très clair, mais avec un exemple, ça ira mieux.

Par simplicité, j'utiliserai un dictionnaire par PnJ, vous faites bien comme vous voulez, du moment que vous obtenez un truc qui marche… Ces dictionnaires d'évènements doivent être placés dans une fonction qui doit respecter certaines règles :
 - la fonction doit prendre en argument l'expérience, l'id de la map actuelle (qui correspond à son index dans el tuple des maps), les coordonnées du joueur et les statistiques
 - la fonction doit renvoyer un dictionnaire d'évènement ou un évènement.

Concrètement, votre fonction va ressembler à :
```
def evenement(xp, carte_actuelle, x, y, stat):
    coords = (x, y)

    # Si on est en extérieur
    if carte_actuelle == 0:
        if coords == (X1, Y1): return {
            xp_1: [...],
            xp_2: [...],
            ...
            "base": [...]
            }

        elif coords == (X2, Y2): return ...
    
    # Si on est dans la première maison
    elif carte_actuelle == 1:
        ...

    # Si on a pas encore renvoyé d'évènement, il faut prévoir un "cas par défaut"
    return [0, "Hmm ?"]
```
Les tests conditionnels testent quel PnJ le joueur regarde (sur quelle carte, et à quelles coordonnées).

Ici, on voit peut-être un peu mieux le fonctionnement : les clefs du dictionnaires d'évènements correspondent à des points d'expérience : si le joueur à `xp_1` points d'expérience, alors c'est ce dialogue là qui sera lu, et si aucun évènement ne correspond, mais que le PnJ a quand même un texte à dire à un moment, l'évènement `"base"` sera lu.

Cette fonction est appelée lors d'un dialogue avec un PnJ, mais aussi à l'issue d'un combat, si le joueur est vainqueur. Le principe reste le même.

#### Gestion des combats

Vous êtes (presque) totalement libre ! Votre fonction doit respecter quelques points :
 - la fonction, comme pour les évènements, doit prendre en argument l'expérience, le numéro de la carte, les coordonnées du joueur et les statistiques. (vous pouvez toujours objecter que ça fait beaucoup de variables, mais ça peut servir)
 - la fonction doit retourner un booleen égal à `True` si le joueur a gagné, `False` sinon.

Vous devriez avoir une fonction qui ressemble un peu à ça :
```
def combats(xp, carte_actuelle, x, y, stat):
    ...
    return stat[0] > 0
```

#### Affichage des statistiques

La fonction est assez triviale :
 - la fonction devra prendre en argument la liste des statistiques (les points d'expérience, au sens du moteur, sont considérés comme ne faisant pas partie des statistiques)
 - la fonction devra afficher elle-même les statistiques.

Vous aurez une fonction qui va ressembler ainsi à quelque chose comme :
```
def affichage_stat(stat):
    print("<*> Statistiques <*>")
    print("Points de vie .: {}".format(stat[0]))
```

#### Finalisation

Il ne reste plus qu'à faire une petite fonction de nom du votre jeu qui va créer un modèle vierge de jeu rôle et qui va transmettre toutes ces données au modèle. Il vous restera ensuite à lancer cette fonction pour jouer.

Cette fonction devra prendre dans l'ordre : 
 - le tuple des cartes
 - la fonction des évènements
 - la fonction des combats
 - la fonction d'affichages des statistiques
 - les points d'expérience de la partie (lorsque l'expérience du joueur atteint cette valeur, le jeu se termine)
 - la liste des statistiques (avec les points de vie en première place)

### Exemples d'utilisation

#### Exemple de manipulations basique

Quelques réflexions préliminaires sur les mécaniques de notre petit jeu :
 - en terme de stat : PV et Argent suffiront
 - un seul dialogue à deux issues et modification de statistiques par les dialogues, on aura un arbre d'XP qui va ressembler à ça :
```
    +--1--+
-0--+     +--3-
    +--2--+     
```

Nous allons commencer par créer une carte simple. Juste le monde, sans maison.
```
carte_monde = (
r"""
 _         ###
/o\__     #####
|  <>\     ###  
|____|     /_\

  *


|==|==|==|==|==|==|==|""",)
```
Nous avons un PnJ aux coordonnées `(2, 5)`, et pas d'adversaire, il nous reste à faire les dialogues avec cet unique PnJ, la fonction de combat ne sera pas traitée ici vu qu'il n'y a pas d'ennemi.

Comme il n'y a pas grand chose à faire, je vais en profiter pour vous montrer les dialogues et les statistiques.
```
def evenements(xp, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5): return {
            0: [0, "Mon bon monsieur, vous n'auriez pas quelques sous pour moi ? 1. He non mon brave... 2. Mais si, bien sur, tenez.", 2],
                1: [2, "Radin !"],
                # 0 réponse possibles, +0 PV, -1 Argent
                2: [1, "Merci !", 0, 0, -1],

            "base": [0, "Hmm ?"]
        }

    return [0, "Hmm ?"]
```

Comme dit plus haut : pas de combat, donc la fonction de combat va se résumer à un simple `def ...: pass` :
```
def combat(xp, carte_actuelle, x, y, stat): 
    pass
```

Pour les statistiques, nous avons des points de vie et de l'argent, on va bricoler un truc simple :
```
def affichage_stat(stat):
    pv, argent = stat
    print("Statistiques")
    print("PV : {}".format(pv))
    print("Argent : {}".format(argent))
```

Il ne reste plus qu'à tout donner au moteur !
La limite d'XP de la partie est fixée à 3, on commence la partie avec 100 points de vie et 5 Argent.
```
def mon_jeu():
    rpg_python = Asci(carte_monde, evenements, combat, affichage_stat, 3, [100, 5])
    rpg_python.mainloop()
```

Et voila ! N'oubliez pas d'importer `asci_lib` ! Pour ceux qui veulent tester, le code complet est dans le fichier `rpg_maker/sample_1.py`

#### Autre exemple basique

Nous allons reprendre la même carte que tout à l'heure, mais nous allons ajouter une porte à la maison, aux coordonnées `(1, 3)` : 
```
 _         ###
/o\__     #####
|_ <>\     ###  
|^|__|     /_\

  *


|==|==|==|==|==|==|==|
```
Il faut donc dessiner l'intérieur de la maison :
```
+--+--+--------+--+--+
|  |  |  *     |  | *|
|  +  +        +  +  |
|                    |
|  +  +        +  +  |
+--/  \--------/  \--+
|                    |
+---|^|--------------+
```
La porte à l'intérieur est aux coordonnées `(5, 7)`. Nous avons donc le tuple des cartes :
```
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
(1, 3), (5, 7)
))
```

Pour les évènements, rien de nouveau, étant donné que nous n'avons a priori pas de statistiques à part la vie, il n'y a pas forcément grand chose à faire, vous pouvez vous amuser à faire des dialogues un peu complexes avec différentes fins.

```
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
```
De même que pour l'exemple précédent : pas de combat. Je vous laisse gérer l'affichage des statistiques. Il reste la fonction finale :
```
def mon_jeu():
    rpg_python = Asci(cartes, evenements, combat, affichage_statistique, 13, [100])
    rpg_python.mainloop()
```
La limite est à 13 xp comme on peut le voir sur l'arbre :
```
             +--6-X              
    +--1--4--+        +--8--10--11--12--13-
-0--+        +--5--7--+
    +--2--3--+        +--9-X
```
les `X` symbolise les impasses.