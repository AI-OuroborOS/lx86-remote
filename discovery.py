from six.moves import input
from zeroconf import ServiceBrowser, Zeroconf
import socket
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject

class Discovery(GObject.GObject):

    __gsignals__ ={
        'ampli-found': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        'error-found': (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    def __init__(self,log,*arg):
        GObject.GObject.__init__(self)
        self.logger = log
        self.service_name = "SC-LX86._http._tcp.local."

    def add_service(self, zeroconf, type, name):
        if (name == self.service_name):
            try:
                info = zeroconf.get_service_info(type, name)
                self.address = socket.inet_ntoa(info.address)
                self.logger.debug("Service found with address "+self.address)
            except AttributeError:
                self.logger.debug ("Service: " + name + "Not have an address" + " info service " + str(info))
                self.emit('error-found')
            except:
                self.logger.debug("Service: " + name + "Unknow error")
                self.emit('error-found')
            else:
                self.logger.debug("Service found at : " + self.address + "zeroconf will close")
                self.emit('ampli-found',self.address )
                zeroconf.close()

    def __del__(self):
        self.logger = None
        self.service_name = None
