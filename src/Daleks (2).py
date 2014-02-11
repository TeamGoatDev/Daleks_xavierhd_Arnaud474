import random
import os
import msvcrt
import time

#Declaration des variables

game_over = False   #Determine si la partie est terminee ou non
level_complete = False  #Condition pour determiner si le niveau est complete
points = 0  #Variable qui contient le nombre de points accumules par le joueur
vague = 1   #Numero de la vague en cours
surface_l = 20  #Largeur de la surface de jeu
surface_h = 30  #Hauteur de la surface de jeu
nb_total_dalek = 5  #Nombre total de Dalek pour la vague courrante
nb_total_objets = 0 #Nombre d'elements dans la liste
nb_dalek_restant = 0 #Nombre de Dalek restant sur la surface de jeu
liste_objets = [] #Liste qui contiendra les daleks et le docteur
liste_info = [0,0,False]  #Liste qui continet le nombre de le score, daleks restants, statut du niveau, statut du joeur



#Classe pour les objets qui seront dans la surface de jeu 
class Piece:

    def __init__(self, nom, type_piece, x, y):
        self.nom = nom  #Nom de la piece Ex: Dalek1, Dalek2, Dalek3 etc.
        self.type_piece = type_piece    #Type de piece (0 = Dalek, 1 = Ferraile et 2 = Docteur Who)
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y  #Position en y sur la surface de jeu 



#Fonction qui initialise la list contenant les objets(Personnages) pour le jeu (largeur de la surface, hauteur de la surface, nombre de daleks au total, liste qui contient les objets)
def creerListe(largeur, hauteur, daleks, dalek_restant, liste):
    
    position_ok = False
    position_xy = False

    #Creation de variables temporaires pour les postions x et y de chaque piece
    x = 0   # 1 est la premiere case contrairement a 0 dans un tableau
    y = 0   # 1 est la premiere case contrairement a 0 dans un tableau
    
    daleks_restant = daleks

    liste[:] = [] #Vide l'ancienne liste d'objets
 
    #Initialisation de la piece du joueur
    x = random.randint(1, largeur)
    y = random.randint(1, hauteur)
    liste.append(Piece("Docteur Who", 2, x, y))

    #Creation de la liste en fonction du nombre total de dalek pour cette vague
    for i in range(0, daleks):
        
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

            #Replace le position_xy a false au cas ou on devrait retester si position_ok n'est pas true
            position_xy = False

            #Si la case est a deux cases du Docteur Who
            if (x >= (liste[0].x+2) or x <= (liste[0].x-2)):
                if (y >= (liste[0].y+2) or y <= (liste[0].y-2)):
                    position_ok = True


        #Ajoute un Dalek valide a la liste
        liste.append(Piece("Dalek"+str(i+1), 0, x, y))
    
    
    


#Fonction qui fait l'affichage de jeu dans la console        
def afficherJeu(largeur, hauteur, liste, grandeur_liste):
    
    #Nettoye l'ecran avant d'afficher le jeu de nouveau
    os.system('cls')

    #Affichage du terrain 
    for i in range(0,hauteur+1):
        for j in range(0, largeur+1):

            case_vide = True
            
            #Regarde dans la liste si il y a un element  a cette position
            for n in range(0, grandeur_liste):
                
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

                    case_vide = False
               
            if(case_vide == True):
                print('-',end='')
                
        print('')

    print('')
    print('Points: '+str(liste_info[0]))


#Fonction qui gere le deplacement du joueur
def deplacementJoueur(liste, largeur, hauteur, grandeur_liste):

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
        if(liste[0].x+v_x > largeur or liste[0].y+v_y > hauteur or liste[0].x+v_x < 0 or liste[0].y+v_y < 0):
            deplacement_valide = False

        #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
        else :

            deplacement_valide = True

            for i in range(1, grandeur_liste):

                #Si i y a une piece a l'endroit ou le joueur veut se deplacer
                if(liste[0].x+v_x == liste[i].x and liste[0].y+v_y == liste[i].y):
                    deplacement_valide = False
    
    #Change la position du Docteur Who lorsque le deplacement est valide       
    liste[0].x += v_x
    liste[0].y += v_y


