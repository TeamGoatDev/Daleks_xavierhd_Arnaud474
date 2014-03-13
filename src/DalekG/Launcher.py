from tkinter import *
import subprocess

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
        self.imageBackground = PhotoImage(file="Image/bg.gif")
        self.labelBackground = Label(self.root,image=self.imageBackground)

        #Boutons
        self.boutonShell = Button(self.root, text='Lancer en Console', bg='black', fg='white', activebackground='blue', activeforeground='white', command=self.parent.launchConsole)
        self.boutonGraphique = Button(self.root, text='Lancer en GUI', bg='black', fg='white', activebackground='blue', activeforeground='white', command=self.parent.launchGUI)

        #Texte
        self.textBox = Text(width=self.root.winfo_width(), bg='black', fg='white', font=('Arial', 30))

    def menu(self):
        self.labelBackground.place(x=0, y=0)
        self.textBox.place(height=50, x=0, y=240)
        self.textBox.delete(1.0, END)
        self.textBox.insert(INSERT,"      !!!      ATTENTION : Ce jeu a du son      !!!")
        self.boutonShell.place(y=300, width=self.root.winfo_width()/2, height=self.root.winfo_height()-400)
        self.boutonGraphique.place(x=599, y=300,width=self.root.winfo_width()/2, height=self.root.winfo_height()-400)
class Launch():
    def __init__(self):
        self.affichage=Affichage(self)
        self.affichage.menu()
        self.affichage.root.mainloop()

    def launchConsole(self):
        self.affichage.root.destroy()
        try:
            subprocess.call("C:\Python32\python.exe Dalek2.0.py -shell")
        except OSError:
            try:
                subprocess.call("C:\Python33\python.exe Dalek2.0.py -shell")
            except OSError:
                try:
                    subprocess.call("python Dalek2.0.py -shell")
                except OSError:
                    try:#cas xavier
                        subprocess.call("C:\Program Files\Python33 Dalek2.0.py -shell")
                    except OSError:
                        raise SystemExit
        


    def launchGUI(self):
        self.affichage.root.destroy()
        try:
            subprocess.call("C:\Python32\python.exe Dalek2.0.py")
        except OSError:
            try:
                subprocess.call("C:\Python33\python.exe Dalek2.0.py")
            except OSError:
                try:
                    subprocess.call("python Dalek2.0.py")
                except OSError:
                    try:#cas xavier
                        subprocess.call("C:\Program Files\Python33 Dalek2.0.py")
                    except OSError:
                        raise SystemExit
        





#    python launcher.py



if __name__ == '__main__':
    c=Launch()
