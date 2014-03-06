from tkinter import *
import os

class Affichage():
    def __init__(self, parent):
        self.parent=parent
        self.root=Tk()
        self.root.resizable(0,0)
        self.root.title("Launcher")
        self.root.geometry("1200x800")

        #Update la grosseur du frame pour qu'on puisse utiliser winfo
        self.root.update()

        #Background pour le menu
        self.imageBackground = PhotoImage(file="bg.gif")    
        self.labelBackground = Label(self.root,image=self.imageBackground)
        
        #Boutons
        self.boutonShell = Button(self.root, text='Lancer en Console', bg='black', fg='white', activebackground='blue', activeforeground='white', command=self.parent.launchConsole)
        self.boutonGraphique = Button(self.root, text='Lancer en GUI', bg='black', fg='white', activebackground='blue', activeforeground='white', command=self.parent.launchGUI)
        

    def menu(self):
        self.labelBackground.place(x=0, y=0)
        self.boutonShell.place(y=300, width=self.root.winfo_width()/2, height=self.root.winfo_height()-400)
        self.boutonGraphique.place(x=599, y=300,width=self.root.winfo_width()/2, height=self.root.winfo_height()-400)
        
class Launch():
    def __init__(self):
        self.affichage=Affichage(self)
        self.affichage.menu()
        self.affichage.root.mainloop()

    def launchConsole(self):
        self.affichage.root.destroy()
        
        os.system("C:\Python32\python.exe Dalek2.0.py -shell")
        os.system("C:\Python33\python.exe Dalek2.0.py -shell")
                
        

    def launchGUI(self):
        self.affichage.root.destroy()     
        os.system("C:\Python32\python.exe Dalek2.0.py")
        os.system("C:\Python33\python.exe Dalek2.0.py")
    
        

    
        
   
if __name__ == '__main__':
    c=Launch()
