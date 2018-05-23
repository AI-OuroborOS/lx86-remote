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
from ampli import Amplifier
from config import Config
from wiz import Assistant


class Controller:
    def __init__(self):

        self.address_ip = None
        self.tn = None
        self.connected = False
        self.needToRun = True
        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.semaphore = True
        self.address = None
        self._view = None
        self.ampli = None
        self.central_buffer = None
        self.assistant = None
        self.log = Log()
        self.logger = self.log.get_logger()
        self.config = Config(self.logger)
        if self.config.check_config():
            self.start_view()
            self.log.set_view_label(self._view.label)
        else:
            self.start_wiz()

        self.logger.debug("Controller is starting")

    def start_wiz(self):
        self.assistant = Assistant()
        self.assistant.show_all()
        self.assistant.connect("close", self.on_close_clicked)

    def start_view(self):
        self._view = View()
        self._view.bt_wiz.connect("clicked",self.on_wiz_clicked)
        self._view.bt_audio_select.connect("clicked", self.on_audio_click)
        self._view.bt_output_selection.connect("clicked", self.on_output_click)
        self._view.bt_vol_up.connect("clicked", self.on_vol_up_click)
        self._view.bt_vol_down.connect("clicked", self.on_vol_down_click)
        self._view.bt_dvd.connect("clicked", self.on_dvd_select)
        self._view.bt_bray.connect("clicked", self.on_bray_select)
        self._view.bt_dvr.connect("clicked", self.on_dvr_select)
        self._view.bt_hdmi1.connect("clicked", self.on_hdmi1_select)
        self._view.bt_hdmi2.connect("clicked", self.on_hdmi2_select)
        self._view.bt_hdmi3.connect("clicked", self.on_hdmi3_select)
        self.address_ip = self.config.read_config()
        self._view.set_subtitle("Address is : " +str(self.address_ip))
        self.ampli = Amplifier(self.logger)
        self.central_buffer = self._view.label2.get_buffer()
        self.ampli.set_ip(self.address_ip)

    def on_wiz_clicked(self,bt):
        self.logger.debug("Lu")
        self._view.destroy()
        self.start_wiz()

    def on_close_clicked(self, *args):
        print("The 'Close' button has been clicked")
        ip = self.assistant.address_ip
        self.logger.debug("Ip :" +str(ip))
        self.config.create_config(ip)
        self.assistant.destroy()
        self.start_view()

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

    def get_volume(self):
        self.semaphore = False
        self.logger.debug("From controller starting getvolume")
        volume = self.ampli.get_volume()
        self.logger.debug("From controller volume is : " + str(volume))
        self.semaphore = True

    def error(self,arg):
        self.logger.debug("From controller error found on discovery")
        self.browser.cancel()
        self.zeroconf.close()
        self.logger.debug("From controller restart zeroconf")
        self.start_discover()

    def __del__(self):
        self.logger.debug("Controler autodestructed")
        #self.ampli.close()
        self.logger = None
        self.zeroconf = None
        self.listener = None
        self.browser = None
        self.buffer = None
        self.label = None


