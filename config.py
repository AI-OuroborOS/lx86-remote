from os.path import expanduser,isfile,dirname
from log import Log
from json import dumps, dump, load
from io import open
from os import mkdir,stat

class Config:

    path = "/.amplifier/config"

    def __init__(self,log):
        self.logger = log
        self.home = expanduser("~")
        self.path = "/.amplifier/config"
        self.full_path = self.home+self.path
        self.logger.debug("Home directory is : " + self.full_path)

    def check_config(self):
        value_to_return = False
        if isfile(self.full_path):
            self.logger.debug("file found")
            value_to_return = True
        else:
            self.logger.debug("file not found")

        return value_to_return

    def create_config(self,ip):
        data = {}
        data['address'] = ip
        json_data = dumps(data)
        self.logger.debug("From Config create json : " + str(json_data))
        directory = dirname(self.full_path)

        try:
            stat(directory)
        except:
            mkdir(directory)
        with open(self.full_path, 'w') as outfile:
            dump(data, outfile)

    def read_config(self):
        directory = dirname(self.full_path)
        try:
            stat(directory)
        except:
            self.logger.debug("From config : file not exist")
            return None
        else:
            with open(self.full_path) as f:
                data = load(f)

            self.logger.debug("reading  data : " + str(data))
            return data['address']



if __name__ == "__main__":
    # execute only if run as a script
    test = None
    logger = Log(test).get_logger()
    maconf = Config(logger)
    if maconf.check_config():
        logger.debug("path : "+str(maconf.check_config()))
        ip = maconf.read_config()
        logger.debug("Ip was read at : " + str(ip))
    else:
        maconf.create_config("192.168.0.200")
