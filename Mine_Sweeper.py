import tkinter
from tkinter import messagebox
import random
import time
import math


class Minesweeper():
    def __init__(self, root, retry_diffic):
        self.master = root
        #Sets up frame when game is run
        self.frame = tkinter.Frame(self.master)
        self.info_frame = tkinter.Frame(self.master)  #Shows the number of mines and the timer
        self.init_frame = tkinter.Frame(self.master)  
        self.init_frame.pack(padx=10, pady=10)

        # initialization
        self.start_time = time.time()
        self.running_time = tkinter.IntVar(value=0)

        self.max=0
        self.flag = 0
        self.mines = tkinter.IntVar(value=0)  #Number of mines 
        self.clicked_num = tkinter.IntVar(value=0)
        self.Diffic_Var = tkinter.StringVar(value='0')
        self.probability = 0

        # import images from graphics folder
        self.emoji = tkinter.PhotoImage(file="graphics/thinking.png")
        self.dedemoji = tkinter.PhotoImage(file="graphics/thinking_ded.png")
        self.watch = tkinter.PhotoImage(file="graphics/timer.png")
        self.tile_plain = tkinter.PhotoImage(file="graphics/tile_plain.gif")
        self.tile_clicked = tkinter.PhotoImage(file="graphics/tile_clicked.gif")
        self.tile_mine = tkinter.PhotoImage(file="graphics/tile_mine.gif")
        self.tile_flag = tkinter.PhotoImage(file="graphics/tile_flag.gif")
        self.tile_wrong = tkinter.PhotoImage(file="graphics/tile_wrong.gif")
        self.tile_no = []
        
        for x in range(1, 9):
            self.tile_no.append(tkinter.PhotoImage(file="graphics/tile_" + str(x) + ".gif"))

        #Starts the game
        self.set_menubar()
        if retry_diffic == '0':
            self.start_game()
        self.grid_widgets()

    def start_game(self):
        self.Diffic_Var.set(0)

        self.help = tkinter.Button(self.init_frame, text="Help", command=self.instructions)
        self.help.grid(row=2, column=0, padx=20, pady=5)

        self.Start_btn = tkinter.Button(self.init_frame, padx=5, pady=5, text="Start", command=self.clear_init_frame)
        self.Start_btn.grid(row=2, column=1, padx=10, rowspan=1)

    def set_menubar(self):
        menubar = tkinter.Menu(self.master)
        self.master['menu'] = menubar

        game_menu = tkinter.Menu(menubar, tearoff=0, bd=5)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Exit", command=self.master.destroy)

    def create_buttons(self):
        # create buttons
        self.buttons = dict({})
        
        while True:
            x_coord = 0
            y_coord = 1
            for x in range(0, self.max ** 2):
                mine = 0
                if random.uniform(0.0, 1.0) < self.probability:  
                    mine = 1
                    self.mines.set(self.mines.get() + 1)
                # 0 = Button widget
                # 1 = if a mine y/n (1/0)
                # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
                # 3 = button id
                # 4 = [x, y] coordinates in the grid
                self.buttons[x] = [tkinter.Button(self.frame, image=self.tile_plain), mine, 0, x, [x_coord, y_coord]]
                self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
                self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))

                # calculate coords:
                x_coord += 1
                if x_coord == self.max:
                    x_coord = 0
                    y_coord += 1

            if self.mines.get() == 0:
                continue
            else:
                break

        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key][0].grid(row=self.buttons[key][4][1], column=self.buttons[key][4][0])

    
    def timer(self):
        temp = math.floor(time.time()-self.start_time)
        self.running_time.set(temp)
        self.info_frame.after(500, self.timer)

    #prints instructions message box when help button is clicked
    def instructions(self):
        instructions = tkinter.messagebox.askokcancel("Instructions","Wanna learn more about minesweeper? Well you've come to the right place!\nThe goal of minesweeper is to click as many boxes without detonating any bombs.\nIf you do this you win! Otherwise if you press a bomb it explodes and you die :( \nHave fun!")

    #Destroys opening panel and creates the game, sets probability of mines
    def clear_init_frame(self):
        self.init_frame.destroy()

        self.probability = 0.20
        self.max = 10

        self.frame.pack(padx=20, pady=10)
        self.info_frame.pack()
        self.create_buttons()
        
        self.timer()

    def lclicked(self, x):
        #Checks to see if mine was selected or not
        if self.buttons[x][1] == 1:
            self.show_all_mines_lose()
            self.gameover()
        else:
            self.clicked_num.set(self.clicked_num.get()+1)
            self.buttons[x][2] = 1

            self.check_nearby(x)
            self.buttons[x][0].unbind('<Button-1>')
            if self.mines.get()+self.clicked_num.get()+self.flag == self.max**2:
                self.show_all_mines_win()
                self.victory()

    def rclicked(self, x):
        #Changes graphics of unflagged tile to a flag
        if self.buttons[x][2] == 0:
            self.buttons[x][0].config(image=self.tile_flag)
            self.buttons[x][2] = 2
            self.buttons[x][0].unbind('<Button-1>')
            self.mines.set(self.mines.get() - 1)
            self.flag += 1
        #Changes graphic of flagged tile to unflagged
        elif self.buttons[x][2] == 2:
            self.buttons[x][2] = 0
            self.buttons[x][0].config(image=self.tile_plain)
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.mines.set(self.mines.get() + 1)
            self.flag -= 1

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(x)

    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(x)

    def grid_widgets(self):
        #show icon at the top
        self.icon = tkinter.Button(self.frame, image=self.emoji, borderwidth=0)
        self.icon.grid(row=0, column=0, columnspan = 30)
        
        # lay information in grid
        self.lb_mine = tkinter.Label(self.info_frame, text="Mines :")
        self.lb_mine.grid(row=self.max + 2, column=0)
        self.lb_mine_num = tkinter.Label(self.info_frame, textvariable=self.mines)
        self.lb_mine_num.grid(row=self.max + 2, column=1)

        self.image_time = tkinter.Button(self.info_frame, image=self.watch, borderwidth=0)
        self.image_time.grid(row=self.max + 3, column=0)
        
        self.lb_time = tkinter.Label(self.info_frame, textvariable=self.running_time)
        self.lb_time.grid(row=self.max + 3, column=1)
        self.restart = tkinter.Button(self.info_frame, text="Restart", command=self.retry_game, padx=1)
        self.restart.grid(row=self.max + 3, column=3, padx=10, columnspan=3, sticky='we')
        self.empty_lb = tkinter.Label(self.info_frame, text="   ")
        self.empty_lb.grid(row=self.max + 2, column=2)

    def make_one_mine(self):
        while True:
            temp_x = random.randrange(0, self.max)
            if self.buttons[temp_x][1] == 1: # if mine
                continue
            elif self.buttons[temp_x][1] == 0: #if not mine
                self.buttons[temp_x][1] = 1 # make this mine
                break

    def show_all_mines_lose(self):
        # show all mines
        for x in self.buttons:
            if self.buttons[x][1] == 1:  # if mine
                self.buttons[x][0].config(image=self.tile_wrong)

    def show_all_mines_win(self):
        # show all mines
        for x in self.buttons:
            if self.buttons[x][1] == 1:  # if mine
                self.buttons[x][0].config(image=self.tile_mine)

    def check_nearby(self, x):
        idx = x
        count = 0
        for i in [0, 1, 1]:
            idx += i*self.max
            for j in range(-1, 2):
                key = idx - self.max + j

                if key < 0 or key >= self.max**2:  # none exist space
                    continue
                elif idx % self.max == self.max - 1 and key % self.max == 0 :  # physically not close space
                    continue
                elif idx % self.max == 0 and key % self.max == self.max - 1:  # physically not close space
                    continue
                elif self.buttons[key][1] == 1:  # if mine
                    count += 1

        self.change_to_tile_no(x, count)

    def change_to_tile_no(self, x, count):
        if count != 0:
            self.buttons[x][0].config(image=self.tile_no[count-1])

        elif count == 0:
            self.buttons[x][0].config(image=self.tile_clicked)
            self.show_nearby_none_mine(x)


    def show_nearby_none_mine(self, x):
        idx = x
        for i in [0, 1, 1]:
            idx += i * self.max
            for j in range(-1, 2):
                key = idx - self.max + j

                if key < 0 or key >= self.max ** 2:  # none exist space
                    continue
                elif idx % self.max == self.max - 1 and key % self.max == 0:  # physically not close space
                    continue
                elif idx % self.max == 0 and key % self.max == self.max - 1:  # physically not close space
                    continue
                elif self.buttons[key][1] == 0 and self.buttons[key][2] != 1:  # if not mine and unclicked
                    self.lclicked(key)

    def gameover(self):
        #changes icon to a dead one
        self.iconded = tkinter.Button(self.frame, image=self.dedemoji, borderwidth=0)
        self.iconded.grid(row=0, column=0, columnspan = 30)

        #asks if user would like to replay
        ask_retry = tkinter.messagebox.askokcancel("You Lose.", "Try again?")
        if ask_retry == True:
            self.retry_game()
        else:
            self.master.destroy()

    def victory(self):
        ask_retry = tkinter.messagebox.askokcancel("You Win.", "Congratulations!\nTry again?")
        if ask_retry == True:
            self.new_game()
        else:
            self.master.destroy()

    def retry_game(self):
        self.master.destroy()
        game(self.Diffic_Var.get())
    def new_game(self):
        self.master.destroy()
        game()

def game(retry_diffic='0'):
    root = tkinter.Tk()
    root.title("Minesweeper")
    Minesweeper(root, retry_diffic)
    root.mainloop()

