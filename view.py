""" Simple python classe to represent the view of MVC
Author : Julien Ithurbide
Compagny : CPNV
VERSION : 0.1
LAST Modification :

Date       | Exp.
-----------|------------------------------------
18.01.2018 | First version
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Pango,Gdk


class View(Gtk.Window):

    def __init__(self, **kw):
        self.line_position = 0
        Gtk.Window.__init__(self, title="gControl-LX86")
        self.set_size_request(800, 600)
        self.set_icon_name("audio-volume-high")

        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(False)
        self.header_bar.props.title = "gControl-LX86"
        self.set_titlebar(self.header_bar)

        self.bt_start_con = Gtk.Button.new_from_icon_name("gtk-connect", Gtk.IconSize.BUTTON)
        self.header_bar.pack_start(self.bt_start_con)

        self.bt_power_off = Gtk.Button.new_from_icon_name("process-stop", Gtk.IconSize.BUTTON)
        self.header_bar.pack_start(self.bt_power_off)

        self.bt_close = Gtk.Button.new_from_icon_name("window-close", Gtk.IconSize.BUTTON)
        self.bt_close.connect("clicked", self.on_close)
        self.header_bar.pack_end(self.bt_close)

        self.bt_wiz = Gtk.Button.new_from_icon_name("gtk-edit", Gtk.IconSize.BUTTON)
        self.header_bar.pack_end(self.bt_wiz)
        self.header_bar.set_has_subtitle(True)
        self.header_bar.set_subtitle("")


        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.grid.compute_expand(True)

        self.infobar = Gtk.InfoBar()
        self.infobar.set_show_close_button(True)
        self.infobar.connect("response", self.on_infobar_response)
        self.grid.attach(self.infobar, 0, self.line_position, 1, 1)

        self.load_css()
        self.line_position += 1
        self.box = Gtk.Box(spacing=6)
        self.grid.attach(self.box,0,self.line_position,1,1)
        self.box.compute_expand(True)

        css = "GtkButton { font: 24}"
        self.bt_output_selection = Gtk.Button(label="Output")
        self.bt_output_selection.set_hexpand(True)
        self.bt_output_selection.set_size_request(-1, 100)
        self.bt_output_selection.get_style_context().add_class("btn_moins")
        self.box.pack_start(self.bt_output_selection, True, True, 0)

        self.popover_outpup = Gtk.Popover()
        vbox_output = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.bt_dvd = Gtk.ModelButton(label="DVD")
        self.bt_dvd.get_style_context().add_class("btn_moins")
        vbox_output.pack_start(self.bt_dvd, False, True, 10)

        self.bt_bray = Gtk.ModelButton(label="BD")
        self.bt_bray.get_style_context().add_class("btn_moins")
        vbox_output.pack_start(self.bt_bray, False, True, 10)

        self.bt_dvr = Gtk.ModelButton(label="DVR")
        self.bt_dvr.get_style_context().add_class("btn_moins")
        vbox_output.pack_start(self.bt_dvr, False, True, 10)

        self.bt_hdmi1 = Gtk.ModelButton(label="HDMI 1")
        self.bt_hdmi1.get_style_context().add_class("btn_moins")
        vbox_output.pack_start(self.bt_hdmi1, False, True, 10)

        self.bt_hdmi2 = Gtk.ModelButton(label="HDMI 2")
        self.bt_hdmi2.get_style_context().add_class("btn_moins")
        vbox_output.pack_start(self.bt_hdmi2, False, True, 10)

        self.bt_hdmi3 = Gtk.ModelButton(label="HDMI 3")
        self.bt_hdmi3.get_style_context().add_class("btn_moins")
        vbox_output.pack_start(self.bt_hdmi3, False, True, 10)
        self.popover_outpup.add(vbox_output)
        self.popover_outpup.set_position(Gtk.PositionType.BOTTOM)

        self.bt_audio_select = Gtk.Button(label="Audio")
        self.bt_audio_select.set_hexpand(True)
        self.bt_audio_select.set_size_request(-1, 100)
        self.bt_audio_select.get_style_context().add_class("btn_moins")
        self.box.pack_start(self.bt_audio_select, True, True, 0)

        self.popover_audio = Gtk.Popover()
        vbox_audio = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        bt_ext_stereo = Gtk.ModelButton(label="EXTENDED STEREO")
        bt_ext_stereo.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_ext_stereo, False, True, 10)

        bt_direct = Gtk.ModelButton(label="DIRECT")
        bt_direct.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_direct, False, True, 10)

        bt_pure_direct = Gtk.ModelButton(label="PUR DIRECT")
        bt_pure_direct.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_pure_direct, False, True, 10)

        bt_adv_sur = Gtk.ModelButton(label="ADV. SURROUND Cycle")
        bt_adv_sur.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_adv_sur, False, True, 10)

        bt_action = Gtk.ModelButton(label="ACTION")
        bt_action.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_action, False, True, 10)

        bt_drama = Gtk.ModelButton(label="DRAMA")
        bt_drama.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_drama, False, True, 10)

        bt_sci_fi = Gtk.ModelButton(label="SCI-FI")
        bt_sci_fi.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_sci_fi, False, True, 10)

        bt_mono = Gtk.ModelButton(label="MONO")
        bt_mono.get_style_context().add_class("btn_moins")
        vbox_audio.pack_start(bt_mono, False, True, 10)


        self.popover_audio.add(vbox_audio)
        self.popover_audio.set_position(Gtk.PositionType.BOTTOM)

        self.bt_vol_up = Gtk.Button(label="+")
        self.bt_vol_up.get_style_context().add_class("btn_moins")
        self.bt_vol_up.set_hexpand(True)

        self.box.pack_start(self.bt_vol_up, True, True, 0)
        self.bt_vol_down = Gtk.Button(label="-")
        self.bt_vol_down.set_hexpand(True)
        self.bt_vol_down.get_style_context().add_class("btn_moins")
        self.box.pack_start(self.bt_vol_down, True, True, 0)

        # self.label2 = Gtk.TextView()
        # self.label2.set_vexpand(True)
        # self.grid.attach(self.label2,0,2,1,1)

        self.line_position += 1
        self.box_info = Gtk.Box(spacing=10)
        self.box_info.set_homogeneous(False)
        self.grid.attach(self.box_info,0,self.line_position,1,1)
        self.box_info.compute_expand(True)



        self.info_volume = Gtk.Label(label = "Vol : ")
        #self.info_volume.set_line_wrap(True)
        self.info_volume.set_justify(Gtk.Justification.RIGHT)
        self.info_volume.get_style_context().add_class("info_texte")
        self.box_info.pack_start(self.info_volume,False,False,0)

        self.lbl_volume = Gtk.Label(label="---")
        self.lbl_volume.set_justify(Gtk.Justification.LEFT)
        self.lbl_volume.get_style_context().add_class("info_texte")
        self.box_info.pack_start(self.lbl_volume,False, False,0)

        self.info_input = Gtk.Label(label="Input :")
        self.info_input.get_style_context().add_class("info_texte")
        self.box_info.pack_start(self.info_input,False, False, 0)

        self.lbl_input = Gtk.Label(label="DVD")
        self.lbl_input.get_style_context().add_class("info_texte")
        self.lbl_input.set_justify(Gtk.Justification.RIGHT)
        self.box_info.pack_start(self.lbl_input, False, False, 0)

        self.line_position += 1
        self.drawing_area = Gtk.DrawingArea()
        # add the type of events we are interested in retrieving, skip this step and your events will never fire
        self.drawing_area.add_events(Gdk.EventMask.TOUCH_MASK)
        self.drawing_area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.drawing_area.connect('button_press_event', self.touched)
        self.drawing_area.connect('touch-event', self.touched)
        self.drawing_area.set_double_buffered(False)
        self.drawing_area.set_vexpand(True)
        self.grid.attach(self.drawing_area,0,self.line_position,1,1)

        self.line_position += 1
        self.notebook = Gtk.Notebook()
        self.notebook.set_valign(Gtk.Align.END)
        self.notebook.set_size_request(-1, 200)
        self.grid.attach(self.notebook,0,self.line_position,1,5)

        self.scrolledWinPage1 = Gtk.ScrolledWindow()
        self.label = Gtk.TextView()
        self.scrolledWinPage1.add(self.label)
        self.notebook.append_page(self.scrolledWinPage1, Gtk.Label(label='Log'))

        self.scrolledWinPage2 = Gtk.ScrolledWindow()
        self.info = Gtk.TextView()
        self.scrolledWinPage2.add(self.info)

        self.notebook.append_page(
            self.scrolledWinPage2,
            Gtk.Image.new_from_icon_name(
                "help-about",
                Gtk.IconSize.MENU
            )
        )
        self.show_all()

    def touched(self,widget,event):
        pass

    def on_infobar_response(self):
        pass

    def load_css(self):
        style_provider = Gtk.CssProvider()
        css = open('bt_class.css', 'rb')
        css_data = css.read()
        css.close()
        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )


    def on_close(self,widget):
        Gtk.main_quit()

    def set_subtitle(self,title):
        self.header_bar.set_subtitle(title)
    def get_logger(self):
        return self.logger

    def _quit(self, button, *args):
        Gtk.main_quit()


