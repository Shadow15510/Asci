end = 30


def get_interaction(xp, current_map):
    if current_map == 4:
        if xp in (7, 27): xp += 1

    return xp


def get_dialogue(xp, pv, current_map, outdoor):
    xp_str = str(xp)
    
    # Palais
    if not outdoor and current_map == 1:
        dialogue = {
        "0": [2, 0, "La ville d'Asci est divisee en quartiers. Chaque quatier est separe des autres par des distances inimaginables ! Une grande part d'aleatoire regit ce monde... et seuls quelques inities peuvent passer outre."],
        "2": [0, 0, "J'ai parle de toi a Thyel, un ami. Il t'attends chez lui, tu reconnaitra la maison : il y a un grand arbre plante sur la droite."],

        "9": [2, 0, "Ah, te voila enfin ! Bravo pour ton d'arme ! En guise de reconnaissance voici une epee de mon armurerie personnelle. Elle repond au code 25."],
        "11": [1, 0, "Maintenant que tu as fait tes preuves, j'ai un service a te demander... J'ai un long voyage a faire, avec toutes les perturbations aleatoires, j'ai peur de ne pas arriver a temps, aussi j'aimerai connaitre le secret de la teleportation. Je compte sur toi !"],
        "12": [1, 50, "Bois, cela te donnera des forces !"],
        "13": [0, 0, "La bibliotheque regorge d'informations."],
        
        "17": [2, 0, "Oui, c'est vrai, Thyel etait bien avec moi hier soir, et nous n'avons pas quitte le palais."],
        "19": [0, 0, "Continues tes recherches, tu avances bien. As-tu ete voir l'ancien archiviste ?"],

        "29": [1, 0, "Ah mais tu es doue ! Merci jeune homme ! Je te garde a mon service. De ce fait, voici ta nouvelle epee [>50]."],

        "base": [0, 0, "Bonjour, je suis le Roi d'Asci."]
        }

        if xp_str in dialogue: return dialogue[xp_str]
        else: return dialogue["base"]
    
    # Thyel
    elif not outdoor and current_map == 2:
        dialogue = {
        "<2": [0, 0, "Hey ! Je suis Thyel, ami du Roi. Bienvenue dans Asci !"],
        "2": [3, 0, "Ah, te voila ! Tu verras, Asci est une ville speciale. Les quartiers ne sont pas les uns a cote des autres. Ils sont relies entre eux par des ponts aleatoires. Quand tu quittes un quartier, tu te retrouves aleatoirement dans un autre."],
        "5": [1, 0, "On murmure qu'il est possible d'echapper a cet aleatoire..."],
        "6": [1, 0, "Bon, assez parlé, il est temps de t'equiper un minimum ! Tiens, prend cette dague, [>10] pour l'utiliser."],
        "7": [0, 0, "Des maraudeurs s'en prennent aux visiteurs dans la foret. Reviens me voir après."],
        
        "8+pv<100": [1, 25, "Ah mais tu es blesse ! Bon, je t'ai panse comme j'ai pu, mais si tu as besoin, il y a des medecins dans un quartier. Leur officine est entoure de barrieres."],
        "8": [1, 0, "Meme pas blesse ! Impressionnant !"],
        "9": [0, 0, "Je viens de recevoir un courrier du Roi : il t'attend au palais. Bon courage pour le trajet !"],

        "15": [2, 0, "HEIN ?! Je ne savais meme pas que la bibliotheque avait un tel ouvrage ! Quelqu'un a usurpe mon nom !"],
        "17": [0, 0, "Le Roi te confirmera que j'etais avec lui tout hier soir."],

        "base": [0, 0, "Hey, comment vas-tu ?"]
        }

        if xp < 2: return dialogue["<2"]
        elif xp == 8:
            if pv < 100: return dialogue["8+pv<100"]
            else: return dialogue["8"]
        elif xp_str in dialogue: return dialogue[xp_str]
        else: return dialogue["base"]

    
    # Medecins
    elif not outdoor and current_map == 3:
        dialogue = {
        "pv<100": [0, 100, "Quelle idee de tuer quelqu'un !? Regarde tu t'es blesse !"],
        "pv>=100": [0, 0, "Tu es en pleine forme !"]
        }
        
        if pv < 100: return dialogue["pv<100"]
        else: return dialogue["pv>=100"]

    # Bibliothèque
    elif not outdoor and current_map == 5:
        dialogue = {
        "13": [2, 0, "Un ouvrage sur la teleportation ? Oui, je dois avoir ça... Je ne comprends pas, il devrait etre ici... Le dernier emprunt !? Ces ouvrages ne sortent pas d'ici. La derniere consultation ? J'ai du le reporter dans le registre, je vais regarder... C'est Thyel, hier, dans la soirée."],

        "base": [0, 0, "Bonjour et bienvenue dans la bibliotheque d'Asci."]
        }

        if xp_str in dialogue: return dialogue[xp_str]
        else: return dialogue["base"]
    
    # Plage
    elif current_map == 6:
        dialogue = {
        "19": [6, 0, "L'ancien archiviste, oui c'est moi... J'ai été limoge suite a une vieille affaire. Il faut savoir qu'en ce temps-la les livres etaient tous ouverts au public. Puis le bibliothecaire a eu le droit de censurer les livres a sa guise. Voulant proteger le droit a l'information, j'ai cache des livres censures chez moi ou le public pouvait les consulter. De quoi parlaient-ils ? Certains de politique d'autre de sorcelerie. Que sais-je ? Les sujets ne manquaient pas ! He non je ne les ais plus ils ont ete brules. Avant beaucoup savaient se teleporter... Maintenant, quelques voleurs astucieux connaissent la formule et c'est bien tout."],
        "base": [0, 0, "Bonjour jeune homme."]
        }

        if xp_str in dialogue: return dialogue[xp_str]
        else: return dialogue["base"]

    # Forêt
    elif current_map == 4:
        dialogue = {
        "25": [2, 0, "Envoye par le Roi ! Mais... ca fait grimper la rancon ca !! Le code de teleportation ! Rien que ca ? J'en ai evicere pour moins que ca alors debale un argument credible. Me rendre un service ? Mmm... va donc tuer ce detrousseur la un peu plus bas. Ce malhonnete vole mes clients !"],
        "28": [1, 0, "Bien, tu a de l'avenir petit. Le code est 15510 tu le connaissais sans doute deja..."],
        "base": [0,0,"Si tu tiens a ta vie", "plie bagages avant", "que je ne te les", "prennes !"]
        }

        if xp_str in dialogue: return dialogue[xp_str]
        else: return dialogue["base"]

    else:
        return [0, 0, "Hmm ?"]
