"""
@author: plantec
"""
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox


class Example:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        # A COMPLETER
        self.player_image = tk.PhotoImage(file='player.png')
        self.player_id = self.canvas.create_image(0, 0,image=self.player_image, anchor=tk.NW)

    def keypress(self, event):
        # A MODIFIER
        if event.keysym == 'Left':
            self.canvas.move(self.player_id, -300, 0)

        elif event.keysym == 'Right':
            self.canvas.move(self.player_id, 10, 0)
        
        elif event.keysym == 'Up':
            self.canvas.move(self.player_id, 0, -10)

        elif event.keysym == 'Down':
            self.canvas.move(self.player_id, 0, 10)


    def start(self):
        #self.install()
        # Quand n'importe quelle touche du clavier est appuyée, exécuter keypress
        self.root.bind("<Key>", self.keypress)
        self.root.mainloop()

ex = Example()
ex.start()
