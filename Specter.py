from tkinter import *
from tooltip_module import *
from defines import *
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
    ti.tip_info('I will be here waiting for order! :)')


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
        ti.tip_info('Taken!', (work_area[2] - 50, 0))
        if settings[3] == 2:
            # sleep(1)
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
        if screenshot_box.draw_box(settings[4], 1) == 1:
            if settings[3] == 2:
                pass
                # sleep(1)
            elif settings[3] == 1:
                sleep(1)
                root.deiconify()
            ti.tip_info('Taken!', (work_area[2] - 50, 0))

def Const_box():
    while True:
        settings = cfg_load()
        if settings[8][1] == '':
            keys = settings[8][0]
        elif settings[8][2] == '':
            keys = settings[8][0] + '+' + settings[8][1]
        else:
            keys = settings[8][0] + '+' + settings[8][1] + '+' + settings[8][2]
        wait(keys)
        settings = cfg_load()
        root.withdraw()
        ti.tip_info('Taken!', (work_area[2] - 50, 0))
        if not all(settings[7]):
            messagebox.showwarning(title='Invaild area', message='Select area first',
                                   icon='warning')
            root.deiconify()
        else:
            if screenshot_box.take_shot(settings[4],settings[7]):
                Sw.button_refresh()
                if settings[3] == 2:
                    pass
                    # sleep(1)
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

    def tip_info(self, text = 'Example', coords = (0,0)):
        self.text = text
        self.tip = Toplevel(root)
        if coords == (0,0):
            x1, y1 = work_area[2] - 310, work_area[3] - 20
            coords = (x1,y1)

        self.tip.wm_overrideredirect(1)
        self.tip.wm_geometry("+%d+%d" % coords)

        label = Label(self.tip, text=self.text, justify=LEFT,
                      foreground="white", background=theme_color, relief=SOLID, borderwidth=2,
                      font=("tahoma", "9", "normal"))
        label.pack(ipadx=1)
        self.tip.after(1200, self.tip_kill)

    def tip_kill(self):
        self.tip.after(1400, lambda: self.tip.wm_attributes('-alpha', 0.6))
        self.tip.after(1600, lambda: self.tip.wm_attributes('-alpha', 0.5))
        self.tip.after(1800, lambda: self.tip.wm_attributes('-alpha', 0.3))
        self.tip.after(2000, lambda: self.tip.wm_attributes('-alpha', 0.2))
        self.tip.after(2200, lambda: self.tip.wm_attributes('-alpha', 0.1))
        self.tip.after(2400, self.tip.destroy)


