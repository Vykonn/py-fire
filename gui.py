from tkinter import *
import customtkinter
import fire
import threading
import sys
import os
import pystray
import json
import keyboard
import time
if os.path.isfile("data.json"):  
    with open('data.json', 'r') as f:
        data = json.load(f)
else:
    dictionary = {
    "lightup": "false",
    "rainbow": "false"
    }
    with open("data.json", "w") as outfile:
        json.dump(dictionary, outfile)
    with open('data.json', 'r') as f:
        data = json.load(f)

    

from PIL import Image
global knob
knob = False
def record_buttonc():
    print("button pressed")
def record_buttonl():
    print("button pressed")
def record_buttonr():
    print("button pressed")
class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        global currentsel
        global currentcol
        global recordingkey
        global inputGc
        global currentpressdir
        currentpressdir = 0
        inputGc = []
        currentsel = 0 
        currentcol = 0
        recordingkey = False
        def typeselcall(choice):
            self.effectsel.grid()
            if choice == "Pad":
                self.typeselpadrow.grid()
                self.typeselpadrow.set("Select a row")
                self.typeselpadcol.grid()
                self.typeselpadcol.set("Select a column")
                self.actionselbutton.grid()
            else:
                self.typeselpadrow.grid_remove()
                self.typeselpadcol.grid_remove()
                if choice != "Button": self.actionselbutton.grid_remove()
            if choice == "Knob":
                self.typeselknobid.grid()
                self.typeselknobid.set("Select a Knob")
                self.actionselknob.grid()
            else:
                self.typeselknobid.grid_remove()
                self.actionselknob.grid_remove()
            if choice == "Button":
                self.typeselbuttonloc.grid()
                self.typeselbuttonloc.set("Select a button location")
                self.typeselbuttontopid.set("Select a button")
                self.typeselbuttonbottomid.set("Select a button")
                self.typeselbuttonsoloid.set("Select a button")
                self.actionselbutton.grid()
            else:
                self.typeselbuttonloc.grid_remove()
                self.typeselbuttontopid.grid_remove()
                self.typeselbuttonbottomid.grid_remove()
                self.typeselbuttonsoloid.grid_remove()
                if choice != "Pad": self.actionselbutton.grid_remove()

        def buttonloccall(choice):
            if choice == "Top Buttons":
                self.typeselbuttontopid.grid()
                self.typeselbuttontopid.set("Select a button")
            else:
                self.typeselbuttontopid.grid_remove()
            if choice == "Bottom Buttons":
                self.typeselbuttonbottomid.grid()
                self.typeselbuttonbottomid.set("Select a button")
            else:
                self.typeselbuttonbottomid.grid_remove()
            if choice == "SOLO Buttons":
                self.typeselbuttonsoloid.grid()
                self.typeselbuttonsoloid.set("Select a button")
            else:
                self.typeselbuttonsoloid.grid_remove()
        def knobselcall(choice):
            global currentsel
            if choice == "Knob 1": currentsel = 16
            if choice == "Knob 2": currentsel = 17
            if choice == "Knob 3": currentsel = 18
            if choice == "Knob 4": currentsel = 19
            if choice == "SELECT Knob": currentsel = 118
            if "{}{}".format(currentsel,currentpressdir) in data:
                if data["{}{}".format(currentsel,currentpressdir)][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["{}{}".format(currentsel,currentpressdir)]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["{}{}".format(currentsel,currentpressdir)][1])
            else:
                self.keypresspreview.configure(text="None")
        def buttontopcall(choice):
            global currentsel
            if choice == "User Button": currentsel = 26
            if choice == "Pattern Up": currentsel = 31
            if choice == "Pattern Down": currentsel = 32
            if choice == "Browser": currentsel = 33
            if choice == "Grid Left": currentsel = 34
            if choice == "Grid Right": currentsel =  35
            if "%s" % currentsel in data:
                if data["%s" % currentsel ][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["%s" % currentsel ]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["%s" % currentsel ][1])
            else:
                self.keypresspreview.configure(text="None")
        def buttonbottomcall(choice):
            global currentsel
            if choice == "Button 1": currentsel = 44
            if choice == "Button 2": currentsel = 45
            if choice == "Button 3": currentsel = 46
            if choice == "Button 4": currentsel = 47
            if choice == "Button 5": currentsel = 48
            if choice == "Button 6": currentsel = 49
            if choice == "Button 7": currentsel = 50
            if choice == "Button 8": currentsel = 51
            if choice == "Button 9": currentsel = 52
            if choice == "Button 10": currentsel = 53
            if "%s" % currentsel in data:
                if data["%s" % currentsel ][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["%s" % currentsel ]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["%s" % currentsel ][1])
            else:
                self.keypresspreview.configure(text="None")
        def buttonsolocall(choice):
            global currentsel
            if choice == "Solo 1": currentsel = 36
            if choice == "Solo 2": currentsel = 37
            if choice == "Solo 3": currentsel = 38
            if choice == "Solo 4": currentsel = 39
            if "%s" % currentsel in data:
                if data["%s" % currentsel ][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["%s" % currentsel ]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["%s" % currentsel ][1])
            else:
                self.keypresspreview.configure(text="None")
        def padrowcall(choice):
            global currentsel
            global currentcol
            global currentrow  
            if choice == "Row 1": currentrow = 0
            if choice == "Row 2": currentrow = 16
            if choice == "Row 3": currentrow = 32
            if choice == "Row 4": currentrow = 48
            currentsel = (currentcol+currentrow) + 53
            if "%s" % currentsel in data:
                if data["%s" % currentsel ][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["%s" % currentsel ]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["%s" % currentsel ][1])
            else:
                self.keypresspreview.configure(text="None")
        def padcolcall(choice):
            global currentcol
            global currentsel
            global currentrow
            if choice == "Column 1": currentcol = 1
            if choice == "Column 2": currentcol = 2
            if choice == "Column 3": currentcol = 3
            if choice == "Column 4": currentcol = 4
            if choice == "Column 5": currentcol = 5
            if choice == "Column 6": currentcol = 6
            if choice == "Column 7": currentcol = 7
            if choice == "Column 8": currentcol = 8
            if choice == "Column 9": currentcol = 9
            if choice == "Column 10": currentcol = 10
            if choice == "Column 11": currentcol = 11
            if choice == "Column 12": currentcol = 12
            if choice == "Column 13": currentcol = 13
            if choice == "Column 14": currentcol = 14
            if choice == "Column 15": currentcol = 15
            if choice == "Column 16": currentcol = 16
            currentsel = (currentcol+currentrow) + 53
            if "%s" % currentsel in data:
                if data["%s" % currentsel ][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["%s" % currentsel ]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["%s" % currentsel ][1])
            else:
                self.keypresspreview.configure(text="None")
        def actionselknobcall(choice):
            global currentpressdir
            if choice == "Press": currentpressdir = 1
            if choice == "Left": currentpressdir = 2
            if choice == "Right": currentpressdir = 3
            if "{}{}".format(currentsel,currentpressdir) in data:
                if data["{}{}".format(currentsel,currentpressdir)][0] != "cmd":
                    self.effectsel.set("Simulate keypress")
                    effectselcall("Simulate keypress")
                    self.keypresspreview.configure(text="+".join(data["{}{}".format(currentsel,currentpressdir)]))
                else:
                    self.effectsel.set("Run command")
                    effectselcall("Run command")
                    self.runcommandboxvar.set(data["{}{}".format(currentsel,currentpressdir)][1])
            else:
                self.keypresspreview.configure(text="None")
        self.typesel = customtkinter.CTkOptionMenu(self, values=["Pad", "Knob", "Button"], command=typeselcall)
        self.typesel.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.typesel.set("Select a button type")

        self.typeselpadrow = customtkinter.CTkOptionMenu(self, values=["Row 1","Row 2","Row 3", "Row 4"],command=padrowcall)
        self.typeselpadrow.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.typeselpadrow.set("Select a row")
        self.typeselpadrow.grid_remove()
        self.typeselpadcol = customtkinter.CTkOptionMenu(self, values=["Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7", "Column 8", "Column 9", "Column 10", "Column 11", "Column 12", "Column 13", "Column 14", "Column 15", "Column 16"],command=padcolcall)
        self.typeselpadcol.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.typeselpadcol.set("Select a column")
        self.typeselpadcol.grid_remove()

        self.typeselknobid = customtkinter.CTkOptionMenu(self, values=["Knob 1","Knob 2","Knob 3", "Knob 4", "SELECT Knob"],command=knobselcall)
        self.typeselknobid.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.typeselknobid.set("Select a Knob")
        self.typeselknobid.grid_remove()

        self.typeselbuttonloc = customtkinter.CTkOptionMenu(self, values=["Top Buttons", "Bottom Buttons", "SOLO Buttons"],command=buttonloccall)
        self.typeselbuttonloc.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.typeselbuttonloc.set("Select a button location")
        self.typeselbuttonloc.grid_remove()
        
        self.typeselbuttontopid = customtkinter.CTkOptionMenu(self, values=["User Button", "Pattern Up", "Pattern Down", "Browser", "Grid Left", "Grid Right"],command=buttontopcall)
        self.typeselbuttontopid.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.typeselbuttontopid.set("Select a button")
        self.typeselbuttontopid.grid_remove()

        self.typeselbuttonbottomid = customtkinter.CTkOptionMenu(self, values=["Button 1", "Button 2", "Button 3", "Button 4", "Button 5", "Button 6", "Button 7", "Button 8", "Button 9", "Button 10"],command=buttonbottomcall)
        self.typeselbuttonbottomid.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.typeselbuttonbottomid.set("Select a button")
        self.typeselbuttonbottomid.grid_remove()

        self.typeselbuttonsoloid = customtkinter.CTkOptionMenu(self, values=["Solo 1", "Solo 2", "Solo 3", "Solo 4"],command=buttonsolocall)
        self.typeselbuttonsoloid.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        self.typeselbuttonsoloid.set("Select a button")
        self.typeselbuttonsoloid.grid_remove()

        self.actionselbutton = customtkinter.CTkOptionMenu(self, values=["Press"],state="disabled")
        self.actionselbutton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.actionselbutton.grid_remove()

        self.actionselknob = customtkinter.CTkOptionMenu(self, values=["Press","Left","Right"],command=actionselknobcall)
        self.actionselknob.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.actionselknob.set("Select an action")
        self.actionselknob.grid_remove()


        def effectselcall(choice):
            if choice == "Run command":
                self.runcommandbox.grid()
                self.runcommandbutton.grid()
            else:
                self.runcommandbox.grid_remove()
                self.runcommandbutton.grid_remove()
            if choice == "Simulate keypress":
                self.keypressrecbutton.grid()
                self.keypresspreview.grid()
            else:
                self.keypressrecbutton.grid_remove()
                self.keypresspreview.grid_remove()                
        self.effectsel = customtkinter.CTkOptionMenu(self, values=["Run command", "Simulate keypress"],command=effectselcall)
        self.effectsel.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.effectsel.set("Select an effect")
        self.effectsel.grid_remove()

        def savecommandcall():
            commandsaveto = self.runcommandbox.get()
            global currentsel
            global currentpressdir
            if currentsel == 16 or currentsel == 17 or currentsel == 18 or currentsel == 19 or currentsel == 118:
                if commandsaveto != "":
                    if currentsel != 0:
                        if currentpressdir != 0:
                            data["{}{}".format(currentsel,currentpressdir)] = ["cmd", commandsaveto]
                            with open('data.json', 'w') as json_file:
                                json.dump(data, json_file)             
            else:
                if commandsaveto != "":
                    if currentsel != 0:
                        data["%s" % currentsel] = ["cmd", commandsaveto]
                        with open('data.json', 'w') as json_file:
                            json.dump(data, json_file)
        self.runcommandbutton = customtkinter.CTkButton(self, text="Save Command",command=savecommandcall)
        self.runcommandbutton.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.runcommandbutton.grid_remove()

        self.runcommandboxvar = customtkinter.StringVar(value="None")
        self.runcommandbox = customtkinter.CTkEntry(self, placeholder_text="None",textvariable=self.runcommandboxvar)
        self.runcommandbox.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.runcommandbox.grid_remove()

        def setkeycall():
            selwind = customtkinter.CTk()
            selwind.title("Text selection")
            selwind.geometry("500x100")
            selwind.minsize(500,100)
            selwind.maxsize(500,100)
            def inputtf():
                inputtr = keyboard.read_key()
                global inputGc
                inputGc.append(inputtr)
                inputtext.configure(text="Record Key")
                inputGct = ("+".join(inputGc))
                keypreview.configure(text=inputGct)
            def reckeycall():
                inputtext.configure(text="Recording!")
                inputt = threading.Thread(target=inputtf)
                inputt.setDaemon(True)
                inputt.start()
            def resetkeycall():
                global inputGc
                inputGc = []
                keypreview.configure(text="None")
            def savebuttoncall():
                inputGct = ("+".join(inputGc))
                if currentsel == 16 or currentsel == 17 or currentsel == 18 or currentsel == 19 or currentsel == 118:
                    if inputGct == "":
                        if "{}{}".format(currentsel,currentpressdir) in data:
                            self.keypresspreview.configure(text="+".join(data["{}{}".format(currentsel,currentpressdir)]))
                        else:
                            self.keypresspreview.configure(text="None")
                    else:
                        if currentsel != 0:
                            if currentpressdir != 0:
                                data["{}{}".format(currentsel,currentpressdir)] = inputGc
                                with open('data.json', 'w') as json_file:
                                    json.dump(data, json_file)
                                self.keypresspreview.configure(text=inputGct)
                        else:
                            self.keypresspreview.configure(text="Select a Button!")
                else:
                    if inputGct == "":
                        if "%s" % currentsel in data:
                            self.keypresspreview.configure(text="+".join(data["%s" % currentsel ]))
                        else:
                            self.keypresspreview.configure(text="None")
                    else:
                        if currentsel != 0:
                            data["%s" % currentsel] = inputGc
                            with open('data.json', 'w') as json_file:
                                json.dump(data, json_file)
                            self.keypresspreview.configure(text=inputGct)
                        else:
                            self.keypresspreview.configure(text="Select a Button!")
                print(data)
                selwind.destroy()
            inputtext = customtkinter.CTkButton(selwind, text="Record Key",command=reckeycall)
            inputtext.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
            keypreview = customtkinter.CTkLabel(selwind, text="None", fg_color="transparent")
            keypreview.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
            inputtext2 = customtkinter.CTkButton(selwind, text="Reset Keys",command=resetkeycall)
            inputtext2.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
            savebutton = customtkinter.CTkButton(selwind, text="Save Key",command=savebuttoncall)
            savebutton.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
            selwind.mainloop()
        self.keypressrecbutton = customtkinter.CTkButton(self, text="Set Key",command=setkeycall)
        self.keypressrecbutton.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.keypressrecbutton.grid_remove()
        self.keypresspreview = customtkinter.CTkLabel(self, text="None", fg_color="transparent")
        self.keypresspreview.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        self.keypresspreview.grid_remove()
        

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fire Control")
        self.geometry("600x325")
        self.minsize(600,325)
        self.maxsize(600,325)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="Button Press Lighting")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="Rainbow Background Lighting")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        self.button = customtkinter.CTkButton(self, text="Apply and Restart", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        if data['lightup'] == "true":
            self.checkbox_1.select()
        if data['rainbow'] == "true":
            self.checkbox_2.select()
    def button_callback(self):
        if app.checkbox_1.get() == 1:
            data['lightup'] = "true"
        else:
            data['lightup'] = "false"
        if app.checkbox_2.get() == 1:
            data['rainbow'] = "true"
        else:
            data['rainbow'] = "false"
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
        os.execl(sys.executable, sys.executable, *sys.argv)
def close():
    app.destroy()
app = App()
app.protocol("WM_DELETE_WINDOW", close)
mainfire = threading.Thread(target=fire.main)
mainfire.setDaemon(True)
mainfire.start()
app.mainloop()