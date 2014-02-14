import random
import os
import msvcrt
import time

#Declaration des objets

class Jeu:
    def __init__(self):
        self.game_over = False          #Determine si la partie est terminee ou non
        self.level_complete = False     #Condition pour determiner si le niveau est complete
        self.points = 0                 #Variable qui contient le nombre de points accumules par le joueur
        self.vague = 0                  #Numero de la vague en cours
        self.surface_l = 20             #Largeur de la surface de jeu
        self.surface_h = 30             #Hauteur de la surface de jeu
        self.nb_total_dalek = 0         #Nombre total de Dalek pour la vague courrante
        self.nb_total_objets = 0        #Nombre d'elements dans la liste
        self.nb_dalek_restant = 0       #Nombre de Dalek restant sur la surface de jeu
        self.liste_objets = []          #Liste qui contiendra les daleks et le docteur
        self.drWho = DrWho(random.randint(1, self.surface_l), random.randint(1, self.surface_h))  #Messieurs mesdames, je vous presente Dr. Who!  (Initialisation de la piece du joueur)


    def setNextVague(self):
        self.nb_total_dalek += 5
        self.vague += 1
        self.drWho.nb_zapper += 1
        self.creerListe()                                    #Creation de la liste pour la nouvelle vague
        self.nb_total_objets = len(self.liste_objets)   #Calcule le nombre d'objet dans la liste






    #Fonction qui initialise la list contenant les objets(Personnages) pour le jeu (largeur de la surface, hauteur de la surface, nombre de daleks au total, liste qui contient les objets)
    def creerListe(self):
    
        position_ok = False
        position_xy = False

        #Creation de variables temporaires pour les postions x et y de chaque piece
        x = 0   # 1 est la premiere case contrairement a 0 dans un tableau
        y = 0   # 1 est la premiere case contrairement a 0 dans un tableau
        
        self.nb_dalek_restant = self.nb_total_dalek

        self.liste_objets[:] = [] #Vide l'ancienne liste d'objets
     
        #Creation d'une position au hasard pour le docteur
        self.drWho.x = random.randint(1, self.surface_l)
        self.drWho.y = random.randint(1, self.surface_h)

        #ajout du dr who a la liste
        self.liste_objets.append(self.drWho)

        #Creation de la liste en fonction du nombre total de dalek pour cette vague
        for i in range(0, self.nb_total_dalek):
            
            position_ok = False
            
            #Tant que la position n'est pas une position valide par rapport a la postion du Docteur et n'est pas occupee
            while position_ok != True:

                #Replace le position_xy a false au cas ou on devrait retester si position_ok n'est pas true
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
            self.liste_objets.append(Dalek(x,y)






    #Fonction qui fait l'affichage de jeu dans la console
    def afficher(self):
    
        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain 
        for i in range(0,hauteur+1):
            for j in range(0, largeur+1):

                case_vide = True
                
                #Regarde dans la liste si il y a un element  a cette position
                for n in range(0, nb_total_objets):
                    
                    #Si la case courante corespond a la case de la liste 
                    if(j == self.liste_objets[n].x and i == self.liste_objets[n].y):
                        #Si c'est un Dalek
                        if(self.liste_objets[n].type_piece == 0):
                            print(chr(177),end='')
                        #Si c'est un tas de feraille
                        if(self.liste_objets[n].type_piece == 1):
                            print('#',end='')
                        #Si c'est le docteur who
                        if(self.liste_objets[n].type_piece == 2):
                            print(chr(1),end='')

                        case_vide = False
                   
                if(case_vide == True):
                    print('-',end='')
                    
            print('')

        print('')
        print('Points: '+self.liste_objets.points)



    #Fonction gerant les collisions des daleks entre eux et les ferrailles
    def collision(self):
        liste_a_POPER = []      #liste de tous les objets a retirer de la liste
        unChiffre = -1          #-1 est un moyen broche a foin de faire marcher cette fonction
        for i in range(1, nb_total_objets):      #regarde tout les objets de la liste
            if(isinstance(jeu.liste_objets[i]),Dalek): #On veux seulement des dalek pour l_objet i
                for j in range(1, nb_total_objets):#regarde tout les objets de la liste afin de comparer
                    if(i != j): #les deux objets ne doivent pas etre le meme
                        if(self.liste_objets[i].x == self.liste_objets[j].x and self.liste_objets[i].y == self.liste_objets[j].y): #Verifie si les deux pieces sont sur la meme case
                            if(len(liste_a_POPER) > 0): #verifie s_il y a des element dans la liste de suppression
                                unChiffre = 0           
                                jOK = True
                                iOK = True
                            for k in range(unChiffre, len(liste_a_POPER)-1):  #-1 est un moyen broche a foin de faire marcher cette fonction (sinon il ne rentre pas une seul fois dans aucune de ces verification)
                                if(j != liste_a_POPER[k]): #verifie que j n_est pas un objet a supprimer
                                    jOK = False #Afin de savoir si j est a supprimer et vaux des points
                                if(i != liste_a_POPER[k]):
                                    iOK = False #Afin de savoir si i est a supprimer

                            
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
                    


#Classe pour les objets qui seront dans la surface de jeu 
class DrWho:
    def __init__(self, x, y):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y; #Position en y sur la surface de jeu
        self.nb_zapper = 0 #Nombre de zapper dont a droit Dr Who

    def is_he_dead(jeu):
        for i in range(1,len(jeu.liste_objets-1)):
            if(self.x == jeu.liste_objets[i].x and self.y == jeu.liste_objets[i].y):
                return True #veux dire qu_il est mort

     #Fonction qui gere le deplacement du joueur
    def deplacer(jeu):

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
            if(key == b'5'):
                print('')
                           
            #Zappeur
            if(key == b'*'):
                print('')
            
            #Determine is le deplacement sera a l'interieur de la zone de jeu
            if(jeu.liste_objets[0].x+v_x > largeur or jeu.liste_objets[0].y+v_y > hauteur or jeu.liste_objets[0].x+v_x < 0 or jeu.liste_objets[0].y+v_y < 0):
                deplacement_valide = False

            #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
            else :

                deplacement_valide = True

                for i in range(1, nb_total_objets):

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
    def deplacer(jeu):

        #Variables pour la variation de x et y

        v_x = 0
        v_y = 0
        
        #Variation des x

        #Si la position x du Docteur est plus grande
        if(jeu.liste_objets[0].x > super.x):
            v_x = 1

        #Si la position x du Docteur est plus petite
        elif(jeu.liste_objets[0].x < super.x):
            v_x = -1

        #Si la position x du Docteur est egale
        else:
            v_x = 0

        #Variation des y

        #Si la position y du Docteur est plus grande
        if(jeu.liste_objets[0].y > super.y):
            v_y = 1

        #Si la position y du Docteur est plus petite
        elif(jeu.liste_objets[0].y < super.y):
            v_y = -1

        #Si la position y du Docteur est egale
        else:
            v_y = 0

        jeu.liste_objets[i].x += v_x
        jeu.liste_objets[i].y += v_y


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


    
#Game Loop ------------------------------------------------------------------------------------------------

jeu = Jeu()

level_complete = False

while level_complete != True:

    #Preparation de la vague, increment les dalek, zappeur, et autre goodies. Cree une liste d'objet contenant les dalek et le docteur
    jeu.setNextVague()
    #Affichage de la surface de jeu 
    jeu.afficher()
    print(liste_info[1])
    
    #Deplacement du joueur
    jeu.liste[0].deplacer(jeu)
    print(liste_objets[0].x,liste_objets[0].y)
    
    #Affichage de la surface de jeu 
    jeu.afficher()
    time.sleep(0.5)
    
    #Deplacement automatique des Daleks
    for i in range(1, nb_total_objets): #regarde tout les objets de la liste
        if(isinstance(jeu.liste[i], Dalek)): #recherche d_objet Dalek
            jeu.liste[i].deplacer(jeu)

    #Verifie les collisions
    jeu.collision()

    #Verifie si le joueur a ete capturer
    jeu.liste[0].is_he_dead()
     
    #Verifie si il ne reste plus de daleks
    
        
            
        
#----------------------------------------------------------------------------------------------------------

os.system('cls')
print('GAME OVER !!!')
print('')
print('Vague : '+str(vague))
print('Points : '+str(liste_info[0]))
msvcrt.getch()