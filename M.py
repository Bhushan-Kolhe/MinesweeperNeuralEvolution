from tkinter import *
from tkinter.filedialog import askopenfilename
from G import GeneticAlgorithm
import random
import threading


event2canvas = lambda e, c: (c.canvasx(e.x), c.canvasy(e.y))

class Minesweeper():
    def __init__(self):
        self.IsPlaying = True
        self.score = 0
        self.width = 500
        self.height = 500
        self.BlocksPerRow = 10
        self.NoOfBombs = 15
        self.Bombs = []
        self.openTiles = []
        self.Tiles = [0 for i in range(self.BlocksPerRow**2)]
        self.CurrentTiles = [-1 for i in range(self.BlocksPerRow**2)]
        self.root = Tk()
        self.root.title("Minesweeper")
        self.frame = Frame(self.root, bd=2, relief=SUNKEN)
        self.frame.grid(column=0, row=0)
        self.canvas = Canvas(self.frame, bd=0, bg="#f7f0bb")
        self.canvas.grid(row=0, column=0)
        self.root.resizable(False, False)
        self.canvas.config(width=self.width, height=self.height)
        self.BlockSize = int(self.width/self.BlocksPerRow)
        for i in range(self.NoOfBombs):
            x = random.randint(0,self.BlocksPerRow**2-1)
            while x in self.Bombs:
                x = random.randint(0,self.BlocksPerRow**2-1)
            self.Bombs.append(x)
        
        #print(self.Bombs)
        
        for b in self.Bombs:
            if((b+1)%self.BlocksPerRow==0):
                self.Tiles[b-1] +=1
                if b - self.BlocksPerRow >0:
                    self.Tiles[b - self.BlocksPerRow] += 1
                    self.Tiles[b - self.BlocksPerRow - 1] +=1
                if b + self.BlocksPerRow < self.BlocksPerRow**2:
                    self.Tiles[b + self.BlocksPerRow] += 1
                    self.Tiles[b + self.BlocksPerRow - 1] += 1
            elif (b)%self.BlocksPerRow == 0:
                self.Tiles[b+1] +=1
                if b - self.BlocksPerRow >0:
                    self.Tiles[b - self.BlocksPerRow] += 1
                    self.Tiles[b - self.BlocksPerRow + 1] +=1
                if b + self.BlocksPerRow < self.BlocksPerRow**2:
                    self.Tiles[b + self.BlocksPerRow] += 1
                    self.Tiles[b + self.BlocksPerRow + 1] += 1
            else:
                self.Tiles[b+1] += 1
                self.Tiles[b-1] += 1
                if b+self.BlocksPerRow < self.BlocksPerRow**2:
                    self.Tiles[b+self.BlocksPerRow] += 1
                    self.Tiles[b+self.BlocksPerRow+1] += 1
                    self.Tiles[b+self.BlocksPerRow-1] += 1
                if b-self.BlocksPerRow > 0:
                    self.Tiles[b-self.BlocksPerRow] += 1    
                    self.Tiles[b-self.BlocksPerRow+1] += 1
                    self.Tiles[b-self.BlocksPerRow-1] += 1

        for b in self.Bombs:
            self.Tiles[b] = 'X'
        
        
        for i in range(self.BlocksPerRow-1):
            self.canvas.create_line(self.BlockSize * (i+1), 0, self.BlockSize * (i+1), self.height, fill="#51504a")
            self.canvas.create_line(0, self.BlockSize * (i+1), self.width, self.BlockSize * (i+1), fill="#51504a")

        self.canvas.bind("<Control-ButtonPress-1>",self.callGeneticAlgorithm)
        self.canvas.bind("<Control-ButtonPress-3>",self.resetGame)
        self.canvas.bind("<ButtonRelease-1>",self.revealTile)
        self.canvas.bind("<ButtonRelease-3>",self.markTile)
        self.root.mainloop()
        
    def callGeneticAlgorithm(self,event):
        G = GeneticAlgorithm(self, False, 25)
        threading.Thread(target=G.trainNetwork).start()
        #G.trainNetwork()

    def showTile(self, CurrentTile, Vno, Hno):
        global BlocksPerRow
        global openTiles
        if self.Tiles[CurrentTile] == 0:
            if CurrentTile in self.openTiles:
                return
            self.canvas.create_rectangle((Hno-1)*self.BlockSize, (Vno-1)*self.BlockSize,Hno*self.BlockSize, Vno*self.BlockSize, fill="#51504a")
            self.CurrentTiles[CurrentTile] = 50
            self.openTiles.append(CurrentTile)
            self.score += 1
            if (CurrentTile+1)%self.BlocksPerRow != 0:
                self.showTile(CurrentTile+1, Vno, Hno+1)
            if (CurrentTile)%self.BlocksPerRow != 0:
                self.showTile((CurrentTile-1), Vno, Hno-1)        
            if (CurrentTile)+self.BlocksPerRow < self.BlocksPerRow**2:
                self.showTile(CurrentTile+self.BlocksPerRow, Vno+1, Hno)
            if (CurrentTile)-self.BlocksPerRow > 0:
                self.showTile(CurrentTile-self.BlocksPerRow, Vno-1, Hno)
        elif self.Tiles[CurrentTile] == 'X':
            if CurrentTile in self.openTiles:
                return
            self.canvas.create_rectangle((Hno-1)*self.BlockSize, (Vno-1)*self.BlockSize,Hno*self.BlockSize, Vno*self.BlockSize, fill="#51504a")
            self.openTiles.append(CurrentTile)
            self.IsPlaying = False
            self.canvas.unbind("<ButtonRelease-3>")
            self.canvas.unbind("<Control-ButtonPress-1>")
            self.canvas.unbind("<Control-ButtonRelease-3>")
            self.canvas.unbind("<ButtonRelease-1>")
            #print("GameOver : {} {}".format(self.score,self.CurrentTiles))
            #self.showAllTiles()
            #self.resetGame()
            return
        else:
            if CurrentTile in self.openTiles:
                return
            self.canvas.create_rectangle((Hno-1)*self.BlockSize, (Vno-1)*self.BlockSize,Hno*self.BlockSize, Vno*self.BlockSize, fill="#51504a")
            self.openTiles.append(CurrentTile)
            self.CurrentTiles[CurrentTile] = self.Tiles[CurrentTile] * 100
            self.canvas.create_text(25 + (Hno-1)*self.BlockSize, 25 + (Vno-1)*self.BlockSize,fill="#828282",font="Times 30 bold",
                        text=self.Tiles[CurrentTile])
            self.score += 1
            return

    def isPlaying(self):
        return self.IsPlaying

    def revealTile(self, event):
        global Tiles
        cx, cy = event2canvas(event, self.canvas)
        Vno = int(cy/self.BlockSize) + 1
        Hno = int(cx/self.BlockSize) + 1
        CurrentTile = self.BlocksPerRow*(Vno-1)+Hno-1
        self.showTile(CurrentTile, Vno, Hno)

    def getCurrentTiles(self):
        return self.CurrentTiles

    def showAllTiles(self):
        for i in range(self.BlocksPerRow**2):
            self.canvas.create_rectangle((i%self.BlocksPerRow)*self.BlockSize, self.BlockSize*int(i/self.BlocksPerRow)*self.BlockSize,(i%self.BlocksPerRow+1)*self.BlockSize, self.BlockSize*int(i/self.BlocksPerRow+1)*self.BlockSize, fill="#51504a")
            if self.Tiles[i] != 0:
                self.canvas.create_text(25 + self.BlockSize*(i%self.BlocksPerRow), 25 + self.BlockSize*int(i/self.BlocksPerRow),fill="#828282",font="Times 30 bold",
                        text=self.Tiles[i])
        for i in range(self.BlocksPerRow-1):
            self.canvas.create_line(self.BlockSize * (i+1), 0, self.BlockSize * (i+1), self.height)
            self.canvas.create_line(0, self.BlockSize * (i+1), self.width, self.BlockSize * (i+1))
            
    def markTile(self, event):
        cx, cy = event2canvas(event, self.canvas)
        Vno = int(cy/self.BlockSize) + 1
        Hno = int(cx/self.BlockSize) + 1
        self.canvas.create_text(25 + (Hno-1)*self.BlockSize, 25 + (Vno-1)*self.BlockSize,fill="#c10707",font="Times 30 bold",
                        text='M')

    def getScore(self):
        return self.score

    def resetGame(self,event=None):
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="#f7f0bb")
        self.IsPlaying = True
        self.score = 0
        self.Bombs = []
        self.openTiles = []
        self.Tiles = [0 for i in range(self.BlocksPerRow**2)]
        self.CurrentTiles = [-1 for i in range(self.BlocksPerRow**2)]
        self.BlockSize = int(self.width/self.BlocksPerRow)
        for i in range(self.NoOfBombs):
            x = random.randint(0,self.BlocksPerRow**2-1)
            while x in self.Bombs:
                x = random.randint(0,self.BlocksPerRow**2-1)
            self.Bombs.append(x)
        
        #print(self.Bombs)
        
        for b in self.Bombs:
            if((b+1)%self.BlocksPerRow==0):
                self.Tiles[b-1] +=1
                if b - self.BlocksPerRow >0:
                    self.Tiles[b - self.BlocksPerRow] += 1
                    self.Tiles[b - self.BlocksPerRow - 1] +=1
                if b + self.BlocksPerRow < self.BlocksPerRow**2:
                    self.Tiles[b + self.BlocksPerRow] += 1
                    self.Tiles[b + self.BlocksPerRow - 1] += 1
            elif (b)%self.BlocksPerRow == 0:
                self.Tiles[b+1] +=1
                if b - self.BlocksPerRow >0:
                    self.Tiles[b - self.BlocksPerRow] += 1
                    self.Tiles[b - self.BlocksPerRow + 1] +=1
                if b + self.BlocksPerRow < self.BlocksPerRow**2:
                    self.Tiles[b + self.BlocksPerRow] += 1
                    self.Tiles[b + self.BlocksPerRow + 1] += 1
            else:
                self.Tiles[b+1] += 1
                self.Tiles[b-1] += 1
                if b+self.BlocksPerRow < self.BlocksPerRow**2:
                    self.Tiles[b+self.BlocksPerRow] += 1
                    self.Tiles[b+self.BlocksPerRow+1] += 1
                    self.Tiles[b+self.BlocksPerRow-1] += 1
                if b-self.BlocksPerRow > 0:
                    self.Tiles[b-self.BlocksPerRow] += 1    
                    self.Tiles[b-self.BlocksPerRow+1] += 1
                    self.Tiles[b-self.BlocksPerRow-1] += 1
        
        for b in self.Bombs:
            self.Tiles[b] = 'X'
        
        
        for i in range(self.BlocksPerRow-1):
            self.canvas.create_line(self.BlockSize * (i+1), 0, self.BlockSize * (i+1), self.height, fill="#51504a")
            self.canvas.create_line(0, self.BlockSize * (i+1), self.width, self.BlockSize * (i+1), fill="#51504a")

        self.canvas.bind("<Control-ButtonPress-1>",self.callGeneticAlgorithm)
        self.canvas.bind("<Control-ButtonPress-3>",self.resetGame)
        self.canvas.bind("<ButtonRelease-1>",self.revealTile)
        self.canvas.bind("<ButtonRelease-3>",self.markTile)

B = Minesweeper()
