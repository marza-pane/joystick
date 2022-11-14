# from common.utils import *

import pynput
import tkinter as tk
import tkinter.font
import random

from matplotlib import colors as mpl_colors

MIN_WINDOW_W = 600
MIN_WINDOW_H = 480

#       ╔═══════════════════════════════════════════════════════════════════╗
#       ║   F O N T S   A N D   P A L E T T E                               ║
#       ╠═══════════════════════════════════════════════════════════════════╣
#       ║                                                                   ║
class Fonts:

    @staticmethod
    def mono(size):
        return tkinter.font.Font(family='mono', size=size)

    @staticmethod
    def monobold(size):
        return tkinter.font.Font(family='mono', weight="bold", size=size)

class PaletteManager:

    class GenericPalette:
        def __init__(self):
            self.R_TITLE = 'light sky blue'
            # self.ERROR_GUI = 'red4'
            # self.DISABLED = 'grey35'
            # self.WARNING = 'dark orange'
            # self.ONLINE = 'green3'
            # self.OFFLINE = 'firebrick3'
            # self.FG_DEFAULT = 'white'
            # self.BG_DEFAULT = 'red'
            # self.BLACK = 'grey5'
            # self.WHITE = 'snow'
            # self.OFF = 'firebrick4'
            # self.ON = 'chartreuse'

    class ReportPalette:
        def __init__(self):
            self.BG_DEBUG       = 'snow'
            self.BG_INFO        = 'light sky blue'
            self.BG_ALERT       = 'dark orange'
            self.BG_WARNING     = 'orange red'
            self.BG_ERROR       = 'firebrick1'
            self.BG_CRITICAL    = 'red'
            self.BG_FATAL       = 'red4'
            self.BG_UNKNOWN     = 'purple4'

            self.FG_DEBUG       = 'black'
            self.FG_INFO        = 'black'
            self.FG_ALERT       = 'navy'
            self.FG_WARNING     = 'navy'
            self.FG_ERROR       = 'navy'
            self.FG_CRITICAL    = 'snow'
            self.FG_FATAL       = 'snow'
            self.FG_UNKNOWN     = 'snow'

    class BoardPalette:

        class BoardProjectPalette:
            def __init__(self):
                self.SAMPLER    ='SpringGreen4'
                self.ESPROUTER  ='DeepSkyBlue4'
                self.CONTROLLER ='MediumOrchid4'
                self.CAMERA     ='SlateBlue1'
                self.PHONEDOOR  ='RoyalBlue1'

        class BoardHardwarePalette:
            def __init__(self):
                self.UNO    ='blue4'
                self.DUE    ='firebrick4'
                self.MEGA   = 'dark violet4'
                self.ESP    ='dark green'

        def __init__(self):
            self.projects = self.BoardProjectPalette()
            self.hardware = self.BoardHardwarePalette()

    class DevicePalette:
        def __init__(self):
            self.GENERIC='aquamarine2'
            self.DHT22='goldenrod1'
            self.LDR='gold'
            self.RELAY='cornflower blue'

    class PlotPalette:
        def __init__(self):

            self._colors = list(mpl_colors.CSS4_COLORS)
            self._current = self._colors

        def new(self):
            if len(self._current) == 0:
                self._current = self._colors

            shot = random.choice(self._current)
            self._current.remove(shot)
            return shot

    class Frames:
        def __init__(self):
            self.SERVER='lime green'
            self.DEVICES='DarkOliveGreen1'
            self.LAYOUT='light sky blue'
            self.LIGHTS='light goldenrod'
            self.ALARMS='light coral'
            self.WEATHER='peach puff'
            # self.WEATHER='light slate blue'

    def __init__(self):
        self.generic=self.GenericPalette()
        self.report=self.ReportPalette()
        self.device=self.DevicePalette()
        self.board=self.BoardPalette()
        self.plot=self.PlotPalette()
        self.frames=self.Frames()

        self.BLACK = 'grey5'
        self.WHITE = 'snow'
        self.RED = 'salmon'
        self.FG = 'white'
        self.BG = 'grey15'
