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
        self.builder = Gtk.Builder()
        self.builder.add_from_file("mainWin.glade")
        window = self.builder.get_object("mainWin")

        window.maximize()
        window.show_all()

    def getLogger(self):
        return self.logger

    def _quit(self, button, *args):
        Gtk.main_quit()

    def _clear(self, button, *args):
        self.emit('button-clear-notes')

