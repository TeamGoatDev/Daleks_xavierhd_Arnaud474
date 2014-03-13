from tkinter import *
import random
import os
import sys
import msvcrt
import time
import winsound

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
        self.imageBackground = PhotoImage(file="Image/bg.gif")
        self.labelBackground = Label(self.root,image=self.imageBackground)

        #Offset Y
        self.offSetY = 20

        #Size des pieces
        self.sizePieces = 32

        #Surface de jeu
        self.imageSurface = PhotoImage(file="Image/space.gif")
        self.imageDalek = PhotoImage(file="Image/dalek.gif")
        self.imageDrWho = PhotoImage(file="Image/drwho.gif")
        self.imageFerraille = PhotoImage(file="Image/ferraille.gif")
        self.surfaceJeu = Canvas(self.root, width=self.root.winfo_width(), height=self.root.winfo_height(), bg="black")
        self.surfaceJeu.bind('<Button-1>', self.getUserInputCode)



        #Loading des images explosives
        self.listeImage = []
        self.listeImageExplosion = []
        self.listeImageZappeur = []

        for ii in range(1,16):
            self.listeImageExplosion.append(PhotoImage(file="Image/explosion"+ str(ii) + ".gif"))
            print("Image/explosion"+ str(ii) + ".gif")
            self.listeImageZappeur.append(PhotoImage(file="Image/zappeur"+ str(ii) + ".gif"))
            print("Image/zappeur"+ str(ii) + ".gif")

        #Loading des son explosifs
        self.son = None
        file = "Son/boom.wav"
        self.sonBoom = file

        file = "Son/zap.wav"
        self.sonZap = file

        self.changerExplosionType(self.listeImageZappeur, self.sonZap)#set default explosion

        self.listeImageOriginal = self.listeImage
        self.imageSurfaceOriginal = self.imageSurface
        self.imageDalekOriginal = self.imageDalek
        self.imageDrWhoOriginal = self.imageDrWho
        self.imageFerrailleOriginal = self.imageFerraille

        #Variable pour que les boutons soient tous de la meme grosseur
        self.buttonWidth= 400

        self.textBox = Text(width=self.root.winfo_width(), bg='black', fg='white', font=('Arial', 18))
        self.gameOver = Text(width=self.root.winfo_width(), bg='black', fg='white', font=('Arial', 40))
        self.userStringInput = Text(width=self.root.winfo_width(), bg='white', fg='black', font=('Arial', 20))


        self.boutonJouer = Button(self.root, text='Jouer',width=50, bg='black', fg='white',activebackground='black', activeforeground='white',command=self.parent.newGame)
        self.boutonInstructions = Button(self.root, text='Instructions',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command=self.instruction)
        self.boutonHighscore = Button(self.root, text='Highscore',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command= lambda: self.highScore(self.parent.jeu.getHighScore()))
        self.boutonOption = Button(self.root, text='Option',width=50, bg='black', fg='white',activebackground='black', activeforeground='white',command=self.option)
        self.boutonAbout = Button(self.root, text='À propos',width=50, bg='black', fg='white',activebackground='black', activeforeground='white',command=self.about)
        self.boutonQuitter = Button(self.root, text='Quitter',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command=self.root.destroy)
        self.boutonQuitterPartie = Button(self.root, text='Quitter',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command= lambda: self.parent.turn(12))
        self.boutonInfo = Button(self.root, text='Aide',width=50, bg='black', fg='white',activebackground='black', activeforeground='white', command= lambda: self.parent.turn(13))
        self.boutonRetourMenu = Button(self.root, text='Retour au menu', width=100, bg='black', fg='white',activebackground='black', activeforeground='white', command=self.menu)
        self.boutonTeleportation = Button(self.root, text='Teleportation', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= lambda: self.parent.turn(10))
        self.boutonZappeur = Button(self.root, text='Zappeur', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= lambda: self.parent.turn(11))
        self.boutonSetHighscore = Button(self.root, text='Entrez Votre HighScore', width=100, bg='black', fg='white', activebackground='blue', activeforeground='white', command= self.setHighScore)
        self.boutonWriteHighScore = Button(self.root, text='Enregistrer', width=100, bg='black', fg='white', activebackground='blue', activeforeground='white', command=lambda: self.menu(self.parent.jeu.setHighScore(self.userStringInput.get(1.0,END))) )
        self.boutonRetourJeu = Button(self.root, text='Retour au jeu', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= self.retourAuJeu)

        self.boutonOui = Button(self.root, text='Oui', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= self.menu)
        self.boutonNon = Button(self.root, text='Non', width=50, bg='black', fg='white', activebackground='blue', activeforeground='white', command= self.retourAuJeu)

        self.boutonExplosionTypeZappeur = Button(self.root, width=110, height=110, activebackground='blue', command= lambda: self.changerExplosionType(self.listeImageZappeur, self.sonZap))
        self.boutonExplosionTypeZappeur.config(image=self.listeImageZappeur[10],width=96,height=96)
        self.boutonExplosionTypeExplosion = Button(self.root, width=110, height=110, activebackground='blue', command= lambda: self.changerExplosionType(self.listeImageExplosion, self.sonBoom))
        self.boutonExplosionTypeExplosion.config(image=self.listeImageExplosion[10],width=96, height=96)



    def changerExplosionType(self, listeD_Image, son):
        self.listeImage[:] = []
        for ii in range(0, len(listeD_Image)):
            self.listeImage.append(listeD_Image[ii].copy())
        self.son = son
        print("changement fait")


    def changerSizePiece(self, mod1, mod2):
        self.sizePieces = self.sizePieces * mod1/mod2
        for image in listeImage:
            image = image.zoom(mod1,mod1)
            image = image.subsample(mod2,mod2)

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
        self.imageFerraille = self.imageFerrailleOriginal

    def setBackground(self):
        self.effacerFrame()
        #Creation de l'image pour la surface de jeu et ajout du canevas
        self.surfaceJeu.create_image(0,0, anchor=NW, image=self.imageSurface)
        self.boutonTeleportation.place(width=100, x=20, y=750)
        self.boutonZappeur.place(width=100, x=140, y=750)
        self.boutonQuitterPartie.place(width=50, x=self.root.winfo_width()-85, y=self.root.winfo_height()-25)
        self.boutonInfo.place(width=35, x=self.root.winfo_width()-35,y=self.root.winfo_height()-25)

    def retourAuJeu(self):
        self.setBackground()
        self.afficher(self.parent.jeu)
        self.root.update()

    def afficher(self, jeu):

        #Effacage initial du frame pour pouvoir
        self.surfaceJeu.delete("pieces")



        #Test pour la premiere position ainsi que le fonctionnement d'une image dans un canevas
        #self.surfaceJeu.create_image(self.trouverDepartX(), 100, anchor=NW, image=self.imageDalek)

        self.surfaceJeu.place(x=-1, y=-1)

        for y in range(0, self.parent.jeu.surface_h):
            for x in range(0, self.parent.jeu.surface_l):

                case_vide = True

                #Regarde dans la liste si il y a un element a cette position
                for objet in jeu.liste_objets:

                    #Si la case courante correspond a la case de la liste
                    if(x == objet.x and y == objet.y):
                        print(objet.x, objet.y)

                        #Si c'est le docteur who
                        if(isinstance(objet, DrWho)):
                            self.surfaceJeu.create_image(self.trouverDepartX()+(x*self.sizePieces), self.offSetY+(y*self.sizePieces), anchor=NW, tags="pieces", image=self.imageDrWho)

                        #Si c'est un Dalek
                        elif(isinstance(objet, Dalek)):
                            self.surfaceJeu.create_image(self.trouverDepartX()+(x*self.sizePieces), self.offSetY+(y*self.sizePieces), anchor=NW, tags="pieces", image=self.imageDalek)

                        #Si c'est un tas de ferraille
                        elif(isinstance(objet, Ferraille)):
                            self.surfaceJeu.create_image(self.trouverDepartX()+(x*self.sizePieces), self.offSetY+(y*self.sizePieces), anchor=NW, image=self.imageFerraille)



        self.surfaceJeu.create_text(380, 765, text='Points : '+str(self.parent.jeu.points), font=('Arial', 16), fill='white', tags="pieces")
        self.surfaceJeu.create_text(580, 765, text='Zappeur : '+str(jeu.liste_objets[0].nb_zapper), font=('Arial', 16), fill='white', tags="pieces")
        self.surfaceJeu.create_text(780, 765, text='Vague : '+str(jeu.vague), font=('Arial', 16), fill='white', tags="pieces")
        self.surfaceJeu.create_text(1000, 765, text='Daleks Restant : '+str(jeu.nb_dalek_restant)+'/'+str(jeu.nb_total_dalek), font=('Arial', 16), fill='white', tags="pieces")



    def zapAnimation(self, jeu):

        for ii in self.listeImage:
            print (ii)
            self.surfaceJeu.create_image(self.trouverDepartX()+(self.parent.jeu.liste_objets[0].x*self.sizePieces-self.sizePieces), self.offSetY+(self.parent.jeu.liste_objets[0].y*self.sizePieces-self.sizePieces), anchor=NW, tags="explosion", image = ii)
            self.root.update()
            time.sleep(0.028)#temps d_affichage de chaque frame
            self.surfaceJeu.delete("explosion")


    def splashNiveau(self, jeu):
        self.gameOver.delete(1.0, END)
        self.gameOver.place(height=100, x=0, y=self.root.winfo_height()/2)
        self.gameOver.insert(INSERT,"Nouveau niveau!!!")
        self.root.update()
        time.sleep(0.7)
        self.setBackground()
        self.afficher(self.parent.jeu)

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
        self.gameOver.delete(1.0, END)
        self.gameOver.place(height=100, x=0, y=self.root.winfo_height()/2)
        self.gameOver.insert(INSERT,"Action Impossible!!!")
        self.root.update()
        time.sleep(0.7)
        self.setBackground()
        self.afficher(self.parent.jeu)

    def endGame(self, jeu, scoreDejaEntre = False):
        self.surfaceJeu.place_forget()
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)

        self.gameOver.delete(1.0, END)
        self.gameOver.place(height=200, x=0, y=0)
        self.gameOver.insert(INSERT, "Game Over")

        self.textBox.delete(1.0, END)

        self.boutonSetHighscore.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=400)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)



    def menu(self,valUseless = None):
        self.effacerFrame()
        self.textBox.delete(1.0, END)
        self.labelBackground.place(x=0, y=0)
        self.boutonJouer.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=300)
        self.boutonInstructions.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=380)
        self.boutonHighscore.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=460)
        self.boutonOption.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=540)
        self.boutonAbout.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=620)
        self.boutonQuitter.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)

    def instruction(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        if(self.parent.jeu.liste_objets):
            self.boutonRetourJeu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        else:
            self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.textBox.place(height=620, x=0, y=0)
        self.textBox.delete(1.0, END)
        self.textBox.insert(INSERT,"Les Daleks contre Dr. Who\n")
        self.textBox.insert(INSERT, "_________________________\n")
        self.textBox.insert(INSERT, "Instruction\n\n\n")

        self.textBox.insert(INSERT, "Objectif :")
        self.textBox.insert(INSERT,"\n\nVotre objectif est de détruire le plus de Daleks possible avant qu'ils ne vous capturent.")
        self.textBox.insert(INSERT,"\n\nChaque Dalek détruit vous attribut 5 crédits galactiques.")

        self.textBox.insert(INSERT, "\n\n\nDéplacement :")
        self.textBox.insert(INSERT,"\n\nCliquez dans la direction voulue pour vous deplacer")
        self.textBox.insert(INSERT,"\n\nVous avez aussi l'habileté de vous téléporter aleatoirement n'importe quand")

        self.textBox.insert(INSERT, "\n\n\nArme :")
        self.textBox.insert(INSERT,"\n\nVous disposerez d'un rayon laser cosmique, à utiliser avec parcimonie.")

        self.textBox.insert(INSERT,"\n\nBonne chance Docteur. Ce n'est qu'une question de temps avant de vous voir succomber...")

    def highScore(self, highScore):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.textBox.place(height=600, x=0, y=0)
        self.textBox.delete(1.0, END)
        self.textBox.insert(INSERT,"Les Daleks contre Dr. Who\n")
        self.textBox.insert(INSERT,"_________________________\n\n")
        self.textBox.insert(INSERT,"HighScores\n\n\n")
        if(highScore):
            for i in highScore:
               self.textBox.insert(INSERT, i)
        else:
            self.textBox.insert(INSERT,"Il n'y a pas encore de highScores...\n\nA vous de jouer!!!")

    def option(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)

        self.gameOver.delete(1.0, END)
        self.gameOver.place(height=200, x=0, y=0)
        self.gameOver.insert(INSERT,"Option")

        self.textBox.place(height=400, x=0, y=200)
        self.textBox.delete(1.0, END)
        self.textBox.insert(INSERT,"Apparence : ")
        self.boutonExplosionTypeExplosion.place(x=200, y=200)
        self.boutonExplosionTypeZappeur.place(x=400,y=200)


    def about(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)
        self.boutonRetourMenu.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)
        self.textBox.place(height=600, x=0, y=0)
        self.textBox.delete(1.0, END)
        self.textBox.insert(INSERT,"Les Daleks contre Dr. Who\n")
        self.textBox.insert(INSERT,"_________________________\n")
        self.textBox.insert(INSERT,"A propos\n\n\n\n")
        self.textBox.insert(INSERT,"Projet réalisé par Arnaud et Xavier \n\n\nGit du projet: https://github.com/TeamGoatDev/Daleks_xavierhd_Arnaud474\n\n\n\n")
        self.textBox.insert(INSERT,"Pesez sur une touche pour retourner au menu principal")


    def questionQuitterEnPartie(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)

        self.gameOver.delete(1.0, END)
        self.gameOver.place(height=200, x=0, y=200)
        self.gameOver.insert(INSERT,"Quitter?\n")

        self.textBox.delete(1.0, END)
        self.textBox.place(height=200, x=0, y=400)
        self.textBox.insert(INSERT,"Êtes-vous certain de vouloir quitter?\n")

        self.boutonOui.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=600)
        self.boutonNon.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)


    #Cette fonction permet d'enlever toutes les composantes presentes sur le frame sans le detruire
    def effacerFrame(self):

        listeWidgets = self.root.winfo_children()

        for i in listeWidgets:
            i.pack_forget()
            i.place_forget()



    #Cette fonction permet de calculer la position initiale en x
    def trouverDepartX(self):
        return ((self.root.winfo_width()-(self.parent.jeu.surface_l*32))/2)

    def setHighScore(self):
        self.effacerFrame()
        self.labelBackground.place(x=0, y=0)

        self.gameOver.delete(1.0, END)
        self.gameOver.place(height=60, x=0, y=0)
        self.gameOver.insert(INSERT,"HighScore\n")

        self.textBox.delete(1.0, END)
        self.textBox.place(height=50, x=0, y=300)
        self.textBox.insert(INSERT,"Entrez votre nom : \n")

        self.userStringInput.place(height=50, x=200, y=300)
        self.boutonWriteHighScore.place(width=self.buttonWidth, x=(self.root.winfo_width()-self.buttonWidth)/2, y=700)






