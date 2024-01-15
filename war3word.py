import keyboard as kb
import time
import tkinter as tk
import configparser
import os

def trigger_key_press(keystring):
    time.sleep(0.15)
    kb.press_and_release('enter')
    kb.write(keystring)
    kb.press_and_release('enter')

def center_window(window,width,hight):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_x = int((screen_width - width) / 2)
    window_y = int((screen_height - hight) / 2)
    window.geometry("{}x{}+{}+{}".format(width,hight,window_x, window_y))

def on_closing():
    print("Exit the program,Save the config in config.ini")
    config.set('Settings', 'Alt+1', entry1.get())
    config.set('Settings', 'Alt+2', entry2.get())
    config.set('Settings', 'Alt+3', entry3.get())
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
    window.destroy()

def update_hotkey():
    kb.unhook_all_hotkeys()
    kb.add_hotkey('alt+1', trigger_key_press, args=[entry1.get()])
    kb.add_hotkey('alt+2', trigger_key_press, args=[entry2.get()])
    kb.add_hotkey('alt+3', trigger_key_press, args=[entry3.get()])

def init_config(config):
    config['Settings'] = {
        'Window-Width': 400,
        'Window-height': 100,
        'Icon': 'icon2.ico',
        'Alt+1': 'hg',
        'Alt+2': '3',
        'Alt+3': 'q'
        }
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
        
config = configparser.ConfigParser()
if not os.path.exists('config.ini'):
    init_config(config)
config.read('config.ini')
width  = config.getint('Settings', 'Window-Width')
hight  = config.getint('Settings', 'Window-height')
icon   = config.get('Settings', 'Icon')
alt_1  = config.get('Settings', 'Alt+1')
alt_2  = config.get('Settings', 'Alt+2')
alt_3  = config.get('Settings', 'Alt+3')

window = tk.Tk(className="一键喊话")
window.iconbitmap(icon)
arg1 = tk.StringVar(value = alt_1)
arg2 = tk.StringVar(value = alt_2)
arg3 = tk.StringVar(value = alt_3)
window.geometry("{}x{}".format(width,hight))
center_window(window,width,hight)
window.resizable(False, False)

label1 = tk.Label(text="Alt + 1:",justify="left",width=10,height=1,font=(12))
label2 = tk.Label(text="Alt + 2:",justify="left",width=10,height=1,font=(12))
label3 = tk.Label(text="Alt + 3:",justify="left",width=10,height=1,font=(12))
entry1 = tk.Entry(textvariable=arg1,font=(12),bg="#edf7f7")
entry2 = tk.Entry(textvariable=arg2,font=(12),bg="#edf7f7")
entry3 = tk.Entry(textvariable=arg3,font=(12),bg="#edf7f7")
button = tk.Button(window, text="Update", command=update_hotkey,fg="#000000",bg="#7086ff")

button.grid(row=1, column=2, rowspan=3, padx=20)
label1.grid(row=0, column=0)
label2.grid(row=1, column=0)
label3.grid(row=2, column=0)
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)
entry3.grid(row=2, column=1)

window.protocol("WM_DELETE_WINDOW", on_closing) 
kb.add_hotkey('alt+1', trigger_key_press, args=[entry1.get()])
kb.add_hotkey('alt+2', trigger_key_press, args=[entry2.get()])
kb.add_hotkey('alt+3', trigger_key_press, args=[entry3.get()])

window.mainloop()
