from rtmidi import (API_LINUX_ALSA, API_MACOSX_CORE, API_RTMIDI_DUMMY,
                    API_UNIX_JACK, API_WINDOWS_MM, MidiIn, MidiOut,
                    get_compiled_api)
from rtmidi.midiutil import open_midioutput, open_midiinput
import time
import sys
global message
message = [0, 0, 0]
global onp
global onpb
onpb = []
onp = []
class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        global message
        message, deltatime = event
        self._wallclock += deltatime
        if message[1] in range(54, 118):
            global onp
            if message[2] in range(1,127):
                drawpad(message[1]-54,[127,127,127])
                onp.append(message[1]-54)
            else:
                onp.remove(message[1]-54)
        if message[1] in range(44, 53):
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
            else:
                lrtd = bytearray.fromhex("B0 %s 00" % lrt)
                midiout.send_message(lrtd)
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
    if len('{0:x}'.format(color[0])) == 1:
        r = ("0"+'{0:x}'.format(color[0]))
    else:
        r = ('{0:x}'.format(color[0]))

    if len('{0:x}'.format(color[1])) == 1:
        g = ("0"+'{0:x}'.format(color[1]))
    else:
        g = ('{0:x}'.format(color[1]))

    if len('{0:x}'.format(color[2])) == 1:
        b = ("0"+'{0:x}'.format(color[2]))
    else:
        b = ('{0:x}'.format(color[2]))

    if len('{0:x}'.format(pad)) == 1:
        padf = ("0"+'{0:x}'.format(pad))
    else:
        padf = ('{0:x}'.format(pad))
    data = bytearray.fromhex("F0 47 7F 43 65 00 04 {} {} {} {} F7".format(padf, r, g, b))
    if not pad in onp:
        midiout.send_message(data)
lightreg = 43
def rainbow():
    """Displays a rainbow forever. 
    """
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

            lightregold = lightreg
            lighttestold = bytearray.fromhex("B0 %s 00" % lr)
            lightreg = lightreg + 1
            if lightreg == 54:
                lightreg = 44
            if len('{0:x}'.format(lightreg)) == 1:
                lr = ("0"+'{0:x}'.format(lightreg))
            else:
                lr = ('{0:x}'.format(lightreg))
            lighttest = bytearray.fromhex("B0 %s 02" % lr)
            if not lightregold in onpb:
                midiout.send_message(lighttestold)
            if not lightreg in onpb:
                midiout.send_message(lighttest)

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

            lighttestold = bytearray.fromhex("B0 %s 00" % lr)
            lightreg = lightreg + 1
            if lightreg == 54:
                lightreg = 44
            if len('{0:x}'.format(lightreg)) == 1:
                lr = ("0"+'{0:x}'.format(lightreg))
            else:
                lr = ('{0:x}'.format(lightreg))
            lighttest = bytearray.fromhex("B0 %s 02" % lr)
            if not lighttestold in onpb:
                midiout.send_message(lighttestold)
            if not lighttest in onpb:
                midiout.send_message(lighttest)       

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

            lighttestold = bytearray.fromhex("B0 %s 00" % lr)
            lightreg = lightreg + 1
            if lightreg == 54:
                lightreg = 44
            if len('{0:x}'.format(lightreg)) == 1:
                lr = ("0"+'{0:x}'.format(lightreg))
            else:
                lr = ('{0:x}'.format(lightreg))
            lighttest = bytearray.fromhex("B0 %s 02" % lr)
            if not lighttestold in onpb:
                midiout.send_message(lighttestold)
            if not lighttest in onpb:
                midiout.send_message(lighttest)

            time.sleep(0.05)  
def plain():
    while True:
        for i in range(0, 64):
            drawpad(i, [0,0,0])
        time.sleep(0.05)
def clear():
    for i in range(0, 64):
        drawpad(i, [0,0,0])
    midiout.send_message(bytearray.fromhex("B0 1F 00"))
    midiout.send_message(bytearray.fromhex("B0 20 00"))
    midiout.send_message(bytearray.fromhex("B0 21 00"))
    midiout.send_message(bytearray.fromhex("B0 22 00"))
    midiout.send_message(bytearray.fromhex("B0 23 00"))
    for i in range(44, 53):
        if len('{0:x}'.format(i)) == 1:
            clearid = ("0"+'{0:x}'.format(i))
        else:
            clearid = ('{0:x}'.format(i))
        midiout.send_message(bytearray.fromhex("B0 %s 00" % clearid))
if not inmain is None:
    midiin, port_name = open_midiinput(inmain)
    midiin.set_callback(MidiInputHandler(port_name))   
if not outmain is None:
    midiout, port_name = open_midioutput(outmain)
    clear()
    plain()
    
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin