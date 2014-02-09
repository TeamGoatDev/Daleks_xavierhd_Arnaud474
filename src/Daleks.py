import random
import os
import msvcrt

#Declaration des variables

game_over = false	#Determine si la partie est terminee ou non
level_complete = false	#Condition pour determiner si le niveau est complete
points = 0	#Variable qui contient le nombre de points accumules par le joueur
vague = 1	#Numero de la vague en cours
surface_l = 20	#Largeur de la surface de jeu
surface_h = 30	#Hauteur de la surface de jeu
nb_total_dalek = 5	#Nombre total de Dalek pour la vague courrante
nb_dalek_restant = 0 #Nombre de Dalek restant sur la surface de jeu
liste_objets = [] #Liste qui contiendra les daleks et le docteur



#Classe pour les objets qui seront dans la surface de jeu 
class Piece:

    def __init__(self, nom, type_piece, x, y):
        self.nom = nom  #Nom de la piece Ex: Dalek1, Dalek2, Dalek3 etc.
        self.type_piece = type_piece	#Type de piece (0 = Dalek, 1 = Ferraile et 2 = Docteur Who)
        self.x = x	#Position en x sur la surface de jeu 
        self.y = y	#Position en y sur la surface de jeu 



#Fonction qui initialise la list contenant les objets(Personnages) pour le jeu (largeur de la surface, hauteur de la surface, nombre de daleks au total, liste qui contient les objets)
def creerListe(largeur, hauteur, daleks, liste):
    
    position_ok = false
    position_xy = false

    #Creation de variables temporaires pour les postions x et y de chaque piece
    x = 0	# 1 est la premiere case contrairement a 0 dans un tableau
    y = 0	# 1 est la premiere case contrairement a 0 dans un tableau
    
    liste[:] = [] #Vide l'ancienne liste d'objets
 
    #Initialisation de la piece du joueur
    x = random.randint(1, largeur)
    y = random.randint(1, hauteur)
    liste.append(Piece("Docteur Who", 2, x, y))

    #Creation de la liste en fonction du nombre total de dalek pour cette vague
    for i in range(0, daleks):
    	
        position_ok = false
        
        #Tant que la position n'est pas une position valide par rapport a la postion du Docteur et n'est pas occupee
        while position_ok != true:

            #Regarde tout d'abord si la position n'est pas deja occupee par une autre piece
       	    while position_xy != true:

                x = random.randint(1, largeur)
                y = random.randint(1, hauteur)

                for n in range(0,len(liste)):
                    if(x != liste[n].x and y != liste[n].y):
                        position_xy = true

            #Replace le position_xy a false au cas ou on devrait retester si position_ok n'est pas true
            position_xy = false

            #Si la case est a deux cases du Docteur Who
            if (x >= (liste[0].x+2) or x <= (liste[0].x-2)):
                if (y >= (liste[0].y+2) or y <= (liste[0].y-2)):
                    position_ok = true


    	#Ajoute un Dalek valide a la liste
        liste.append(Piece("Dalek"+str(i+1), 0, x, y))

#Fonction qui fait l'affichage de jeu dans la console        
def afficherJeu(largeur, hauteur, liste, daleks):

    #Nettoye l'ecran avant d'afficher le jeu de nouveau
    os.system('cls')

    #Affichage du terrain vide
    for i in range(0,hauteur):
        for j in range(0, largeur):
            #Regarde dans la liste si il y a un element  a cette position
            for n in range(0, daleks+1):
                
                #Si la case courante corespond a la case de la liste 
                if(j == liste[n].x and i == liste[n].y):
                    #Si c'est un Dalek
                    if(liste[n].type_piece == 0):
                        print(chr(177),end='')
                    #Si c'est un tas de feraille
                    if(liste[n].type_piece == 1):
                        print('#',end='')
                    #Si c'est le docteur who
                    if(liste[n].type_piece == 2):
                        print(chr(1),end='')
                else :
                    print(' ',end='')
        print('')



#Fonction qui gere le deplacement du joueur
def deplacementJoueur(liste, largeur, hauteur, daleks):

    deplacement_valide = false

    #Variables pour la variation de x et y
    v_x = 0
    v_y = 0

    while deplacement_valide != true:

        key = msvcrt.getch()
        
        #Deplacement vers le bas a gauche
        if(key == 1)
            v_x = -1
            v_y = 1
        
        #Deplacement vers le bas
        if(key == 2)
            v_x = 0
            v_y = 1

        #Deplacement vers le bas a droite
        if(key == 3)
            v_x = 1
            v_y = 1

        #Depplacement vers la droite
        if(key == 6)
            v_x = 1
            v_y = 0

        #Deplacement vers le haut a droite
        if(key == 9)
            v_x = 1
            v_y = -1

        #Deplacement vers le haut
        if(key == 8)
            v_x = 0
            v_y = -1

        #Deplacement vers le haut a gauche
        if(key == 7)
            v_x = -1
            v_y = -1

        #Deplacement vers la gauche
        if(key == 4)
            v_x = -1
            v_y = 0 
        
        #Determine is le deplacement sera a l'interieur de la zone de jeu
        if(liste[0].x+v_x > largeur or liste[0].y+v_y > hauteur or liste[0].x+v_x < 0 or liste[0].y+v_y < 0)
            deplacement_valide = false

        #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
        else :

            for i in range(1,daleks+1)

                deplacement_valide = true

                if(liste[0].x+v_x == liste[i].x and liste[0].y+v_y == liste[i].y)
                    deplacement_valide = false
    
    #Changel a position du Docteur Who lorsque le deplacement est valide       
    liste[0].x += v_x
    liste[0].y += v_y


#Fonction qui gere le deplacement des daleks
#def deplacerDalek():
  
    

#Game Loop ------------------------------------------------------------------------------------------------
while game_over != true:
    
    #Creation de la liste pour la nouvelle vague
    creerListe(surface_l, surface_h, nb_total_dalek, liste_objets)
    level_complete = false

    while level_complete != true:

        afficherJeu(surface_l, surface_h, liste_objets, nb_total_dalek)

            
    #Incrementation de la vague lorsqu'une vague est completee
    vague++
        
#----------------------------------------------------------------------------------------------------------
