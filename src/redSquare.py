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
        self.creerFormes()
        self.getHighScores()
        
    def getHighScores(self):

        temp = []
        
        #Obtenir les Highscores dans le fichier .csv
        with open('highScores.csv', 'rt') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
                temp.append(row)

        #Changer les Strings en float    
        if(temp):
            for i in temp:
                i[1] = float(i[1])
                
        #Sort en ordre croissant
        temp.sort(key=lambda joueur: joueur[1])
        
        #Reverse la liste pour la mettre en ordre decroissant
        temp.reverse()

        #On insert la liste temp dans highScores
        self.highScores = temp
        print(len(self.highScores))

        
    
    def newHighScore(self):
        
        #Si il n'y a pas de Highscore
        if(len(self.highScores) == 0):
            highScore = [self.parent.vue.entrerHighScore.get()[:7],round(self.temps, 2)]
            self.highScores.append(highScore)
            
        #Sinon si il y a deja des highscores
        else:
            #On parcours la liste de highScores
            for score in self.highScores:
                print(str(score[1]), self.temps)

                #Si le temps est plus grand que celui de ce highscore
                if(self.temps > score[1]):
                    #On insert le highScore à cette position
                    highScore = [self.parent.vue.entrerHighScore.get()[:7],round(self.temps,2)]
                    self.highScores.insert(self.highScores.index(score),highScore)
                    break
                
        #On clear le champ et reset le temps à 0
        self.parent.vue.entrerHighScore.delete(0, END)
        self.temps = 0

        #On enleve les widgets devant la surface de jeu
        self.parent.vue.labelYouDied.place_forget()
        self.parent.vue.entrerHighScore.place_forget()
        self.parent.vue.boutonOK.place_forget()

        #On update l'affichage des highScores
        self.parent.vue.afficherHighScore()
        
        print(str(len(self.highScores)))

        

    
    def collisionMurJoueur(self):
        
        #Si le joueur touche la limite de la surface de jeu
        if(self.joueur.x1 <= 0 or self.joueur.x2 >= self.surfaceX or self.joueur.y1 <= 0 or self.joueur.y2 >= self.surfaceY):
            self.vivant = False

        return self.vivant
            
            
        
    def collisionMurFormes(self):

        #Pour chaque forme de la liste
        for forme in self.formes:
            #Si la forme touche a la limite de la surface de dessin
            if(forme.x1 <= 0 or forme.x2 >= self.surfaceX or forme.y1 <= 0 or forme.y2 >= self.surfaceY):
                #Si x1 est plus petit que 0 ou si x2 est plus grand que la surface
                if(forme.x1 <= 0 or forme.x2 >= self.surfaceX):
                    if(forme.vX < 0):
                        forme.vX -= 1
                    else:
                        forme.vX += 1
                        
                    forme.vX = -forme.vX
                    
                #Si y1 est plus petit que 0 ou si y2 est plus grand que la surface  
                elif(forme.y1 <= 0 or forme.y2 >= self.surfaceY):
                    if(forme.vY < 0):
                        forme.vY -= 1
                    else:
                        forme.vY += 1
                    
                    forme.vY = -forme.vY

    def changementDirection(self):
        #Selection aleatoire du pourcentage
        randomPourcentage = random.randint(0,100)
        #Longueur de la liste de formes
        indexForme = len(self.formes)-1
        #Selection aleatoire d'un index 
        randomIndex = random.randint(0,indexForme)
        #Chance qu'il y ait un changement de direction
        chance = 2

        #Si le poucentage est plus petit que chance
        if(randomPourcentage < chance):
            self.formes[randomIndex].vX = self.formes[randomIndex].vX*-1
            self.formes[randomIndex].vY = self.formes[randomIndex].vY*-1
            
            
        
        
    def update(self):
        #Update du temps de jeu
        self.temps = time.time() - self.temps_debut
        self.parent.vue.labelTemps.configure(text="Temps : "+str(round(self.temps,2)))

        #Update des positions des formes
        for forme in self.formes:
            forme.x1 += forme.vX
            forme.x2 += forme.vX
            forme.y1 += forme.vY
            forme.y2 += forme.vY
            

    def creerFormes(self):

        #Vitesse de depart des formes
        v = 5
        
        for i in range(0,4):

            #Selection aleatoire des grandeurs
            width = random.randint(40, 100)
            height = random.randint(40,100)

            #Premiere forme
            if(i == 0):
                posX = random.randint(0,300)
                posY = random.randint(0,300)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", v, v))
            #Deuxieme forme
            elif(i == 1):
                posX = random.randint(0,300)
                posY = random.randint(500,700)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", v, -v))
            #Troisieme forme
            elif(i == 2):
                posX = random.randint(500,700)
                posY = random.randint(0,300)
                self.formes.append(Formes.FormeMobile(posX, posY, posX+width, posY+height, "blue", -v, v))
            #Quatrieme forme
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
        self.estSelect = None
        self.root.geometry(str(self.parent.modele.surfaceX+400)+"x"+str(self.parent.modele.surfaceY+self.borderSize*2))

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
        self.listeHighScore = Listbox(self.root, font=("Arial", 24))
        self.labelHighScore = Label(self.root,text="High Scores", font=("Arial",24),bg='black', fg='white',anchor=N)

        #SetUp Vitesse
        self.labelVitesse = Label(self.root, text="Vitesse", font=("Arial",16), fg='white', bg='black', anchor=N)
        self.scaleVitesse = Scale(self.root, from_=15, to=35, orient=HORIZONTAL)
        self.scaleVitesse.set(25)
        self.labelVitesse.place(x=900, y=750, width=250)
        self.scaleVitesse.place(x=900, y=800, width=250)
        
        #Mouse Motion event
        self.surfaceJeu.bind("<B1-Motion>", self.moveRedSquare)
        self.surfaceJeu.bind("<Button-1>", self.debuterMouvement)
        self.surfaceJeu.bind("<ButtonRelease-1>", self.stopMouvement)

        #Affichage Initial
        self.afficherFormes()
        self.afficherHighScore()
        

    
    def fermeture(self):
        print("fermeture")
        #Fermeture du fichier .csv avec les nouveaux highScores
        with open("highScores.csv", "wt", newline="") as f:
            #Écriture dans le fichier .csv
            writer = csv.writer(f)
            writer.writerows(self.parent.modele.highScores)
        #Destruction du root
        self.root.destroy()
    
    def afficherFormes(self):
        #On efface les formes de la surface
        self.surfaceJeu.delete("formes")

        #On affiche les formes
        for forme in self.parent.modele.formes:
            self.surfaceJeu.create_rectangle(forme.x1, forme.y1, forme.x2, forme.y2, fill=forme.couleur, outline=forme.couleur, tags="formes")

    def afficherHighScore(self):

        #On efface le listBox
        self.listeHighScore.delete(0, END)

        print("highscore")

        #Si on a moins de 10 highScores
        if(len(self.parent.modele.highScores) < 10):
            h = len(self.parent.modele.highScores)
        #Sinon prendre les 10 premiers highScores
        else:
            h = 10
        #On insert les 10 premiers highScores dans la listBox
        for i in range(0,h):
            self.listeHighScore.insert(END, self.parent.modele.highScores[i][0]+" "+str(self.parent.modele.highScores[i][1]))
        
        self.listeHighScore.place(x=900, y=50, width=250)
        self.labelHighScore.place(x=900, y=0, width=250)
        
            
    #Permet de bouger le carré rouge
    def moveRedSquare(self, event):
        #Si le carré rouge est tenu par le joueur
        if(self.enMouvement and self.estSelect):
            self.surfaceJeu.delete("joueur")
            self.parent.modele.joueur.x1 = event.x-(self.parent.modele.sizeJoueur/2)
            self.parent.modele.joueur.y1 = event.y-(self.parent.modele.sizeJoueur/2)
            self.parent.modele.joueur.x2 = event.x+(self.parent.modele.sizeJoueur/2)
            self.parent.modele.joueur.y2 = event.y+(self.parent.modele.sizeJoueur/2)
            #Regarde si le joueur touche a un mur, si il ne touche pas un mur on return True et on passe dans le if
            if(self.parent.modele.collisionMurJoueur()):
                self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1,
                                                 self.parent.modele.joueur.y1,
                                                 self.parent.modele.joueur.x2,
                                                 self.parent.modele.joueur.y2,
                                                 fill=self.parent.modele.joueur.couleur,
                                                 outline=self.parent.modele.joueur.couleur, tags="joueur")
            #Sinon le joueur est mort et on le reinitialise a sa position de départ
            else:
                self.enMouvement = False
                self.surfaceJeu.delete("joueur")
                self.parent.modele.joueur = Formes.Forme((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2, (self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2, ((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, ((self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, 'red')
                self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")

    #S'execute lorsqu'on clique sur le carré rouge
    def debuterMouvement(self, event):
        #Verification pour déterminer si on clique sur le carré rouge
        if(event.x >= self.parent.modele.joueur.x1 and event.x <= self.parent.modele.joueur.x2):
            if(event.y >= self.parent.modele.joueur.y1 and event.y <= self.parent.modele.joueur.y2):
                if(self.estSelect == None and not self.enMouvement):
                    #On initialise le temps
                    self.parent.modele.temps_debut = time.time()
                    self.enMouvement = True
                    self.estSelect = True
                    self.parent.modele.vivant = True 
                    self.parent.gameLoop()
                else:
                    self.estSelect = True
        

    #S'execute lorsqu'on lache le carré rouge
    def stopMouvement(self, event):
        self.estSelect = False
        """self.parent.modele.vivant = False
        self.surfaceJeu.delete("joueur")
        self.parent.modele.joueur = Formes.Forme((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2, (self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2, ((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, ((self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, 'red')
        self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")"""
    
    #Permet de déterminer si il y a collision entre le carré rouge et les formes
    def collisionFormes(self):
        
        joueur = self.parent.modele.joueur
        enCollision = self.surfaceJeu.find_overlapping(joueur.x1, joueur.y1, joueur.x2, joueur.y2)

        #Si il y a plusieurs objet a l'endroit du joueur 
        if(len(enCollision) >= 2):
            #Le joueur est mort
            self.parent.modele.vivant = False
            self.surfaceJeu.delete("joueur")
            #On reinitialise le carré rouge a sa position de depart
            self.parent.modele.joueur = Formes.Forme((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2, (self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2, ((self.parent.modele.surfaceX-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, ((self.parent.modele.surfaceY-self.parent.modele.sizeJoueur)/2)+self.parent.modele.sizeJoueur, 'red')
            self.surfaceJeu.create_rectangle(self.parent.modele.joueur.x1, self.parent.modele.joueur.y1, self.parent.modele.joueur.x2, self.parent.modele.joueur.y2, fill=self.parent.modele.joueur.couleur, outline=self.parent.modele.joueur.couleur, tags="joueur")
            
        
        
        
class Controleur:
    def __init__(self):
        #Initialisation du Modele
        self.modele = Modele(self)
        #Initialisation de la Vue
        self.vue = Vue(self)
        #On lance la mainloop
        self.vue.root.mainloop()

    def gameLoop(self):
        if(self.modele.vivant):
            self.modele.changementDirection()
            self.modele.update()
            self.vue.collisionFormes()
            self.modele.collisionMurFormes()
            self.vue.afficherFormes()
            self.vue.root.after(self.vue.scaleVitesse.get(),self.gameLoop)
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
