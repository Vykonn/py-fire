import json
import keyboard
import os
import threading
def main():
    with open('data.json', 'r') as f:
        data = json.load(f)
    currentexport = ["clear()"]
    if data["lightup"] == "true":
        currentexport.append("lightup()")
    if data["rainbow"] == "true":
        currentexport.append("rainbow()")
    else:
        currentexport.append("plain()")
        
    return currentexport
def handleinput(input):
    with open('data.json', 'r') as f:
        data = json.load(f)
    inputm = input[1]
    global command
    global commande
    command = False
    commande = []
    print(input)
    if input[1] == 16 or input[1] == 17 or input[1] == 18 or input[1] == 19 or input[1] == 118 or input[1] == 25:
        if input[0] == 144:
            if input[2] == 127:
                ##CLICK INPUT
                if input[1] == 25:
                    inputm = 118
                if "%s1" % inputm in data:
                    if data["%s1" % inputm][0] == "cmd":
                        commande = data["%s1" % inputm][1]
                        command = True
                    else:
                        keyboard.send("+".join(data["%s1" % inputm]))
        if input[0] == 176:
            if input[2] == 127:
                ##LEFT INPUT - 2
                if "%s2" % inputm in data:
                    if data["%s2" % inputm][0] == "cmd":
                       commande = data["%s2" % inputm][1]
                       command = True
                    else:
                        keyboard.send("+".join(data["%s2" % inputm]))
            if input[2] == 1:
                ##RIGHT INPUT - 3
                if "%s3" % inputm in data:
                    if data["%s3" % inputm][0] == "cmd":
                        commande = data["%s3" % inputm][1]
                        command = True
                    else:
                        keyboard.send("+".join(data["%s3" % inputm]))
    else:
        if input[2] >= 1:
            if "{}".format(inputm) in data:
                if data["{}".format(inputm)][0] == "cmd":
                    commande = data["%s" % input[1]][1]
                    command = True
                else:
                    keyboard.send("+".join(data["%s" % input[1]]))
    if command:
        return commande
    else:
        return False
    