class Switcher:
    def __init__(self, master):

        self.master = master

        ### STYLES ###
        style = ttk.Style(self.master)
        style.configure('TButton', foreground="black", background="#FFFFFF", border=10, relief="flat")
        style.configure('bar.TButton', foreground="white", background="gray", border=10, relief="flat")
        style.configure('.', foreground="white", background=theme_color, border=0)


        ### MENU BAR ###

        self.menu_bar = ttk.Frame(self.master, height=25)
        self.menu_bar.pack(side=RIGHT, fill=Y, anchor=E, expand=False)

        self.hide_ico = ico_open('hide.ico')
        self.hide_B = Button(self.menu_bar, image=self.hide_ico, command=minimize, bg=theme_color, relief="flat")
        self.hide_B.pack(anchor=E)

        self.set_ico = ico_open('settings.ico')
        self.config_B = Button(self.menu_bar, image=self.set_ico, command=self.s_options, bg=theme_color, relief="flat")


        self.ret_ico = ico_open('return.ico')
        self.back_B = Button(self.menu_bar, image=self.ret_ico, command=self.back, bg=theme_color, relief="flat")

        self.info_ico = ico_open('info.ico')
        self.info_B = Button(self.menu_bar, image=self.info_ico,state=DISABLED, command = self.info_trigger, bg=theme_color, relief="flat")
        self.info_B.pack(anchor=E)
        self.config_B.pack(anchor=E)

        ### Tool tips to main menu ###

        CreateToolTip(self.hide_B, text='Hide me to tray ;)')
        CreateToolTip(self.config_B, text='Main program settings')
        CreateToolTip(self.back_B, text='Go back to main menu')
        CreateToolTip(self.info_B, text='Info (disabled)')


        ### MAIN MENU ###

        self.main_menu = ttk.Frame(self.master, padding=(3, 3, 12, 12))
        self.main_menu.pack(fill=BOTH, expand=YES)


        self.M_Lab_A = ttk.Label(self.main_menu,
                                 text='Press key [  ' + settings[1][0] + ' ' + settings[1][1] + ' ' +
                                      settings[1][2] + '] to make fullscreen screenshot',padding=(6, 6, 16, 6))

        self.M_Lab_B = ttk.Label(self.main_menu,
                                 text='Press key [  ' + settings[2][0] + ' ' + settings[2][1] + ' ' +
                                      settings[2][2] + '] to draw screenshot box',padding=(6, 6, 16, 6))

        self.packer_frame = ttk.Frame(self.main_menu, padding=(6, 6, 16, 6))
        self.M_Lab_C = ttk.Label(self.packer_frame,
                                 text='Press key [  ' + settings[8][0] + ' ' + settings[8][1] + ' ' +
                                      settings[8][2] + '] to make screenshot from coordinations ' + self._repack_postions())

        self.eye = ico_open('eye.ico')
        self.draw_box = Button(self.packer_frame, image=self.eye, command=None, bg=theme_color, relief="flat")

        self.draw_box.bind('<Enter>', self.bdraw)
        self.draw_box.bind('<Leave>', self.bdestroy)

        self.M_Lab_A.pack(anchor=CENTER)
        self.M_Lab_B.pack(anchor = CENTER)
        self.M_Lab_C.pack(side = LEFT)
        self.packer_frame.pack(anchor= CENTER)
        self.draw_box.pack(side = LEFT)


        ### OPTIONS ###

        self.optionsL = ttk.Frame(self.master, padding=(2, 3, 12, 12))
        self.optionsR = ttk.Frame(self.master, padding=(2, 3, 12, 12))

        self.O_Lab_F = ttk.Label(text='Save settings?')
        self.save = ttk.LabelFrame(self.optionsR, labelwidget=self.O_Lab_F, padding=(6, 6, 6, 6))
        self.Lab_info = ttk.Label(self.save, text=info_desc_A)
        self.save_ico = ico_open('save.ico')
        self.save_button = Button(self.save, image=self.save_ico, command=reload, bg=theme_color, relief="flat")

        self.O_Lab_A = ttk.Label(text=hotkey_desc_A)
        self.O_Lab_B = ttk.Label(text=hotkey_desc_B)
        self.O_Lab_C = ttk.Label(text=hotkey_desc_C)
        self.O_Lab_D = ttk.Label(text='Show this window after screenshot?')
        self.O_Lab_E = ttk.Label(text='Start hidden?')
        self.O_Lab_F = ttk.Label(text='Set predefined box hotkeys')
        self.O_Lab_G = ttk.Label(text='Set area for predefined box')

        self.col1 = ttk.LabelFrame(self.optionsR, labelwidget=self.O_Lab_A, padding=(6, 6, 6, 6)) #keys
        self.col2 = ttk.LabelFrame(self.optionsR, labelwidget=self.O_Lab_B, padding=(6, 6, 6, 6)) #keys
        self.col3 = ttk.LabelFrame(self.optionsL, labelwidget=self.O_Lab_C, padding=(6, 6, 6, 6)) #save button
        self.col4 = ttk.LabelFrame(self.optionsL, labelwidget=self.O_Lab_D, padding=(8, 8, 8, 8)) #mode
        self.col5 = ttk.LabelFrame(self.optionsL, labelwidget=self.O_Lab_E, padding=(8, 8, 8, 8)) #mode
        self.col6 = ttk.LabelFrame(self.optionsR, labelwidget=self.O_Lab_F, padding=(8, 8, 8, 8)) #keys
        self.col7 = ttk.LabelFrame(self.optionsL, labelwidget=self.O_Lab_G, padding=(8, 8, 8, 8)) #area

        self.patch_frame = ttk.Frame(self.col3, padding=(1, 1, 6, 6))
        self.O_Lab_C1 = ttk.Label(self.patch_frame, text='Current is:')
        self.O_Lab_C2 = ttk.Label(self.col3, text='' + settings[4])
        self.O_Lab_D1 = ttk.Label(self.col7, text='Coords: '+str(settings[7]))


        self.keysetterA = ttk.Button(self.col1, text=settings[1][0], command=lambda: self.keysetter(0))
        self.keysetterB = ttk.Button(self.col1, text=settings[1][1], command=lambda: self.keysetter(1))
        self.keysetterC = ttk.Button(self.col1, text=settings[1][2], command=lambda: self.keysetter(2))

        self.BOXkeysetterA = ttk.Button(self.col2, text=settings[2][0], command=lambda: self.keysetter(3))
        self.BOXkeysetterB = ttk.Button(self.col2, text=settings[2][1], command=lambda: self.keysetter(4))
        self.BOXkeysetterC = ttk.Button(self.col2, text=settings[2][2], command=lambda: self.keysetter(5))

        self.Const_boxA = ttk.Button(self.col6, text=settings[8][0], command=lambda: self.keysetter(6))
        self.Const_boxB = ttk.Button(self.col6, text=settings[8][1], command=lambda: self.keysetter(7))
        self.Const_boxC = ttk.Button(self.col6, text=settings[8][2], command=lambda: self.keysetter(8))

        self.fol_ico = ico_open('F_pic.ico')
        self.asker = Button(self.patch_frame, image=self.fol_ico, command=self.path_setter, bg=theme_color, relief="flat")

        self.resize_imgA = ico_open('arrows.ico')
        self.resize_imgB = ico_open('square.ico')
        self.resizer = Button(self.col7, image=self.resize_imgA, command= self.link_command, bg=theme_color, relief="flat")
        self.resizer.bind('<Enter>', self.anim_b)

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

        self.Const_boxA.pack(side=LEFT, fill=X, expand=YES)
        self.Const_boxB.pack(side=LEFT, fill=X, expand=YES)
        self.Const_boxC.pack(side=LEFT, fill=X, expand=YES)

        self.col1.pack(anchor=N, fill=X, expand=YES) # fullshot setters
        self.col2.pack(anchor=N, fill=X, expand=YES) # screenshot box setters
        self.col6.pack(anchor=N, fill=X, expand=YES) # Constbox setters
        self.col7.pack(anchor=N, fill=X, expand=YES)

        self.save.pack(anchor=N, fill=X, expand=YES) # save button
        self.Lab_info.pack(side=LEFT)
        self.save_button.pack(side=LEFT)

        self.resizer.pack(side = RIGHT)

        self.col3.pack(anchor=N, fill=X, expand=YES)
        self.patch_frame.pack(anchor = N,fill = X)
        self.O_Lab_C1.pack(side = LEFT)
        self.asker.pack(side = RIGHT)
        self.O_Lab_C2.pack(side = LEFT)
        self.O_Lab_D1.pack(side=LEFT)

        self.col4.pack(anchor=N,fill=X, expand=YES)
        self.col5.pack(anchor=N,fill=X, expand=YES)

        ### OPTIONS TIPS ###

        CreateToolTip(self.save_button, 'Save and restart')
        CreateToolTip(self.asker, 'Change output location')

        ### TUTORIAL ### # discontinued

        self.info_frame_A = ttk.Frame(self.master, padding=(3, 3, 12, 12))
        self.inf_lab_A = ttk.Label(self.info_frame_A, text='NoTHING here',padding=(0, 0, 0, 12))
        self.inf_lab_B = ttk.Label(self.info_frame_A, text='')
        if settings[6] :
            settings[6] = False
            cfg_save(settings)
        self.inf_lab_C = ttk.Label(self.info_frame_A, text='')



        ### GEOMETRY SETTINGS ###
        self.element_height = self.M_Lab_A.winfo_reqheight()
        self.window_width = str(self.M_Lab_A.winfo_reqwidth() + 400)
        self.master.update()
        self.menu_height = str(self.M_Lab_A.winfo_reqheight() * 3 + 40)
        master.geometry(self.window_width + 'x' + str(self.menu_height))
        self.option_height = str(1 * (self.optionsL.winfo_reqheight()))
        # self.option_height = str(8 * (self.element_height + self.keysetterA.winfo_reqheight() + 10))
        self.info_height = str(4 * (self.element_height + self.keysetterA.winfo_reqheight() + 10))

        if settings[5] == 1:
            self.master.withdraw()
            ti.tip_info(' ** Ready! **')

    def link_command(self):
        th = Thread(target = screenshot_box.draw_box, args=(settings[4], 2))
        th.start()
        th.join()
        self.button_refresh()
        st = cfg_load()
        txt = str(st[7])
        self.O_Lab_D1.config(text='Coords:' + txt)

    def anim_b(self,event):
        '''swap images'''
        self.resizer.after(400, lambda:  self.resizer.config(image = self.resize_imgB))
        self.resizer.after(800, lambda:  self.resizer.config(image = self.resize_imgA))
        self.resizer.after(1200, lambda:  self.resizer.config(image = self.resize_imgB))
        self.resizer.after(1600, lambda:  self.resizer.config(image = self.resize_imgA))

    def bdraw(self,event):
        '''draw selected area'''
        settings = cfg_load()
        x1,y1,x2,y2 = settings[7][0],settings[7][1],settings[7][2],settings[7][3]
        x1 = str(x1)
        x2 = str(x2)
        y1 = str(y1)
        y2 = str(y2)

        # noinspection PyAttributeOutsideInit
        self.postion_box = Toplevel(self.master)
        self.postion_box.wm_overrideredirect(1)
        self.postion_box.wm_geometry(x2+'x'+y2+'+'+x1+'+'+y1)
        self.postion_box.wm_attributes('-alpha', 0.4)
        w = Canvas(self.postion_box,background= theme_color, width = x2, height = y2)
        w.pack()
        self.master.focus_get()

    def bdestroy(self,event):
        '''drawed area destroy'''
        self.postion_box.after(100, lambda: self.postion_box.wm_attributes('-alpha', 0.4))
        self.postion_box.after(200, lambda: self.postion_box.wm_attributes('-alpha', 0.3))
        self.postion_box.after(300, lambda: self.postion_box.wm_attributes('-alpha', 0.2))
        self.postion_box.after(400, lambda: self.postion_box.wm_attributes('-alpha', 0.1))
        self.postion_box.after(500, self.postion_box.destroy)

    def _repack_postions(self):
        settings = cfg_load()
        self._r_pos = []
        self._r_pos = settings[7][0], settings[7][1], settings[7][0] + settings[7][2], settings[7][1] + settings[7][3]
        self._r_pos = str(self._r_pos)
        return self._r_pos

    def info_trigger(self): # discontinued
        self.main_menu.pack_forget()
        self.optionsL.pack_forget()
        self.optionsR.pack_forget()
        self.back_B.pack_forget()
        self.config_B.pack(anchor=E)
        self.master.geometry(self.window_width + 'x' + self.info_height)
        self.info_frame_A.pack(fill = BOTH)
        self.inf_lab_A.pack(anchor = NE)
        self.inf_lab_B.pack(anchor=SE, fill = Y, expand = YES)
        self.inf_lab_C.pack(anchor = CENTER, fill = Y, expand = YES)

    def blink(self,button,xtimes):
        if not xtimes==0:
            button.after(500, lambda: button.config(bg= 'green'))
            button.after(1000, lambda: button.config(bg=theme_color))
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
        self.optionsL.pack(side="left", expand=True, fill="both")
        self.optionsR.pack(side="right", expand=True, fill="both")

    def back(self):
        self.master.geometry(self.window_width + 'x' + str(self.menu_height))
        self.optionsL.pack_forget()
        self.optionsR.pack_forget()
        self.back_B.pack_forget()
        self.config_B.pack(anchor=E)
        self.main_menu.pack(fill=BOTH, expand=YES)

    def keysetter(self, number):
        if number < 3 and number >= 0:
            V = 1
        elif number > 2 and number < 6:
            V = 2
            number -= 3
        elif number >= 6 and number < 9:
            V = 8
            number -= 6


        k = read_key()
        if k == 'esc':
            settings[V][number] = ''
        elif k == str(settings[V][0]) or k == str(settings[V][1]) or k == str(settings[V][2]):
            settings[V][number] = ''
        else:
            settings[V][number] = k

        if (settings[1][0] == settings[2][0] and settings[1][1] == settings[2][1] and settings[1][2] == settings[2][2] or
        settings[1][0] == settings[8][0] and settings[1][1] == settings[8][1] and settings[1][2] == settings[8][2] or
        settings[2][0] == settings[8][0] and settings[2][1] == settings[8][1] and settings[2][2] == settings[8][2]):
            messagebox.showwarning(title='Information', message='Settings cannot have the same configuration!', icon='warning')
            settings[1] = ['print screen', '', '']
            settings[2] = ['pause', '', '']
            settings[8] = ['home', '', '']

        elif settings[V][0] == '':
            settings[V][1] = ''
            settings[V][2] = ''
            messagebox.showerror('Error', 'Cannot be empty!')
            if V == 1:
                settings[V][0] = 'print screen'
            elif V == 2:
                settings[V][0] = 'pause'
            elif V == 8:
                settings[V][0] = 'home'

        elif settings[V][1] == '':
            settings[V][2] = ''

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
        self.M_Lab_C.config(text='Press key [  ' + settings[8][0] + ' ' + settings[8][1] + ' ' +settings[8][2] + '] to make screenshot from coordinations ' +  self._repack_postions())

        self.keysetterA.config(text=settings[1][0])
        self.keysetterB.config(text=settings[1][1])
        self.keysetterC.config(text=settings[1][2])
        self.BOXkeysetterA.config(text=settings[2][0])
        self.BOXkeysetterB.config(text=settings[2][1])
        self.BOXkeysetterC.config(text=settings[2][2])
        self.Const_boxA.config(text=settings[8][0])
        self.Const_boxB.config(text=settings[8][1])
        self.Const_boxC.config(text=settings[8][2])
        self.O_Lab_C2.config(text='' + settings[4])
        self.O_Lab_D1.config(text='Coords:' + str(settings[7]))


settings = cfg_load()

t1 = Thread(target=listener, args=())
t2 = Thread(target=listener_BOX, args=())
t3 = Thread(target=Const_box, args=())
t1.daemon = True
t1.start()
t2.daemon = True
t2.start()
t3.daemon = True
t3.start()

ti = TrayIco()
ti.init_icon_tray()

root = Tk()
root.configure(bg=theme_color)
root.title(settings[0])
root.iconbitmap(resource_path("ghost.ico"))
root.resizable(width=False, height=False)

if settings[5] == 1:
    root.deiconify()

Sw = Switcher(root)

root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()
del Sw
