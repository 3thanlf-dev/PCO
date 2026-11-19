try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox


class Level(object):
    def __init__(self, root, xsbMatrix):
        self.root = root
        self.xsbMatrix = xsbMatrix

        # calcul des dimensions de la matrice
        nbrows = len(xsbMatrix)
        nbcolumns = 0

        for line in xsbMatrix:
            nbc = len(line)
            if nbc > nbcolumns:
                nbcolumns = nbc

        self.height = nbrows * 64 
        self.width = nbcolumns * 64 
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="gray")
        self.canvas.pack(side="top", expand=True)


        # on a besoin de deux matrices pour pouvoir déplacer les éléments déplacables
        # sans écraser les éléments non déplacables
        self.staticMatrix = []
        self.movableMatrix = []
        for lineIdx in range(nbrows):
            self.staticMatrix.append([])
            self.movableMatrix.append([])
            for elemIdx in range(nbcolumns):
                self.staticMatrix[lineIdx].append(None)
                self.movableMatrix[lineIdx].append(None)

        # Initialisation des matrices à partir de la matrice Xsb
        y = 0
        for lineIdx in range(len(xsbMatrix)):
            x = 0
            for elemIdx in range(len(xsbMatrix[lineIdx])):
                e = xsbMatrix[lineIdx][elemIdx]
                if e == '#':
                    image = tk.PhotoImage(file='wall.png')
                    self.staticMatrix[y][x] = tk.PhotoImage(file='wall.png')
                    self.canvas.create_image(x*64, y*64,image=self.staticMatrix[y][x], anchor=tk.NW, tag = "static")
                elif e == '@':
                    image = tk.PhotoImage(file='playerDown.png')
                    self.movableMatrix[y][x] = image
                    self.playerId = self.canvas.create_image(x*64, y*64,image=self.movableMatrix[y][x], anchor=tk.NW, tag = "movable")
                    self.playerX = x
                    self.playerY = y
                else:
                    None
                x = x + 1
            y = y + 1
            x = 0
        self.canvas.tag_raise("movable","static")

    def getwall(self,x , y):
        if self.xsbMatrix[y][x] == '#':
            print("mur")
            return True
        print("pas mur")
        return False


           
class Mover(object):

    def __init__(self, level):
        self.level = level


    def keypressed(self, event):
        level = self.level
        x = level.playerX
        y = level.playerY
        
        # adapter les coordonnées du player en fonction du déplacement voulu
        if event.keysym == 'Up':
            if level.playerY == 0:
                print("tu sors")
                return
            if level.getwall(x, (y - 1)):
                print("Aïe")
                return
            level.playerY = level.playerY - 1
            print("coordonnées : Y= ", level.playerY, " X= ", level.playerX)
        
        elif event.keysym == 'Down':
            if level.playerY == len(level.movableMatrix) - 1:
                print("tu sors")
                return
            if level.getwall(x, (y + 1)):
                print("Aïe")
                return
            level.playerY = level.playerY + 1
            print("coordonnées : Y= ", level.playerY, " X= ", level.playerX)
        
        elif event.keysym == 'Left':
            if level.playerX == 0:
                print("tu sors")
                return
            if level.getwall((x - 1), y):
                print("Aïe")
                return
            level.playerX = level.playerX - 1
            print("coordonnées : Y= ", level.playerY, " X= ", level.playerX)
        
        elif event.keysym == 'Right':
            if level.playerX == len(level.movableMatrix[0]) - 1:
                print("tu sors")
                return
            if level.getwall((x + 1), y):
                print("Aïe")
                return
            level.playerX = level.playerX + 1
            print("coordonnées : Y= ", level.playerY, " X= ", level.playerX)
        
        
        # déplacer l'image dans la bonne case de movableMatrix
        level.movableMatrix[level.playerY][level.playerX] = level.movableMatrix[y][x]
        # l'ancienne case de movableMatrix est mise à jour
        level.movableMatrix[y][x] = None
        # supprimer l'ancienne image dans le canvas
        level.canvas.delete(level.playerId)
        # créer une nouvelle image dans le canvas à la bonne coordonnée
        level.playerId = level.canvas.create_image(level.playerX * 64, level.playerY * 64, image=level.movableMatrix[level.playerY][level.playerX], anchor=tk.NW, tag="movable")



class Sokoban(object):
    '''
    Main Level class
    '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sokoban")
        mat = [
            [' ', ' ', '#', '#', '#'],
            [' ', ' ', '#', '.', '#'],
            [' ', ' ', '#', ' ', '#', '#', '#', '#'],
            ['#', '#', '#', '$', ' ', '$', '.', '#'],
            ['#', '.', ' ', '$', '@', '#', '#', '#'],
            ['#', '#', '#', '#', '$', '#'],
            [' ', ' ', ' ', '#', '.', '#'],
            [' ', ' ', ' ', '#', '#', '#'] ]
        self.level = Level(self.root, mat)
        self.mover = Mover(self.level)
        self.root.bind("<Key>", self.mover.keypressed)
    def play(self):
        self.root.mainloop()

Sokoban().play()