#       ║                                                                   ║
#       ╚═══════════════════════════════════════════════════════════════════╝

Palette     = PaletteManager()

class ScreenMonitor:

    def __init__(self):

        self.screen_width = 1
        self.screen_height = 1

        self.win_x = 0
        self.win_y = 0

        self.win_width = 1
        self.win_height = 1

        self.resize_flag = False

#       ╔═══════════════════════════════════════════════════════════════════╗
#       ║   I C O N   A S S E T                                             ║
#       ╠═══════════════════════════════════════════════════════════════════╣
#       ║                                                                   ║
#       ║                                                                   ║
#       ╚═══════════════════════════════════════════════════════════════════╝

#       ╔═══════════════════════════════════════════════════════════════════╗
#       ║   T O O L   T I P                                                 ║
#       ╠═══════════════════════════════════════════════════════════════════╣
#       ║                                                                   ║
class MouseMonitor:

    def __init__(self):

        self._mouse_controller = pynput.mouse.Controller()
        self._mouse_listen = pynput.mouse.Listener(
            on_move=self._update_position,
            on_click=self._update_click,
            on_scroll=self._update_scroll)
        self._mouse_listen.start()

        self._pX = 0
        self._pY = 0

        self._on_move=False
        self._on_click=False
        self._on_scroll=0

#       ╠═══ P R O P E R T I E S ═══════════════════════════════════════════╣

    def stop(self):
        self._mouse_listen.stop()

    @property
    def x(self):
        return self._pX

    @property
    def y(self):
        return self._pY

    @property
    def on_move(self):
        return self._on_move

    @property
    def on_click(self):
        return self._on_click

    @property
    def on_scroll(self):
        return self._on_scroll

#       ╠═══ M E T H O D S ═════════════════════════════════════════════════╣

    def _update_position(self, x, y):
        self._mouse_controller.ON_MOVE=True
        self._pX = x
        self._pY = y

    def _update_click(self,x, y, button, pressed):
        if pressed:
            self._on_click=True
        else:
            self._on_click=False

    def _update_scroll(self,x, y, dx, dy):
        self._on_scroll=max(dx, dy)

class ToolTip(object):

    """ create a tooltip for a given widget """

    def __init__(self, widget, text=''):
        self.text=text
        self.widget=widget
        self.widget.bind_mouse_motion()
        self.tip=None

    def show(self):
        if self.tip:
            self.tip.destroy()
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.label = tk.Text(self.tip,
                        relief=tk.FLAT,
                        wrap=tk.WORD,
                        bd=0,
                        padx=5,
                        font=Fonts.mono(8),
                        )
        self.tip.label.insert(tk.END, self.text)
        self.tip.label.pack(expand=True, fill=tk.BOTH)
        self.place()

    def place(self):
        chunks = str(self.text).split('\n')
        if len(chunks) == 1:
            w = 8 * len(self.text)
            h = 16

        else:
            h = 15 * len(chunks)
            w = 0
            for entry in chunks:
                size = len(entry) * 8
                if size > w:
                    w = size

        self.tip.wm_geometry('%dx%d%+d%+d' % (
            w + 5, h + 5,
            self.widget.mouse.x,
            self.widget.mouse.y + 30))

    def on_enter(self, *event):
        if len(self.text) == 0:
            return
        if self.widget.mouse.x == 0 and self.widget.mouse.y == 0:
            return
        self.show()

    def on_motion(self, *event):

        if len(self.text) == 0:
            return

        if self.tip:
            if self.widget.mouse.x == 0 and self.widget.mouse.y == 0:
                return

            if len(self.text) == 0:
                self.on_leave()
                return

            if not self.tip.label.get('1.0', tk.END).strip('\n') == self.text:
                self.tip.label.delete('1.0', tk.END)
                self.tip.label.insert(tk.END, self.text)

            self.place()

        else:
            self.show()

    def on_leave(self, *event):
        if self.tip:
            self.tip.destroy()
            self.tip=None
#       ║                                                                   ║
#       ╚═══════════════════════════════════════════════════════════════════╝

print('Loaded gui.utils')

# print( Icons.BOARD_GREEN() )