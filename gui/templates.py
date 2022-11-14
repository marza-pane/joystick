import logging
import tkinter as tk
from gui.utils import Fonts, ToolTip

logging.basicConfig(

    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(module)s:%(message)s',
)

#       ╔═══════════════════════════════════════════════════════════════════╗
#       ║   B A S E   C L A S S                                             ║
#       ╠═══════════════════════════════════════════════════════════════════╣
#       ║                                                                   ║
class   _GObjectTemplate:

    def __init__(self, parent, widget_class, *args, **kwargs):
        if not issubclass(widget_class, tk.Widget):
            raise AssertionError(
                'invalid widget class : <{}> not subclass of tkinter.Widget'.format(widget_class.__name__)
            )
        widget_class.__init__(self, parent)
        self.mouse = parent.mouse
        tool_tip = kwargs.pop('tooltip', '')
        if tool_tip:
            self._tooltip = ToolTip(self, tool_tip)

        logging.debug('INIT _GObjectTemplate:{}:{} with {}|{}'.format(
            self.__str__(), widget_class.__name__, args, kwargs))

    def build(self, *args, **kwargs):
        logging.debug('BUILD {} with {}|{}'.format(self.__str__(), args, kwargs))

    def bind_keyboard(self):
        self.bind("<Return>", lambda evt, key='ENTER': self.on_keystroke(key))
        self.bind("<Delete>", lambda evt, key='DEL': self.on_keystroke(key))
        self.bind("<Escape>", lambda evt, key='ESC': self.on_keystroke(key))
        self.bind("<Cancel>", lambda evt, key='CANC': self.on_keystroke(key))
        self.bind("<Key>",    lambda event: self.on_keystroke(str(event.char).upper()))

    def bind_mouse_motion(self):
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind('<Motion>', self.on_motion)

    def bind_mouse_key(self):
        self.bind("<ButtonPress-1>", self.on_mouse_press)
        self.bind("<ButtonRelease-1>", self.on_mouse_release)

    def settooltip(self, message=''):
        self._tooltip.text=message

    def loop(self):
        pass

    def on_update(self, *args, **kwargs):
        logging.debug('ON_UPDATE {} with {}|{}'.format(self.__str__(), args, kwargs))

    def on_resize(self, *args, **kwargs):
        logging.debug('ON_RESIZE {} with {}|{}'.format(self.__str__(), args, kwargs))
        self.update()
        try:
            w = self.winfo_width()
            h = self.winfo_height()
            return w, h
        except tk.TclError as error:
            logging.warning('can not place element [{}]'.format(error))
            return 1, 1

    def on_motion(self, *event):
        self._tooltip.on_motion(*event)

    def on_leave(self, *event):
        self._tooltip.on_leave(*event)
        logging.debug('LEAVE {} with {}'.format(self.__str__(), event))

    def on_enter(self, *event):
        self._tooltip.on_enter(*event)
        logging.debug('ENTER {} with {}'.format(self.__str__(), event))

    def on_mouse_press(self, *event):
        logging.debug('MOUSE KEY PRESS {} with {}'.format(self.__str__(), event))
        pass

    def on_mouse_release(self, *event):
        logging.debug('MOUSE KEY RELEASE {} with {}'.format(self.__str__(), event))
        pass

    def on_keystroke(self, char:str):
        logging.debug('KEYBOARD STROKE {} : {}'.format(self.__str__(), char))

    def on_scroll(self, *event):
        logging.debug('MOUSE SCROLL {} with {}'.format(self.__str__(), event))
        pass

    def on_close(self):
        for child in self.children:
            try:
                child.on_close()
            except AttributeError:
                pass
        self.destroy()

#       ║                                                                   ║
#       ╚═══════════════════════════════════════════════════════════════════╝

#       ╔═══════════════════════════════════════════════════════════════════╗
#       ║   TEMPLATES                                                       ║
#       ╠═══════════════════════════════════════════════════════════════════╣
#       ║                                                                   ║
class PanelBase(_GObjectTemplate, tk.PanedWindow):
    def __init__(self, parent, *args, **kwargs):
        _GObjectTemplate.__init__(self, parent, tk.PanedWindow, *args, **kwargs)

class ButtonBase(_GObjectTemplate, tk.Button):
    def __init__(self, parent, *args, **kwargs):
        _GObjectTemplate.__init__(self, parent, tk.Button, *args, **kwargs)

class LabelBase(_GObjectTemplate, tk.Label):
    def __init__(self, parent, *args, **kwargs):
        _GObjectTemplate.__init__(self, parent, tk.Label, *args, **kwargs)
        self.configure( font = Fonts.monobold(10) )

class EntryBase(_GObjectTemplate, tk.Entry):
    def __init__(self, parent, *args, **kwargs):
        _GObjectTemplate.__init__(self, parent, tk.Entry, *args, **kwargs)
#       ║                                                                   ║
#       ╚═══════════════════════════════════════════════════════════════════╝
class CanvasBase(_GObjectTemplate, tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        _GObjectTemplate.__init__(self, parent, tk.Canvas, *args, **kwargs)
        self.current = self.find_withtag(tk.CURRENT)

    def on_motion(self, *event):
        super(CanvasBase, self).on_motion(*event)
        fid = self.find_withtag(tk.CURRENT)
        if not fid == self.current:
            self.current = fid
            logging.debug('Canvas:current item ID <{}:{}>'.format(tk.CURRENT, fid))

print('Loaded gui.templates')
