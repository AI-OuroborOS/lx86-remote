import logging


class MyHandler(logging.Handler):

    def __init__(self, label):
        logging.Handler.__init__(self)
        self.buffer = label.get_buffer()

    def handle(self, rec):
        original = self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter(),False )
        if isinstance(rec.msg, str):
            self.buffer.set_text(rec.asctime + " - " + rec.name + " - " + rec.levelname + " - " + rec.msg + "\n" + original)
        else:
            self.buffer.set_text(rec.asctime + " - " + rec.name + " - " + rec.levelname + " - " + str(rec.msg) + "\n" + original)


class Log():

    def __init__(self,label):
        self.logger = logging.getLogger('gestClasse.Database')
        self.logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        lblHandler = MyHandler(label)
        hdlr = logging.FileHandler('gestClasse.log')

        ch.setLevel(logging.DEBUG)
        lblHandler.setLevel(logging.DEBUG)
        hdlr.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        hdlr.setFormatter(formatter)
        lblHandler.setFormatter(formatter)

        self.logger.addHandler(ch)
        self.logger.addHandler(hdlr)
        self.logger.addHandler(lblHandler)

    def get_logger(self):
        return self.logger
