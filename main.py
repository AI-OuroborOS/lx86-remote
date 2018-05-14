import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from controller import Controller
import sys

try :
    Controller()
    Gtk.main()
except IOError as e:
    print("I/O error({0}): {1}".format(e.errno, e.strerror))
except ValueError:
    print("Could not convert data to an integer.")
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise


