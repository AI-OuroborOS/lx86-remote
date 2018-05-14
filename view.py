""" Simple python classe to represent the view of MVC
Author : Julien Ithurbide
Compagny : CPNV
VERSION : 0.1
LAST Modification :

Date       | Exp.
-----------|------------------------------------
18.01.2018 | First version
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango



class View(Gtk.Window):

    def __init__(self, **kw):
        Gtk.Window.__init__(self, title="Hello World")


        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(False)
        self.header_bar.props.title = "HeaderBar example"
        self.set_titlebar(self.header_bar)

        self.bt_power_off = Gtk.Button.new_from_icon_name("process-stop", Gtk.IconSize.BUTTON)
        self.header_bar.pack_start(self.bt_power_off)

        self.bt_close = Gtk.Button.new_from_icon_name("window-close", Gtk.IconSize.BUTTON)
        self.bt_close.connect("clicked", self.on_close)
        self.header_bar.pack_end(self.bt_close)


        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.box = Gtk.Box(spacing=6)
        self.grid.add(self.box)

        self.button1 = Gtk.Button(label="Button 1")
        self.box.pack_start(self.button1, True, True, 0)
        self.button2 = Gtk.Button(label="Button 2")
        self.box.pack_start(self.button2, True, True, 0)
        self.button3 = Gtk.Button(label="Button 3")
        self.box.pack_start(self.button3, True, True, 0)



        self.label = Gtk.TextView()
        self.grid.attach(self.label,0,1,1,1)


        self.show_all()



    def on_close(self,widget):
        Gtk.main_quit()

    def getLogger(self):
        return self.logger

    def _quit(self, button, *args):
        Gtk.main_quit()


