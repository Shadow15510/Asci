def Evnt (liste):
  xp = liste[0]
  carte = liste[1]
  if carte == 7 and xp == 34:
    xp = 35
  if carte == 8 and xp == 38:
    xp = 39
    input("Vous trouvez une\nlettre sur le mort...\nIl y est ecrit\n'MWVBER NM LAXZE WP\nAEUWZILG. BHQGT'\n")
  if carte ==5+liste[2] and xp == 50:
    txt = input("Entrez le message\nentier et decode en\nmajuscules :\n")
    if txt == "METTEZ LE LIVRE EN SECURITE. THYEL":
      xp = 51
  return xp

def discussion(lieu,map_no,xp,pv):
  if lieu == 1+map_no:
    if xp == 30:
      return[1,0,"Bonjour. Je vais", "devoir partir en", "province pour des", "affaires urgentes."]
    elif xp == 31:
      return[1,0,"Pendant mon abcence", "je voudrais que tu", "trouves le voleur de", "ce livre. Son contenu", "est tres sensible."]
    elif xp == 32:
      return[0,0,"On se reverra des mon", "retour en attendant", "tu peux te confier a", "Thyel, il a ma", "confiance."]
    else:
      return[0,0,"Le Roi ?", "Il est en", "deplacement..."]
  elif lieu == 2+map_no:
    if xp == 32:
      return[1,0,"Ah, c'est le Roi qui", "t'envoie ! Je suis", "moi-meme plus ou", "moins espion ayant", "beaucoup d'amis..."]
    elif xp == 33:
      return[1,0,"On ma rapporte qu'un", "riche villageois", "s'est vante d'avoir", "le secret de la", "teleportation"]
    elif xp == 34:
      return[0,0,"Tu peux commencer", "tes recherches par", "le village..."]
    elif xp == 42:
      return[1,0,"Un message code", "dis-tu ? Montre moi", "ca... Mmmh, bon", "travail, et ce", "livre ? C'est pour", "demain ?"]
    elif xp == 43:
      return[1,0,"Donne-le moi, je le", "ferais decrypter."]
    elif xp == 44:
      return[0,0,"Tu veux en referer au", "Roi ? Quelle idee !", "On ne le derange pas", "pour des bouts de", "papiers ! Allez", "donne-moi ce papier !"]  
    
    else:
      return[0,0,"Salut !","Tes recherches", "avancent comme tu le", "souhaite ?"]
      
  elif lieu == 7+map_no:
    if xp == 34:
      return[0,0,"Aah... enfin !", "Un homme de peu de", "foi rode devant ma", "maison j'ai peur de", "sortir..."]
    elif xp == 35:
      return[1,0,"Voila un travail bien", "fait ! Non je n'ai", "jamais entendu parle", "d'un tel livre."]
    elif xp == 36:
      return[1,0,"Attend ! Je me", "souviens avoir", "consulte un ouvrage", "sur la teleportation", "chez un archiviste", "anarchiste."]
    elif xp == 37:
      return[0,0,"Peut etre trouverez", "vous plus", "d'informations aupres", "de la bibliotheque ou", "de l'archiviste ?"]
    elif xp == 46:
      return[1,0,"Ah te voila.","J'ai horreur de", "retrouver mes hommes", "de mains en pieces", "detachees ! QUOI ! Un"]
    elif xp == 47:
      return[0,0,"message ? Mais... je", "n'utilise que des", "illetres. Hors", "d'ici imposteur !"]
    else:
      return[0,0,"Je ne vous permet de", "m'introduire chez moi", "de la sorte !!"]
  elif lieu == 6:
    if xp == 37:
      return[1,0,"Tu as ete voir 'le", "bourgeois' ? C'est un", "manipulateur cynique", "prends garde !"]
    elif xp == 38:
      return [0,0,"Je n'en sais pas plus", "mais des sbires a lui", "trainent dans", "le bois. Prend cette", "potion de", "soins. [>295]"]
    elif xp == 52:
      return[1,0,"Thyel un traitre !?","Bon la question est", "ou est cache", "le livre... Le", "'bourgeois' doit", "tremper dans la..."]
    elif xp == 53:
      return[1,0,"...combine c'etait", "son sbire qui avait", "le billet... Ou alors", "le sbire etait un", "simple", "intermediaire ?"]
    elif xp == 54:
      return[1,0,"Thyel va chercher a", "t'eliminer. Essaie", "d'abord de savoir ou", "est le livre."]
    elif xp == 55:
      return[0,0,"Je connais un brigand", "qui pourra sans doute", "t'aider. Il se trouve", "dans la foret"]
    else:
      return[0,0,"Ah, te revoila !","Tes recherches", "avancent ?"]
  elif lieu == 5+map_no:
    if xp == 39:
      return[1,0,"De la documentation", "sur la cryptographie", "? Oui j'ai cela...", "Ah voila c'etait ici", "!"]
    elif xp == 40:
      return[1,0,"Il y est dit que les", "methodes recentes", "utilisent un mot ou", "une phrase comme cle.", "Cette methode empeche", "une analyse..."]
    elif xp == 41:
      return[1,0,"...frequencologique.", "Sans le code", "parfois lui-meme code", "il est impossible de", "dechiffrer le texte."]
    elif xp == 42:
      return[0,0,"Je n'ai pas d'autres", "informations pour", "l'instant, mais", "revient plus tard je", "mene mes recherches", "sur le sujet !"]
    elif xp == 45:
      return[1,0,"Ton message est code", "par un mot de 4", "lettres mais je n'en", "sais pas plus. Si tu", "trouves le mot..."]
    elif xp == 46:
      return[0,0,"On m'a dit que", "'le Bourgeois' te", "cherche..."]  
    elif xp == 49:
      return[1,0,"CUEK ? Mmmh... Voyons", "voir... On dirait un", "decalage... Ca", "pourrait etre 'BTDJ'", "a voir si ca marche", ",a toi de jouer !"]
    elif xp == 50:
      return[0,0,"Reviens ici quand", "tu auras tout decode", "et presse [7]."]
    elif xp == 51:
      return[1,0,"C'est Thyel qui a", "vole mon livre ?", "Mais... pourquoi ?","Le Roi doit", "etre prevenu !"]
    elif xp == 52:
      return[0,0,"Mon ancien archiviste", "est toujours mon ami,", "va le voir les", "magouilles c'est son", "rayon."]
    else:
      return[0,0,"Bonjour !", "Des nouvelles de", "mon livre ?"]
  elif lieu == 4:
    if xp == 44:
      return[1,0,"Tu vas me tuer avec", "tes conneries ! Filer", "Thyel ? Tu", "prefererais pas tuer", "le Roi ?"]
    elif xp == 45:
      return[0,0,"Bon ok reviens me", "voir je le ferais", "suivre..."]  
    elif xp == 47:
      return[1,0,"Thyel a rencontre", "'le Bourgeois'","Fouiller la baraque", "de Thyel ?? Pour qui", "tu me prends ?"]
    elif xp == 48:
      return[1,0,"Bien sur que je l'ai", "fouillee !"]
    elif xp == 49:
      return[0,0,"J'ai trouve du pain", "des chaussures et...", "un bout de papier", "avec marque 'CUEK'", "dessus."]
    elif xp == 55:
      return[1,0,"ENCORE !!", "Trouver un livre ?", "Je crois que t'as", "toujours pas", "compris..."]
    elif xp == 56:
      return[1,0,"Ah ben voila ouvrir", "les yeux je sais", "faire ! Par contre", "si tu veux des infos", "je veux un service !"]
    elif xp == 57:
      return[1,0,"Va jeter un oeil", "vers le village et", "ramene-moi des tuyaux", "sur le 'bourgeois'"]
    elif xp == 58:
      return[0,0,"Pourquoi ? Je t'en", "pose, moi des", "questions ? File !"]
    elif xp == 59:
      return[1,0,"Bien. Ton livre est", "planque chez", "le 'bourgeois'."]
    else:
      return[0,0,"Toi, si tu continues", "tu vas finir les", "boyaux par terre..."]
  elif lieu == 7:
    if xp == 58:
      return[1,0,"Le 'bourgeois' ? Bah", "il a recu", "un envoye du Roi et", "Thyel. il parait", "qu'un de ses homme", "de main est mort..."]
    else:
      return[0,0,"S'lut."]
  elif lieu == 3+map_no:
    if pv < 100:
      return [0,100,"Quoi ?!", "Tu es encore blesse !","Tu le fais expres !?"]
    else:
      return [0,0,"Que fais-tu ici ?","Ici c'est pour les", "blesses pas les gens", "en pleine forme !"]
  else:
    return[0,0,"..."]