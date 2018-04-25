from tkinter import *
import time
from tkinter.messagebox import *
import random
from tkinter import Tk, Label, Button

class OpeningScreen:
    def __init__(self, master):
        self.master = master
        master.title("Opening")

        self.label = Label(master, text="Welcome to Minesweeper!")
        self.label.pack()

        self.greet_button = Button(master, text="Help", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=root.destroy)
        self.close_button.pack()

        def greet(self):
        print("Wanna Learn more about minesweeper, well you came to the right place")
        print ("")
        print ("The goal of minesweeper is to click as many boxes without detonating any bombs")
        print ("")
        print ("If you do this you win! Otherwise if you press a bomb it explodes and you lose")
        print ("")
        print ("Now have fun!")
        print ("")
        print (" Start by pressing close on the opening Screen")
root = Tk()
my_gui = OpeningScreen(root)
root.mainloop()

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

        self.total = 0
        self.count = 0
        for i in self.buttons:
            if self.buttons[i][4][0] == 1:
                self.total += 1
        
    def createButtons(self, parent):
        self.buttons = {}
        row = 0
        col = 0
        for x in range(0, 200):
            status = random.choice(['safe', 'danger'])
            self.buttons[x] = [
            Button(parent, bg='#8a8a8a'),
            status,
            row,
            col,
            [0 if status == 'danger' else 1]
            ]

            self.buttons[x][0].bind('<Button-1>', self.leftClick_w(x))
            self.buttons[x][0].bind('<Button-3>', self.rightClick_w(x))
            col += 1
            if col == 20:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row= self.buttons[k][2], column= self.buttons[k][3])

     def leftClick_w(self, x):
        return lambda Button: self.leftClick(x)

    def rightClick_w(self, x):
        return lambda Button: self.rightClick(x)

    def leftClick(self, btn):
        check = self.buttons[btn][1]
        if check == 'safe':

            self.buttons[btn][0].config(bg='green')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.count += 1
            self.nearbyMines(btn)
            self.showNearby(btn)
            win = self.checkWin()
            if win:
                self.victory()

        if check == 'danger':
            self.buttons[btn][0].config(bg='red')
            self.buttons[btn][0].config(state='disabled', relief=SUNKEN)
            self.lost()

    def quit(self):
        global root
        root.destroy()

def main():
    n = input ("Welcome to Minesweeper, press any key to continue: ") 
    global root
    root = Tk()
    root.title('MiNeSwEePeR')
    game = Game(root)
    root.mainloop()

if __name__ == '__main__':
    main()
