from tkinter import *
import time
from tkinter.messagebox import *
import random

class Game:

    def __init__(self, master):

        self.flags = 60
        self.createButtons(master)

        self.bottomFrame = Frame(root)
        self.bottomFrame.grid(row=11, columnspan=10)

        self.flagRemainning = Label(self.bottomFrame, text='Flag Remaining : '+str(self.flags))
        self.flagRemainning.grid(row=12)

        self.quitBtn = Button(self.bottomFrame, text='Quit', command=self.quit)
        self.quitBtn.grid(row=13, columnspan=2)


def main():
    global root
    root = Tk()
    root.title('MiNeSwEePeR')
    game = Game(root)
    root.mainloop()
