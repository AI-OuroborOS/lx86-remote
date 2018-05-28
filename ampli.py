import sys
import telnetlib


class Amplifier:

    def __init__(self, log):
        self.logger = log
        self.address_ip = None
        self.tn = None
        self.connected = False

    def is_connected(self):
        return self.connected

    def set_ip(self, ip):
        self.address_ip = ip
        self.logger.debug("From ampli setting ip " + self.address_ip)

    def connect(self):
        try:
            self.logger.debug("From Amplifier connect to " + self.address_ip)  # update to your receiver's IP (recommend setting a static/DHCP reserved IP)
            self.tn = telnetlib.Telnet(self.address_ip, 23, 120)
            self.logger.debug("From Amplifier connection etablished")
        except ConnectionRefusedError:
            self.logger.debug("From Amplifier wait finish")
        else:
            self.connected = True
            self.tn.write(b"?V\r\n")  # send "?V" command to get the current Amplifier level
            output = self.tn.read_until(b"\r\n")

    def close(self):
        self.logger.debug("From Amplifier connection close")
        try:
            self.tn.close()
        except ConnectionAbortedError:
            self.logger.debug("From Amplifier can't close connection")
        except AttributeError:
            self.logger.debug("From Amplifier connection opened")
        else:
            self.connected = False

    def set_direct_volume(self,vol):
        if self.connected:
            if vol < 0:
                self.logger.debug("From Amplifier Amplifier need to be higher to 0")
                return
            elif vol < 10:
                cmd = ("00"+str(vol)+"vl\r\n").encode('ascii')
            elif vol < 99:
                cmd = ("0"+str(vol)+"vl\r\n").encode('ascii')
            else:
                self.logger.debug("From Amplifier Amplifier need to be lower to 100")
                return
            self.logger.debug("From Amplifier will send cmd : " + str(cmd))
            self.tn.write(cmd)

    def set_volume_up(self):
        currentlevel = "Not Connected"
        if self.connected:
            self.tn.write(b"?V\r\n")  # send "?V" command to get the current Amplifier level
            output = self.tn.read_until(b"\r\n")
            while not "VOL" in str(output):
                output = self.tn.read_until(b"\r\n")
            currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)
            if currentlevel < 100:
                self.tn.write(b"VU\r\n")
                output = self.tn.read_until(b"\r\n")
                while not "VOL" in str(output):
                    output = self.tn.read_until(b"\r\n")
                currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)
        return currentlevel

    def set_volume_down(self):
        currentlevel = "Not connected"
        if self.connected:
            self.tn.write(b"?V\r\n")  # send "?V" command to get the current Amplifier level
            output = self.tn.read_until(b"\r\n")
            while not "VOL" in str(output):
                output = self.tn.read_until(b"\r\n")
            currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)
            if currentlevel > 0:
                self.tn.write(b"VD\r\n")
                output = self.tn.read_until(b"\r\n")
                while not "VOL" in str(output):
                    output = self.tn.read_until(b"\r\n")
                currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)
        return currentlevel

    def get_volume(self):
        currentlevel =None
        if self.connected:
            self.tn.write(b"?V\r\n")  # send "?V" command to get the current Amplifier level
            output = self.tn.read_until(b"\r\n")
            currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)
            self.logger.debug("From Amplifier value find : " +str(currentlevel))
        return currentlevel

    def set_output(self,key):
        choices = {'DVD': b"04FN\r\n", 'BD': b"25FN\r\n", "DVR": b"15FN\r\n", "HDMI1": b"19FN\r\n", "HDMI2": b"20FN\r\n",
                   "HDMI3": b"21FN\r\n"}
        result = choices.get(key, b"04FN\r\n")
        if self.connected:
            self.tn.write(result)
        else:
            self.logger.debug("From ampli if connected will send : " + str(result))

    def __del__(self):
        self.close()