#Fonction qui gere le deplacement des daleks
def deplacerDalek(liste, largeur, hauteur, grandeur_liste, liste_i):
    
    case_libre = False


    #Variables pour la variation de x et y
    v_x = 0
    v_y = 0

    #Regarder chacun des daleks dans la liste
    for i in range(1, grandeur_liste):

        #Si la piece est un dalek
        if(liste[i].type_piece == 0 and liste_i[2] != True):

            v_x = 0
            v_y = 0
            
            #Variation des x

            #Si la position x du Docteur est plus grande
            if(liste[0].x > liste[i].x):
                v_x = 1

            #Si la position x du Docteur est plus petite
            elif(liste[0].x < liste[i].x):
                v_x = -1

            #Si la position x du Docteur est egale
            else:
                v_x = 0

            #Variation des y

            #Si la position y du Docteur est plus grande
            if(liste[0].y > liste[i].y):
                v_y = 1

            #Si la position y du Docteur est plus petite
            elif(liste[0].y < liste[i].y):
                v_y = -1

            #Si la position y du Docteur est egale
            else:
                v_y = 0

            case_libre = True

            #Regarde si la case d'arrivee est occupee
            for j in range(0, grandeur_liste):

                #Si la case contient quelque chose
                if(liste[i].x+v_x == liste[j].x and liste[i].y+v_y == liste[j].y):

                    case_libre = False

                
                    #Si la piece est un tas de ferraille
                    if(liste[j].type_piece == 1):
                        liste.pop(i)
                        liste_i[1] -= 1
                        j = grandeur_liste
                        grandeur_liste = len(liste)
                        liste_i[0] += 5
                        return
        
                    #Si la piece est un Dalek 
                    elif(liste[j].type_piece == 0):
                        liste[j].type_piece = 1
                        liste[j].nom = "Ferraille"
                        liste.pop(i)
                        liste_i[1] -= 2
                        grandeur_liste = len(liste)
                        j = grandeur_liste
                        liste_i[0] += 10
                        return

                    #Si la piece est le Docteur Who
                    elif(liste[j].type_piece == 2):
                        liste_i[2] = True
                        return
                       

                 
            if(case_libre == True):
                liste[i].x += v_x
                liste[i].y += v_y






    
#Game Loop ------------------------------------------------------------------------------------------------
while game_over != True:
    
    #Creation de la liste pour la nouvelle vague
    creerListe(surface_l, surface_h, nb_total_dalek, nb_dalek_restant, liste_objets)
    level_complete = False
    liste_info[1] = nb_total_dalek
    

    while level_complete != True:

        nb_total_objets = len(liste_objets)
        
        #Affichage de la surface de jeu 
        afficherJeu(surface_l, surface_h, liste_objets, nb_total_objets)
        print(liste_info[1])
        
        #Deplacement du joueur
        deplacementJoueur(liste_objets, surface_l, surface_h, nb_total_objets)
        print(liste_objets[0].x,liste_objets[0].y)
        
        afficherJeu(surface_l, surface_h, liste_objets, nb_total_objets)
        time.sleep(0.5)
        
        #Deplacement automatique des Daleks
        deplacerDalek(liste_objets, surface_l, surface_h, nb_total_objets, liste_info)

        #Verifie si le jouer a ete capturer
        game_over = liste_info[2]

        if(game_over == True):
            level_complete = True
         
        #Si il ne reste plus de daleks
        if(liste_info[1] == 0):
            level_complete = True
        

    if(game_over != True):
        vague += 1
        #Augmentation du nombre de Dalek apres chaque vague
        nb_total_dalek += 5
            
        
#----------------------------------------------------------------------------------------------------------

os.system('cls')
print('GAME OVER !!!')
print('')
print('Vague : '+str(vague))
print('Points : '+str(liste_info[0]))
msvcrt.getch()
