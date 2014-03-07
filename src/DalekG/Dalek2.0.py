from tkinter import *
import random
import os
import sys
import msvcrt
import time

class Vue2:
    def __init__(self,parent):
        self.parent = parent

        #Parametres de la fenetre
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("Dalek Vs. Dr Who")
        self.root.geometry("1200x800")

        #Update la grosseur du frame pour qu'on puisse utiliser winfo
        self.root.update()

        #Background pour le menu
        self.imageBackground = PhotoImage(file="bg.gif")    
        self.labelBackground = Label(self.root,image=self.imageBackground)

        #Offset Y
        self.offSetY = 20

        #Size des pieces
        self.sizePieces = 32

        #Surface de jeu
        self.imageSurface = PhotoImage(file="space.gif")
        self.imageDalek = PhotoImage(file="dalek.gif")
        self.imageDrWho = PhotoImage(file="drwho.gif")
        self.imageFerraille = PhotoImage(file="ferraille.gif")
        self.surfaceJeu = Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), bg="black")
        self.surfaceJeu.bind('<Button-1>', self.getUserInputCode)
        


        #Loading des images explosives
        self.listeImage = []
        for ii in range(1,16):
            self.listeImage.append(PhotoImage(file="explosion"+ str(ii) + ".gif"))
            print("explosion"+ str(ii) + ".gif")
        
        self.listeImageOriginal = self.listeImage
        self.imageSurfaceOriginal = self.imageSurface
        self.imageDalekOriginal = self.imageDalek
        self.imageDrWhoOriginal = self.imageDrWho
        self.imageFerrailleOriginal = self.imageFerraille
        
        #Variable pour que les boutons soient tous de la meme grosseur
        self.buttonWidth= 400
        
        self.boutonJouer = Button(self.root, text='Jouer',width=50, bg='black', fg='white',activebackground='black', activeforeground='white',command=self.parent.newGame)
        self.boutonInstructions = Button(self.root, text='Instructions',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command=self.instruction)
        self.boutonHighscore = Button(self.root, text='Highscore',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command= lambda: self.highScore(self.parent.jeu.getHighScore()))
        self.boutonAbout = Button(self.root, text='About',width=50, bg='black', fg='white',activebackground='black', activeforeground='white',command=self.about)
        self.boutonQuitter = Button(self.root, text='Quitter',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command=self.root.destroy)
        self.boutonRetourMenu = Button(self.root, text='Retour au menu', width=100, bg='black', fg='white',activebackground='black', activeforeground='white', command=self.menu)
        self.boutonTeleportation = Button(self.root, text='Teleportation', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= lambda: self.parent.turn(10))
        self.boutonZappeur = Button(self.root, text='Zappeur', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= lambda: self.parent.turn(11))

        
        self.textBox = Text(width=self.root.winfo_width(), bg='black', fg='white', font=('Arial', 18))
        self.gameOver = Text(width=self.root.winfo_width(), bg='black', fg='white', font=('Arial', 40))
    

    """
    Ceci est fonctionnel, mais je ne sais pas si c_est vraiment utile au programme.
    def changerSizePiece(self, mod1, mod2):
        self.sizePieces = self.sizePieces * mod1/mod2
        for ii in range(0,15):
            self.listeImage[ii] = self.listeImage[ii].zoom(mod1,mod1)
            self.listeImage[ii] = self.listeImage[ii].subsample(mod2,mod2)

        self.imageSurface = self.imageSurface.zoom(mod1,mod1)
        self.imageDalek = self.imageDalek.zoom(mod1,mod1)
        self.imageDrWho = self.imageDrWho.zoom(mod1,mod1)
        self.imageFerraille = self.imageFerraille.zoom(mod1,mod1)
        self.imageSurface = self.imageSurface.subsample(mod2,mod2)
        self.imageDalek = self.imageDalek.subsample(mod2,mod2)
        self.imageDrWho = self.imageDrWho.subsample(mod2,mod2)
        self.imageFerraille = self.imageFerraille.subsample(mod2,mod2)

    def resetSizePiece(self):
        self.listeImage = self.listeImageOriginal
        self.imageSurface = self.imageSurfaceOriginal
        self.imageDalek = self.imageDalekOriginal
        self.imageDrWho = self.imageDrWhoOriginal
        self.imageFerraille = self.imageFerrailleOriginal"""

    def afficher(self, jeu):
        
        #Effacage initial du frame pour pouvoir 
        self.effacerFrame()
        
        #Creation de l'image pour la surface de jeu et ajout du canevas
        self.surfaceJeu.create_image(0,0, anchor=NW, image=self.imageSurface)

        #Test pour la premiere position ainsi que le fonctionnement d'une image dans un canevas
        #self.surfaceJeu.create_image(self.trouverDepartX(), 100, anchor=NW, image=self.imageDalek)

        self.surfaceJeu.place(x=-1, y=-1)

        for y in range(0, self.parent.jeu.surface_h):
            for x in range(0, self.parent.jeu.surface_l):

                case_vide = True
                
                #Regarde dans la liste si il y a un element a cette position
                for n in range(0, self.parent.jeu.nb_total_objets):
                    
                    #Si la case courante correspond a la case de la liste
                    if(x == self.parent.jeu.liste_objets[n].x and y == self.parent.jeu.liste_objets[n].y):
                        print(self.parent.jeu.liste_objets[n].x, self.parent.jeu.liste_objets[n].y)
                        
                        #Si c'est le docteur who
                        if(isinstance(self.parent.jeu.liste_objets[n], DrWho)):
                            self.surfaceJeu.create_image(self.trouverDepartX()+(x*self.sizePieces), self.offSetY+(y*self.sizePieces), anchor=NW, image=self.imageDrWho)
                            
                        #Si c'est un Dalek
                        elif(isinstance(self.parent.jeu.liste_objets[n], Dalek)):
                            self.surfaceJeu.create_image(self.trouverDepartX()+(x*self.sizePieces), self.offSetY+(y*self.sizePieces), anchor=NW, image=self.imageDalek)
                            
                        #Si c'est un tas de ferraille
                        elif(isinstance(self.parent.jeu.liste_objets[n], Ferraille)):
                            self.surfaceJeu.create_image(self.trouverDepartX()+(x*self.sizePieces), self.offSetY+(y*self.sizePieces), anchor=NW, image=self.imageFerraille)

    
        self.boutonTeleportation.place(width=100, x=20, y=750)            
        self.boutonZappeur.place(width=100, x=140, y=750)
        self.surfaceJeu.create_text(350, 765, text='Points : '+str(self.parent.jeu.points), font=('Arial', 16), fill='white')
        self.surfaceJeu.create_text(550, 765, text='Zappeur : '+str(jeu.liste_objets[0].nb_zapper), font=('Arial', 16), fill='white')
        self.surfaceJeu.create_text(750, 765, text='Vague : '+str(jeu.vague), font=('Arial', 16), fill='white')
        self.surfaceJeu.create_text(1000, 765, text='Daleks Restant : '+str(jeu.nb_dalek_restant)+'/'+str(jeu.nb_total_dalek), font=('Arial', 16), fill='white')
        
        
        
    def zapAnimation(self, jeu):

        for ii in range(1,15):
            self.afficher(jeu)
            self.surfaceJeu.create_image(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces-self.sizePieces), self.offSetY+(self.parent.jeu.liste_objets[0].y*self.sizePieces-self.sizePieces), anchor=NW, image = self.listeImage[ii])
            time.sleep(0.3)

    def splashNiveau(self, jeu):
        pass

    def getUserInputCode(self,event):
        print(event.x, event.y)
        
        keyCode = None
        
        #Gestion du click de souris

        #Si le click est au Sud-Ouest du Docteur
        if(event.x < (self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))
           and event.y > (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)+self.sizePieces):
            keyCode = 1

        #Si le click est au Sud du Docteur
        elif(event.x >=(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))
             and event.x <=(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces)+self.sizePieces)
             and event.y > (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)+self.sizePieces):
            keyCode = 2

        #Si le click est au Sud-Est du Docteur   
        elif(event.y > (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)+self.sizePieces
             and event.x >(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces)+self.sizePieces)):
            keyCode = 3

        #Si le click est a l'Ouest du Docteur
        elif(event.x < (self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))
             and event.y >= (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)
             and event.y <= ((self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)+self.sizePieces)):
            keyCode = 4

        #Si le click est directement sur le Docteur
        elif(event.x >=(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))
             and event.x <=(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces)+self.sizePieces)
             and event.y >= (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)
             and event.y <= ((self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)+self.sizePieces)):
            keyCode = 5
            
        #Si le click est a l'Est du Docteur
        elif(event.x > ((self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))+self.sizePieces)
             and event.y >= (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)
             and event.y <= ((self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)+self.sizePieces)):
            keyCode = 6

        #Si le click est au Nord-Ouest du Docteur
        elif(event.x < (self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))
             and event.y < (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)):
            keyCode = 7

        #Si le click est au Nord du Docteur
        elif(event.x >=(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))
             and event.x <=(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces)+self.sizePieces)
             and event.y < (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)):
            keyCode = 8

        #Si le click est au Nord-Est du Docteur
        elif(event.x > ((self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces))+self.sizePieces)
             and event.y < (self.offSetY + self.parent.jeu.liste_objets[0].y*self.sizePieces)):
            keyCode = 9
            
        self.parent.turn(keyCode)


    def splashPasZapper(self):
        pass

    def endGame(self, jeu, scoreDejaEntre = False):
        self.surfaceJeu.place_forget()
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.gameOver.place(height=600, x=0, y=0)   
        self.gameOver.insert(INSERT, "Game Over")
        
        
        
    def menu(self):      
        self.effacerFrame()
        self.textBox.delete(1.0, END)
        self.labelBackground.place(x=0, y=0)
        self.boutonJouer.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=300)
        self.boutonInstructions.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=400)
        self.boutonHighscore.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=500)
        self.boutonAbout.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=600)
        self.boutonQuitter.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        
    def instruction(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.textBox.place(height=600, x=0, y=0)
        self.textBox.insert(INSERT,"Les Daleks contre Dr. Who\n")
        self.textBox.insert(INSERT, "_________________________\n")
        self.textBox.insert(INSERT, 'Instruction\n\n\n')
        self.textBox.insert(INSERT,'Votre objectif est de detruire le plus de Daleks possible avant qu_ils ne vous capture. \n\n\nChaque Dalek detruit vous attribut 5 credit galactique.\n\n')
        self.textBox.insert(INSERT,'Utiliser les touches du clavier numerique (1 a 9) pour vous deplacer  et pieger les Daleks\n\n')
        self.textBox.insert(INSERT,'Vous disposerez d_une arme extrement puissante, le rayon laser cosmique, a utiliser avec parcimonie car ils \nsont une resource rare. Pour en declancher un, appuyez sur la touche " - ".\n\n')
        self.textBox.insert(INSERT,'Vous avez aussi l_habilete de vous teleporter aleatoirement n_importe quand avec la touche " * ", afin de pieger \nles Daleks\n\n')
        self.textBox.insert(INSERT,'Bonne chance Docteur. Ce n_est qu_une question de temps avant de vous voir succomber...\nSinon, si vous ne vous en croyez plus capable en plein milieu du jeu, appuyez sur "q" pour quitter\n\n\n\n')

    def highScore(self, highScore):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.textBox.place(height=600, x=0, y=0)
        self.textBox.insert(INSERT,'Les Daleks contre Dr. Who\n')
        self.textBox.insert(INSERT,'_________________________\n\n')
        self.textBox.insert(INSERT,'HighScores\n\n\n')
        if(hightScore):
            for i in highScore:
               self.textBox.insert(INSERT, i + '\n\n')
        else:
            self.textBox.insert(INSERT,'Il n_y a pas encore de hightScores...\n\nA vous de jouer!!!')
       
    def about(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.textBox.place(height=600, x=0, y=0)
        self.textBox.insert(INSERT,'Les Daleks contre Dr. Who\n')
        self.textBox.insert(INSERT,'_________________________\n')
        self.textBox.insert(INSERT,'A propos\n\n\n\n')
        self.textBox.insert(INSERT,'Projet realiser par Arnaud et Xavier \n\n\nGit du projet: https://github.com/TeamGoatDev/Daleks_xavierhd_Arnaud474\n\n\n\n')
        self.textBox.insert(INSERT,'Pesez sur une touche pour retourner au menu principal')
        
        
    def questionQuitterEnPartie(self):
        pass

    #Cette fonction permet d'enlever toutes les composantes presentes sur le frame sans le detruire
    def effacerFrame(self):
    
        listeWidgets = self.root.winfo_children()

        for i in listeWidgets:
            i.pack_forget()
            i.place_forget()

        

    #Cette fonction permet de calculer la position initiale en x
    def trouverDepartX(self):
        return ((self.root.winfo_width()-(self.parent.jeu.surface_l*32))/2)
    
    



#Declaration des objets
class Vue:
    def __init__(self):
        os.system('mode con:cols=125 lines=60')
    
    #Fonction qui fait l'affichage de jeu dans la console
    def afficher(self, jeu):

        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain 
        for y in range(0,jeu.surface_h):
            for x in range(0, jeu.surface_l):
                case_vide = True
                
                #Regarde dans la liste si il y a un element a cette position
                for n in range(0, jeu.nb_total_objets-1):
                    #Si la case courante correspond a la case de la liste
                    if(x == jeu.liste_objets[n].x and y == jeu.liste_objets[n].y):

                        #Si c'est le docteur who
                        if(n==0):
                            print(chr(1),end='')
                            break
                        #Si c'est un Dalek
                        elif(isinstance(jeu.liste_objets[n], Dalek)):
                            print(chr(177),end='')
                            break
                        #Si c'est un tas de ferraille
                        elif(isinstance(jeu.liste_objets[n], Ferraille)):
                            print('#',end='')
                            break
                        
                else:
                    print('-',end='')
            if(y == 0):
                print(' Points: '+str(jeu.points),end='') #Affiche les points
            elif(y == 1):
                print(' Zappeur: '+str(jeu.liste_objets[0].nb_zapper),end='') #Affiche les points
            elif(y == 2):
                print(' Vague: '+str(jeu.vague),end='') #Affiche le numero de vague
            elif(y == 3):
                print(' '+str(jeu.nb_dalek_restant)+'/'+str(jeu.nb_total_dalek),end='') #Affiche les points
                
                
            print('')   #end line
        print('')   #end line


    def changerSizePiece(self, mod1, mod2):
        pass
    def resetSizePiece():
        pass

    def zapAnimation(self, jeu):
        
        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain 
        for y in range(0,jeu.surface_h):
            for x in range(0, jeu.surface_l):

                case_vide = True
                
                #Regarde dans la liste si il y a un element a cette position
                for n in range(0, jeu.nb_total_objets):
                    
                    #Si la case courante correspond a la case de la liste
                    if(x == jeu.liste_objets[n].x and y == jeu.liste_objets[n].y):
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

                if((x == jeu.liste_objets[0].x-1 and y == jeu.liste_objets[0].y-1) or (x == jeu.liste_objets[0].x and y == jeu.liste_objets[0].y-1) or (x == jeu.liste_objets[0].x+1 and y == jeu.liste_objets[0].y-1) or (x == jeu.liste_objets[0].x+1 and y == jeu.liste_objets[0].y) or (x == jeu.liste_objets[0].x+1 and y == jeu.liste_objets[0].y+1) or (x == jeu.liste_objets[0].x and y == jeu.liste_objets[0].y+1) or (x == jeu.liste_objets[0].x-1 and y == jeu.liste_objets[0].y+1) or (x == jeu.liste_objets[0].x-1 and y == jeu.liste_objets[0].y)):
                    case_vide = False
                    print('&',end='')

                if(case_vide == True):
                    print('-',end='')        
                        
            if(y == 0):
                print(' Points: '+str(jeu.points),end='') #Affiche les points
            elif(y == 1):
                print(' Zappeur: '+str(jeu.liste_objets[0].nb_zapper),end='') #Affiche le nombre de zappeurs
            elif(y == 2):
                print(' Vague: '+str(jeu.vague),end='') #Affiche le numero de vague
            elif(y == 3):
                print(' '+str(jeu.nb_dalek_restant)+'/'+str(jeu.nb_total_dalek),end='') #Affiche le nombre de daleks
                
            print('')   #end line
        print('')   #end line
        time.sleep(0.5)#afin de voir les petits caractere de zap plus d_une microseconde

    def splashNiveau(self, jeu):
        os.system('cls')
        print('')
        print('Vague : '+str(jeu.vague))
        print('Points : '+str(jeu.points))
        time.sleep(2)


    def getUserInputCode(self):
        
        key = msvcrt.getch()
        try:
            return int(key)
        except:
            if key == b'*':
                return 10
            elif key == b'-':
                return 11
            elif key == b'q':
                return 12
        return 0

    def splashPasZapper(self):
        os.system('cls')
        print('\n\n\n\nPas de zappeur disponible !!!')
        time.sleep(1)

    def endGame(self, jeu, scoreDejaEntre = False):
        os.system('cls')
        print('GAME OVER !!!\n\n\n')
        print('Vague : '+str(jeu.vague))
        print('Points : '+str(jeu.points))
        if(not scoreDejaEntre):
            print('\n\nAppuyer sur 4 pour enregistrer votre score')
        print('\n\n\n\nVoulez-vous recommencer une partie? oui[1] ou non[2]')

        retour = self.getUserInputCode()

        if(not scoreDejaEntre and retour == 4):
            self.parent.jeu.setHightScore(self.getUserName(self.parent.jeu.score))
            self.endGame(jeu,True)
        if(retour == 2 or retour == 3):
            return retour
        
            

    def menu(self,parent):

        while (True):#boucle infini tant que le retour de la fonction nest pas appele
            os.system('cls')
            print('Les Daleks contre Dr. Who')
            print('_________________________\n\n\n')
            print('1. Jouer\n\n')
            print('2. Instruction\n\n')
            print('3. HighScores\n\n')
            print('4. About\n\n')
            print('5. Quitter')
        
            retourMenu = self.getUserInputCode()
            
            if (retourMenu == 1):
                retour = b'1'
                while(retour == b'1'):
                    retour = parent.gameLOOP()
            elif (retourMenu == 2):
                self.instruction()
            elif(retourMenu == 3):
                self.highScore(parent.jeu.getHighScore())
            elif (retourMenu == 4):
                self.about()
            elif (retourMenu == 5):
                os.system('cls')
                return 0

        
        

    def instruction(self):
        os.system('cls')
        print('Les Daleks contre Dr. Who')
        print('_________________________\n')
        print('Instruction\n\n\n')
        print('Vous voici : '+chr(1))
        print('\nVoici un Dalek : '+chr(177))
        print('\nEt enfin, voila une ferraille : #\n\n')
        print('Votre objectif est de detruire le plus de Daleks possible avant qu_ils ne vous capture. \n\n\nChaque Dalek detruit vous attribut 5 credit galactique.\n\n')
        print('Utiliser les touches du clavier numerique (1 a 9) pour vous deplacer  et pieger les Daleks\n\n')
        print('Vous disposerez d_une arme extrement puissante, le rayon laser cosmique, a utiliser avec parcimonie car ils sont \nresource rare. Pour en declancher un, appuyez sur la touche " - ".\n\n')
        print('Vous avez aussi l_habilete de vous teleporter aleatoirement n_importe quand avec la touche " * ", afin de pieger les Daleks\n\n')
        print('Bonne chance Docteur. Ce n_est qu_une question de temps avant de vous voir succomber...\nSinon, si vous ne vous en croyez plus capable en plein milieu du jeu, appuyez sur "q" pour quitter\n\n\n\n')
        print('Pesez sur une touche pour retourner au menu principal')
        self.getUserInputCode()

    def about(self):
        os.system('cls')
        print('Les Daleks contre Dr. Who')
        print('_________________________\n')
        print('A propos\n\n\n\n')
        print('Projet realiser par Arnaud et Xavier \n\n\nGit du projet: https://github.com/TeamGoatDev/Daleks_xavierhd_Arnaud474\n\n\n\n')
        print('Pesez sur une touche pour retourner au menu principal')
        self.getUserInputCode()

    def questionQuitterEnPartie(self):
        os.system('cls')
        print('\n\n\n\nQuitter?    oui[1] ou non[2]')
        return self.getUserInputCode()

    def highScore(self, highScore):
        os.system('cls')
        print('Les Daleks contre Dr. Who')
        print('_________________________\n')
        print('HightScores\n\n\n')
        if(highScore):
            for i in highScore:
                print(i + '\n\n')
        else:
            print('Il n_y a pas encore de hightScores...\n\nA vous de jouer!!!')

        print('\n\n\n\nPesez sur une touche pour retourner au menu principal')
        self.getUserInputCode()

    def getUserName(self, jeu):
        os.system('cls')
        print('Score : '+str(jeu.points))
        return raw_input("Entrez votre nom : ")



class Jeu:
    def __init__(self, parent):
        self.parent = parent
        self.points = 0                 #Variable qui contient le nombre de points accumules par le joueur
        self.vague = 0                  #Numero de la vague en cours
        self.nb_dalek_restant = 0       #Nombre total des Daleks restant dans la liste
        self.nb_total_dalek = 0         #Nombre total de Dalek pour la vague courrante
        self.nb_total_objets = 0        #Nombre d'elements dans la liste
        self.liste_objets = []          #Liste qui contiendra les daleks et le docteur
        self.surface_l = 30             #Largeur de la surface de jeu
        self.surface_h = 20             #Hauteur de la surface de jeu

    def setNextVague(self):
        self.nb_total_dalek += 5
        self.creerListe()                               #Creation de la liste pour la nouvelle vague
        self.denombreObjet()
        self.denombreDalek()
        self.vague += 1
        if(self.vague%15 == 2):
            self.surface_l += 1
            self.surface_h += 1
            """if(self.vague%45 == 2):
                self.parent.vue.changerSizePiece(20,11)"""
        self.liste_objets[0].nb_zapper += 1
        self.nb_total_objets = len(self.liste_objets)   #Calcule le nombre d'objet dans la liste

    def reset(self):
        self.points = 0
        self.vague = 0
        self.nb_dalek_restant = 0
        self.nb_total_dalek = 0
        self.nb_total_objets = 0
        self.liste_objets[:] = []
        self.surface_l = 30
        self.surface_h = 20
        #self.parent.vue.resetSizePiece()

    def deplacerDalek(self):
        for i in range(1, self.nb_total_objets): #regarde tout les objets de la liste
                if(isinstance(self.liste_objets[i], Dalek)): #recherche d_objet Dalek
                    self.liste_objets[i].deplacer(self)
    
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
            drWho = DrWho(random.randint(0, self.surface_l-1),random.randint(0, self.surface_h-1)) #Creation d_un nouveau docteur who
        else:
            drWho.x = random.randint(0, self.surface_l-1)#Creation d'une position au hasard pour le docteur deja existant
            drWho.y = random.randint(0, self.surface_h-1)

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

                    x = random.randint(0, self.surface_l-1)
                    y = random.randint(0, self.surface_h-1)

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

    def getHighScore(self):
        
        try:
            tampon = open("hight.Score", 'r+')#rb == read binary
            highScore = tampon.readlines()
            tampon.close()
            return highScore
        except:
            tampon = open("hight.Score", 'w+')#w == write
            tampon.close()
            return 0



    def setHightScore(self, name):
        tampon = open("high.Score", 'a')#ab == append binary
        aEcrire = name + ';' + str(self.points) + '\n'
        tampon.write(aEcrire)
        tampon.close()


#Classe pour les objets qui seront dans la surface de jeu 
class DrWho:
    def __init__(self, x, y):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y #Position en y sur la surface de jeu
        self.nb_zapper = 0 #Nombre de zapper dont a droit Dr Who

    def notDead(self, jeu):
        for i in range(1,jeu.nb_total_objets):
            if(self.x == jeu.liste_objets[i].x and self.y == jeu.liste_objets[i].y):
                return False #veux dire qu_il est morte
            
        return True

    def zapper(self, jeu):

        for i in range(jeu.nb_total_objets-1,0,-1):
            if((jeu.liste_objets[i].x == jeu.liste_objets[0].x-1 and jeu.liste_objets[i].y == jeu.liste_objets[0].y-1) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x and jeu.liste_objets[i].y == jeu.liste_objets[0].y-1) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x+1 and jeu.liste_objets[i].y == jeu.liste_objets[0].y-1) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x+1 and jeu.liste_objets[i].y == jeu.liste_objets[0].y) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x+1 and jeu.liste_objets[i].y == jeu.liste_objets[0].y+1) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x and jeu.liste_objets[i].y == jeu.liste_objets[0].y+1) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x-1 and jeu.liste_objets[i].y == jeu.liste_objets[0].y+1) or (jeu.liste_objets[i].x == jeu.liste_objets[0].x-1 and jeu.liste_objets[i].y == jeu.liste_objets[0].y)):   
                if(isinstance(jeu.liste_objets[i], Dalek)):
                   jeu.points += jeu.liste_objets[i].valeurPoint
                jeu.liste_objets.pop(i)
                jeu.nb_total_objets = len(jeu.liste_objets)
        self.nb_zapper -= 1
                
                   

        


    def teleportation(self, jeu):

        position_ko = True
        compteur = 0 # cherche un certain nombre de fois une bonne case puis s_il ne trouve pas, redonne le choix a l'usager quoi faire
        #Tant que la position n'est pas une position valide par rapport a la postion des Daleks
        while position_ko == True:

            x = random.randint(0, jeu.surface_l-1)
            y = random.randint(0, jeu.surface_h-1)

            compteur +=1

            for i in range(1, jeu.nb_total_objets):
                #Si la case est a au moins deux cases du Dalek
                if (x >= jeu.liste_objets[i].x+2 or x <= jeu.liste_objets[i].x-2 or y >= jeu.liste_objets[i].y+2 or y <= jeu.liste_objets[i].y-2):
                    position_ko = False
                else:
                    position_ko = True
                    break

            if(compteur == 15):
                break
        else:
            self.x = x
            self.y = y
            return False #ca a marcher
        return True    #ca n_a pas marcher





     #Fonction qui gere le deplacement du joueur
    def deplacer(self, jeu, key):

        var = 1#variable pour augmenter la largeure du déplacement du joueur
        #Variables pour la variation de x et y
        v_x = 0
        v_y = 0
        
        #Deplacement vers le bas a gauche
        if(key == 1):
            v_x = -var
            v_y = var
        
        #Deplacement vers le bas
        if(key == 2):
            v_x = 0
            v_y = var

        #Deplacement vers le bas a droite
        if(key == 3):
            v_x = var
            v_y = var

        #Pas de deplacement
        if(key == 5):
            v_x = 0
            v_y = 0

        #Depplacement vers la droite
        if(key == 6):
            v_x = var
            v_y = 0

        #Deplacement vers le haut a droite
        if(key == 9):
            v_x = var
            v_y = -var

        #Deplacement vers le haut
        if(key == 8):
            v_x = 0
            v_y = -var

        #Deplacement vers le haut a gauche
        if(key == 7):
            v_x = -var
            v_y = -var

        #Deplacement vers la gauche
        if(key == 4):
            v_x = -var
            v_y = 0


        #Determine si le deplacement sera a l'interieur de la zone de jeu
        if(jeu.liste_objets[0].x+v_x < jeu.surface_l and jeu.liste_objets[0].y+v_y < jeu.surface_h and jeu.liste_objets[0].x+v_x >= 0 and jeu.liste_objets[0].y+v_y >= 0):
            for i in range(1, jeu.nb_total_objets):
                #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
                if(jeu.liste_objets[0].x+v_x == jeu.liste_objets[i].x and jeu.liste_objets[0].y+v_y == jeu.liste_objets[i].y):
                    return 0
            else:
                #Change la position du Docteur Who lorsque le deplacement est valide       
                jeu.liste_objets[0].x += v_x
                jeu.liste_objets[0].y += v_y
                return 1
        else:    
            return 0


