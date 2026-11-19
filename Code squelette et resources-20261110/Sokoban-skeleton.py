# -*- coding: utf-8 -*-
"""
@author: Alain Plantec

Voici un skelette possible.
Vous devez programmez les classes contenues dans ce squelette.
Les fonctions et leurs paramètres ainsi que les variables contenues dans le classes
ont du sens par rapport à une version programmée pour la préparation du projet.
Votre version sera forcément différente.
Donc, vous pouvez ajouter/retirer des variables et/ou des fonctions et/ou des paramètres.

"""
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

from sokobanXSBLevels import *
from enum import Enum


#Direction :
#    Utile pour gérer le calcul des positions pour les mouvements

class Direction(Enum):
    Up = 1
    Down = 2
    Left = 3
    Right = 4


#Position :
#    - stockage de coordoannées x et y,
#    - vérification de x et y par rapport à une matrice
#    - calcule de position relative à partir d'un offset (un décalage) et une direction 

class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'Position(' + str(self.x) + ',' + str(self.y) + str(')') 

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # retoune la position vers la direction #direction en tenant compte de l'offset
    #   Position(3,4).positionTowards(Direction.Right, 2) == Position(5,4)
    def positionTowards(self, direction, offset):
        offsets = {
            Direction.Up: (0, -offset),
            Direction.Down: (0, offset),
            Direction.Left: (-offset, 0),
            Direction.Right: (offset, 0),
        }
        if direction not in offsets:
            raise ValueError("Direction inconnue: " + str(direction))
        dx, dy = offsets[direction]
        return Position(self.x + dx, self.y + dy)

    # Retourne True si les coordonnées sont valides dans le wharehouse
    def isValidInWharehouse(self, wharehouse):
        return wharehouse.isPositionValid(self)

    # Convertit le receveur en une position correspondante dans un Canvas
    def asCanvasPositionIn(self, elem):
        lx = self.getX() * elem.getWidth() 
        ly = self.getY() * elem.getHeight()
        return Position(lx, ly)


#WharehousePlan : Plan de l'entrepot pour stocker les éléments.
#    Les éléments sont stockés dans une matrice (#rawMatrix)

class WharehousePlan(object):
    def __init__(self):
        # la matrice d'Elem
        self.rawMatrix = []

    def appendRow(self, row):
        self.rawMatrix.append(row)
                              
    def at(self, position):
        return self.rawMatrix[position.getY()][position.getX()]

    def atPut(self, position, elem):
        self.rawMatrix[position.getY()][position.getX()] = elem

    def isPositionValid(self, position):
        if position.getY() < 0 or position.getY() >= len(self.rawMatrix):
            return False
        if position.getX() < 0 or position.getX() >= len(self.rawMatrix[0]):
            return False
        return True

    def hasFreePlaceAt(self, position):
        return self.at(position).isFreePlace()

    def asXsbMatrix(self):
        return xsbMatrix(self.rawMatrix)


#Floor :
#    Représente une case vide de la matrice
#    (pas de None dans la matrice)

class Floor(object):
    def __init__(self):
        None
    def isMovable(self):
        return False
    def canBeCovered(self):
        return True
    def xsbChar(self):
        return ' '
    def isFreePlace(self):
        return True

#Goal :
#    Représente une localisation à recouvrir d'un BOX (objectif du jeu).
#    Le déménageur doit parvenir à couvrir toutes ces cellules à partir des caisses.
#    Un Goal est static, il est toujours déssiné en dessous :
#        Le zOrder est assuré par le tag du create_image (tag='static')
#        et self.canvas.tag_raise("movable","static") dans Level

class Goal(object):
    def __init__(self, canvas, position):
        self.canvas = canvas
        self.position = position
        self.image = tk.PhotoImage(file='goal.png')
        self.width = self.image.width()
        self.height = self.image.height()

        canvasPosition = position.asCanvasPositionIn(self)
        self.imageId = self.canvas.create_image(
            canvasPosition.getX(),
            canvasPosition.getY(),
            image=self.image,
            anchor=tk.NW,
            tag="static"
        )

    def isMovable(self):
        return False

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def canBeCovered(self):
        return True

    def xsbChar(self):
        return '.'

    def isFreePlace(self):
        return False