#Declaration des objets
class Vue:
    def __init__(self):
        os.system('mode con:cols=125 lines=60')
        file = "Son/zap.wav"
        self.son = file

    #Fonction qui fait l'affichage de jeu dans la console
    def afficher(self, jeu):

        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain
        for y in range(0,jeu.surface_h):
            for x in range(0, jeu.surface_l):
                case_vide = True

                #Regarde dans la liste si il y a un element a cette position
                for objet in jeu.liste_objets:
                    #Si la case courante correspond a la case de la liste
                    if(x == objet.x and y == objet.y):

                        #Si c'est le docteur who
                        if(isinstance(objet, DrWho)):
                            print(chr(1),end='')
                            break
                        #Si c'est un Dalek
                        elif(isinstance(objet, Dalek)):
                            print(chr(177),end='')
                            break
                        #Si c'est un tas de ferraille
                        elif(isinstance(objet, Ferraille)):
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
    def resetSizePiece(self):
        pass

    def zapAnimation(self, jeu):

        #Nettoye l'ecran avant d'afficher le jeu de nouveau
        os.system('cls')

        #Affichage du terrain
        for y in range(0,jeu.surface_h):
            for x in range(0, jeu.surface_l):

                case_vide = True

                #Regarde dans la liste si il y a un element a cette position
                for objet in jeu.liste_objets:

                    #Si la case courante correspond a la case de la liste
                    if(x == objet.x and y == objet.y):
                        #Si c'est le docteur who
                        if(isinstance(objet, DrWho)):
                            print(chr(1),end='')
                            break
                        #Si c'est un Dalek
                        elif(isinstance(objet, Dalek)):
                            print(chr(177),end='')
                            break
                        #Si c'est un tas de ferraille
                        elif(isinstance(objet, Ferraille)):
                            print('#',end='')
                            break
                    elif((x == jeu.liste_objets[0].x-1 and y == jeu.liste_objets[0].y-1) or (x == jeu.liste_objets[0].x and y == jeu.liste_objets[0].y-1) or (x == jeu.liste_objets[0].x+1 and y == jeu.liste_objets[0].y-1) or (x == jeu.liste_objets[0].x+1 and y == jeu.liste_objets[0].y) or (x == jeu.liste_objets[0].x+1 and y == jeu.liste_objets[0].y+1) or (x == jeu.liste_objets[0].x and y == jeu.liste_objets[0].y+1) or (x == jeu.liste_objets[0].x-1 and y == jeu.liste_objets[0].y+1) or (x == jeu.liste_objets[0].x-1 and y == jeu.liste_objets[0].y)):
                        print('&',end='')
                        break
                else:
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
        time.sleep(0.7)


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
            elif key == b'i':
                return 13
        return 0

    def splashPasZapper(self):
        os.system('cls')
        print("\n\n\n\nPas de zappeur disponible !!!")
        time.sleep(0.7)

    def endGame(self, jeu, scoreDejaEntre = False):
        os.system("cls")
        print("GAME OVER !!!\n\n\n")
        print("Vague : "+str(jeu.vague))
        print("Points : "+str(jeu.points))
        if(not scoreDejaEntre):
            print("\n\nAppuyer sur 4 pour enregistrer votre score")
            print("\n\n\n\nAppuyez sur une touche (sauf 4) pour revenir au menu principal")
        else:
            print("\n\n\n\nAppuyez sur une touche pour revenir au menu principal")
        retour = self.getUserInputCode()

        if(not scoreDejaEntre and retour == 4):
            jeu.setHighScore(self.getUserName(jeu))
            return self.endGame(jeu,True)



    def menu(self,parent):

        while (True):#boucle infini tant que le retour de la fonction nest pas appele
            os.system("cls")
            print("Les Daleks contre Dr. Who")
            print("_________________________\n\n\n")
            print("1. Jouer\n\n")
            print("2. Instruction\n\n")
            print("3. HighScores\n\n")
            print("4. About\n\n")
            print("5. Quitter")

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
        print("Les Daleks contre Dr. Who")
        print("_________________________")
        print("\nInstruction")

        print("\n\nPrésentation")
        print("\nDr. Who ( "+chr(1) + " )    /    Dalek ( "+chr(177) + " )    /    Ferraille ( # )")
        print("\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n")
        print("Objectif :")
        print("\nVotre objectif est de detruire le plus de Daleks possible avant qu'ils ne vous capturent.")
        print("\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n")
        print("Déplacement :")
        print("\nUtiliser les touches du clavier numerique (1 à 9) pour vous déplacer")
        print("\nLa touche ' * ' vous permet de vous téléporter aléatoirement n'importe quand")
        print("\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n")
        print("Arme :")
        print("\nLa touche ' - ' vous permet de déclancher un rayon lazer cosmique, à  utiliser avec parcimonie")
        print("\n\n\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n\n")
        print("Bonne chance Docteur. Ce n'est qu'une question de temps avant de vous voir succomber...")
        print("\n\nAppuyez sur ' q ' pour quitter en partie")
        print("\n\nAppuyez sur ' i ' pour afficher les instructions en partie")
        print("\n\n\n\nPesez sur une touche pour retourner au menu principal")
        self.getUserInputCode()

    def about(self):
        os.system('cls')
        print("Les Daleks contre Dr. Who")
        print("_________________________\n")
        print("À propos\n\n\n\n")
        print("Projet realiser par Arnaud et Xavier \n\n\nGit du projet: https://github.com/TeamGoatDev/Daleks_xavierhd_Arnaud474\n\n\n\n")
        print("Pesez sur une touche pour retourner au menu principal")
        self.getUserInputCode()

    def questionQuitterEnPartie(self):
        os.system("cls")
        print("\n\n\n\nQuitter?    oui[1] ou non[2]")
        return self.getUserInputCode()

    def highScore(self, highScore):
        os.system("cls")
        print("Les Daleks contre Dr. Who")
        print("_________________________\n")
        print("HightScores\n\n\n")
        if(highScore):
            for i in highScore:
                print(i + "\n\n")
        else:
            print("Il n'y a pas encore de hightScores...\n\nA vous de jouer!!!")

        print("\n\n\n\nPesez sur une touche pour retourner au menu principal")
        self.getUserInputCode()

    def getUserName(self, jeu):
        os.system("cls")
        print("Score : "+str(jeu.points))
        return input("Entrez votre nom : ")



