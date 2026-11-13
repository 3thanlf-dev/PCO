"""
@author: plantec
"""
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import tkinter as tk
    import tkMessageBox

class Example:
    def __init__(self):
        self.root = tk.Tk()
        self.player_id = None
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.player_image = tk.PhotoImage(file='player.png')
        self.player_id = self.canvas.create_image(0, 0,image=self.player_image, anchor=tk.NW)

    def start(self):
        self.root.mainloop()

# Creation d'une instance de Example et stockage de sa reference dans ex
ex = Example()
# Envoie le message start à l'objet ex
ex.start()
