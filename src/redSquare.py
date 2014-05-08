from tkinter import *
import Formes
import random
import time
import csv

class Modele:
    def __init__(self, parent):
        self.parent = parent
        self.surfaceX = 800
        self.surfaceY = 800
        self.sizeJoueur = 60
        self.temps = 0
        self.temps_debut = 0
        self.vivant = True
        self.highScores = []
        self.formes = []
        self.joueur = Formes.Forme((self.surfaceX-self.sizeJoueur)/2, (self.surfaceY-self.sizeJoueur)/2, ((self.surfaceX-self.sizeJoueur)/2)+self.sizeJoueur, ((self.surfaceY-self.sizeJoueur)/2)+self.sizeJoueur, 'red')

    def getHighScores(self):

        temp = []

        with open('highScores.csv', 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
                temp.append(row)

                
        if(temp):
            for i in temp:
                i[1] = float(i[1])

        temp.sort(key=lambda joueur: joueur[1])
        temp.reverse()

        self.highScores = temp
        print(len(self.highScores))

    def newHighScore(self):
        print("dedans")

        if(len(self.highScores) == 0):
            highScore = [self.parent.vue.entrerHighScore.get(),round(self.temps, 2)]
            self.highScores.append(highScore)
        else:
            for score in self.highScores:
                print(str(score[1]), self.temps)
                if(self.temps > score[1]):
                    print("marche")
                    highScore = [self.parent.vue.entrerHighScore.get(),round(self.temps,2)]
                    self.highScores.insert(self.highScores.index(score),highScore)
                    break

        self.temps = 0
            
        self.parent.vue.labelYouDied.place_forget()
        self.parent.vue.entrerHighScore.place_forget()
        self.parent.vue.boutonOK.place_forget()
        
        print(str(len(self.highScores)))

        

    
    def collisionMurJoueur(self):

        if(self.joueur.x1 <= 0 or self.joueur.x2 >= self.surfaceX or self.joueur.y1 <= 0 or self.joueur.y2 >= self.surfaceY):
            self.vivant = False

        return self.vivant
            
            
        
    def collisionMurFormes(self):

        for forme in self.formes:
            if(forme.x1 <= 0 or forme.x2 >= self.surfaceX or forme.y1 <= 0 or forme.y2 >= self.surfaceY):
                if(forme.x1 <= 0 or forme.x2 >= self.surfaceX):
                    if(forme.vX < 0):
                        forme.vX -= 1
                    else:
                        forme.vX += 1
                        
                    forme.vX = -forme.vX
                    
                elif(forme.y1 <= 0 or forme.y2 >= self.surfaceY):
                    if(forme.vY < 0):
                        forme.vY -= 1
                    else:
                        forme.vY += 1
                    
                    forme.vY = -forme.vY
                

    def update(self):
        self.temps = time.time() - self.temps_debut
        self.parent.vue.labelTemps.configure(text="Temps : "+str(round(self.temps,2)))
        
        for forme in self.formes:
            forme.x1 += forme.vX
            forme.x2 += forme.vX
            forme.y1 += forme.vY
            forme.y2 += forme.vY
            

    def creerFormes(self):

        v = 5
        
        for i in range(0,4):

            width = random.randint(40, 100)
            height = random.randint(40,100)
            
            if(i == 0):
                posX = random.randint(0,300)
                posY = random.randint(0,300)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", v, v))
            elif(i == 1):
                posX = random.randint(0,300)
                posY = random.randint(500,700)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", v, -v))
            elif(i == 2):
                posX = random.randint(500,700)
                posY = random.randint(0,300)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", -v, v))
            elif(i == 3):
                posX = random.randint(500,700)
                posY = random.randint(500,700)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", -v, -v))

            

class Vue:
    def __init__(self, parent):
        self.parent = parent
        self.root = Tk()
        self.root.resizable(0,0)
        self.root.title("Red Square")
        self.root.configure(background='black')
        self.root.protocol("WM_DELETE_WINDOW", self.fermeture)
        self.borderSize = 50
        self.enMouvement = False
        self.root.geometry(str(self.parent.modele.surfaceX+self.borderSize*2)+"x"+str(self.parent.modele.surfaceY+self.borderSize*2))

        #Surface de jeu
        self.surfaceJeu = Canvas(self.root, width=self.parent.modele.surfaceX,height=self.parent.modele.surfaceY, bg='white', highlightthickness=0)
        self.surfaceJeu.place(x=self.borderSize, y=self.borderSize)
        self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")

        #Labels 
        self.labelTemps = Label(self.root, text="Temps : 0", font=("Arial",16), fg='white', bg='black', anchor=NW)
        self.labelTemps.place(width=200)
        self.labelYouDied = Label(self.root, text="YOU DIED", font=("Old English Text MT", 60), fg='red', bg='black', anchor=N)

        #HighScore
        self.entrerHighScore = Entry(self.root, font=("Arial",16), fg='red', bg='black', justify=CENTER, insertbackground='red')
        self.boutonOK = Button(self.root, font=("Arial",16), fg='red', bg='black', text="OK", command=self.parent.modele.newHighScore)
        
        #Mouse Motion event
        self.surfaceJeu.bind("<B1-Motion>", self.moveRedSquare)
        self.surfaceJeu.bind("<Button-1>", self.debuterMouvement)
        self.surfaceJeu.bind("<ButtonRelease-1>", self.stopMouvement)


    
    def fermeture(self):
        print("fermeture")
        with open("highScores.csv", "wt", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.parent.modele.highScores)
        self.root.destroy()
    
    def afficherFormes(self):
        self.surfaceJeu.delete("patate")
        
        for forme in self.parent.modele.formes:
            self.surfaceJeu.create_rectangle(forme.x1, forme.y1, forme.x2, forme.y2, fill=forme.couleur, outline=forme.couleur, tags="patate")
    
    def moveRedSquare(self, event):
        if(self.enMouvement):
            self.surfaceJeu.delete("joueur")
            self.parent.modele.joueur.x1 = event.x-(self.parent.modele.sizeJoueur/2)
            self.parent.modele.joueur.y1 = event.y-(self.parent.modele.sizeJoueur/2)
            self.parent.modele.joueur.x2 = event.x+(self.parent.modele.sizeJoueur/2)
            self.parent.modele.joueur.y2 = event.y+(self.parent.modele.sizeJoueur/2)
            if(self.parent.modele.collisionMurJoueur()):
                self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")
            else:
                self.enMouvement = False
                self.surfaceJeu.delete("joueur")
                self.parent.modele.joueur = Formes.Forme((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2, (self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2, ((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, ((self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, 'red')
                self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")


    def debuterMouvement(self, event):
        self.parent.modele.temps_debut = time.time()
        if(event.x >= self.parent.modele.joueur.x1 and event.x <= self.parent.modele.joueur.x2):
            if(event.y >= self.parent.modele.joueur.y1 and event.y <= self.parent.modele.joueur.y2):
                self.enMouvement = True
                self.parent.modele.vivant = True
                self.parent.gameLoop()

    def stopMouvement(self, event):
        self.enMouvement = False
        self.parent.modele.vivant = False
        self.surfaceJeu.delete("joueur")
        self.parent.modele.joueur = Formes.Forme((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2, (self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2, ((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, ((self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, 'red')
        self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")

    def collisionFormes(self):
        joueur = self.parent.modele.joueur
        enCollision = self.surfaceJeu.find_overlapping(joueur.x1, joueur.y1, joueur.x2, joueur.y2)

        if(len(enCollision) >= 2):
            self.parent.modele.vivant = False
            self.surfaceJeu.delete("joueur")
            self.parent.modele.joueur = Formes.Forme((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2, (self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2, ((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, ((self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, 'red')
            self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")
            
        
        
        
class Controleur:
    def __init__(self):
        self.modele = Modele(self)
        self.modele.creerFormes()
        self.modele.getHighScores()
        self.vue = Vue(self)
        self.vue.afficherFormes()
        self.vue.root.mainloop()

    def gameLoop(self):
        if(self.modele.vivant):
            self.modele.update()
            self.vue.collisionFormes()
            self.modele.collisionMurFormes()
            self.vue.afficherFormes()
            self.vue.root.after(10,self.gameLoop)
        else:
            self.vue.labelYouDied.place(y=330, x=0, width=900, height=200)
            self.vue.entrerHighScore.place(y=460, x=200)
            self.vue.boutonOK.place(y=450, x=600)
            self.vue.labelTemps.configure(text="Temps : "+str(round(self.modele.temps,2)))
            self.modele.formes = []
            self.modele.creerFormes()
            self.vue.afficherFormes()
            return
            
            

    

if __name__ == "__main__":
    c = Controleur()
