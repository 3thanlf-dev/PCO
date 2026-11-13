"""
@author: plantec
"""
try:  # import as appropriate for 2.x vs. 3.x
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
except:
    import Tkinter as tk
    import tkMessageBox

class Mobile:
    def __init__(self, canvas, y, speed):
        self.canvas = canvas
        self.canvas_width = int(self.canvas.cget("width"))
        self.player_image = tk.PhotoImage(file='player.png')
        self.player_id = self.canvas.create_image(0, y,image=self.player_image, anchor=tk.NW)

        self.speed = speed

    def moveOrComeBack(self):
        # calcul du deplacement dans self.gap
        self.gap = self.speed
        x1, y1 = self.canvas.coords(self.player_id)
        if (x1 + self.player_image.width()) >= self.canvas_width:
            self.gap = -x1
        # deplacement du player
        self.canvas.move(self.player_id, self.gap, 0)

class MobileFleet:
    def __init__(self, canvas):
        self.fleet = []
        self.fleet.append(Mobile(canvas, 0, 10))
        self.fleet.append(Mobile(canvas, 100, 20))
        self.fleet.append(Mobile(canvas, 200, 30))
        self.fleet.append(Mobile(canvas, 300, 40))


    def moveOrComeBack(self):
        for m in self.fleet:
            m.moveOrComeBack()

class Example:
    def __init__(self):
        self.root = tk.Tk()
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.fleet = MobileFleet(self.canvas)
        self.canvas.pack()

    def start_animation(self):
        # execute self.animation dans 10ms
        self.canvas.after(10, self.animation)

    def animation(self):
        self.fleet.moveOrComeBack()
        # execute a nouveau self.animation dans 300ms
        self.canvas.after(300, self.animation)

    def start(self):
        self.start_animation()
        self.root.mainloop()


ex = Example()
ex.start()
