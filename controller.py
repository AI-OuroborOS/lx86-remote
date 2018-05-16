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
from ampli import Amplifier
import socket


class Controller:
    def __init__(self):

        self.address_ip = None
        self._view = View()
        self._view.connect("destroy", Gtk.main_quit)
        self._view.bt_audio_select.connect("clicked", self.on_audio_click)
        self._view.bt_output_selection.connect("clicked", self.on_output_click)
        self._view.bt_vol_up.connect("clicked", self.on_vol_up_click)
        self._view.bt_vol_down.connect("clicked", self.on_vol_down_click)
        self._view.bt_dvd.connect("clicked",self.on_dvd_select)
        self._view.bt_bray.connect("clicked", self.on_bray_select)
        self._view.bt_dvr.connect("clicked", self.on_dvr_select)
        self._view.bt_hdmi1.connect("clicked", self.on_hdmi1_select)
        self._view.bt_hdmi2.connect("clicked", self.on_hdmi2_select)
        self._view.bt_hdmi3.connect("clicked", self.on_hdmi3_select)

        self.logger = Log(self._view.label).get_logger()

        self.tn = None
        self.connected = False
        self.needToRun = True

        self.logger.debug("Controller is starting")

        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.semaphore = True
        self.address = None
        self.ampli = Amplifier(self.logger)
        self.central_buffer = self._view.label2.get_buffer()
        self.start_discover()

    def on_hdmi1_select(self, bt):
        self.ampli.set_output("HDMI1")

    def on_hdmi2_select(self, bt):
        self.ampli.set_output("HDMI2")

    def on_hdmi3_select(self, bt):
        self.ampli.set_output("HDMI3")

    def on_bray_select(self, bt):
        self.ampli.set_output("BD")

    def on_dvd_select(self, bt):
        self.ampli.set_output("DVD")

    def on_dvr_select(self, bt):
        self.ampli.set_output("DVR")

    def on_audio_click(self,button):
        self._view.popover_audio.set_relative_to(button)
        self._view.popover_audio.show_all()
        self._view.popover_audio.popup()

    def on_output_click(self,button):
        self._view.popover_outpup.set_relative_to(button)
        self._view.popover_outpup.show_all()
        self._view.popover_outpup.popup()

    def on_vol_up_click(self, bt):
        self.ampli.set_volume_down()
        self.get_volume()

    def on_vol_down_click(self, bt):
        self.ampli.set_volume_down()
        self.get_volume()

    def value_changed(self, volumebutton, value):
        self.logger.debug("From controller volume change detected : " + str(value))

    def on_service_state_change(self,zeroconf, service_type, name, state_change):

        if state_change is ServiceStateChange.Added:
            if (name == "SC-LX86._http._tcp.local."):
                self.logger.debug("From controller find IP of amplifier")
                info = zeroconf.get_service_info(service_type, name)
                if info.address is not None:
                    self.address_ip = socket.inet_ntoa(info.address)
                    self.logger.debug("Found at " + self.address_ip)
                    self._view.header_bar.set_subtitle(self.address_ip)
                    self.ampli.set_ip(self.address_ip)
                    self.ampli.connect()
                    self.connected = True
                zeroconf.close()

    def get_volume(self):
        self.semaphore = False
        self.logger.debug("From controller starting getvolume")
        volume = self.ampli.get_volume()
        self.logger.debug("From controller volume is : " + str(volume))
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
        self.ampli.close()
        self.logger = None
        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.buffer = None
        self.label = None


