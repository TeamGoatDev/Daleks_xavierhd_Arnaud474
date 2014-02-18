import random
import os
import sys
import msvcrt
import time

#Declaration des objets
class Vue:

    #Fonction qui fait l'affichage de jeu dans la console
    def afficher(self, jeu):

        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain 
        for y in range(0,jeu.surface_h+1):
            for x in range(0, jeu.surface_l+1):
                #Si la case courante correspond a un element de la liste
                for n in range(0, jeu.nb_total_objets-1):
                    if(x == jeu.liste_objets[n].x and y == jeu.liste_objets[n].y):
                        print(jeu.liste_objets[n].apparence, end='')
                        break
                else:
                    print('-',end='')

            if(y == 0):
                print('Points: '+str(jeu.points),end='') #Affiche les points
            elif(y == 1):
                print('Zappeur: '+str(jeu.liste_objets[0].nb_zapper),end='') #Affiche les points
            print('')   #end line
        print('')   #end line

    def splashNiveau(self, jeu):
        os.system('cls')
        print('')
        print('Vague : '+str(jeu.vague))
        print('Points : '+str(jeu.points))
        time.sleep(2)


class Jeu:
    def __init__(self):
        self.points = 0                 #Variable qui contient le nombre de points accumules par le joueur
        self.vague = 0                  #Numero de la vague en cours
        self.nb_dalek_restant = 0       #Nombre total des Daleks restant dans la liste
        self.nb_total_dalek = 0         #Nombre total de Dalek pour la vague courrante
        self.nb_total_objets = 0        #Nombre d'elements dans la liste
        self.liste_objets = []          #Liste qui contiendra les daleks et le docteur
        self.surface_l = 20             #Largeur de la surface de jeu
        self.surface_h = 30             #Hauteur de la surface de jeu

    def setNextVague(self):
        self.nb_total_dalek += 5
        self.creerListe()                               #Creation de la liste pour la nouvelle vague
        self.denombreObjet()
        self.denombreDalek()
        self.vague += 1
        self.liste_objets[0].nb_zapper += 1
        self.nb_total_objets = len(self.liste_objets)   #Calcule le nombre d'objet dans la liste

    def deplacerDalek(self,jeu):
        for i in range(1, self.nb_total_objets): #regarde tout les objets de la liste
                if(isinstance(self.liste_objets[i], Dalek)): #recherche d_objet Dalek
                    self.liste_objets[i].deplacer(jeu)
    
    def denombreDalek(self):
        self.nb_dalek_restant = 0

        self.nb_total_objets = len(self.liste_objets)
        
        for i in range(0, self.nb_total_objets): #regarde tout les objets de la liste
                if(isinstance(self.liste_objets[i], Dalek)): #recherche d_objet Dalek
                    self.nb_dalek_restant +=1

    def denombreObjet(self):
        self.nb_total_objets = len(self.liste_objets)


    #Fonction qui initialise la list contenant les objets(Personnages) pour le jeu (largeur de la surface, hauteur de la surface, nombre de daleks au total, liste qui contient les objets)
    def creerListe(self):
    
        position_ok = False
        position_xy = False

        #Creation de variables temporaires pour les postions x et y de chaque piece
        x = 0   # 1 est la premiere case contrairement a 0 dans un tableau
        y = 0   # 1 est la premiere case contrairement a 0 dans un tableau

        #Creation d'une position au hasard pour le docteur et inicialisation ci pas deja fait
        try:
            drWho = self.liste_objets[0] #Tentative de sauvegarder un docteur who deja existant
        except:
            drWho = DrWho(random.randint(1, self.surface_l),random.randint(1, self.surface_h)) #Creation d_un nouveau docteur who
        else:
            drWho.x = random.randint(1, self.surface_l)#Creation d'une position au hasard pour le docteur deja existant
            drWho.y = random.randint(1, self.surface_h)

        #Vide l'ancienne liste d'objets
        self.liste_objets[:] = [] 
 
        #ajout du dr who a la liste vide
        self.liste_objets.append(drWho)

        #Creation de la liste en fonction du nombre total de dalek pour cette vague
        for i in range(0, self.nb_total_dalek):
            
            position_ok = False
            
            #Tant que la position n'est pas une position valide par rapport a la postion du Docteur et n'est pas occupee
            while position_ok != True:

                position_xy = False

                #Regarde tout d'abord si la position n'est pas deja occupee par une autre piece
                while position_xy != True:

                    x = random.randint(1, self.surface_l)
                    y = random.randint(1, self.surface_h)

                    for n in range(0,len(self.liste_objets)):
                        if(x != self.liste_objets[n].x and y != self.liste_objets[n].y):
                            position_xy = True


                #Si la case est a deux cases du Docteur Who
                if ( (x >= (self.liste_objets[0].x+2) or x <= (self.liste_objets[0].x-2)) or (y >= (self.liste_objets[0].y+2) or y <= (self.liste_objets[0].y-2)) ):
                        position_ok = True

            #Ajoute un Dalek valide a la liste
            self.liste_objets.append(Dalek(x,y,5))


    #Fonction gerant les collisions des daleks entre eux et les ferrailles
    def collision(self):
 
        #Boucle pour regader les differents objets de la liste
        for i in range(self.nb_total_objets-1,0,-1):
            
            self.nb_total_objets = len((self.liste_objets))
            
            #Regarde si la piece est un Dalek
            if(isinstance(self.liste_objets[i], Dalek)):
                #Boucle pour faire la comparaison entre les deux pieces
                for j in range(self.nb_total_objets-1,0,-1):
                    
                    
                    #Si les positions de j et i sont identiques
                    if(self.liste_objets[i].x == self.liste_objets[j].x and self.liste_objets[i].y == self.liste_objets[j].y and i != j):
           
                        #Si l'objet de comparaison est un Dalek
                        if(isinstance(self.liste_objets[j], Dalek)):
                            self.liste_objets.append(Ferraille(self.liste_objets[i].x, self.liste_objets[i].y))
                            self.points += self.liste_objets[i].valeurPoint
                            self.liste_objets.pop(i)
                            self.points += self.liste_objets[j].valeurPoint
                            self.liste_objets.pop(j)
                            break
                            
                        #Si l'objet de comparaison est une Ferraille
                        elif(isinstance(self.liste_objets[j], Ferraille)):
                            self.points += self.liste_objets[i].valeurPoint
                            self.liste_objets.pop(i)
                            break
                                         
                                  
