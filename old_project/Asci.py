from random import randint
from mapset import *
from locate import * 

def convert(n):
    try:
        n = int(n)
    except:
        n = 0
    return n

def opus(partie):
    if partie == 1:
        import Evnt1 as e
    elif partie == 2:
        import Evnt2 as e
    elif partie == 3:
        import Evnt3 as e
    global evnt
    evnt = e

def main (liste):
    xp = liste[1]
    carte = liste[2]
    pv = liste[3]
    fin = liste[4]
    ecran = Screen()
    map_no = 8
    liste = [4+map_no,6+map_no,8+map_no]
    if (carte > 2*map_no) or (carte <= 0) or ((carte in liste) == 1):
        carte = 1
    carte_chg = carte
    i = 0
    X = 10
    Y = 5
    key_buffer = 0
    key = 0
    test= 0
    map_list = []
    liste = []
    while key != 9 and pv > 0 and xp < fin:
        map_list = map_init(carte,map_no)
        disp_vram(ecran,map_list)
        ecran.locate(X,Y,"@")
        key = ecran.refresh(1)
        key = convert(key)
        if key != 0:
            key_buffer = key
        else:
            key = key_buffer
        test = case_test([key,X,Y,ecran])
        if test != 1 and test != 3:
            liste = getkey([key,X,Y])
            X = liste[0]
            Y = liste[1]
            if key==15510 and xp >= 29:
                test = tport(carte,map_no)
                if test != carte:
                    X = 10
                    Y = 5
                    carte = test
                test = 0
                carte_chg = carte
            elif key == 7:
                xp = evnt.Evnt([xp,carte,map_no])
            elif key == 8:
                liste = ["Palais","Thyel","Medecins","Foret","Bibliotheque","Plage","Village","Bois","Palais","Thyel","Medecins","","Bibliotheque","","Village"]
                ecran.__init__()
                ecran.locate(1,1,">Experience :")
                ecran.locate(14,1,xp)
                ecran.locate(1,2,">Pts de vie :")
                ecran.locate(14,2,pv)
                ecran.locate(1,3,">Qrt actuel :")
                ecran.locate(14,3,carte)
                ecran.locate(1,5,">Info du quartier :")
                ecran.locate(1,6,liste[carte-1])
                ecran.refresh(1)
            if liste[2] == 1:
                while carte == carte_chg:
                    carte_chg = randint(1,map_no)
                carte = carte_chg
                X = 10
                Y = 5
        if test == 2:
            carte = carte+map_no
            X = 10
            Y = 6
        elif test == 3:
            liste = evnt.discussion(carte,map_no,xp,pv)
            map_list = liste[2:]
            xp += liste[0]
            pv += liste[1]
            disp_vram(ecran,map_list,liste[0])
            ecran.refresh(1)
        elif test == 4:
            liste = combat(pv)
            pv = liste[0]
            if liste[1] == 1:
                xp = evnt.Evnt([xp,carte,map_no])
    if pv <= 0:
        pv = 100
    return [xp,carte,pv]
    
def disp_vram(ecran,map_list,suite=0):
    ecran.__init__()
    for i in range(1,len(map_list)+1):
        ecran.locate(1,i,map_list[i-1])
    if suite != 0:
        ecran.locate(21,6,">")

def getkey(liste):
    key = liste[0]
    X = liste[1]
    Y = liste[2]
    map_chg = 0
    if key==1:
        X-=1
    elif key==5:
        Y-=1
    elif key==3:
        X+=1
    elif key==2:
        Y+=1
    if X > 21:
        X = 21
        map_chg = 1
    if X < 1:
        X = 1
        map_chg = 1
    if Y > 6:
        Y = 6
        map_chg = 1
    if Y < 1:
        Y = 1
        map_chg = 1
    return [X,Y,map_chg]

def case_test(liste):
    key = liste[0]
    X = liste[1]
    Y = liste[2]
    ecran = liste[3]
    liste = getkey([key,X,Y])
    X = liste[0]
    Y = liste[1]
    cell = ecran.get_cell_content(X,Y)
    if cell == " " or cell == "@":
        return 0
    elif cell == "^":
        return 2
    elif cell == "*":
        return 3
    elif cell == "$":
        return 4
    else:
        return 1
     
def tport(actu,maxi):
    code = input("Entrez le code du\nquartier:\n")
    try:
        code = int(code)
    except:
        code = actu
    if code > maxi or code <= 0:
        code = actu
    return code
    
def combat(pv):
    adv_pv = randint(50,100)
    adv_pa = 0
    degat = 0
    obj = 1
    test = 0
    while pv > 0 and adv_pv > 0 and obj != 0:
        obj = input("Entrez le code de\nl'objet: ")
        obj = convert(obj)
        if obj < 0:
            obj = 1 
        adv_pa = 0
        pa = 0
        if obj == 666:
            adv_pv -= randint(int(adv_pv/2),adv_pv)
        elif obj == 295:
            pv += 50    
        else:
            pa = randint(int(obj/4),int(obj/2))
            adv_pa = randint(int(pa/4),int(obj/2))
            degat = (pa - adv_pa)*2
        if degat >= 0:
            adv_pv -= degat
            print("Points de vie :\n>Vous :",pv,"\n>Adversaire :",adv_pv,"\nVous attaquez et\ninfligez",degat)
        else:
            pv += degat
            print("Points de vie :\n>Vous :",pv,"\n>Adversaire :",adv_pv,"\nVotre ennemi se rue\nsur vous",1-degat)
    if pv <= 0:
        print("Vous etes mort.")
    elif adv_pv <= 0:
        print("Vous avez tue votre\nadversaire.")
        test = 1
    else:
        print("Vous avez\nabandonne le combat")    
    input()
    return [pv,test]