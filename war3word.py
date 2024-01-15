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
    for index in range(3):
        kb.add_hotkey('alt+{}'.format(index+1), trigger_key_press, args=[entry_list[index].get()])
        config.set('Settings', 'Alt+{}'.format(index+1), entry_list[index].get())
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
    window.destroy()

def update_hotkey():
    kb.unhook_all_hotkeys()
    for index in range(3):
        kb.add_hotkey('alt+{}'.format(index+1), trigger_key_press, args=[entry_list[index].get()])

def init_config():
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

if __name__ == "__main__":
    #config the variable      
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        init_config()
    config.read('config.ini')
    width  = config.getint('Settings', 'Window-Width')
    hight  = config.getint('Settings', 'Window-height')
    icon   = config.get('Settings', 'Icon')
    bg_entry  = '#edf7f7'
    bg_button = '#7086ff'
    bg_window = '#ffffff'
    #internal variable
    alt_list = [config.get('Settings', 'Alt+{}'.format(index+1)) for index in range(3)]

    #Tkinter initialize
    window = tk.Tk(className="一键喊话")
    window.iconbitmap(icon)
    window.geometry("{}x{}".format(width,hight))
    window.configure(bg = bg_window)
    center_window(window,width,hight)
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    #Tkinter variable
    arg_list = [tk.StringVar(value=alt_list[index]) for index in range(3)]
    label_list = [tk.Label(text="Alt + {}:".format(index+1),justify="left",width=10,height=1,font=(12)) for index in range(3)]
    entry_list = [tk.Entry(textvariable=arg_list[index],font=(12),bg= bg_entry) for index in range(3)]

    #add the widget in window
    button = tk.Button(window, text="Update", command=update_hotkey,fg="#000000",bg = bg_button)
    button.grid(row=1, column=2, rowspan=3, padx=20)
    for index in range(3):
        label_list[index].grid(row=index, column=0)
        entry_list[index].grid(row=index, column=1)  

    #add the hotkey
    for index in range(3):
        kb.add_hotkey('alt+{}'.format(index+1), trigger_key_press, args=[entry_list[index].get()])

    window.mainloop()
