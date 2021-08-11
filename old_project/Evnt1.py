def Evnt (liste):
    xp = liste[0]
    carte = liste[1]
    if xp == 7 and carte == 4:
        xp = 8
    elif xp == 27 and carte == 4:
        xp = 28
    return xp

def discussion(lieu,map_no,xp,pv):
    if lieu == 1+map_no:
        if xp == 0:
            return [1,0,"La ville d'Asci est", "divisee en quartiers.", "Chaque quartier", "est separe des autres", "par des distances ", "inimaginables !"]
        elif xp == 1:
            return [1,0,"Une grande part", "d'aleatoire regit", "ce monde et seuls", "quelques inities", "peuvent passer outre."]
        elif xp == 2:
            return [0,0,"Bon courage !", "Tu peux te rendre au", "quartier 2. Il y a un", "grand arbre a l'est", "de ce quartier.", "Thyel, t'aidera."]
        elif xp == 9:
            return [2,0,"Ah te voila enfin !", "Bravo pour ton fait", "d'arme. Voici une", "epee neuve repondant", "a [>28]"]
        elif xp == 11:
            return [1,0,"J'ai besoin de toi !", "Je dois faire un", "long voyage. Aussi", "j'aimerai connaitre", "le moyen de se", "teleporter."]
        elif xp == 12:
            return [1,50,"Bois cela te donnera", "des forces ! La", "bibliotheque du", "quartier 5 pourra", "peut-etre t'aider."]
        elif xp == 13:
            return [0,0,"La bibliotheque", "regorge", "d'informations !"]
        elif xp == 17:
            return [2,0,"Oui c'est vrai, Thyel", "etait avec moi hier", "et nous n'avons pas", "quitte le Palais."]
        elif xp == 19:
            return [0,0,"Continue tes", "recherches. Tu", "avances bien.", "As-tu ete voir", "l'ancien archiviste ?"]
        elif xp == 29:
            return [1,0,"Ah mais tu es doue !", "Merci jeune homme !", "Je te garde a mon", "service. De ce fait", "voici ta nouvelle", "epee [>50]"]
        else:         
            return [0,0,"Bonjour, je suis le", "Roi d'Asci.", "Que puis-je faire", "pour t'aider ?"]
    elif lieu == 2+map_no:
        if xp < 2:
            return [0,0,"Hey ! Je suis Thyel,", "ami du Roi.", "Bienvenu dans Asci !"]
        elif xp == 2:
            return [2,0,"Aha, tu verras,", "Asci est une", "ville speciale. Les", "quartiers ne sont pas", "cote a cote."]
        elif xp == 4:
            return [1,0,"Les quartiers sont", "relies entre eux par", "des ponts aleatoires:", "quand tu quittes", "un quartier tu es", "envoye dans un autre."]
        elif xp == 5:
            return [1,0,"Et ce de maniere", "aleatoire ! On", "murmure qu'il est", "possible d'echapper a", "cet aleatoire."]
        elif xp == 6:
            return [1,0,"Il est temps", "que tu apprennes", "les armes ! Tiens", "prend cette dague,", "[>10] pour l'utiliser"]
        elif xp == 7:
            return [0,0,"Des maraudeurs s'en", "prennent aux", "visiteurs dans la", "foret du quartier 4.", "Reviens me voir", "apres !"]
        elif xp == 8:
            return [1,50,"He mais tu es blesse", "! Je t'ai gueris", "comme j'ai pu mais si", "tu as besoin il y a", "un medecin dans le", "quartier 3"]
        elif xp == 9:
            return [0,0,"Le Roi a eu vent", "de tes exploits, il", "veux te remercier,", "bon courage pour le", "trajet !"]
        elif xp == 15:
            return [2,0,"HEIN ! Je ne savais", "meme pas que la", "bibliotheque avait un", "tel ouvage !", "Quelqu'un a usurpe", "mon nom !"]
        elif xp == 17:
            return [0,0,"Le Roi te confirmera", "que j'etais avec lui", "tout hier."]
        else:    
            return [0,0,"Hey !", "Tu vas bien vieux ?"]
    elif lieu == 3+map_no:
        if pv < 100:
            return [0,100,"Ah ! Quelle idee de", "tuer quelqu'un,", "regarde tu t'es", "blesse !"]
        else:
            return [0,0,"Tu es en pleine", "forme !"]
    elif lieu == 5+map_no:
        if xp == 13:
            return [1,0,"Un ouvrage sur la", "teleportation ? Oui,", "je dois avoir ca..."]
        elif xp == 14:
            return [1,0,"Je ne comprend pas", "il devrait etre ici.", "Le dernier emprunt ?!", "Ces ouvrages ne", "sortent pas d'ici."] 
        elif xp == 15:
            return [0,0,"La derniere personne", "qui l'a consulte ?", "Je vais regarder le", "registre", "...", "C'est Thyel, hier."]
        else:
            return [0,0,"Bienvenu dans la", "bibliotheque d'Asci."]
    elif lieu == 6:
        if xp == 19:
            return [1,0,"L'ancien archiviste", "oui c'est moi..."]
        elif xp == 20:
            return [1,0,"J'ai ete limoge suite", "a une vieille affaire", "il faut savoir qu'en", "ce temps-la les", "livres etaient tous", "ouverts au public."]
        elif xp == 21:
            return [1,0,"Puis le", "bibliothecaire a eu", "le droit de censurer", "les livres a sa guise", "Voulant proteger le", "droit a l'..."]
        elif xp == 22:    
            return [1,0,"...l'information,", "j'ai cache des livres", "censures chez moi ou", "le public pouvait les", "consulter."]
        elif xp == 23:
            return [1,0,"De quoi parlaient-ils", "? Certains de", "politique d'autre de", "sorcelerie."]
        elif xp == 24:
            return [1,0,"He non je ne les ais", "plus ils ont ete", "brules. Avant", "beaucoup savaient se", "teleporter..."]
        elif xp == 25:
            return [0,0,"Maintenant, quelques", "voleurs astucieux", "connaissent la", "formule et c'est", "bien tout."]
        else:
            return [0,0,"Bonjour jeune homme."]
    elif lieu == 4:
        if xp == 25:
            return [1,0,"Envoye par le Roi !", "Mais... ca fait", "grimper la rancon", "ca !!"]
        elif xp == 26:
            return [1,0,"Le code de", "teleportation ! Rien", "que ca ? J'en ai", "evicere pour moins", "que ca alors debale", "un argument credible"]
        elif xp == 27:
            return [0,0,"Un service ? Mmm...", "Va donc tuer ce", "detrousseur la un", "peu plus bas.","Ce malhonnete vole", "mes clients !"]
        elif xp == 28:
            return [1,0,"Bien, tu a de", "l'avenir petit. Le", "code est 15510 tu le", "connaissais sans", "doute deja..."]
        else:
            return [0,0,"Si tu tiens a ta vie", "plie bagages avant", "que je ne te les", "prennes !"]
    else:
        return [0,0,"..."]
