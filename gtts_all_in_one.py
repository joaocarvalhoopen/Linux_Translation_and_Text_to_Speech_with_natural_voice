#!/usr/bin/env /home/joao/anaconda3/bin/python

# Proj. name:  Linux Translation and Text to Speech with natural voice
# Filename:    gtts_all_in_one.py
# Author:      João Nuno Carvalho
# Date:        2021.03.09
# License:     MIT Open Source License
# Description: This is a program to make TTS - Text to Speech in Linux.
#              More specific in Ubuntu or Debian with Gnome windows manager.
#              With it you can select a text with mouse or keyboard and 
#              speak it or translate and speak it.
#
#              In the following languages:
#                1 - Kill current speech.
#                2 - Speech in English.
#                3 - Translate from English into Portuguese and speak.
#                4 - Translate from Portuguese into English and speak.
#                5 - Speech in Spanish.
#                6 - Translate from Spanish into Portuguese and speak.
#                7 - Translate from Portuguese into Spanish and speak.
#                5 - Speech in Portuguese.
#
#
# The programs that we use:
#
#              xclip
#              deep_translator - https://github.com/nidhaloff/deep-translator
#              sleep
#              gtts-cli
#              play from SOX - Sound utilities.
#              mp3 pakage 
#
#
# To install do (I have Anaconda Python installed):
#   
#              pip install gTTS
#              pip install -U deep_translator
#              sudo apt install xclip
#              sudo apt install sox
#              sudo apt-get install libsox-fmt-mp3
#
# To test do:
#
#              gtts-cli -l en 'Good morning!' | play -t mp3 -              
#
#
#              
# Steps:   
#              mkdir ~/gtts_my_speak
#              cd ~/gtts_my_speak
#
#              # Download and put the files inside the directory.
#
#              # Edit the file "gtts_all_in_one.desktop" and change the user
#              # path in gtts_all_in_one.desktop to your user.
#
#              cp gtts_all_in_one.desktop ~/.local/share/applications
#
#              # Edit the python file "gtts_all_in_one.py" and change the 
#              # MY_USER_DIR to your user directory.
#              # Change /home/joao to your username /home/username.
#
#              # Make the Python file executable.
# 
#              chmod u+x ./gtts_all_in_one.py
#
#
# To test the GUI program do:
#              
#              ./gtts_all_in_one.py
#              
#              # ... and then do ...
#
#              gtk-launch gtts_all_in_one.desktop
#
#
# Add the shortcuts to the Ubuntu or Debian gnome Window Manager:
#              Note: Change "joao" to your username.
#
#              Name: gtts - speak selected text - Menu
#              Command: gtk-launch gtts_all_in_one.desktop
#              keys shortcut: super + '.'
#
#
#              Name: gtts - speak selected text - Repeat last option
#              Command: /home/joao/gtts_my_speak/gtts_all_in_one.py last_option
#              keys shortcut: super + '-'
#
#
# Have fun!
#


import sys
import os
from pathlib import Path

# https://github.com/nidhaloff/deep-translator
from deep_translator import GoogleTranslator 

# Registered to the Shortcut Windows Key + "+".

# TODO: Configure the path to your users dir.
MY_USER_DIR = "/home/joao"


#
# Start of the program.
#

# os.system('play "/home/joao/gtts_my_speak/audio_test_portuguese.mp3"')

print(str(sys.argv))

# Path("/dev/shm/argv.txt").write_text(str(sys.argv)) 

if len(sys.argv) != 1 and len(sys.argv) != 2:
    print(f"Usage: python gtts_all_in_one.py [last_option] ")
    exit()

import tkinter as tk

TEXT_SOURCE_FILE = "/dev/shm/speak_a.txt"
TEXT_TARGET_FILE = "/dev/shm/speak_b.txt"
LAST_OPTION_FILE = "/dev/shm/last_option.txt"


EN = "en"
ES = "es"
PT = "pt"

