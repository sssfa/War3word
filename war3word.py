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
    config.set('Settings', 'Theme', str(theme_index))
    for index in range(hk_totoals):
        kb.add_hotkey('alt+{}'.format(index+1), trigger_key_press, args=[entry_list[index].get()])
        config.set('Settings', 'Alt+{}'.format(index+1), entry_list[index].get())
    with open('config.ini', 'w') as config_file:
        config.write(config_file)
    window.destroy()

def update_hotkey():
    kb.unhook_all_hotkeys()
    for index in range(hk_totoals):
        kb.add_hotkey('alt+{}'.format(index+1), trigger_key_press, args=[entry_list[index].get()])

def init_config():
    config['Settings'] = {
        'Window-Width': 400,
        'Window-height': 200,
        'Icon': 'icon2.ico',
        'Theme': 0,
        'Alt+1': 'hg',
        'Alt+2': '3',
        'Alt+3': 'q',
        'Alt+4': '4'
        }
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

class Theme:
    def __init__(self,name,bg_entry,bg_button,fg_button,bg_window):
        self.name      = name
        self.bg_entry  = bg_entry
        self.fg_entry  = fg_button
        self.bg_button = bg_button
        self.fg_button = fg_button
        self.bg_window = bg_window
        self.bg_label  = bg_window
        self.fg_label  = fg_button

def switch_theme():
    global theme_index
    theme_index = (theme_index + 1)%len(theme_list)
    print('{} switch to {},totals {}'.format(theme_index,theme_index+1,len(theme_list)))
    next_theme = theme_list[theme_index]
    theme_name.set(next_theme.name)
    window.configure (bg=next_theme.bg_window)
    topic.configure(bg=next_theme.bg_label,fg=next_theme.fg_label)
    button1.configure(bg=next_theme.bg_button, fg=next_theme.fg_button)
    button2.configure(bg=next_theme.bg_button, fg=next_theme.fg_button)
    for index in range(hk_totoals):
        label_list[index].configure(bg=next_theme.bg_label,fg=next_theme.fg_label)
        entry_list[index].configure(bg=next_theme.bg_entry,fg=next_theme.fg_entry)

if __name__ == "__main__":
    #config the variable      
    config = configparser.ConfigParser()
    if not os.path.exists('config.ini'):
        init_config()
    config.read('config.ini')
    width  = config.getint('Settings', 'Window-Width')
    hight  = config.getint('Settings', 'Window-height')
    icon   = config.get('Settings', 'Icon')
    #internal variable
    hk_totoals = 4
    theme0 = Theme('竹雅白','#edf7f7','#a3d4b9','#000000','#d5dbd9')
    theme1 = Theme('赭宸紫','#542d66','#542d66','#b9c9c4','#181b47')
    theme2 = Theme('天素青','#859699','#68a9b3','#000000','#c8dde0')
    theme_list = [theme0,theme1,theme2]
    theme_index = config.getint('Settings', 'Theme')
    alt_list = [config.get('Settings', 'Alt+{}'.format(index+1)) for index in range(hk_totoals)]

    #Tkinter initialize
    window = tk.Tk(className="一键喊话")
    window.iconbitmap(icon)
    window.geometry("{}x{}".format(width,hight))
    window.configure(bg = theme_list[theme_index].bg_window)
    center_window(window,width,hight)
    window.resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    #Tkinter variable
    theme_name = tk.StringVar(value=theme_list[theme_index].name)
    arg_list = [tk.StringVar(value=alt_list[index]) for index in range(hk_totoals)]
    label_list = [tk.Label (text="Alt + {}:".format(index+1),
                            fg= theme_list[theme_index].fg_label,
                            bg= theme_list[theme_index].bg_label,
                            justify="left",
                            width  =10,
                            height =1,
                            font =(12)) for index in range(hk_totoals)]
    entry_list = [tk.Entry(textvariable=arg_list[index],
                           font=(12),
                           fg  = theme_list[theme_index].fg_entry,
                           bg  = theme_list[theme_index].bg_entry) for index in range(hk_totoals)]
    button1 = tk.Button(window,
                        text="保存热键",
                        command=update_hotkey,
                        fg = theme_list[theme_index].fg_button,
                        bg = theme_list[theme_index].bg_button
                        )
    button2 = tk.Button(window, 
                        textvariable=theme_name, 
                        command=switch_theme,
                        fg = theme_list[theme_index].fg_button,
                        bg = theme_list[theme_index].bg_button
                        )
    topic = tk.Label(bg=theme_list[theme_index].bg_label)

    #add the widget in window
    topic.grid(row=0)
    button2.place(x=30,y=160)
    button1.place(x=300,y=160)
    for index in range(hk_totoals):
        label_list[index].grid(row=index+1, padx=30, column=0, sticky="e")
        entry_list[index].grid(row=index+1, padx=30, column=1, sticky="w")  

    #add the hotkey
    for index in range(hk_totoals):
        kb.add_hotkey('alt+{}'.format(index+1), trigger_key_press, args=[entry_list[index].get()])

    window.mainloop()