#Wall : pour délimiter les murs
#    Le déménageur ne peut pas traverser un mur.
#    Un Wall est static, il est toujours déssiné en dessous :
#        Le zOrder est assuré par le tag du create_image (tag='static')
#        et self.canvas.tag_raise("movable","static") dans Level

class Wall(object):
    def __init__(self, canvas, position):
        self.canvas=canvas
        self.position=position
        self.image = tk.PhotoImage(file='wall.png')
        self.width = self.image.width()
        self.height = self.image.height()

        canvasPosition = position.asCanvasPositionIn(self)
        self.imageId = self.canvas.create_image(canvasPosition.getX(),canvasPosition.getY(),image=self.image,anchor=tk.NW,tag="static")

    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMovable(self):
        return False

    def canBeCovered(self):
        return False

    def xsbChar(self):
        return '#'

    def isFreePlace(self):
        return False


#Box : Caisse à déplacer par le déménageur.
#    Etant donné qu'une caisse doit être déplacé, le canvas et la matrice sont necessaires pour
#    reconstruire l'image et mettre en oeuvre sont déplacement (dans le canvas et dans la matrice)
#    Un Box est "movable", il est toujours déssiné au dessus des objets "static" :
#        Le zOrder est assuré par le tag du create_image (tag='movable')
#        et self.canvas.tag_raise("movable","static") dans Level
#    Un Box est représenté differemment (image différente) suivant qu'il se situe sur un emplacement marqué par un Goal ou non.

class Box(object):
    def __init__(self, canvas, wharehouse, position, onGoal):
        self.canvas=canvas
        self.position=position
        self.warehouse=wharehouse
        self.onGoal=onGoal
        self.under = self.warehouse.at(position)
        self.onGoal = not self.under.isFreePlace()
        self.image = tk.PhotoImage(file='boxOnTarget.png' if self.onGoal else 'box.png')
        self.width = self.image.width()
        self.height = self.image.height()

        canvasPosition = position.asCanvasPositionIn(self)
        self.imageId = self.canvas.create_image(canvasPosition.getX(),canvasPosition.getY(),image=self.image,anchor=tk.NW,tag="movable")
        self.warehouse.atPut(position, self)

    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMovable(self):
        return True

    def canBeCovered(self):
        return False

    def moveTowards(self, direction):
        destination = self.position.positionTowards(direction, 1)
        if not destination.isValidInWharehouse(self.warehouse):
            return False

        destinationElement = self.warehouse.at(destination)
        if not destinationElement.canBeCovered():
            return False

        self.warehouse.atPut(self.position, self.under)
        self.position = destination
        self.under = destinationElement
        self.onGoal = not self.under.isFreePlace()
        self.warehouse.atPut(self.position, self)

        self.image = tk.PhotoImage(
            file='boxOnTarget.png' if self.onGoal else 'box.png'
        )
        self.canvas.itemconfigure(self.imageId, image=self.image)
        canvasPosition = self.position.asCanvasPositionIn(self)
        self.canvas.coords(
            self.imageId, canvasPosition.getX(), canvasPosition.getY()
        )
        return True
 
    def xsbChar(self):
        if self.under.isFreePlace(): return '$'
        else: return '*'

    def isFreePlace(self):
        return False

    def startGoalCoveredAnimation(self):
        return
 
    def cleanUpAnimation(self):
        return
    
    def goalCoveredAnimation(self):
        return
 
#Mover : C'est  le déménageur.
 #   La classe Mover met en oeuvre la logique du jeu dans #canMove et #moveTowards.
  #  Etant donné qu'un Mover se déplace, le canvas et la matrice sont necessaires pour
   # reconstruire l'image et mettre en oeuvre sont déplacement (dans le canvas et dans la matrice)
    #Un Mover est "movable", il est toujours déssiné au dessus des objets "static" :
     #   Le zOrder est assuré par le tag du create_image (tag='movable')
      #  et self.canvas.tag_raise("movable","static") dans Level
    #Un Box est représenté differemment (image différente) suivant la direction de déplacement (même si le dépplacement s'avère impossible).

