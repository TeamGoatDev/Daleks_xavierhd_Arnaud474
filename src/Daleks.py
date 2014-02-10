import random
import os
import msvcrt

#Declaration des variables


points = 0	#Variable qui contient le nombre de points accumules par le joueur


liste_objets = [] #Liste qui contiendra les daleks et le docteur


class Jeu:

    nb_total_dalek = 0  #Nombre total de Dalek pour la vague courrante
    nb_dalek_restant = 0 #Nombre de Dalek restant sur la surface de jeu

    def __init__(self):
        self.game_over = False #Determine si la partie est terminee ou non
        self.level_complete = False  #Condition pour determiner si le niveau est complete
        self.vague = 0   #Numero de la vague en cours
        self.surface_l = 20  #Largeur de la surface de jeu
        self.surface_h = 30  #Hauteur de la surface de jeu
        drWho = DrWho(getPositionHazard(self.surface_l), getPositionHazard(self.surface_h))
    
    

    #Fonction qui initialise la list contenant les objets(Personnages) pour le jeu (largeur de la surface, hauteur de la surface, nombre de daleks au total, liste qui contient les objets)
    def creerListe(largeur, hauteur, dalekTotal, liste):
        
        position_ok = False
        position_xy = False

        #Creation de variables temporaires pour les postions x et y de chaque piece
        x = 0   # 1 est la premiere case contrairement a 0 dans un tableau
        y = 0   # 1 est la premiere case contrairement a 0 dans un tableau
        drWho = liste[0]
        liste[:] = [] #Vide l'ancienne liste d'objets
     
        #Initialisation de la piece du joueur

        liste.append(drWho)

        #Creation de la liste en fonction du nombre total de dalek pour cette vague
        for i in range(0, dalekTotal):
            
            position_ok = False
            
            #Tant que la position n'est pas une position valide par rapport a la postion du Docteur et n'est pas occupee
            while position_ok != True:

                #Regarde tout d'abord si la position n'est pas deja occupee par une autre piece
                while position_xy != True:

                    x = random.randint(1, largeur)
                    y = random.randint(1, hauteur)

                    for n in range(0,len(liste)):
                        if(x != liste[n].x and y != liste[n].y):
                            position_xy = True

                #Replace le position_xy a False au cas ou on devrait retester si position_ok n'est pas True
                position_xy = False

                #Si la case est a deux cases du Docteur Who
                if (x >= (liste[0].x+2) or x <= (liste[0].x-2)):
                    if (y >= (liste[0].y+2) or y <= (liste[0].y-2)):
                        position_ok = True


            #Ajoute un Dalek valide a la liste
            liste.append(Piece("Dalek"+str(i+1), 0, x, y))

    def setNextVague():
        self.nb_total_dalek += 5
        self.vague += 1
        drWho.nb_zapper += 1

class Vue():
    #def __init__(self, arg):   --Rien encore pour l'instant

    #Fonction qui fait l'affichage de jeu dans la console        
    def afficherJeu(largeur, hauteur, liste, dalekTotal):

        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain vide
        for i in range(0,hauteur):
            for j in range(0, largeur):
                #Regarde dans la liste si il y a un element  a cette position
                for n in range(0, dalekTotal+1):
                    
                    #Si la case courante correspond a la case de la liste 
                    if(j == liste[n].x and i == liste[n].y):
                        #Si c'est un Dalek
                        if isinstance (liste[n], Dalek):
                            print chr(177),
                        #Si c'est un tas de ferraille
                        if isinstance (liste[n], Ferraille):
                            print '#',
                        #Si c'est le docteur who
                        if isinstance (liste[n], DrWho):
                            print chr(1),
                    else :
                        print ' ',
            print('')


#Classe pour les objets qui seront dans la surface de jeu 
class Piece:
    def __init__(self, x, y):
        self.x = x	#Position en x sur la surface de jeu 
        self.y = y;	#Position en y sur la surface de jeu
        
        #Fonction qui retourne un chiffre entre 1 et le max donne en parametre 
        def getPositionHazard(maximum):
            return random.randint(1, maximum)


class DrWho(Piece):
    def __init__(self, x, y):
        super(x, y)
        self.nb_zapper = 0 #Nombre de zapper dont a droit Dr Who


class Dalek(Piece):
    def __init__(self, x, y):
        super(x,y);
        #possibilite d'ajouter des attributs de "super dalek"

class Ferraille(Piece):
    def __init__(self, x, y):
        super(x,y);









#Fonction qui gere le deplacement du joueur
def deplacementJoueur(liste, largeur, hauteur, dalekTotal):

    deplacement_valide = False

    #Variables pour la variation de x et y
    v_x = 0
    v_y = 0

    while deplacement_valide != True:

        key = msvcrt.getch()
        
        #Deplacement vers le bas a gauche
        if(key == 1):
            v_x = -1
            v_y = 1
        
        #Deplacement vers le bas
        if(key == 2):
            v_x = 0
            v_y = 1

        #Deplacement vers le bas a droite
        if(key == 3):
            v_x = 1
            v_y = 1

        #Depplacement vers la droite
        if(key == 6):
            v_x = 1
            v_y = 0

        #Deplacement vers le haut a droite
        if(key == 9):
            v_x = 1
            v_y = -1

        #Deplacement vers le haut
        if(key == 8):
            v_x = 0
            v_y = -1

        #Deplacement vers le haut a gauche
        if(key == 7):
            v_x = -1
            v_y = -1

        #Deplacement vers la gauche
        if(key == 4):
            v_x = -1
            v_y = 0 
        
        #Determine is le deplacement sera a l'interieur de la zone de jeu
        if(liste[0].x+v_x > largeur or liste[0].y+v_y > hauteur or liste[0].x+v_x < 0 or liste[0].y+v_y < 0):
            deplacement_valide = False

        #Determine s'il y a une piece sur l'endroit ou le joueur veut se deplacer
        else :

            for i in range(1,dalekTotal+1):

                deplacement_valide = True

                if(liste[0].x+v_x == liste[i].x and liste[0].y+v_y == liste[i].y):
                    deplacement_valide = False
    
    #Change la position du Docteur Who lorsque le deplacement est valide       
    liste[0].x += v_x
    liste[0].y += v_y


#Fonction qui gere le deplacement des daleks
def deplacerDalek(liste, largeur, hauteur, dalekRestant):
    for i in range(dalekRestant)



  
#Game Loop ------------------------------------------------------------------------------------------------
def main():

    jeu = Jeu()

    while jeu.game_over != True:

        #Creation de la liste pour la nouvelle vague
        jeu.setNextVague()
        jeu.creerListe(surface_l, surface_h, nb_total_dalek, liste_objets)
        level_complete = False

        while level_complete != True:

            jeu.afficherJeu(surface_l, surface_h, liste_objets, nb_total_dalek)
            deplacementJoueur(liste_objets, surface_l, surface_h)
        
        
#----------------------------------------------------------------------------------------------------------
main()