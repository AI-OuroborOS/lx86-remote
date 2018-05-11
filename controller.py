""" Simple python classe to represent the controller of MVC
https://bitbucket.org/NGY_CPNV/teacherplanner
Author : Julien Ithurbide
Compagny : CPNV
VERSION : 0.1
LAST Modification :

Date       | Exp.
-----------|------------------------------------
07.02.2017 | First version
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from view import View
from log import Log
import telnetlib
from zeroconf import ServiceBrowser, Zeroconf
import socket
import sys
from discovery import Discovery


class Handler:
    def __init__(self,log,*args):
        self.logger = log

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self,*args):
        print("Hello World!")

    def onPowerOff(self,*args):
        self.logger.debug("Hello World!")

    def onConnect(self,*args):
        HOST = "towel.blinkenlights.nl"
        tn = telnetlib.Telnet(HOST)
        all = tn.read_all()
        self.logger.debug(all)
        self.logger.debug("test 111")

    def onParameters(self,*args):
        self.logger.debug("Hello World!")

    def onParameters(self,*args):
        self.logger.debug("Hello World!")

    def onClose(self,*args):
        Gtk.main_quit()

    def onVolume(self,*args):
        self.logger.debug("clicked powervol")

    def onVolValChange(self,value,*args):
        self.logger.debug("new value :" + str(value.get_value()))


class Controller:

    def __init__(self):

        self._view = View()
        label = self._view.builder.get_object("txtBuffer")
        buffer = label.get_buffer()
        self.logger = Log(label).get_logger()
        self._view.builder.connect_signals(Handler(self.logger))
        self.logger.debug("Controller is starting")
        self.logger.debug("Controller start database")
        self.logger.debug("Controller start view")
        self.logger.debug("View is starting")

        zeroconf = Zeroconf()
        listener = Discovery(self.logger)
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
        listener.connect('ampli-found',self.found)
    def found(self,str):
        self.logger.debug("Found "+str)
    def __del__(self):
        self.newClass = None
        self.database = None
        self.menu = None