#Classe pour les objets qui seront dans la surface de jeu 
class DrWho:
    def __init__(self, x, y):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y #Position en y sur la surface de jeu
        self.nb_zapper = 0 #Nombre de zapper dont a droit Dr Who
        self.apparence = chr(1) #Caractere d_affichage

    def notDead(self, jeu):
        for i in range(1,jeu.nb_total_objets):
            if(self.x == jeu.liste_objets[i].x and self.y == jeu.liste_objets[i].y):
                return False #veux dire qu_il est morte
            
        return True

    def zapper(self, jeu):

        liste_a_POPER = []      #liste de tous les objets a retirer de la liste

        for i in range(1, jeu.nb_total_objets):
            while aPoper:
                if( (self.x-1 == jeu.liste_objets[i].x and self.y-1 == jeu.liste_objets[i].y) or (self.x-1 == jeu.liste_objets[i].x and self.y == jeu.liste_objets[i].y) or (self.x-1 == jeu.liste_objets[i].x and self.y+1 == jeu.liste_objets[i].y) or (self.x == jeu.liste_objets[i].x and self.y-1 == jeu.liste_objets[i].y) or (self.x == jeu.liste_objets[i].x and self.y-1 == jeu.liste_objets[i].y) or (self.x+1 == jeu.liste_objets[i].x and self.y-1 == jeu.liste_objets[i].y) or (self.x+1 == jeu.liste_objets[i].x and self.y == jeu.liste_objets[i].y) or (self.x+1 == jeu.liste_objets[i].x and self.y+1 == jeu.liste_objets[i].y)):
                    liste_a_POPER.append(i)

        return liste_a_POPER


    def teleportation(self, jeu):

        position_ko = True
        compteur = 0 # cherche un certain nombre de fois une bonne case puis s_il ne trouve pas, redonne le choix a l'usager quoi faire
        #Tant que la position n'est pas une position valide par rapport a la postion des Daleks
        while position_ko == True:

            position_ko = False

            x = random.randint(1, jeu.surface_l)
            y = random.randint(1, jeu.surface_h)

            compteur +=1

            for i in range(1, jeu.nb_total_objets):
                #Si la case est a au moins deux cases du Dalek
                if ( (x >= jeu.liste_objets[i].x+2 or x <= jeu.liste_objets[0].x-2) or (y >= jeu.liste_objets[0].y+2 or y <= jeu.liste_objets[0].y-2) ):
                        position_ko = True

            if(compteur == 15):
                break
        else:
            self.x = x
            self.y = y
            return True #ca a marcher
        return False    #ca n_a pas marcher





     #Fonction qui gere le deplacement du joueur
    def deplacer(self, jeu):

        deplacement_valide = False
        var = 2

        while deplacement_valide == False:

            key = msvcrt.getch()

            #Variables pour la variation de x et y
            v_x = 0
            v_y = 0
            
            
            #Deplacement vers le bas a gauche
            if(key == b'1'):
                v_x = -var
                v_y = var
            
            #Deplacement vers le bas
            if(key == b'2'):
                v_x = 0
                v_y = var

            #Deplacement vers le bas a droite
            if(key == b'3'):
                v_x = var
                v_y = var

            #Pas de deplacement
            if(key == b'5'):
                v_x = 0
                v_y = 0

            #Depplacement vers la droite
            if(key == b'6'):
                v_x = var
                v_y = 0

            #Deplacement vers le haut a droite
            if(key == b'9'):
                v_x = var
                v_y = -var

            #Deplacement vers le haut
            if(key == b'8'):
                v_x = 0
                v_y = -var

            #Deplacement vers le haut a gauche
            if(key == b'7'):
                v_x = -var
                v_y = -var

            #Deplacement vers la gauche
            if(key == b'4'):
                v_x = -var
                v_y = 0 

            #Teleportation
            if(key == b'x'):
                print('')
                           
            #Zappeur
            if(key == b'z'):
                print('')
            
            #Determine si le deplacement sera a l'interieur de la zone de jeu
            if(jeu.liste_objets[0].x+v_x <= jeu.surface_l and jeu.liste_objets[0].y+v_y <= jeu.surface_h and jeu.liste_objets[0].x+v_x >= 0 and jeu.liste_objets[0].y+v_y >= 0):
                deplacement_valide = True
            
            for i in range(1, jeu.nb_total_objets):
                #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
                if(jeu.liste_objets[0].x+v_x == jeu.liste_objets[i].x and jeu.liste_objets[0].y+v_y == jeu.liste_objets[i].y):
                    deplacement_valide = False
        
        #Change la position du Docteur Who lorsque le deplacement est valide       
        jeu.liste_objets[0].x += v_x
        jeu.liste_objets[0].y += v_y

        return key


