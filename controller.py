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
from zeroconf import ServiceBrowser, Zeroconf,ServiceStateChange
from volume import Volume
import socket
import time
from threading import Timer


class Handler:
    def __init__(self,log,controller,*args):
        self.logger = log
        self.ctrl = controller

    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self,*args):
        print("Hello World!")

    def onPowerOff(self,*args):
        self.logger.debug("Hello World!")


    def onParameters(self,*args):
        self.logger.debug("From parameters start getvolume")
        self.ctrl.getVolume()


    def onClose(self,*args):
        Gtk.main_quit()

    def onVolume(self,*args):
        self.logger.debug("clicked powervol")

    def onVolValChange(self,value,*args):
        self.logger.debug("From controller handler new volume set :" + str(value.get_value()))
        if self.ctrl.connected and self.ctrl.semaphore:
            self.ctrl.semaphore = False
            self.ctrl.vol.setVolume(value.get_value()*100)
            self.ctrl.semaphore = True
    def onPopDown(self):
        pass

    def onPopUp(self):
        pass

class Controller:
    def __init__(self):

        self.address_ip = None
        self._view = View()
        self._view.connect("destroy", Gtk.main_quit)

        self.logger = Log(self._view.label).get_logger()

        self.tn = None
        self.connected = False
        self.needToRun = True

        self.logger.debug("Controller start database")
        self.logger.debug("Controller start view")
        self.logger.debug("View is starting")
        self.logger.debug("Controller is starting")

        #self._view.btVolume.connect("value-changed", self.value_changed)


        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.semaphore = True
        self.start_discover()

    def value_changed(self, volumebutton, value):
        self.logger.debug("From controller volume change detected : " + str(value))

    def on_service_state_change(self,zeroconf, service_type, name, state_change):

        if state_change is ServiceStateChange.Added:
            if (name == "SC-LX86._http._tcp.local."):
                info = zeroconf.get_service_info(service_type, name)
                if info.address is not None :
                    self.address = socket.inet_ntoa(info.address)
                    self.logger.debug("Found at " + self.address)
                    self.address_ip = self.address
                    self._view.header.set_subtitle(self.address_ip)
                    self.vol.setIP(self.address_ip)
                    self.connected = True
                zeroconf.close()

    def getVolume(self):
        self.semaphore = False
        self.logger.debug("From controller starting getvolume")
        volume = self.vol.getVolume()
        realValue = volume /100.0
        self.logger.debug("From controller volume will be set to " +str(realValue))
        self._view.btVolume.set_value(realValue)
        self.semaphore = True

    def start_discover(self):
        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.",  handlers=[self.on_service_state_change])


    def error(self,arg):
        self.logger.debug("From controller error found on discovery")
        self.browser.cancel()
        self.zeroconf.close()
        self.logger.debug("From controller restart zeroconf")
        self.start_discover()

    def found(self,arg,ip):
        self.logger.debug("From controller Found "+str(ip))
        self.address_ip = ip
        self.header.set_subtitle = 'Found'

    def __del__(self):
        self.logger = None
        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.buffer = None
        self.label = None