class Dalek:
    def __init__(self, x, y, valeurPoint):
        self.x = x  #Position en x sur la surface de jeu 
        self.y = y #Position en y sur la surface de jeu
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
        self.y = y  #Position en y sur la surface de jeu
    

class Controleur:

    def __init__(self):
        self.jeu = Jeu(self)
        try:
            if(sys.argv[1] == '-shell'):#argument 0 est le nom du fichier, le 1 est le parametre entrer qui le suit.
                self.vue = Vue()
                self.vue.menu(self)
        except ChildProcessError as e:
            print(e.args)
            self.vue = Vue2(self)
            self.vue.menu()
            self.vue.root.mainloop() 


    def newGame(self):
        self.jeu.reset()
        self.jeu.setNextVague()
        self.vue.afficher(self.jeu)


    def gameLOOP(self):

        self.jeu.reset()
        continuer = 1           #Afin de savoir si le controleur doit redonner le tour au joueur pour un faux mouvement
            
        while (continuer == 1):  #Verifie si il ne reste plus de daleks ou verifie si le joueur a ete capturer

            continuer = 0
           
            while (not continuer):
                #Affichage de la surface de jeu
                self.vue.afficher(self.jeu)
                keyCode = self.vue.getUserInputCode()#retourne la touche appuyer par le joueur
                continuer = self.turn(keyCode)     


    def turn(self,keyCode): #type de retour accepter : 0 = recommencer, 1 = continuer, 2 = quitter,

        if(self.jeu.nb_dalek_restant == 0):
            self.jeu.setNextVague()#Preparation de la prochaine vague, incremente les dalek, zappeur, et autre goodies. Et cree une liste d'objet contenant les dalek et le docteur
            self.vue.splashNiveau(self.jeu)

        #Action du joueur :

        if(keyCode == 0): #code pas valide
            return 0

        elif(keyCode >= 1 and keyCode <= 9):
            self.jeu.liste_objets[0].deplacer(self.jeu, keyCode)     #Deplacement du DrWho
        
        elif(keyCode == 10):
            if(self.jeu.liste_objets[0].teleportation(self.jeu)):    #Teleportation du DrWho
                return 0 #si la teleportation retourne True

        elif(keyCode == 11):                                #Zappeur du DrWho
            if(self.jeu.liste_objets[0].nb_zapper > 0):
                self.jeu.liste_objets[0].zapper(self.jeu)   #Le zap de drwho logique 
                self.vue.zapAnimation(self.jeu)             #Affichage du zap sur l_espace de jeu (le zap de drwho graphique)
            else:
                self.vue.splashPasZapper()
                return 0

        elif(keyCode == 12):                                #Pour quitter en pleine partie
            if(self.vue.questionQuitterEnPartie() == 1):
                return 2
        
        self.jeu.deplacerDalek() #Deplacement automatique des Dalek
        self.jeu.collision() #Verifie les collisions
        self.jeu.denombreDalek()

        if (not self.jeu.liste_objets[0].notDead(self.jeu)):
            if(self.jeu.points > 0):
                return self.vue.endGame(self.jeu)
            else:
                return self.vue.endGame(self.jeu, True)

        self.vue.afficher(self.jeu) #Affichage de la surface de jeu
        return 1 #Tout est aller comme il faut


if __name__ == "__main__":
    c = Controleur()
    