class Dalek:
    def __init__(self, x, y, valeurPoint):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y; #Position en y sur la surface de jeu
        self.valeurPoint = valeurPoint
        self.apparence = chr(177) #Caractere d_affichage
        #possibilite d'ajouter des attributs de "super dalek"

    #Fonction qui gere le deplacement des daleks
    def deplacer(self, jeu):

        #Variables pour la variation de x et y
        v_x = 0
        v_y = 0
        
        #Variation des x
        #Si la position x du Docteur est plus grande
        if(jeu.liste_objets[0].x > self.x):
            v_x = 1

        #Si la position x du Docteur est plus petite
        elif(jeu.liste_objets[0].x < self.x):
            v_x = -1

        #Variation des y
        #Si la position y du Docteur est plus grande
        if(jeu.liste_objets[0].y > self.y):
            v_y = 1

        #Si la position y du Docteur est plus petite
        elif(jeu.liste_objets[0].y < self.y):
            v_y = -1

        self.x += v_x
        self.y += v_y


class Ferraille:
    def __init__(self, x, y):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y; #Position en y sur la surface de jeu
        self.apparence = '#' #Caractere d_affichage


#Tout le code suivant a ete pris sur internet a cette addresse : http://code.activestate.com/recipes/134892/
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


    

class Controleur:

    def __init__(self):
        self.jeu = Jeu()
        self.vue = Vue()
        #os.system('mode con:cols=30 lines=40')
        os.system('mode con:cols=120 lines=60')

    def main(self):
        #call du menu
        retourMenu = 0 #fonction menu ICI
        if (retourMenu == 0):
            self.gameLOOP()
        elif (retourMenu == 1):
            pass #do something
        elif (retourMenu == 2):
            pass #do something
        elif (retourMenu == 3):
            pass #do something

        return 0

    def gameLOOP(self):

        self.jeu.setNextVague()
        self.vue.splashNiveau(self.jeu)
        drWhoIsNotDead = True

        while drWhoIsNotDead:
            #Verifie si il ne reste plus de daleks ou verifie si le joueur a ete capturer
            while (drWhoIsNotDead == True and self.jeu.nb_dalek_restant != 0):
                self.runLevel()
                self.jeu.denombreDalek()
                drWhoIsNotDead = self.jeu.liste_objets[0].notDead(self.jeu)
                
                
                if(self.jeu.nb_dalek_restant == 0):
                    #Preparation de la prochaine vague, incremente les dalek, zappeur, et autre goodies.
                    #et cree une liste d'objet contenant les dalek et le docteur
                    self.jeu.setNextVague()
            
        else:
            self.endGame()


    def runLevel(self):
        #Affichage de la surface de jeu 
        self.vue.afficher(self.jeu)
        
        aFontionner = False #Afin de stocker le retour de la teleportation
        while (not aFontionner):
            
            aFontionner = True
            
            #Deplacement du joueur
            retour = self.jeu.liste_objets[0].deplacer(self.jeu) #retourne la touche appuyer par le joueur
        
            if(retour == b'x'):#teleportation
                aFontionner = self.jeu.liste_objets[0].teleportation()

            elif(retour == b'z'):#zappeur
                self.jeu.suppressionDalek(  self.jeu.liste_objets[0].zapper()  , False)#suppressionDalek supprime les elements qui sont retourner par la fonction qu_elle a en parametre (le zap de drwho) 
                self.vue.zapAnimation(self.jeu) #Affichage du zap sur l'espace de jeu

        #Affichage de la surface de jeu
        self.vue.afficher(self.jeu)

        """#Afficher les positions
        for i in range(0, self.jeu.nb_total_objets):
            print(self.jeu.liste_objets[i].x, self.jeu.liste_objets[i].y)"""
        time.sleep(0.5)
        
        #Deplacement automatique des Daleks
        self.jeu.deplacerDalek(self.jeu)

        #Verifie les collisions
        self.jeu.collision()
       
       
        

    def endGame(self):
        os.system('cls')
        print('GAME OVER !!!')
        print('')
        print('Vague : '+str(self.jeu.vague))
        print('Points : '+str(self.jeu.points))
        msvcrt.getch()


if __name__ == "__main__":
    c = Controleur()
    sys.exit(c.main())
