import PySimpleGUI as sg
import os.path

import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back


#GUI initaial##########
#sg.ChangeLookAndFeel('Dark')
 
column_list = [
   
    [   sg.Multiline(size=(35,10),
                     autoscroll=True,
                     pad=(0, (15,0)),
                     key="-OUTPUT-")
    ],
    [
        
        sg.In(size=(25,1), enable_events=True, key="-INPUT-"),
        sg.Button("SEND")
    ]
    ]
chat_history=[]
history_offset = 0
window = sg.Window("Chatter", column_list)

#SOCKEtS#################
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5000
separator_token = "<SEP>"

s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}....")
s.connect((SERVER_HOST, SERVER_PORT))
print("[+]Connecter.")

#listining for messages#########
def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)
        chat_history.append(message)
        history_offset = len(chat_history)
        
        window['-OUTPUT-'].update(('\n').join(chat_history[-history_offset:]), text_color="Blue")
        
    
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

name = "GUIClient"
while True:
     
#gui handler###
    event, values = window.read()
    #end if user closes the window
    if event == sg.WIN_CLOSED:
        break
    elif event == "SEND" :
        if values['-INPUT-'] != '': 
            to_send = values['-INPUT-'].rstrip()
            date_now = str(datetime.now().strftime('[%Y-%m-%d %H:%M:%S]'))
            
            to_send = f"{date_now} {name}{separator_token}{to_send}"
            s.send(to_send.encode())
                       
                    
            window['-INPUT-'].update('')
          

s.close()            
window.close()
    