class Mover(object):
    def __init__(self, canvas, wharehouse, position, onGoal):
        self.canvas=canvas
        self.position=position
        self.warehouse=wharehouse
        self.onGoal=onGoal
        self.under = self.warehouse.at(position)
        self.onGoal = not self.under.isFreePlace()
        self.image = tk.PhotoImage(file='playerDown.png')
        self.width = self.image.width()
        self.height = self.image.height()
        self.direction = Direction.Down
        self._animation_after_id = None
        self._animation_origin = None
        self._animation_offsets = []
        self._animation_step = 0

        canvasPosition = position.asCanvasPositionIn(self)
        self.imageId = self.canvas.create_image(canvasPosition.getX(),canvasPosition.getY(),image=self.image,anchor=tk.NW,tag="movable")
        self.warehouse.atPut(position, self)
        
         
    def getHeight(self):
        return self.height
    
    def getWidth(self):
        return self.width

    def isMoveable(self):
        return True

    def canBeCovered(self):
        return False

    def moveInCanvas(self, direction):
        #Retourne True si le Mover peut se déplacer dans la direction demandée.
        #Le calcul necessite de voir l'élément adjacent mais aussi l'élément suivant (offset de 2)
        destination = self.position.positionTowards(direction, 1)
        if not destination.isValidInWharehouse(self.warehouse):
            return False

        destinationElement = self.warehouse.at(destination)
        if destinationElement.canBeCovered():
            return True

        if not isinstance(destinationElement, Box):
            return False

        boxDestination = destination.positionTowards(direction, 1)
        if not boxDestination.isValidInWharehouse(self.warehouse):
            return False
        return self.warehouse.at(boxDestination).canBeCovered()


    def canMove(self, direction):
        return self.moveInCanvas(direction)

    #Pour le déplacement, il faut penser à déplacer éventuellemnt le Box et ensuite déplacer le Mover
    def moveTowards(self, direction):
        if not self.canMove(direction):
            return False

        destination = self.position.positionTowards(direction, 1)
        destinationElement = self.warehouse.at(destination)
        if isinstance(destinationElement, Box):
            destinationElement.moveTowards(direction)

        self.warehouse.atPut(self.position, self.under)
        self.position = destination
        self.under = self.warehouse.at(destination)
        self.onGoal = not self.under.isFreePlace()
        self.warehouse.atPut(self.position, self)

        canvasPosition = self.position.asCanvasPositionIn(self)
        self.canvas.coords(
            self.imageId, canvasPosition.getX(), canvasPosition.getY()
        )
        return True

    #Le Mover est représenté differemment suivant la direction de déplacement
    def setupImageForDirection(self, dir):
        images = {
            Direction.Up: 'playerUp.png',
            Direction.Down: 'playerDown.png',
            Direction.Left: 'playerLeft.png',
            Direction.Right: 'playerRight.png',
        }
        if dir not in images:
            raise ValueError("Direction inconnue: " + str(dir))

        self.direction = dir
        self.image = tk.PhotoImage(file=images[dir])
        self.canvas.itemconfigure(self.imageId, image=self.image)

        #Pour le déplacement :
         #   - image changée en fonction de la direction
          #  - si on ne peut pas se déplacer dans cette direction -> abandon
           # - sinon, bin le Mover est déplacé
    def push(self, direction):
        self.setupImageForDirection(direction)
        if not self.canMove(direction):
            self.startImpossiblePushAnimation()
            return False
        return self.moveTowards(direction)

    def xsbChar(self):
        if self.under.isFreePlace(): return '@'
        else: return '+'

    def isFreePlace(self):
        return False

    def startImpossiblePushAnimation(self):
        self.cleanUpAnimation()
        self._animation_origin = self.canvas.coords(self.imageId)
        offsets = {
            Direction.Up: (0, -4),
            Direction.Down: (0, 4),
            Direction.Left: (-4, 0),
            Direction.Right: (4, 0),
        }
        dx, dy = offsets[self.direction]
        self._animation_offsets = [
            (dx, dy), (dx, dy), (0, 0), (0, 0)
        ]
        self._animation_step = 0
        self.impossiblePushAnimation()

    def cleanUpAnimation(self):
        if self._animation_after_id is not None:
            self.canvas.after_cancel(self._animation_after_id)
            self._animation_after_id = None
        if self._animation_origin is not None:
            self.canvas.coords(self.imageId, *self._animation_origin)
            self._animation_origin = None
        self._animation_offsets = []
        self._animation_step = 0

    def impossiblePushAnimation(self):
        if self._animation_step >= len(self._animation_offsets):
            self.cleanUpAnimation()
            return

        self._animation_after_id = None
        dx, dy = self._animation_offsets[self._animation_step]
        x, y = self._animation_origin
        self.canvas.coords(self.imageId, x + dx, y + dy)
        self._animation_step += 1
        self._animation_after_id = self.canvas.after(
            40, self.impossiblePushAnimation
        )

    #Le jeux avec tout ce qu'il faut pour dessiner et stocker/gérer la matrice d'éléments

