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
        self.rect_id = None
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

    def install(self):
        w, x, y = 50, 0, 0
        self.rect_id = 0

    def start(self):
        self.install()
        self.root.mainloop()

# Creation d'une instance de Example et stockage de sa reference dans ex
ex = Example()
# Envoie le message start à l'objet ex
ex.start()
