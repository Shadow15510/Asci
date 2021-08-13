# Asci

## Présentation

### Le projet

À l'origine, Asci est un jeu de rôle en Python pour Graph 90. Le jeu est aujourd'hui accompagné d'un moteur pour que vous puissiez réaliser vos jeux de rôles en Python avec un minimum d'effort.

### Principe

Le moteur repose sur l'évolution de points d'expérience pour déterminer votre avancée dans le jeu. Ces points d'expériences peuvent être donnés au joueur à l'issu de dialogues ou de combats.

### Licence

Tout le projet est soumis à la licence GNU General Public Licence v3.0.

## Utilisation

### Instructions

#### Création d'un nouveau projet

Vous devez commencer par copier le fichier `asci_lib.py` dans le répertoire de votre jeu. Créez ensuite un fichier qui va correspondre à votre jeu. Nommez-le comme vous voulez, le nom ne présente pas d'importance pour le moteur.

Ici, notre fichier s'appellera `sample.py`.

#### Structure du programme

Notre fichier va se découper en plusieurs parties : 
 - l'importation de la bibliothèque `asci_lib.py`
 - la création de la carte
 - la création des dialogues 
 - la création de la fonction qui correspond à votre jeu et finalisation

#### Création de la carte

La carte est un grand tuple qui est de la forme : 
```
carte_monde = (
<carte_du_monde>,
(<carte_maison_1>, (x_entree1, y_entree1), (x_sortie1, y_sortie1)),
(<carte_maison_2>, (x_entree2, y_entree2), (x_sortie2, y_sortie2)),
...)
```
la `<carte_du_monde>` et les `<carte_maison_X>` sont des r-docstrings. Vous pouvez mettre à peu près n'importe quoi, veillez à bien respecter la légende : 
 - `@` : caractère réservé au joueur (ne pas utiliser)
 - `^` : porte de maison
 - `*` : PnJ
 - `$` : adversaire

Dans le cas des maisons, le premier tuple correspond aux coordonnées de la porte de la maison *dans la carte du monde*. Le second tuple correspond aux coordonnées de la porte de la maison *dans la carte de la maison*.

#### Création des dialogues

