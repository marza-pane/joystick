import sys
import logging

from gui.utils import MouseMonitor, ScreenMonitor, MIN_WINDOW_W, MIN_WINDOW_H
from gui.templates import tk, LabelBase
from gui.joystick import Joystick

class ApplicationBase(tk.Tk):

    # Template della Main Window

    def __init__(self):
        tk.Tk.__init__(self)
        self.attributes('-alpha', 1)
        # interfaccia mouse, viene passata a tutti i widget @ __init__
        self.mouse = MouseMonitor()
        # classe per controllo posizione/dimensione finestra sullo schermo
        self.screen = ScreenMonitor()

    def build(self):
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.bind("<Configure>", self._winchange)
        self.minsize(width=MIN_WINDOW_W,
                     height=MIN_WINDOW_H)

    # chiamata ogni volta che avviene un evento <Configure> (resize)
    def _winchange(self, *evt):
        try:
            if self.screen.win_width != self.winfo_width() or self.screen.win_height != self.winfo_height():
                self.screen.resize_flag = True
        except (IndexError, AttributeError):
            pass

    # funzione dummy per la tastiera
    def _keystroke(self, key:str):
        logging.debug('Pressed <{}>'.format(key))

    # loop template, deve esser chiamato dalla super-classe
    def loop(self):
        self.after(5, self.loop)
        if self.screen.resize_flag and not self.mouse.on_click:
            self.on_resize()

    def on_update(self):
        pass

    # questa funzione dispone aggiorna la finestra e dispone gli elementi grafici
    def on_resize(self):
        self.update()
        self.screen.resize_flag = False
        logging.debug('Resizing @ {}x{}'.format(self.winfo_width(), self.winfo_height()))
        try:
            self.screen.win_width = self.winfo_width()
            self.screen.win_height = self.winfo_height()
            return self.screen.win_width, self.screen.win_height
        except tk.TclError as error:
            logging.warning('can not call winfo width/height [{}]'.format(error))
            return 1, 1

    # chiamata quando la finestra viene chiusa o su <CTRL + C>
    def on_close(self, *evt, code=0):
        self.unbind_all('<Configure>')
        self.screen.resize_flag = False
        self.mouse.stop()
        self.quit()
        print('\nGoodbye Space Cowboy\n')
        sys.exit(code)

    # come dice il nome, fa partire la GUI
    def run(self):
        self.build()
        self.on_resize()
        self.on_update()
        self.loop()
        self.mainloop()


class MainApplication(ApplicationBase):

    def __init__(self):
        ApplicationBase.__init__(self)
        self._joystick=Joystick(self, tooltip='a tool tip message')
        self._xspeed = LabelBase(self)
        self._yspeed = LabelBase(self)

        self._xspeed.configure(text='X speed : {}'.format('%3.3f' % self._joystick.camera_x_speed))
        self._yspeed.configure(text='Y speed : {}'.format('%3.3f' % self._joystick.camera_y_speed))

    def build(self):
        super(MainApplication, self).build()
        self.geometry("800x400+100+100")
        self._joystick.build()

    def loop(self):
        super(MainApplication, self).loop()
        if self._joystick.pov_change:
            self._xspeed.configure( text = 'X speed : {}'.format('%3.3f' % self._joystick.camera_x_speed))
            self._yspeed.configure( text = 'Y speed : {}'.format('%3.3f' % self._joystick.camera_y_speed))

    def on_resize(self):
        w,h = super(MainApplication, self).on_resize()
        logging.debug('resizing')
        off = 15
        sj = min(h,w) - 2 * off
        self._joystick.place(
            x=off,
            y=off,
            width=sj,
            heigh=sj
        )
        self._xspeed.place(
            x=2 * off + sj,
            y=off,
            width = w - (3 * off + sj),
            heigh = 25
        )
        self._yspeed.place(
            x=2 * off + sj,
            y=off + 27,
            width = w - (3 * off + sj),
            heigh = 25
        )
        self._joystick.on_resize()

if __name__ == '__main__':


    win = MainApplication()
    win.run()
