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
        for i in range(0,jeu.surface_h+1):
            for j in range(0, jeu.surface_l+1):

                case_vide = True
                
                #Regarde dans la liste si il y a un element  a cette position
                for n in range(0, jeu.nb_total_objets-1):
                    
                    #Si la case courante correspond a la case de la liste
                    if(j == jeu.liste_objets[n].x and i == jeu.liste_objets[n].y):
                        #Si c'est le docteur who
                        if(n==0):
                            print(chr(1),end='')
                        #Si c'est un Dalek
                        elif(isinstance(jeu.liste_objets[n], Dalek)):
                            print(chr(177),end='')
                        #Si c'est un tas de ferraille
                        elif(isinstance(jeu.liste_objets[n], Ferraille)):
                            print('#',end='')
                        
                        case_vide = False
                   
                if(case_vide == True):
                    print('-',end='')
                    
            print('')   #end line

        print('')   #end line
        if(i == 0):
            print('Points: '+jeu.liste_objets.points)


class Jeu:
    def __init__(self):
        self.game_over = False          #Determine si la partie est terminee ou non
        self.level_complete = False     #Condition pour determiner si le niveau est complete
        self.points = 0                 #Variable qui contient le nombre de points accumules par le joueur
        self.vague = 0                  #Numero de la vague en cours
        self.nb_total_dalek = 0         #Nombre total de Dalek pour la vague courrante
        self.nb_total_objets = 0        #Nombre d'elements dans la liste
        self.nb_dalek_restant = 0       #Nombre de Dalek restant sur la surface de jeu
        self.liste_objets = []          #Liste qui contiendra les daleks et le docteur
        self.surface_l = 20             #Largeur de la surface de jeu
        self.surface_h = 30             #Hauteur de la surface de jeu

    def setNextVague(self):
        self.nb_total_dalek += 5
        self.vague += 1
        self.liste_objets[0].nb_zapper += 1
        self.creerListe()                                    #Creation de la liste pour la nouvelle vague
        self.nb_total_objets = len(self.liste_objets)   #Calcule le nombre d'objet dans la liste

    def deplacerDalek(self,jeu):
        for i in range(1, self.nb_total_objets-1): #regarde tout les objets de la liste
                if(isinstance(self.liste_objets[i], Dalek)): #recherche d_objet Dalek
                    self.liste_objets[i].deplacer(jeu)
    
    def denombreDalek(self):
        compteur = 0
        for i in range(1, self.nb_total_objets-1): #regarde tout les objets de la liste
                if(isinstance(self.liste_objets[i], Dalek)): #recherche d_objet Dalek
                    compteur +=1
        return compteur


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
                if (x >= (self.liste_objets[0].x+2) or x <= (self.liste_objets[0].x-2)):
                    if (y >= (self.liste_objets[0].y+2) or y <= (self.liste_objets[0].y-2)):
                        position_ok = True


            #Ajoute un Dalek valide a la liste
            self.liste_objets.append(Dalek(x,y,5))



    #Fonction gerant les collisions des daleks entre eux et les ferrailles
    def collision(self):

        liste_a_POPER = []      #liste de tous les objets a retirer de la liste

        for i in range(1, self.nb_total_objets-1):       #regarde tout les objets de la liste
            if(isinstance(self.liste_objets[i], Dalek)):
                for j in range(1, self.nb_total_objets-1):   #regarde tout les objets de la liste afin de comparer
                    if(i != j): #les deux objets ne doivent pas etre le meme
                        if(self.liste_objets[i].x == self.liste_objets[j].x and self.liste_objets[i].y == self.liste_objets[j].y): #Verifie si les deux pieces sont sur la meme case
                            self.points += self.liste_objets[i].valeurPoint #ajout des points au total
                            liste_a_POPER.append(i) #ajout a la liste de suppression

        for i in range(1, len(liste_a_POPER)-1):
            self.liste_objets.append( Ferraille(self.liste_objets[liste_a_POPER[i]].x, self.liste_objets[liste_a_POPER[i]].y) )
            self.liste_objets.pop(liste_a_POPER[i])

