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
from gi.repository import Gtk, GObject
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

        self.address_ip = None
        self._view = View()
        self.label = self._view.builder.get_object("txtBuffer")
        self.connect_bt = self._view.builder.get_object("btConnect")
        self.buffer = self.label.get_buffer()
        self.logger = Log(self.label).get_logger()
        self._view.builder.connect_signals(Handler(self.logger))
        self.logger.debug("Controller is starting")
        self.logger.debug("Controller start database")
        self.logger.debug("Controller start view")
        self.logger.debug("View is starting")
        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.connect_bt.visible = False
        self.start_discover()

    def start_discover(self):
        self.zeroconf = Zeroconf()
        self.listener = Discovery(self.logger)
        self.browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.", self.listener)
        self.listener.connect('ampli-found', self.found)
        self.listener.connect('error-found', self.error)

    def error(self,arg):
        self.logger.debug("From controller error found on discovery")
        self.browser.cancel()
        self.zeroconf.close()
        self.logger.debug("From controller restart zeroconf")
        self.start_discover()

    def found(self,input,ip):
        self.logger.debug("From controller Found "+str(ip))
        self.address_ip = ip
        self.connect_bt.visible = True

    def __del__(self):
        self.logger = None
        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.buffer = None
        self.label = None


