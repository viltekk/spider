import gi
import sys
import serial

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

port = ''
if len(sys.argv) == 2:
    port = sys.argv[1]
else:
    port = '/dev/ttyUSB0'

class Res():
    SCALE_INIT = 90
    SCALE_LOWER = 0
    SCALE_UPPER = 180
    SCALE_INC = 1

    ARDU_PORT = port
    ARDU_BAUDRATE = 9600
    ARDU_TIMEOUT = 1

class DevGUIWindow(Gtk.Window):
    def serwr(self, s, v):
        s    = max(min(2, s), 0)
        s    = int(s)
        v    = int(max(min(v, Res.SCALE_UPPER), Res.SCALE_LOWER))
        byte = v.to_bytes(1, byteorder='little')
        
        self.serial.write(s.to_bytes(1, byteorder='little'))
        self.serial.write(byte)
    
    def value_changed0(self, widget, scoll, value):
        self.serwr(0, value)

    def value_changed1(self, widget, scoll, value):
        self.serwr(1, value)

    def value_changed2(self, widget, scoll, value):
        self.serwr(2, value)

    def clicked(self, widget):
        self.serwr(0, 90)
        self.serwr(1, 90)
        self.serwr(2, 90)

    def quit(self, widget):
        self.clicked(0)
        Gtk.main_quit(widget)
        
    def __init__(self, title):
        Gtk.Window.__init__(self, title=title)
        
        self.serial = serial.Serial(port=Res.ARDU_PORT,         \
                                    baudrate=Res.ARDU_BAUDRATE, \
                                    timeout=Res.ARDU_TIMEOUT,   \
                                    bytesize=serial.EIGHTBITS)
        self.box = Gtk.Box(spacing=10)
        self.add(self.box)        

        self.scale0 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,          \
                                adjustment=Gtk.Adjustment(value=Res.SCALE_INIT,  \
                                                          lower=Res.SCALE_LOWER, \
                                                          upper=Res.SCALE_UPPER, \
                                                          step_increment=Res.SCALE_INC))
        self.scale0.set_digits(0)
        self.scale0.connect("change-value", self.value_changed0)
        
        self.scale1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,          \
                                adjustment=Gtk.Adjustment(value=Res.SCALE_INIT,  \
                                                          lower=Res.SCALE_LOWER, \
                                                          upper=Res.SCALE_UPPER, \
                                                          step_increment=Res.SCALE_INC))
        self.scale1.set_digits(0)
        self.scale1.connect("change-value", self.value_changed1)
        
        self.scale2 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,          \
                                adjustment=Gtk.Adjustment(value=Res.SCALE_INIT,  \
                                                          lower=Res.SCALE_LOWER, \
                                                          upper=Res.SCALE_UPPER, \
                                                          step_increment=Res.SCALE_INC))
        self.scale2.set_digits(0)
        self.scale2.connect("change-value", self.value_changed2)

        self.btn = Gtk.Button.new_with_label("dance")
        self.btn.connect("clicked", self.clicked)
        
        self.box.pack_start(self.scale0, True, True, 0)
        self.box.pack_start(self.scale1, True, True, 0)
        self.box.pack_start(self.scale2, True, True, 0)
        self.box.pack_start(self.btn   , True, True, 0)
        
        self.set_default_size(512, 64)

window = DevGUIWindow(title="Spider GUI")
window.show_all()
window.connect("destroy", window.quit)
Gtk.main()
