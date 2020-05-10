from pickle import load,dump
from os.path import exists,dirname
from tkinter import messagebox
from pathlib import Path
import sys
import os

def cfg_load():
    mode = 2
    win_mode = 2
    postions = [0,0,0,0]
    first_run = True
    fullscreenshot_keys = ['print screen','', ''] # 0,1,2
    box_keys = ['pause', '',''] # 3,4,5
    constant_box_keys = ['home', '', ''] # 6,7,8
    file = str(dirname(sys.executable)) + '\\ '+ "settings.cfg"
    defaults = ['Specter', fullscreenshot_keys,box_keys,mode, dirname(sys.executable),win_mode,first_run,postions,constant_box_keys] # 8
    size = len(defaults)
    # defaults = ['Specter', 'ctrl', 'shift', 'print screen', str(Path().absolute())]

    if exists(file):
        res = open(file,"rb")
        settings = load(res)
        if len(settings) != size:
            Q = messagebox.showwarning(title='Warning', message='Old setting file found\n this file will be deleted and settings reset', icon='warning')
            settings = defaults
            res.close()
            os.remove(file)
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        res.close()
    else:
        # print('**Not Found**')
        settings = defaults
    return settings


def cfg_save(arr):
    file = str(dirname(sys.executable)) + '\\ '+ "settings.cfg"
    res = open(file, "wb")
    dump(arr,res)
    res.close()