class Jeu:
    def __init__(self, parent):
        self.parent = parent
        self.points = 0                 #Variable qui contient le nombre de points accumules par le joueur
        self.vague = 0                  #Numero de la vague en cours
        self.nb_dalek_restant = 0       #Nombre total des Daleks restant dans la liste
        self.nb_total_dalek = 0         #Nombre total de Dalek pour la vague courrante
        self.liste_objets = []          #Liste qui contiendra les daleks et le docteur
        self.surface_l = 30             #Largeur de la surface de jeu
        self.surface_h = 20             #Hauteur de la surface de jeu

    def setNextVague(self):
        self.nb_total_dalek += 5
        self.creerListe()   #Creation de la liste pour la nouvelle vague
        self.denombreDalek()
        self.vague += 1
        if(self.vague%15 == 14):
            self.surface_l += 1
            self.surface_h += 1
            if(self.vague%30 == 14):
                self.parent.vue.changerSizePiece(20,11)
        self.liste_objets[0].nb_zapper += 1

    def reset(self):
        self.points = 0
        self.vague = 0
        self.nb_dalek_restant = 0
        self.nb_total_dalek = 0
        self.liste_objets[:] = []
        self.surface_l = 30
        self.surface_h = 20
        self.parent.vue.resetSizePiece()

    def deplacerDalek(self):
        for i in self.liste_objets: #regarde tout les objets de la liste
                if(isinstance(i, Dalek)): #recherche d_objet Dalek
                    i.deplacer(self)

    def denombreDalek(self):
        self.nb_dalek_restant = 0

        for i in self.liste_objets: #regarde tout les objets de la liste
                if(isinstance(i, Dalek)): #recherche d_objet Dalek
                    self.nb_dalek_restant +=1


    #Fonction qui initialise la list contenant les objets(Personnages) pour le jeu (largeur de la surface, hauteur de la surface, nombre de daleks au total, liste qui contient les objets)
    def creerListe(self):

        position_ok = False
        position_xy = False

        #Creation de variables temporaires pour les postions x et y de chaque piece
        x = 0   # 1 est la premiere case contrairement a 0 dans un tableau
        y = 0   # 1 est la premiere case contrairement a 0 dans un tableau

        #Creation d"une position au hasard pour le docteur et inicialisation ci pas deja fait
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

                    for objet in self.liste_objets:
                        if(x != objet.x and y != objet.y):
                            position_xy = True


                #Si la case est a deux cases du Docteur Who
                if ( (x >= (self.liste_objets[0].x+2) or x <= (self.liste_objets[0].x-2)) or (y >= (self.liste_objets[0].y+2) or y <= (self.liste_objets[0].y-2)) ):
                        position_ok = True

            #Ajoute un Dalek valide a la liste
            self.liste_objets.append(Dalek(x,y,5))


    #Fonction gerant les collisions des daleks entre eux et les ferrailles
    def collision(self):

            for objet1 in self.liste_objets:#Boucle pour regader les differents objets de la liste

                if(isinstance(objet1, Dalek)):#Regarde si la piece est un Dalek

                    for objet2 in self.liste_objets: #Boucle pour faire la comparaison entre les deux pieces

                        #Si les positions de j et i sont identiques
                        if(objet1.x == objet2.x and objet1.y == objet2.y and self.liste_objets.index(objet1) != self.liste_objets.index(objet2)):

                            #Si l'objet de comparaison est un Dalek
                            if(isinstance(objet2, Dalek)):
                                self.liste_objets.append(Ferraille(objet1.x, objet1.y))
                                self.points += objet1.valeurPoint
                                self.liste_objets.remove(objet1)
                                self.points += objet2.valeurPoint
                                self.liste_objets.remove(objet2)
                                break

                            #Si l'objet de comparaison est une Ferraille
                            elif(isinstance(objet2, Ferraille)):
                                self.points += objet1.valeurPoint
                                self.liste_objets.remove(objet1)
                                break

    def getHighScore(self):

        try:
            tampon = open("high.Score", 'r+')#rb == read binary
            highScore = tampon.readlines()
            tampon.close()
            return highScore
        except:
            tampon = open("high.Score", 'w+')#w == write
            tampon.close()
            return 0



    def setHighScore(self, name):
        name = name.rstrip()
        tampon = open("high.Score", 'a')#ab == append
        aEcrire = name + '-->' + str(self.points) + '\n'
        tampon.write(aEcrire)
        tampon.close()


