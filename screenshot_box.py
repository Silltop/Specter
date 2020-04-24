from tkinter import *
from tkinter import ttk
import time
from ctypes import windll
from pyautogui import size,screenshot

def name_file():
    '''Create File name'''
    now = time.time()
    name = time.strftime("%d%H%M%S", time.gmtime(now))
    return name

def take_shot(PATH):
    '''Create Fullscreen screenshot'''
    print('saving to -> {}'.format(PATH))

    img = screenshot()
    img.save(PATH + '\\' + name_file() + '.png')

def res_check():
    '''Resize screen shot for high resolution (bug tkinter resolution)'''
    w, h = size()
    if h == 1080 and w == 1920:
        return True
    else:
        return False

class DrawingBox(Frame):
    def __init__(self, master):
        Frame.__init__(self, master=master)
        self.pack()
        self.height, self.width = master.winfo_screenheight(), master.winfo_screenwidth()
        print(self.height,self.width)
        self.canvas = Canvas(master, width=self.width, height=self.height)

        self.l1 = ttk.Label(master, text='Draw box to make a Screenshot\n\tClick to start')
        self.l1.config(font=("Arial", 44))
        lh = self.height
        self.l1.pack(pady=lh / 3)

        self.master.bind("<Button-1>", self.on_button_press)
        self.master.bind("<B1-Motion>", self.on_move_press)
        self.master.bind("<ButtonRelease-1>", self.on_button_release)
        # self.master.focus_set()

        self.selection = None
        self.start_x = None
        self.start_y = None
        self.postions = ()

    def on_button_press(self, event):
        self.l1.pack_forget()
        self.canvas.pack()
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        self.selection = self.canvas.create_rectangle(event.x, event.y, event.x + 1, event.y + 1,width=4)

    def on_move_press(self, event):
        # print('mouse moving... ', event.x, event.y)
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.selection, self.start_x, self.start_y, self.curX, self.curY)

    def on_button_release(self, event):
        print(self.start_x, self.start_y, self.curX, self.curY)

        if self.start_x > event.x:
            x1, x2 = event.x, self.start_x-event.x
        else:
            x1, x2 = self.start_x, event.x-self.start_x
        if self.start_y > event.y:
            y1, y2 = event.y, self.start_y-event.y
        else:
            y1, y2 = self.start_y, event.y-self.start_y

        print(x1,y1,x2,y2)

        self.postions = (x1,y1,x2,y2)

        self.canvas.pack_forget()
        self.canvas.delete('all')
        self.master.destroy()

    def getter(self):
        return self.postions

def draw_box(PATH):
    '''main fuction of drawed box'''

    box = Tk()
    box.focus_get()
    box.focus_displayof()

    width, height = box.winfo_screenwidth(), box.winfo_screenheight()
    print(width,height)
    # box.geometry(geometry)
    box.geometry("%dx%d+0+0" % (width, height))
    box.attributes("-fullscreen", True)
    box.attributes("-alpha", 0.2)

    box.overrideredirect(1)
    DB = DrawingBox(box)
    box.mainloop()

    postions = DB.getter()
    del DB

    user32 = windll.user32
    user32.SetProcessDPIAware()
    print(postions)
    img = screenshot(region=(postions))
    img.save(PATH + '\\' + name_file() + '.png')

    return 1

# draw_box('C:\\Users\\Patryk\\Desktop')