class Level(object):
    def __init__(self, root, xsbMatrix):
        self.root = root
        self.wharehouse = WharehousePlan()
        self.initWharehouseFromXsb(xsbMatrix)
        self.root.bind("<Key>", self.keypressed)

    def initWharehouseFromXsb(self,xsbMatrix):
        # legend :
        #   '#' = wall,  '$' = box, '.' = goal, '*' = box on goal, '@' = mover, '+' = mover on goal, '-' = floor, ' ' = floor
        nbrows = len(xsbMatrix)
        nbcolumns = max((len(line) for line in xsbMatrix), default=0)
        self.height = nbrows * 64
        self.width = nbcolumns * 64

        self.wharehouse = WharehousePlan()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="gray")
        self.canvas.pack()
        self.mover = None

        # Installer les cases statiques avant les éléments mobiles.
        for y in range(nbrows):
            row = []
            for x in range(nbcolumns):
                elem = xsbMatrix[y][x] if x < len(xsbMatrix[y]) else ' '
                position = Position(x, y)
                if elem == '#':
                    cell = Wall(self.canvas, position)
                elif elem in ('.', '*', '+'):
                    cell = Goal(self.canvas, position)
                else:
                    cell = Floor()
                row.append(cell)
            self.wharehouse.appendRow(row)

        for y, line in enumerate(xsbMatrix):
            for x, elem in enumerate(line):
                position = Position(x, y)
                if elem in ('$', '*'):
                    Box(self.canvas, self.wharehouse, position, elem == '*')
                elif elem in ('@', '+'):
                    if self.mover is not None:
                        raise ValueError("Le niveau contient plusieurs déménageurs.")
                    self.mover = Mover(
                        self.canvas, self.wharehouse, position, elem == '+'
                    )

        if self.mover is None:
            raise ValueError("Le niveau ne contient pas de déménageur.")

        self.canvas.tag_raise("movable","static")
         
    def keypressed(self, event):
        directions = {
            'Up': Direction.Up,
            'Down': Direction.Down,
            'Left': Direction.Left,
            'Right': Direction.Right,
        }
        direction = directions.get(event.keysym)
        if direction is not None:
            self.mover.push(direction)


class Sokoban(object):
    '''
    Main Level class
    '''

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title("Sokoban")
        print('Sokoban: ' + str(len(SokobanXSBLevels)) + ' levels')
        self.level = Level(self.root, SokobanXSBLevels[5])
        #self.level = Level(self.root, [
            #['-','-','$','+','$','.','-','.','.','.','.','-','-','.','.','-','-','.','-'] ])
        #self.level = Level(self.root, [ ['@'] ])
 
    def play(self):
        self.root.mainloop()


Sokoban().play()

