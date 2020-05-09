import gi
import sys
import serial
import threading
import time
import numpy

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

port = ''
if len(sys.argv) == 2:
    port = sys.argv[1]
else:
    port = '/dev/ttyUSB0'

class Res():
    """ milliseconds """
    SCALE_INIT = 300.0
    SCALE_LOWER = 300.0
    SCALE_UPPER = 5000.0
    SCALE_INC = 15.0

    TIBIA = 0
    FEMUR = 1
    COXA  = 2

    ARDU_PORT = port
    ARDU_BAUDRATE = 9600
    ARDU_TIMEOUT = 1

class DevGUIWindow(Gtk.Window):
    def serwr(self, s, v, slp):
        s    = max(min(2, s), 0)
        s    = int(s)
        v    = int(v)
        byte = v.to_bytes(1, byteorder='little')
        
        self.serial.write(s.to_bytes(1, byteorder='little'))
        self.serial.write(byte)

        time.sleep(slp)

    def dance_thread(self):
        v0 = 0
        v1 = 0
        v2 = 0

        """ create list of values """
        inc  = 180.0 / (self.scale.get_value() / Res.SCALE_INC)

        lst_femur = list(numpy.arange(0, 180, inc*2))
        lst_tibia = list(reversed(lst_femur))
        lst_femur = lst_femur + list(reversed(lst_femur))
        lst_tibia = lst_tibia + list(reversed(lst_tibia))
        lst_coxa  = numpy.arange(0, 180, inc)

        lst  = numpy.arange(0, 180, inc)
        rlst = list(reversed(lst))
        slp  = Res.SCALE_INC/1000.0
        

        print(lst_femur) ; print("")
        print(lst_tibia) ; print("")
        print(lst_coxa ) ; print("")

        print(len(lst_femur))
        print(len(lst_tibia))
        print(len(lst_coxa))
        
        while self.dancing == True:
            for i in range(len(lst_coxa)):
                if self.dancing == False:
                    return
                self.serwr(Res.FEMUR, lst_coxa[i], slp)
                self.serwr(Res.TIBIA, lst_tibia[i], slp)
                #self.serwr(Res.COXA , lst_coxa[i] , slp)
            for i in range(len(lst_coxa)-1, -1, -1):
                if self.dancing == False:
                    return
                self.serwr(Res.FEMUR, lst_femur[i], slp)
                self.serwr(Res.TIBIA, lst_tibia[i], slp)
                #self.serwr(Res.COXA , lst_coxa[i] , slp)

    def clicked(self, widget):
        if self.dancing == False:
            self.dancing = True
            self.thr = threading.Thread(target = self.dance_thread)
            self.thr.start()
        else:
            self.dancing = False
            self.thr.join()
            self.serwr(Res.TIBIA, 90.0, 0.015)
            self.serwr(Res.FEMUR, 90.0, 0.015)
            #self.serwr(Res.COXA , 90.0, 0.015)
            print("stopped dancing")
            
    def __init__(self, title):
        """ create window and set title """
        Gtk.Window.__init__(self, title=title)

        """ open up serial port for communication with arduino """
        self.serial = serial.Serial(port=Res.ARDU_PORT,         \
                                    baudrate=Res.ARDU_BAUDRATE, \
                                    timeout=Res.ARDU_TIMEOUT,   \
                                    bytesize=serial.EIGHTBITS)

        """ add a box to GUI """
        self.box = Gtk.Box(spacing=10)
        self.add(self.box)

        """ add a button that enables dancing when clicked """
        self.dancing = False
        self.btn = Gtk.Button.new_with_label("dance")
        self.btn.connect("clicked", self.clicked)

        """ create a scale widget to set speed of dancing """
        self.scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,          \
                               adjustment=Gtk.Adjustment(value=Res.SCALE_INIT,  \
                                                         lower=Res.SCALE_LOWER, \
                                                         upper=Res.SCALE_UPPER, \
                                                         step_increment=Res.SCALE_INC))
        self.scale.set_digits(0)

        """ finishing GUI touches """
        self.box.pack_start(self.scale, True, True, 0)
        self.box.pack_start(self.btn  , True, True, 0)        
        self.set_default_size(512, 64)

window = DevGUIWindow(title="Spider GUI")
window.show_all()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
