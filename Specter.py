from tkinter import *
from tkinter import ttk, filedialog, messagebox
from keyboard import wait, read_key
from threading import Thread
from cfg_module import cfg_load, cfg_save
import screenshot_box
from time import sleep
from PIL import Image, ImageTk
from systray import SysTrayIcon
import sys
import os


def ask_quit(event=None):
    Q = messagebox.askyesno(title='Quit', message='Are you sure?', icon='warning')
    if Q == True:
        ti.kill_icon_tray()
        root.destroy()
        root.quit()
        sys.exit(0)

def reload():
    Q = messagebox.askyesno(title='Reload Keys', message='Program will now reboot to apply changes', icon='warning')
    if Q == True:
        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


def minimize(event=None):
    root.withdraw()


def restore(event=None):
    root.deiconify()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ico_open(img):
    path = resource_path(img)
    image = Image.open(path)
    image = image.resize((25, 25), Image.ANTIALIAS)
    button_photo = ImageTk.PhotoImage(image)
    return button_photo


def listener():
    while True:
        settings = cfg_load()
        print(settings[4])
        if settings[1][1] == '':
            keys = settings[1][0]
        elif settings[1][2] == '':
            keys = settings[1][0] + '+' + settings[1][1]
        else:
            keys = settings[1][0] + '+' + settings[1][1] + '+' + settings[1][2]
        wait(keys)
        settings = cfg_load()
        root.withdraw()
        if settings[3] == 2:
            sleep(1)
            screenshot_box.take_shot(settings[4])
        elif settings[3] == 1:
            sleep(1)
            screenshot_box.take_shot(settings[4])
            root.deiconify()


def listener_BOX():
    while True:
        settings = cfg_load()
        if settings[2][1] == '':
            keys = settings[2][0]
        elif settings[2][2] == '':
            keys = settings[2][0] + '+' + settings[2][1]
        else:
            keys = settings[2][0] + '+' + settings[2][1] + '+' + settings[2][2]
        wait(keys)
        settings = cfg_load()
        root.withdraw()
        if screenshot_box.draw_box(settings[4]) == 1:
            if settings[3] == 2:
                sleep(1)
            elif settings[3] == 1:
                sleep(1)
                root.deiconify()

class TrayIco:
    def __init__(self):
        self.menu_options = (("Open window", None, restore),)
        self.tray_instance = SysTrayIcon(resource_path("ghost.ico"), "Ready!", self.menu_options, on_quit=ask_quit)

    def init_icon_tray(self):
        self.tray_instance.start()

    def kill_icon_tray(self):
        self.tray_instance.shutdown()


class Switcher:
    def __init__(self, master):

        self.master = master

        ### STYLES ###
        style = ttk.Style(master)
        style.configure('TButton', foreground="black", background="#FFFFFF", border=10, relief="flat")
        style.configure('bar.TButton', foreground="white", background="gray", border=10, relief="flat")
        style.configure('.', foreground="white", background="#40414d", border=0)


        ### MENU BAR ###

        self.menu_bar = ttk.Frame(master, height=25)
        self.menu_bar.pack(side=RIGHT, fill=Y, anchor=E, expand=False)

        self.hide_ico = ico_open('hide.ico')
        self.hide_B = Button(self.menu_bar, image=self.hide_ico, command=minimize, bg='#40414d', relief="flat")
        self.hide_B.pack(anchor=E)

        self.set_ico = ico_open('settings.ico')
        self.config_B = Button(self.menu_bar, image=self.set_ico, command=self.s_options, bg='#40414d', relief="flat")


        self.ret_ico = ico_open('return.ico')
        self.back_B = Button(self.menu_bar, image=self.ret_ico, command=self.back, bg='#40414d', relief="flat")

        self.info_ico = ico_open('info.ico')
        self.info_B = Button(self.menu_bar, image=self.info_ico, command = self.info_trigger, bg='#40414d', relief="flat")
        self.info_B.pack(anchor=E)
        self.config_B.pack(anchor=E)

        ### MAIN MENU ###

        self.main_menu = ttk.Frame(master, padding=(3, 3, 12, 12))
        self.main_menu.pack(fill=BOTH, expand=YES)


        self.M_Lab_A = ttk.Label(self.main_menu,
                                 text='Press key [  ' + settings[1][0] + ' ' + settings[1][1] + ' ' +
                                      settings[1][2] + '] to make fullscreen screenshot',padding=(6, 6, 16, 6))

        self.M_Lab_B = ttk.Label(self.main_menu,
                                 text='Press key [  ' + settings[2][0] + ' ' + settings[2][1] + ' ' +
                                      settings[2][2] + '] to draw screenshot box',padding=(6, 6, 16, 6))

        self.M_Lab_A.pack(anchor=CENTER)
        self.M_Lab_B.pack(anchor = CENTER)


        ### OPTIONS ###

        self.options = ttk.Frame(master, padding=(20, 3, 12, 12))

        self.O_Lab_F = ttk.Label(text='Save settings?')
        self.save = ttk.LabelFrame(self.options, labelwidget=self.O_Lab_F, padding=(6, 6, 6, 6))
        self.Lab_info = ttk.Label(self.save, text='To apply keys settings program have to reboot')
        self.save_ico = ico_open('save.ico')
        self.save_button = Button(self.save, image=self.save_ico, command=reload, bg='#40414d', relief="flat")

        self.O_Lab_A = ttk.Label(text='Set screenshot hotkeys')
        self.O_Lab_B = ttk.Label(text='Set box drawning hotkeys')
        self.O_Lab_C = ttk.Label(text='Set Screenshot location:')
        self.O_Lab_D = ttk.Label(text='Show this window after screenshot?')
        self.O_Lab_E = ttk.Label(text='Start hidden?')

        self.col1 = ttk.LabelFrame(self.options, labelwidget=self.O_Lab_A, padding=(6, 6, 6, 6))



        self.col2 = ttk.LabelFrame(self.options, labelwidget=self.O_Lab_B, padding=(6, 6, 6, 6))
        self.col3 = ttk.LabelFrame(self.options, labelwidget=self.O_Lab_C, padding=(6, 6, 6, 6))
        self.col4 = ttk.LabelFrame(self.options, labelwidget=self.O_Lab_D, padding=(8, 8, 8, 8))
        self.col5 = ttk.LabelFrame(self.options, labelwidget=self.O_Lab_E, padding=(8, 8, 8, 8))

        self.patch_frame = ttk.Frame(self.col3, padding=(1, 1, 6, 6))
        self.O_Lab_C1 = ttk.Label(self.patch_frame, text='Current is:')
        self.O_Lab_C2 = ttk.Label(self.col3, text='' + settings[4])

        self.keysetterA = ttk.Button(self.col1, text=settings[1][0], command=lambda: self.keysetter(0))
        self.keysetterB = ttk.Button(self.col1, text=settings[1][1], command=lambda: self.keysetter(1))
        self.keysetterC = ttk.Button(self.col1, text=settings[1][2], command=lambda: self.keysetter(2))
        self.BOXkeysetterA = ttk.Button(self.col2, text=settings[2][0], command=lambda: self.keysetter(3))
        self.BOXkeysetterB = ttk.Button(self.col2, text=settings[2][1], command=lambda: self.keysetter(4))
        self.BOXkeysetterC = ttk.Button(self.col2, text=settings[2][2], command=lambda: self.keysetter(5))

        self.fol_ico = ico_open('F_pic.ico')
        self.asker = Button(self.patch_frame, image=self.fol_ico, command=self.path_setter, bg='#40414d', relief="flat")

        self.M = IntVar()
        self.M.set(int(settings[3]))

        Radiobutton(self.col4, text='Yes', indicatoron=0, variable=self.M, value=1,
                    command=lambda: self.modesetter(1, 3)).pack(side=LEFT, fill=X, expand=YES)
        Radiobutton(self.col4, text='No', indicatoron=0, variable=self.M, value=2,
                    command=lambda: self.modesetter(2, 3)).pack(side=LEFT, fill=X, expand=YES)

        self.MS = IntVar()
        self.MS.set(int(settings[5]))
        Radiobutton(self.col5, text='Yes', indicatoron=0, variable=self.MS, value=1,
                    command=lambda: self.modesetter(1, 5)).pack(side=LEFT, fill=X, expand=YES)
        Radiobutton(self.col5, text='No', indicatoron=0, variable=self.MS, value=2,
                    command=lambda: self.modesetter(2, 5)).pack(side=LEFT, fill=X, expand=YES)

        self.keysetterA.pack(side=LEFT, fill=X, expand=YES)
        self.keysetterB.pack(side=LEFT, fill=X, expand=YES)
        self.keysetterC.pack(side=LEFT, fill=X, expand=YES)

        self.BOXkeysetterA.pack(side=LEFT, fill=X, expand=YES)
        self.BOXkeysetterB.pack(side=LEFT, fill=X, expand=YES)
        self.BOXkeysetterC.pack(side=LEFT, fill=X, expand=YES)

        self.col1.pack(anchor=N, fill=X, expand=YES)
        self.col2.pack(anchor=N, fill=X, expand=YES)

        self.save.pack(anchor=N, fill=X, expand=YES)
        self.Lab_info.pack(side=LEFT)
        self.save_button.pack(side=LEFT)

        self.col3.pack(anchor=N, fill=X, expand=YES)
        self.patch_frame.pack(anchor = N,fill = X)
        self.O_Lab_C1.pack(side = LEFT)
        self.asker.pack(side = RIGHT)
        self.O_Lab_C2.pack(side = LEFT)

        self.col4.pack(anchor=S, fill=X, expand=YES)
        self.col5.pack(anchor=S, fill=X, expand=YES)

        ### TUTORIAL ###

        self.info_frame_A = ttk.Frame(master, padding=(3, 3, 12, 12))
        self.inf_lab_A = ttk.Label(self.info_frame_A, text='Here You can hide this window ->',padding=(0, 0, 0, 12))
        self.inf_lab_B = ttk.Label(self.info_frame_A, text='\nHere You can change settings ->')
        if settings[6] :
            self.blink(self.info_B,3)
            settings[6] = False
            cfg_save(settings)
        self.inf_lab_C = ttk.Label(self.info_frame_A, text='\n\nWhen hidden, app will work in background\n you can access menu from tray bar below\n\n')



        ### GEOMETRY SETTINGS ###
        self.element_height = self.M_Lab_A.winfo_reqheight()
        self.window_width = str(self.M_Lab_A.winfo_reqwidth() + 100)
        self.menu_height = str(self.M_Lab_A.winfo_reqheight() * 2 + 40)
        master.geometry(self.window_width + 'x' + str(self.menu_height))
        self.option_height = str(7 * (self.element_height + self.keysetterA.winfo_reqheight() + 10))
        self.info_height = str(4 * (self.element_height + self.keysetterA.winfo_reqheight() + 10))

        if settings[5] == 1:
            master.withdraw()


    def info_trigger(self):
        self.main_menu.pack_forget()
        self.options.pack_forget()
        self.back_B.pack_forget()
        self.config_B.pack(anchor=E)
        self.master.geometry(self.window_width + 'x' + self.info_height)
        self.info_frame_A.pack(fill = BOTH)
        self.inf_lab_A.pack(anchor = NE)
        self.inf_lab_B.pack(anchor=SE, fill = Y, expand = YES)
        self.inf_lab_C.pack(anchor = CENTER, fill = Y, expand = YES)
        self.blink(self.hide_B,4)
        self.blink(self.config_B,4)

    def blink(self,button,xtimes):
        if not xtimes==0:
            button.after(500, lambda: button.config(bg= 'green'))
            button.after(1000, lambda: button.config(bg='#40414d'))
            button.after(1000, lambda: self.blink(button,xtimes-1))

    def modesetter(self, mode, field):
        settings[field] = mode
        cfg_save(settings)

    def s_options(self):

        self.master.geometry(self.window_width + 'x' + self.option_height)
        self.main_menu.pack_forget()
        self.info_frame_A.pack_forget()
        self.config_B.pack_forget()
        self.back_B.pack(anchor=E)
        self.options.pack()

    def back(self):
        self.master.geometry(self.window_width + 'x' + str(self.menu_height))
        self.options.pack_forget()
        self.back_B.pack_forget()
        self.config_B.pack(anchor=E)
        self.main_menu.pack(fill=BOTH, expand=YES)

    def keysetter(self, number):
        if number >= 3:
            V = 2
            number -= 3
        else:
            V = 1

        k = read_key()
        if k == 'esc':
            settings[V][number] = ''
        elif k == str(settings[V][0]) or k == str(settings[V][1]) or k == str(settings[V][2]):
            settings[V][number] = ''
        else:
            settings[V][number] = k

        if settings[V][0] == '':
            settings[V][1] = ''
            settings[V][2] = ''
            messagebox.showerror('Error', 'Cannot be empty!')
            if V == 1:
                settings[V][0] = 'print screen'
            else:
                settings[V][0] = 'pause'

        elif settings[V][1] == '':
            settings[V][2] = ''

        elif settings[1][0] == settings[2][0] and settings[1][1] == settings[2][1] and settings[1][2] == settings[2][2]:
            settings[1] = ['print screen', '', '']
            settings[2] = ['pause', '', '']

        self.button_refresh()
        cfg_save(settings)

    def size_getter(self):
        return self.window_width,self.h,self.opth

    def path_setter(self):
        path_to_save = filedialog.askdirectory()
        print(path_to_save)
        settings[4] = path_to_save
        cfg_save(settings)
        self.button_refresh()

    def button_refresh(self):

        self.M_Lab_A.config(text='Press key [  ' + settings[1][0] + ' ' + settings[1][1] + ' ' + settings[1][
            2] + '] to make screenshot')
        self.M_Lab_B.config(text='Press key [  ' + settings[2][0] + ' ' + settings[2][1] + ' ' + settings[2][
            2] + '] to draw screenshot box')
        self.keysetterA.config(text=settings[1][0])
        self.keysetterB.config(text=settings[1][1])
        self.keysetterC.config(text=settings[1][2])
        self.BOXkeysetterA.config(text=settings[2][0])
        self.BOXkeysetterB.config(text=settings[2][1])
        self.BOXkeysetterC.config(text=settings[2][2])
        self.O_Lab_C1.config(text='Current is:\n' + settings[4])


settings = cfg_load()

t1 = Thread(target=listener, args=())
t2 = Thread(target=listener_BOX, args=())
t1.daemon = True
t1.start()
t2.daemon = True
t2.start()

ti = TrayIco()
ti.init_icon_tray()

root = Tk()
root.configure(bg='#40414d')
root.title(settings[0])
root.iconbitmap(resource_path("ghost.ico"))
root.resizable(width=False, height=False)

if settings[5] == 1:
    root.deiconify()

Sw = Switcher(root)

root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()
del Sw