def save_last_option(last_option):
    # Write to file current option as last option selected to be processed
    # by the next fast shortcut key.
    Path(LAST_OPTION_FILE).write_text(str(last_option))    


class Data:

    def __init__(self, translation, source_lang, target_lang, speed):
        self.translation = translation
        self.source_lang = source_lang
        self.target_lang = target_lang 
        self.speed       = speed


def remove_new_lines_and_do_translation(data):

    # This function removes the \n (newlines) if it isn't in the end
    # of a sentence, that terminates with a dot. 

    file_input_name  = TEXT_SOURCE_FILE
    file_output_name = TEXT_TARGET_FILE

    file_input = open(file_input_name, "r")
    input_lines = file_input.readlines()
    file_input.close()

    lst = []
    flag_removed_last_line_newline = False
    for line in input_lines:
        # New Line to be removed if not at the end of a phrase
        # terminated with a dot.
        if line.endswith("\n") and not line.endswith(".\n"):
            lst.append(line[:-1])
            lst.append(" ")
            flag_removed_last_line_newline = True
        else:
            # Normal line.
            if flag_removed_last_line_newline:
                # Corrects the removed \n (new line), by putting it
                # back again. If the the current line starts with a
                # upper case. 
                if len(line) > 0 and line[0].isupper():
                    del lst[-1]
                    lst.append("\n")
            lst.append(line)
            flag_removed_last_line_newline = False

    text_output = "".join(lst)


    # Replace Abbreviations here by source language:
    if data.source_lang == EN:
        text_output = text_output.replace("<", "")
        text_output = text_output.replace(">", "")
        text_output = text_output.replace(" CLI ", " command line ")
        text_output = text_output.replace(" IPv6 ", " I P version 6 ")
        text_output = text_output.replace(" btw ", " by the way ")
        text_output = text_output.replace(" WIP ", " work in progress ")

    print(text_output)

    if data.translation == True:
        text_output = text_output.replace("\n", " ")
        text_output = text_output.replace("-", " ")
        # text_output = text_output.replace("'", " ")
        text_output = GoogleTranslator(source = data.source_lang,
                                       target = data.target_lang).translate (text_output)

    file_output = open(file_output_name, "w")
    file_output.write(text_output)
    file_output.close()


def process_all_in_one(data):
    # Save X text selection to a file.
    # Runs clip to get the the selected text from the GUI in X, in any GUI program.
    os.system('xclip -out > ' + TEXT_SOURCE_FILE)    

    remove_new_lines_and_do_translation(data)

    # Waits for 1 second to give time to focus the eyes on the text.
    os.system('sleep 1.0')
    os.system(MY_USER_DIR + '/anaconda3/bin/gtts-cli -l ' + data.target_lang + ' -f ' + TEXT_TARGET_FILE + ' | play -t mp3 - tempo ' + str(data.speed))

    # os.system('/home/joao/gtts_my_speak/gtts_my_speak_en.sh')


def g_kill_speech():
    print("\nc_kill_speech()")
    # Kill all process's of "play" that are playing the audio
    os.system('''ps aux | grep "play -t mp3 -"| grep -v grep | awk '{print $2}' | xargs kill''')

def g_play_en():
    print("\nc_play_en()")
    save_last_option(2)

    translation = False
    source_lang = EN
    target_lang = EN
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)
        
def g_play_en_to_pt():
    print("\nc_play_en_to_pt()")
    save_last_option(3)

    translation = True
    source_lang = EN
    target_lang = PT
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)

def g_play_pt_to_en():
    print("\nc_play_pt_to_en()")
    save_last_option(4)

    translation = True
    source_lang = PT
    target_lang = EN
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)

def g_play_es():
    print("\nc_play_es()")
    save_last_option(5)

    translation = False
    source_lang = ES
    target_lang = ES
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)

def g_play_es_to_pt():
    print("\nc_play_es_to_pt()")
    save_last_option(6)

    translation = True
    source_lang = ES
    target_lang = PT
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)

