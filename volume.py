import sys
import telnetlib

class Volume:


    def __init__(self, log):
        self.logger = log
        self.address_ip = None
        self.tn = None

    def setIP(self,ip):
        self.address_ip = ip

    def connect(self):
        try:
            self.logger.debug("From volume connect to " + self.address_ip)
            HOST = self.address_ip  # update to your receiver's IP (recommend setting a static/DHCP reserved IP)
            self.tn = telnetlib.Telnet(HOST, 23, 120)
            self.logger.debug("From volume connection etablished")
        except ConnectionRefusedError:
            self.logger.debug("From volume wait finish")

    def close(self):
        self.logger.debug("From volume connection close")
        self.tn.close()

    def setVolume(self,vol):
        self.connect()
        self.tn.write(b"?V\r\n")  # send "?V" command to get the current volume level
        output = self.tn.read_until(b"\r\n")
        currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)

        goal = int(vol)  # input argument: convert from my Sony TV's volume scale to Pioneer's

        if goal <= 100:  # my set upper limit to prevent damage to speakers
            if currentlevel > goal:
                for x in range(currentlevel, goal, -1):
                    self.tn.write(b"VD\r\n")  # send "VD" command (volume down)
            else:
                for x in range(currentlevel, goal, 1):
                    self.tn.write(b"VU\r\n")  # send "VU" command (volume up)
        else:
            print("Out of range")
        self.close()

    def getVolume(self):
        self.connect()
        self.tn.write(b"?V\r\n")  # send "?V" command to get the current volume level
        output = self.tn.read_until(b"\r\n")
        currentlevel = int(output[3:])  # Pioneer responds with "VOL###" (ignore the "VOL" part of the string)
        self.logger.debug("From volume vaule find : " +str(currentlevel))
        self.close()

        return currentlevel
