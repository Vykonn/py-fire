from rtmidi import (API_LINUX_ALSA, API_MACOSX_CORE, API_RTMIDI_DUMMY,
                    API_UNIX_JACK, API_WINDOWS_MM, MidiIn, MidiOut,
                    get_compiled_api)
from rtmidi.midiutil import open_midioutput, open_midiinput
import time
import sys
import threading
import communicate
import os
global message
message = [0, 0, 0]
global onp
global onpb
global stop
global lightupon
global oncircle
global colorid
global commandrrc
commandrrc = ""
colorid = "00"
oncircle = []
onpb = []
onp = []
stop = True
lightupon = False
all_processes = []
def commandr():
    os.system(commandrrc)
def main():
    global stop
    class MidiInputHandler(object):
        def __init__(self, port):
            self.port = port
            self._wallclock = time.time()

        def __call__(self, event, data=None):
            global message
            message, deltatime = event
            self._wallclock += deltatime
            commandrr = communicate.handleinput(message)
            global commandrrc
            commandrrc = "{}".format(commandrr)
            if commandrr != False:
                commandrv = threading.Thread(target=commandr)
                commandrv.dameon = True
                commandrv.start()
            if lightupon:
                if message[1] in range(54, 118):
                    global onp
                    if message[2] in range(1,127):
                        drawpad(message[1]-54,[127,127,127])
                        onp.append(message[1]-54)
                    else:
                        onp.remove(message[1]-54)
                if message[1] in range(44, 54):
                    global onpb
                    if message[2] == 127:
                        if len('{0:x}'.format(message[1])) == 1:
                            lr = ("0"+'{0:x}'.format(message[1]))
                        else:
                            lr = ('{0:x}'.format(message[1]))
                        permadisplay = bytearray.fromhex("B0 %s 02" % lr)
                        midiout.send_message(permadisplay)
                        onpb.append(message[1])
                    else:
                        if len('{0:x}'.format(message[1])) == 1:
                            lr = ("0"+'{0:x}'.format(message[1]))
                        else:
                            lr = ('{0:x}'.format(message[1]))
                        permadisplay = bytearray.fromhex("B0 %s 00" % lr)
                        midiout.send_message(permadisplay)
                        onpb.remove(message[1])
                if message[1] in range(31, 36):
                    if len('{0:x}'.format(message[1])) == 1:
                        lrt = ("0"+'{0:x}'.format(message[1]))
                    else:
                        lrt = ('{0:x}'.format(message[1]))
                    if message[2] == 127:
                        lrtd = bytearray.fromhex("B0 %s 02" % lrt)
                        midiout.send_message(lrtd)
                        onpb.append(message[1])
                    else:
                        lrtd = bytearray.fromhex("B0 %s 00" % lrt)
                        midiout.send_message(lrtd)
                        onpb.remove(message[1])
    apis = {
        API_MACOSX_CORE: "macOS (OS X) CoreMIDI",
        API_LINUX_ALSA: "Linux ALSA",
        API_UNIX_JACK: "Jack Client",
        API_WINDOWS_MM: "Windows MultiMedia",
        API_RTMIDI_DUMMY: "RtMidi Dummy"
    }

    available_apis = get_compiled_api()

    for api, api_name in sorted(apis.items()):
        if api in available_apis:
            for name, class_ in (("input", MidiIn), ("output", MidiOut)):
                try:
                    midi = class_(api)
                    ports = midi.get_ports()
                except StandardError as exc:
                    print("Could not probe MIDI %s ports: %s" % (name, exc))
                    continue

                if not ports:
                    print("No MIDI %s ports found." % name)
                else:
                    test = name
                    for port, name in enumerate(ports):
                        if name == "FL STUDIO FIRE %s" % port:
                            if test == "output":
                                outmain = port
                            print("AKAI Fire Output found.")
                            if test == "input":
                                inmain = port
                                print("AKAI Fire Input found.")
                del midi

    def drawpad(pad, color):
        """Draws a color on the corresponding pad.

        Parameters:

        pad (int): Position of lighting, left-to-right, top-to-bottom.
        
        color (list): [R, G, B] values.
        """ 
        if len('{0:x}'.format(color[0])) == 1: r = ("0"+'{0:x}'.format(color[0]))
        else: r = ('{0:x}'.format(color[0]))

        if len('{0:x}'.format(color[1])) == 1: g = ("0"+'{0:x}'.format(color[1]))
        else: g = ('{0:x}'.format(color[1]))

        if len('{0:x}'.format(color[2])) == 1: b = ("0"+'{0:x}'.format(color[2]))
        else: b = ('{0:x}'.format(color[2]))

        if len('{0:x}'.format(pad)) == 1: padf = ("0"+'{0:x}'.format(pad))
        else: padf = ('{0:x}'.format(pad))
        data = bytearray.fromhex("F0 47 7F 43 65 00 04 {} {} {} {} F7".format(padf, r, g, b))
        if not pad in onp:
            midiout.send_message(data)
    lightreg = 43
    def rainbowbutton():
        lightreg = 43
        lr = "00"
        lrs = "00"
        lrstbo = "00"
        lrstb = "00"
        oi = 0
        global stop
        while stop:
            for i in range(44, 53):
                lightregold = lightreg
                lighttestold = bytearray.fromhex("B0 %s 00" % lr)
                lightreg = lightreg + 1
                if len('{0:x}'.format(lightreg)) == 1:
                    lr = ("0"+'{0:x}'.format(lightreg))
                else:
                    lr = ('{0:x}'.format(lightreg))
                if lightreg in range(44, 49) or lightreg == 53 or lightreg == 50:
                    lighttest = bytearray.fromhex("B0 %s 04" % lr)
                if lightreg == 49 or lightreg == 52:
                    lighttest = bytearray.fromhex("B0 %s 02" % lr)
                if lightreg == 51:
                    lighttest = bytearray.fromhex("B0 %s 04" % lr)
                if not lightregold in onpb:
                    midiout.send_message(lighttestold)
                if not lightreg in onpb:
                    midiout.send_message(lighttest)
                time.sleep(0.1)
            lightreg = 53
            for i in reversed(range(44, 53)):
                lightregold = lightreg
                lighttestold = bytearray.fromhex("B0 %s 00" % lr)
                lightreg = lightreg - 1
                if len('{0:x}'.format(lightreg)) == 1:
                    lr = ("0"+'{0:x}'.format(lightreg))
                else:
                    lr = ('{0:x}'.format(lightreg))
                if lightreg in range(44, 49) or lightreg == 53 or lightreg == 50:
                    lighttest = bytearray.fromhex("B0 %s 04" % lr)
                if lightreg == 49 or lightreg == 52:
                    lighttest = bytearray.fromhex("B0 %s 02" % lr)
                if lightreg == 51:
                    lighttest = bytearray.fromhex("B0 %s 04" % lr)
                if not lightregold in onpb:
                    midiout.send_message(lighttestold)
                if not lightreg in onpb:
                    midiout.send_message(lighttest)
                time.sleep(0.1)
            if not 44 in onpb:
                midiout.send_message(bytearray.fromhex("B0 2C 00"))
            for i in reversed(range(40, 44)):
                lrso = lrs
                if len('{0:x}'.format(i)) == 1:
                    lrs = ("0"+'{0:x}'.format(i))
                else:
                    lrs = ('{0:x}'.format(i))
                midiout.send_message(bytearray.fromhex("B0 %s 00" % lrso))
                midiout.send_message(bytearray.fromhex("B0 %s 03" % lrs))
                time.sleep(0.1)
            midiout.send_message(bytearray.fromhex("B0 28 00"))
            for i in reversed(range(0,4)):
                midiout.send_message(bytearray.fromhex("B0 1B 0%s" % i))
                time.sleep(0.1)
            midiout.send_message(bytearray.fromhex("B0 1B 10"))
            for i in range(31, 36):
                lrstbo = lrstb
                if len('{0:x}'.format(i)) == 1:
                    lrstb = ("0"+'{0:x}'.format(i))
                else:
                    lrstb = ('{0:x}'.format(i))
                if not oi in onpb:
                    midiout.send_message(bytearray.fromhex("B0 %s 00" % lrstbo))
                if not i in onpb:
                    midiout.send_message(bytearray.fromhex("B0 %s 02" % lrstb))
                oi = i
                time.sleep(0.1)
            for i in reversed(range(31, 35)):
                lrstbo = lrstb
                if len('{0:x}'.format(i)) == 1:
                    lrstb = ("0"+'{0:x}'.format(i))
                else:
                    lrstb = ('{0:x}'.format(i))
                if not oi in onpb:
                    midiout.send_message(bytearray.fromhex("B0 %s 00" % lrstbo))
                if not i in onpb:
                    midiout.send_message(bytearray.fromhex("B0 %s 02" % lrstb))
                oi = i
                time.sleep(0.1)
            if not 31 in onpb:
                midiout.send_message(bytearray.fromhex("B0 1F 00"))
            for i in range(1,4):
                midiout.send_message(bytearray.fromhex("B0 1B 0%s" % i))
                time.sleep(0.1)
            midiout.send_message(bytearray.fromhex("B0 1B 10"))
            for i in range(40, 44):
                lrso = lrs
                if len('{0:x}'.format(i)) == 1:
                    lrs = ("0"+'{0:x}'.format(i))
                else:
                    lrs = ('{0:x}'.format(i))
                midiout.send_message(bytearray.fromhex("B0 %s 00" % lrso))
                midiout.send_message(bytearray.fromhex("B0 %s 03" % lrs))
                time.sleep(0.1)
            midiout.send_message(bytearray.fromhex("B0 2B 00")) 
    def rainbow():
        """Displays a rainbow forever. 
        """
        
        rainbowbuttone = threading.Thread(target=rainbowbutton)
        rainbowbuttone.setDaemon(True)
        rainbowbuttone.start()
        midiout.send_message(bytearray.fromhex("B0 1F 00"))
        midiout.send_message(bytearray.fromhex("B0 20 00"))
        midiout.send_message(bytearray.fromhex("B0 21 00"))
        midiout.send_message(bytearray.fromhex("B0 22 00"))
        midiout.send_message(bytearray.fromhex("B0 23 00"))
        a = {}
        lightreg = 43
        lr = "00"
        for i in range(2, 65):
            a[i] = [0, 0, 0]
        while True:
            for i in range(0, 64):
                swap = i*2
                currentcol = [0, 127-swap, swap]
                a[1] = currentcol
                for i in reversed(range(2, 65)):
                    a[i] = a[i-1]
                for i in range(1, 65):
                    p = i-1
                    drawpad(p, a[i])
                time.sleep(0.05)
            for i in range(0, 64):
                swap = i*2
                currentcol = [swap, 0, 127-swap]
                a[1] = currentcol
                for i in reversed(range(2, 65)):
                    a[i] = a[i-1]
                for i in range(1, 65):
                    p = i-1
                    drawpad(p, a[i])
                time.sleep(0.05)
            for i in range(0, 64):
                swap = i*2
                currentcol = [127-swap, swap, 0]
                a[1] = currentcol
                for i in reversed(range(2, 65)):
                    a[i] = a[i-1]
                for i in range(1, 65):
                    p = i-1
                    drawpad(p, a[i])
                time.sleep(0.05)  
    def plain():
        while True:
            for i in range(0, 64):
                drawpad(i, [0,0,0])
            time.sleep(0.05)
    def drawextra(id, color):
        """Draws one of the external lights (Buttons, Rectangle, Circle, etc.)

        Parameters:

        id (int): ID of light to display, bottom right-to-left, bottom left-to-up, top left-to-right.
        More info: 1-10: Bottom buttons, right-to-left.     11-14: SOLO buttons, bottom-to-top 
        More info (ctd.): 15-19: Rectangle lights, bottom-to-top.   20-23: Circular buttons, Bottom to top
        More info (ctd.): 24-28: Top buttons, left-to-right.

        color: Color in text form, "red", "green", "yellow", "off". A "d" in front of the color means dim, e.g "dred"
        More info: Not all lights support all colors. 
        Color Chart:
        Red-Only: PAT BACK, PAT NEXT, BROWSER, GRID LEFT, GRID RIGHT, CIRCULAR BUTTONS
        Green-Only: SOLO BUTTONS
        Yellow-only: ALT, STOP
        Yellow-red: STEP, NOTE, DRUM, PERFORM, SHIFT, LOOP REC
        Yellow-green: PATTERN, PLAY
        """
        colorid = "00"
        circlerun = False
        firstindex = 0
        for i in reversed(range(1,11)):
            firstindex = firstindex + 1
            if firstindex == id:
                id = i + 43
        if id == 11: id = 39
        if id == 12: id = 38
        if id == 13: id = 37
        if id == 14: id = 36
        if id in range(15,20): id = id + 25
        if id in range(20, 24): 
            id = id - 20
            circlerun = True
        if id in range(24,29): id = id + 7
        print(id)
        if circlerun:
            if color == "red": oncircle.append(id)
            if color == "off": oncircle.remove(id)
            midiout.send_message(bytearray.fromhex("B0 1B 10"))
            for currentrespond in oncircle: 
                if len('{0:x}'.format(id)) == 1: showid = ("0"+'{0:x}'.format(currentrespond))
                else: showid = ('{0:x}'.format(currentrespond))    
                print(currentrespond)
                midiout.send_message(bytearray.fromhex("B0 1B {}".format(showid)))
        else:
            if len('{0:x}'.format(id)) == 1: showid = ("0"+'{0:x}'.format(id))
            else: showid = ('{0:x}'.format(id))           
            if color == "red": 
                if id in range(31, 36): colorid = "02"
                if id in range(44, 49) or id == 53: colorid = "03"
            if color == "dred": 
                if id in range(31, 36): colorid = "01"
                if id in range(44, 49) or id == 53: colorid = "01"
            if color == "green":
                if id in range(36,40): colorid = "02"
                if id in range(50, 52): colorid = "03"
            if color == "dgreen":
                if id in range(36,40): colorid = "01"
                if id in range(50,52): colorid = "01"
            if color == "yellow":
                if id == 49 or id == 51: colorid = "04"
            if color == "dyellow":
                if id == 49 or id == 51: colorid = "02"
            if color == "off": colorid = "00"
            midiout.send_message(bytearray.fromhex("B0 {} {}".format(showid, colorid)))  
    def clear():
        for i in range(0, 64):
            drawpad(i, [0,0,0])
        midiout.send_message(bytearray.fromhex("B0 1F 00"))
        midiout.send_message(bytearray.fromhex("B0 20 00"))
        midiout.send_message(bytearray.fromhex("B0 21 00"))
        midiout.send_message(bytearray.fromhex("B0 22 00"))
        midiout.send_message(bytearray.fromhex("B0 23 00"))
        midiout.send_message(bytearray.fromhex("B0 1B 10"))
        midiout.send_message(bytearray.fromhex("B0 1F 00"))
        midiout.send_message(bytearray.fromhex("B0 20 00"))
        midiout.send_message(bytearray.fromhex("B0 21 00"))
        midiout.send_message(bytearray.fromhex("B0 22 00"))
        midiout.send_message(bytearray.fromhex("B0 23 00"))
        midiout.send_message(bytearray.fromhex("B0 24 00"))
        for i in range(40, 53):
            if len('{0:x}'.format(i)) == 1:
                clearid = ("0"+'{0:x}'.format(i))
            else:
                clearid = ('{0:x}'.format(i))
            midiout.send_message(bytearray.fromhex("B0 %s 00" % clearid))
    def lightup():
        global lightupon
        lightupon = True
    if not inmain is None:
        midiin, port_name = open_midiinput(inmain)
        midiin.set_callback(MidiInputHandler(port_name))   
    if not outmain is None:
        midiout, port_name = open_midioutput(outmain)
        while stop:
            if __name__ == "__main__":
                text = input("Run:")
                exec(text)
            else:
                execm = communicate.main()
                for run in range(1, len(execm)):
                    exec(execm[run])
        print("Waiting for loop to shutdown...")
        stop = False
        midiin.close_port()
        del midiin
        sys.exit()    

if __name__ == "__main__":
    main()