def g_play_pt_to_es():
    print("\nc_play_pt_to_es()")
    save_last_option(7)

    translation = True
    source_lang = PT
    target_lang = ES
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)

def g_play_pt():
    print("\nc_play_pt()")
    save_last_option(8)

    translation = False
    source_lang = PT
    target_lang = PT
    speed       = 1.0
    data = Data(translation, source_lang, target_lang, speed)
    process_all_in_one(data)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Label(self)
        self.hi_there["text"] = "\nTTS - Text to Speech\n\nLinux\n"
        self.hi_there.pack(side="top")


        self.kill = tk.Button(self, text="1 - Kill speech", fg="red",
                              command=self.c_kill_speech)
        self.kill.pack(side="top")
        

        self.play_en = tk.Button(self, text="2 - EN         ", 
                              command=self.c_play_en)
        self.play_en.pack(side="top")
        
        self.play_en_to_pt = tk.Button(self, text="3 - EN to PT   ", 
                              command=self.c_play_en_to_pt)
        self.play_en_to_pt.pack(side="top")


        self.c_play_pt_to_en = tk.Button(self, text="4 - PT to EN   ", 
                              command=self.c_play_pt_to_en)
        self.c_play_pt_to_en.pack(side="top")


        self.play_es = tk.Button(self, text="5 - ES         ", 
                              command=self.c_play_es)
        self.play_es.pack(side="top")


        self.c_play_es_to_pt = tk.Button(self, text="6 - ES to PT   ", 
                              command=self.c_play_es_to_pt)
        self.c_play_es_to_pt.pack(side="top")


        self.play_pt_to_es = tk.Button(self, text="7 - PT to ES   ", 
                              command=self.c_play_pt_to_es)
        self.play_pt_to_es.pack(side="top")


        self.play_pt = tk.Button(self, text="8 - PT         ", 
                              command=self.c_play_pt)
        self.play_pt.pack(side="top")


        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")



    def c_kill_speech(self):
        # Closes the thinter GUI window.
        self.master.destroy()
        g_kill_speech()

    def c_play_en(self):
        self.master.destroy()
        g_play_en()

    def c_play_en_to_pt(self):
        self.master.destroy()
        g_play_en_to_pt()

    def c_play_pt_to_en(self):
        self.master.destroy()
        g_play_pt_to_en()

    def c_play_es(self):
        self.master.destroy()
        g_play_es()

    def c_play_es_to_pt(self):
        self.master.destroy()
        g_play_es_to_pt()

    def c_play_pt_to_es(self):
        self.master.destroy()
        g_play_pt_to_es()

    def c_play_pt(self):
        self.master.destroy()
        g_play_pt()


def play_sound():
    os.system('play "/home/joao/gtts_my_speak/audio_test_portuguese.mp3"')


def process_option(key):
    if key == '1':
        g_kill_speech()
    elif key == '2':
        g_play_en()
    elif key == '3':
        g_play_en_to_pt()
    elif key == '4':
        g_play_pt_to_en()
    elif key == '5':
        g_play_es()
    elif key == '6':
        g_play_es_to_pt()
    elif key == '7':
        g_play_pt_to_es()
    elif key == '8':
        g_play_pt()
    

if len(sys.argv) == 2 and sys.argv[1] == "last_option":
    # Read from file the last option selected.
    last_option = Path(LAST_OPTION_FILE).read_text()
    if len(last_option) != 0:
        print(f"\nProcessing shortcut last option...")
        key = last_option
        # Start the processing.
        process_option(key)
        exit()

     
def key_press(event):
    key = event.char
    print("key: " + str(key))
    if key not in ['1','2','3','4','5','6','7','8']:
        return
    # last_option = key
    # save_last_option(last_option)

    # To close the Thinter GUI window.
    app.master.destroy()

    # Start the processing.
    process_option(key)


root = tk.Tk()
# To center the window on the screen.
root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))
root.bind("<Key>", key_press)
app = Application(master=root)

app.mainloop()