"""Criss de gros boute de code qui revient a faire ce qui est juste au dessus... (vive les dessins)
        
        for i in range(1, nb_total_objets-1):      #regarde tout les objets de la liste
            if(isinstance(jeu.liste_objets[i]),Dalek): #On veux seulement des dalek pour l_objet i
                for j in range(1, nb_total_objets-1):#regarde tout les objets de la liste afin de comparer
                    if(i != j): #les deux objets ne doivent pas etre le meme
                        if(self.liste_objets[i].x == self.liste_objets[j].x and self.liste_objets[i].y == self.liste_objets[j].y): #Verifie si les deux pieces sont sur la meme case
                            if(len(liste_a_POPER) > 0): #verifie s_il y a des element dans la liste de suppression
                                jOK = True
                                iOK = True
                                for k in range(0, len(liste_a_POPER)-1):  #-1 est un moyen broche a foin de faire marcher cette fonction (sinon il ne rentre pas une seul fois dans aucune de ces verification)
                                    if(j != liste_a_POPER[k]):
                                        jOK = False #Afin de savoir si j est a supprimer et vaux des points
                                    if(i != liste_a_POPER[k]):
                                        iOK = False #Afin de savoir si i est a supprimer et vaux des points

 
                        #Si la piece est un tas de ferraille
                        if(isinstance(jeu.liste_objets[j]),Ferraille and iOK == True):
                            liste_a_POPER.append(i) #ajout a la liste de suppression
                            jeu.points += jeu.liste_objets[i].valeurPoint #ajout des points au total
                            
            
                        #Si la piece est un Dalek 
                        elif(isinstance(jeu.liste_objets[j]),Dalek and jOK == True and iOK == True):
                            liste_a_POPER.append(i) #ajout a la liste de suppression
                            self.liste_objets.append(Ferraille(self.liste_objets[i].x, self.liste_objets[i].y))#ajout d_une ferraille
                            jeu.points += jeu.liste_objets[i].valeurPoint    #ajout des points au total
                    
                        elif(jOK == False and iOK == True): #pas besoin de verifier le type d_objet, je te gage 10 piastre que c_est un dalek
                            liste_a_POPER.append(i) #ajout a la liste de suppression
                            jeu.points += jeu.liste_objets[i].valeurPoint    #ajout des points au total

        for i in range(1, len(liste_a_POPER)-1)
            self.jeu.liste_objets.append( Ferraille(self.jeu.liste_objets[liste_a_POPER[i]].x, self.jeu.liste_objets[liste_a_POPER[i]].y) )
            self.jeu.liste_objets.pop(liste_a_POPER[i])               
            
"""

#Classe pour les objets qui seront dans la surface de jeu 
class DrWho:
    def __init__(self, x, y):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y; #Position en y sur la surface de jeu
        self.nb_zapper = 0 #Nombre de zapper dont a droit Dr Who

    def is_dead(self, jeu):
        for i in range(1,len(jeu.liste_objets-1)):
            if(self.x == jeu.liste_objets[i].x and self.y == jeu.liste_objets[i].y):
                return True #veux dire qu_il est mort

     #Fonction qui gere le deplacement du joueur
    def deplacer(self, jeu):

        deplacement_valide = False

        #Variables pour la variation de x et y
        v_x = 0
        v_y = 0

        while deplacement_valide != True:

            key = msvcrt.getch()
            
            
            #Deplacement vers le bas a gauche
            if(key == b'1'):
                v_x = -1
                v_y = 1
            
            #Deplacement vers le bas
            if(key == b'2'):
                v_x = 0
                v_y = 1

            #Deplacement vers le bas a droite
            if(key == b'3'):
                v_x = 1
                v_y = 1

            #Pas de deplacement
            if(key == b'5'):
                v_x = 0
                v_y = 0

            #Depplacement vers la droite
            if(key == b'6'):
                v_x = 1
                v_y = 0

            #Deplacement vers le haut a droite
            if(key == b'9'):
                v_x = 1
                v_y = -1

            #Deplacement vers le haut
            if(key == b'8'):
                v_x = 0
                v_y = -1

            #Deplacement vers le haut a gauche
            if(key == b'7'):
                v_x = -1
                v_y = -1

            #Deplacement vers la gauche
            if(key == b'4'):
                v_x = -1
                v_y = 0 

            #Teleportation
            if(key == b'/'):
                print('')
                           
            #Zappeur
            if(key == b'*'):
                print('')
            
            #Determine is le deplacement sera a l'interieur de la zone de jeu
            if(jeu.liste_objets[0].x+v_x > jeu.surface_l or jeu.liste_objets[0].y+v_y > jeu.surface_h or jeu.liste_objets[0].x+v_x < 0 or jeu.liste_objets[0].y+v_y < 0):
                deplacement_valide = False

            #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
            else :

                deplacement_valide = True

                for i in range(1, jeu.nb_total_objets):

                    #Si i y a une piece a l'endroit ou le joueur veut se deplacer
                    if(jeu.liste_objets[0].x+v_x == jeu.liste_objets[i].x and jeu.liste_objets[0].y+v_y == jeu.liste_objets[i].y):
                        deplacement_valide = False
        
        #Change la position du Docteur Who lorsque le deplacement est valide       
        jeu.liste_objets[0].x += v_x
        jeu.liste_objets[0].y += v_y






class Dalek:
    def __init__(self, x, y, valeurPoint):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y; #Position en y sur la surface de jeu
        self.valeurPoint = valeurPoint
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

    def gameLOOP(self):

        #Cree la liste
        self.jeu.creerListe()

        #Preparation de la vague, increment les dalek, zappeur, et autre goodies. Cree une liste d'objet contenant les dalek et le docteur
        self.jeu.setNextVague()
        
        while self.jeu.denombreDalek() != 0 or not self.jeu.liste[0].is_dead():#Verifie si il ne reste plus de daleks ou #Verifie si le joueur a ete capturer

            #Affichage de la surface de jeu 
            self.vue.afficher(self.jeu)
            
            #Deplacement du joueur
            self.jeu.liste_objets[0].deplacer(self.jeu)
            
            #Affichage de la surface de jeu 
            self.vue.afficher(self.jeu)
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
        print('Points : '+str(self.jeu.Points))
        msvcrt.getch()

        


if __name__ == "__main__":
    c = Controleur()
    sys.exit(c.main())