Sur votre carte fraîchement créée, vous avez mis des PnJ (si ce n'est pas le cas, mettez-en, la suite sera plus intéressante ;) ). L'idée est assez simple, il va falloir créer une fonction qui va prendre en argument l'expérience, les points de vie, l'id de la carte (l'index de la carte dans le tuple des maps, 0 : carte du monde, 1 : première maison etc), les coordonnées du joueur et les stat (une liste qui peut contenir des variables nécessaires aux mécaniques de votre jeu). Nous avons donc déjà :
```
def dialogue(xp, pv, carte_actuelle, x, y, stat):
```
Cette fonction va renvoyer un dictionnaire *ou* une liste.

C'est assez important, car, si vous renvoyez un dictionnaire, le dialogue sera lu en fonction des points d'expériences du joueur. Si vous renvoyez une liste, c'est le dialogue de la liste qui sera lu.

Le seul impératif que vous devez absolument respecter est la forme du dictionnaire et des listes.

Le dictionnaire est de la forme : 
```
dialogues = {
	xp_1: [...],
	xp_2: [...],
	...
	"base": [...]
}
```
`xp_X` correspond au nombre de points d'expérience à avoir pour déclencher ce dialogue.
`"base"` est le dialogue lancé par défaut si aucun autre cas ne marche.

Les listes sont, elles, de la forme :
```
[xp_gagne, pv_gagne, "le texte du dialogue", booleen, ...]
```
`xp_gagne` correspond aux nombres de points d'expérience gagné lors de la lecture de ce dialogue.
`pv_gagne` même principe qu'avec l'XP, mais avec les points de vie.
`booleen` détermine s'il s'agit d'un monologue du PnJ ou si vous pouvez répondre au PnJ.
`...` correspond à des modificateurs des stats. Vous pouvez tout à fait les oublier en première utilisation

La question maintenant est de savoir comment relier les dialogues au PnJ. Vous êtes libre de mettre en place un système d'ID, Nous vous proposons un système peut-être plus simple : les coordonnées des PnJ. Nous allons ainsi avoir une fonction qui va ressembler à :
```
def dialogue(xp, pv, carte_actuelle, x, y, stat):
	# Pour des raisons de légèreté, on déclare un tuple avec les coordonnées
	coords = (x, y)

	# Si nous sommes en extérieur
	if carte_actuelle == 0:
		if coords == (X1, Y1):
			return {...}
		elif coords == (X2, Y2):
			return {...}

	# Si nous sommes dans la première maison de la liste
	elif carte_actuelle == 1:
		...

	# Si le PnJ est bien sur la map, mais n'a aucun dialogue d'assigné :
	return [0, 0, "Hmm ?", False]
```
Vous pouvez également créer des dialogues. Pour cela, il vous suffit de mettre le booleen sur `True` et de mettre les réponses possibles dans le corps du dialogue, par exemple : `[0, 0, "Ceci est une question ? 1. Réponse 1 2. Réponse 2", True]`. Le numéro de la réponse correspond au nombre de point d'expérience qu'elle rapporte, cela vous permet de gérer les différents cas dans al suite du dialogue.

#### Finalisation

Il reste à faire une petite fonction qui va créer un "modèle" de jeu de rôle vierge, il faudra lui donner la carte, la fonction des dialogues et ce sera fini !

La fonction est vraiment triviale :
```
def mon_jeu():
	rpg_python = Asci(carte_monde, dialogue, 10, [])
	rpg_python.mainloop()
```
Les deux premiers arguments `carte_monde` et `dialogue` ont déjà été vu. Le `10` correspond aux nombres de points d'expérience au bout duquel le programme s'arrête, il s'agit de la fin de la partie si vous voulez. La liste passée en dernier argument correspondent aux stats.

### Exemples et astuces

#### Exemples de cartes

Pour commencer simplement, voici une carte assez banale (ne pas oublier la virgule à la fin !) : 
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
Nous n'avons pas de maisons, juste un PnJ

#### Exemple de fonction de dialogue

Nous allons faire parler notre PnJ ! Et comme on est chaud, on va directement faire un petit dialogue. Pour bien séparer les réaction à la question du reste, je met un niveau d'indentation supplémentaire, ça ne change rien au comportement du code.
```
def dialogue(xp, pv, carte_actuelle, x, y, stat):
	coords = (x, y)

	if carte_actuelle == 0:
		if coords == (2, 5): return {
			0: [0, 0, "Coucou ! Comment ca va ? 1. Ca va, et toi ? 2. Bof... 3. Je t'emmerde.", True],
				1: [3, 0, "Je vais bien, merci !", False],
				2: [3, 0, "Ow, desole...", False],
				3: [4, 0, "He, reviens quand tu sera de meilleure humeur !", False],

			4: [2, 0, "Bon et bien, je crois bien que cette premiere carte s'est bien passee !", False],
			5: [1, 0, "Je vais y aller, appelle moi si tu as besoin ;)", False],
			6: [1, 0, "A pluche o/", False],

			"base": [0, 0, "Oui ?", False]
			}

	return [0, 0, "Hmm ?", False]
```
Pour mettre en place vos dialogues (parce que j'espère que vous aurez un peu plus qu'un seul PnJ) faire un arbre de progression de l'XP peut être une bonne idée ;) je vais essayer de le faire en ASCII-art pour vous montrer, mais avec une feuille et un stylo c'est plus simple.
```
      1    4
     -=----=---
0   / 2    5   \  6  7
------=----=------=--=
    \ 3            /
     -=------------
```

#### Fin de l'exemple et récapitulation

Il reste la petite fonction à faire : 
```
def mon_jeu():
	rpg_python = Asci(carte_monde, dialogue, 7, [])
	rpg_python.mainloop()
```

Nous avons le fichier complet :
```
from asci_lib import *


carte_monde = (
r"""
 _         ###
/o\__     #####
|  <>\     ###  
|____|     /_\

  *


|==|==|==|==|==|==|==|""",)


def dialogue(xp, pv, carte_actuelle, x, y, stat):
    coords = (x, y)

    if carte_actuelle == 0:
        if coords == (2, 5): return {
            0: [0, 0, "Coucou ! Comment ca va ? 1. Ca va, et toi ? 2. Bof... 3. Je t'emmerde.", True],
                1: [3, 0, "Je vais bien, merci !", False],
                2: [3, 0, "Ow, desole...", False],
                3: [4, 0, "He, reviens quand tu sera de meilleure humeur !", False],

            4: [2, 0, "Bon et bien, je crois bien que cette premiere carte s'est bien passee !", False],
            5: [1, 0, "Je vais y aller, appelle moi si tu as besoin ;)", False],
            6: [1, 0, "A pluche o/", False],

            "base": [0, 0, "Oui ?", False]
            }

    return [0, 0, "Hmm ?", False]


def mon_jeu():
    rpg_python = Asci(carte_monde, dialogue, 7, [])
    rpg_python.mainloop()
```
