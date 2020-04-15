import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Res():
    SCALE_INIT = 0
    SCALE_LOWER = 0
    SCALE_UPPER = 255
    SCALE_INC = 1

class DevGUIWindow(Gtk.Window):
    def value_changed(self, widget, scoll, value):
        value = int(max(min(value, Res.SCALE_UPPER), Res.SCALE_LOWER))
        print(value)

    def __init__(self, title):
        Gtk.Window.__init__(self, title=title)

        self.box = Gtk.Box(spacing=10)
        self.add(self.box)

        self.scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL,          \
                               adjustment=Gtk.Adjustment(value=Res.SCALE_INIT,  \
                                                         lower=Res.SCALE_LOWER, \
                                                         upper=Res.SCALE_UPPER, \
                                                         step_increment=Res.SCALE_INC))

        self.scale.set_digits(0)
        self.box.pack_start(self.scale, True, True, 0)
        self.set_default_size(512, 64)
        self.scale.connect("change-value", self.value_changed)

window = DevGUIWindow(title="Hello World")
window.show_all()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
