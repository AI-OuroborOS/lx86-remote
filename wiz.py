#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from zeroconf import ServiceBrowser, Zeroconf,ServiceStateChange
import socket


class Assistant(Gtk.Assistant):
    def __init__(self):

        Gtk.Assistant.__init__(self)
        self.address_ip = None
        self.set_title("First run")
        self.set_default_size(400, -1)
        self.connect("cancel", self.on_cancel_clicked)
        #self.connect("close", self.on_close_clicked)
        self.connect("apply", self.on_apply_clicked)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(box)
        self.set_page_type(box, Gtk.AssistantPageType.INTRO)
        self.set_page_title(box, "Welcome")
        label = Gtk.Label(label="This is the first time you run this application. The application will start an autodetect of the amplifier. Please click 'next' to continue.")
        label.set_line_wrap(True)
        box.pack_start(label, True, True, 0)
        self.set_page_complete(box, True)

        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(self.content)
        self.set_page_type(self.content, Gtk.AssistantPageType.PROGRESS)
        self.set_page_title(self.content, "Detection page")
        self.label_detect = Gtk.Label(label="")
        self.label_detect.set_line_wrap(True)
        self.content.pack_start(self.label_detect, True, True, 0)
        #self.start_discover()
        checkbutton = Gtk.CheckButton(label="Save IP")
        checkbutton.connect("toggled", self.on_save)

        start_bt = Gtk.Button(label="Start dicovery")
        start_bt.connect("clicked", self.start_discover)
        self.content.pack_start(start_bt, False, False, 0)
        self.content.pack_start(checkbutton, False, False, 0)



        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.append_page(box)
        self.set_page_type(box, Gtk.AssistantPageType.SUMMARY)
        self.set_page_title(box, "Summary")
        self.resume_label = Gtk.Label(label="")
        self.resume_label.set_line_wrap(True)
        box.pack_start(self.resume_label, True, True, 0)
        self.set_page_complete(box, True)

    def on_apply_clicked(self, *args):
        print("The 'Apply' button has been clicked")

    def on_close_clicked(self, *args):
        print("The 'Close' button has been clicked")
        #self.destroy()

    def on_cancel_clicked(self, *args):
        print("The Assistant has been cancelled.")
        self.destroy()

    def on_save(self, checkbutton):
        self.set_page_complete(self.content, checkbutton.get_active())
        #lbl = self.label_detect.get_buffer()
        self.resume_label.set_label("Addresse IP " + self.address_ip + " will be  save")

    def on_service_state_change(self,zeroconf, service_type, name, state_change):

        if state_change is ServiceStateChange.Added:
            if (name == "SC-LX86._http._tcp.local."):
                actual = self.label_detect.get_label()
                self.label_detect.set_label(actual + "\n Amplifier found")
                info = zeroconf.get_service_info(service_type, name)
                if info.address is not None:
                    self.address_ip = socket.inet_ntoa(info.address)
                    actual = self.label_detect.get_label()
                    self.label_detect.set_label(actual + "\n at ip : " + self.address_ip)
                zeroconf.close()

    def start_discover(self,bt):
        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf, "_http._tcp.local.",  handlers=[self.on_service_state_change])


if __name__ == "__main__":
    # execute only if run as a script
    assistant = Assistant()
    assistant.show_all()

    Gtk.main()