#Classe pour les objets qui seront dans la surface de jeu
class DrWho:
    def __init__(self, x, y):
        self.x = x  #Position en x sur la surface de jeu
        self.y = y #Position en y sur la surface de jeu
        self.nb_zapper = 0 #Nombre de zapper dont a droit Dr Who

    def notDead(self, jeu):
        for i in jeu.liste_objets:
            if(self.x == i.x and self.y == i.y):
                if(not isinstance(i, DrWho)):
                    return False #veux dire qu_il est mort

        return True

    def zapper(self, jeu):

        for objet in reversed(jeu.liste_objets):
            if((objet.x == self.x-1 and objet.y == self.y-1) or (objet.x == self.x and objet.y == self.y-1) or (objet.x == self.x+1 and objet.y == self.y-1) or (objet.x == self.x+1 and objet.y == self.y) or (objet.x == self.x+1 and objet.y == self.y+1) or (objet.x == self.x and objet.y == self.y+1) or (objet.x == self.x-1 and objet.y == self.y+1) or (objet.x == self.x-1 and objet.y == self.y)):
                if(isinstance(objet, Dalek)):
                    jeu.points += objet.valeurPoint
                    jeu.liste_objets.remove(objet)
        self.nb_zapper -= 1






    def teleportation(self, jeu):

        position_ko = True
        compteur = 0 # cherche un certain nombre de fois une bonne case puis s_il ne trouve pas, redonne le choix a l'usager quoi faire

        while position_ko == True:#Tant que la position n'est pas une position valide par rapport a la postion des Daleks

            x = random.randint(0, jeu.surface_l-1)
            y = random.randint(0, jeu.surface_h-1)

            compteur +=1

            for objet in jeu.liste_objets:
                #Si la case est a au moins deux cases du Dalek
                if (x >= objet.x+2 or x <= objet.x-2 or y >= objet.y+2 or y <= objet.y-2):
                    position_ko = False
                else:
                    position_ko = True
                    break

            if(compteur == 30):
                break
        else:
            self.x = x
            self.y = y
            return True#ca a marcher
        return False    #ca n_a pas marcher





     #Fonction qui gere le deplacement du joueur
    def deplacer(self, jeu, key):

        var = 1#variable pour augmenter la largeure du dÃ©placement du joueur
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
            for objet in jeu.liste_objets:
                #Determine si il y a une piece sur l'endroit ou le joueur veut se deplacer
                if(jeu.liste_objets[0].x+v_x == objet.x and jeu.liste_objets[0].y+v_y == objet.y):
                    if(not isinstance(objet, DrWho)):
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
        except :#ChildProcessError as e:
            #print(e.args)
            self.vue = Vue2(self)
            self.vue.menu()
            self.vue.root.mainloop()


    def newGame(self):
        self.jeu.reset()
        self.jeu.setNextVague()
        self.vue.setBackground()
        self.vue.afficher(self.jeu)


    def gameLOOP(self):

        self.jeu.reset()
        self.jeu.setNextVague()
        continuer = 1           #Afin de savoir si le controleur doit redonner le tour au joueur pour un faux mouvement

        while (continuer == 1):  #tant que turn retourne 1, donc que continuer est a 1, la partie en cours va continuer

            continuer = 0
            while (not continuer):#tant que turn retourne 0, donc que continuer est a 0, c_est le meme tour qui roule en boucle (tant que le joueur n'entre pas une valeur accepte ou que sont mouvement a reussi)
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
            if(not self.jeu.liste_objets[0].deplacer(self.jeu, keyCode)):     #Deplacement du DrWho donc : si le docteur n_a pas pu ce deplacer...
                return 0

        elif(keyCode == 10):
            if(not self.jeu.liste_objets[0].teleportation(self.jeu)):    #Teleportation du DrWho donc : si le docteur n_a pas pu se teleporter...
                return 0

        elif(keyCode == 11):                                #Zappeur du DrWho
            if(self.jeu.liste_objets[0].nb_zapper > 0):
                winsound.PlaySound(self.vue.son, winsound.SND_FILENAME | winsound.SND_ASYNC)
                self.vue.zapAnimation(self.jeu)             #Affichage du zap sur l_espace de jeu (le zap de drwho graphique)
                self.jeu.liste_objets[0].zapper(self.jeu)   #Le zap de drwho logique
            else:
                self.vue.splashPasZapper()

                return 0

        elif(keyCode == 12):                                #Pour quitter en pleine partie
            retour = self.vue.questionQuitterEnPartie()
            if(retour == 1):
                return 2
            else:
                return 0
        elif(keyCode == 13):                                #Pour afficher les instruction en pleine partie
            retour = self.vue.instruction()
            return 0

        self.jeu.deplacerDalek() #Deplacement automatique des Dalek
        self.jeu.collision() #Verifie les collisions
        self.jeu.denombreDalek()#compte les daleks restant

        if (not self.jeu.liste_objets[0].notDead(self.jeu)):
            self.jeu.liste_objets[:] = []
            if(self.jeu.points > 0):
                retour = self.vue.endGame(self.jeu)
            else:
                retour = self.vue.endGame(self.jeu, True)
            return 2

        self.vue.afficher(self.jeu) #Affichage de la surface de jeu
        return 1 #Tout est aller comme il faut


if __name__ == "__main__":
    c = Controleur()


