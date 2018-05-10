import logging
import pygtk
import gtk

class MyHandler(logging.Handler):
    def __init__(self, label):
        logging.Handler.__init__(self)
        self.label = label

    def handle(self, rec):
        original = self.label.get_text()
        self.label.set_text(rec.msg + "\n" + original)

class MyLogger():
    def __init__(self, label):
        self.logger = logging.getLogger("Example")
        self.handler = MyHandler(label)
        #self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def warning(self, msg):
        self.logger.warning(msg)


class MainWindow(gtk.Window):
    def __init__(self):
        gtk.Window.__init__(self)
        self.set_size_request(200, 100)
        self.connect("delete-event", self.on_delete_event)

        self.loglabel = gtk.Label()
        self.add(self.loglabel)

        self.show_all()

    def run(self):
        gtk.mainloop()

    def on_delete_event(self, w, d):
        gtk.main_quit()


def main():
    mw = MainWindow()

    logger = MyLogger(mw.loglabel)
    logger.warning("This is a test message")
    logger.warning("This is another message")

    mw.run()
    return 0

if __name__ == '__main__':
    main()