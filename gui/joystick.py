from numpy import sign, sqrt
from gui.utils import tk, Palette
from gui.templates import CanvasBase

class Joystick(CanvasBase):

    def __init__(self, parent, *args, **kwargs):
        super(Joystick, self).__init__(parent, *args, **kwargs)
        self.bind_mouse_key()
        self.config(
            bg=Palette.WHITE
        )

        # gli ID degli elementi grafici sono contenuti qui
        self.background = dict()
        self.cursor = list()

        self._cursor_posx = 0
        self._cursor_posy = 0
        self._cursor_offx = 0
        self._cursor_offy = 0
        self._camera_x =0.0
        self._camera_y =0.0
        self._rHole = 80
        self._flag_update = False

    @property
    def pov_change(self):
        flag = self._flag_update
        self._flag_update = False
        return flag

    @property
    def camera_x_speed(self):
        return self._camera_x

    @property
    def camera_y_speed(self):
        return self._camera_y

    def build(self, *args, **kwargs):
        super(Joystick, self).build(*args, **kwargs)

        # i 4 settori direzionali
        self.background['outer'] = list()
        self.background['outer'].append(self.create_arc(0,0,0,0, style=tk.PIESLICE))
        self.background['outer'].append(self.create_arc(0,0,0,0, style=tk.PIESLICE))
        self.background['outer'].append(self.create_arc(0,0,0,0, style=tk.PIESLICE))
        self.background['outer'].append(self.create_arc(0,0,0,0, style=tk.PIESLICE))

        for theta, arc in enumerate(self.background['outer']):
            self.itemconfig(
                arc,
                width=2,
                start=44 + theta * 90,
                extent=88,
                fill='black')

        # Sfondo e buco del joystick
        self.background['inner'] = self.create_oval(0,0,0,0)
        self.background['hole'] = self.create_oval(0,0,0,0)

        self.itemconfig(self.background['inner'], width=2, fill=Palette.WHITE)
        self.itemconfig(self.background['hole'],  fill=Palette.BLACK)

        self.cursor.append( self.create_oval(0,0,0,0) )
        self.itemconfig(self.cursor[0],  fill=Palette.WHITE)

    def on_motion(self, *event):
        super(Joystick, self).on_motion(*event)
        if self.current and self.current[0] == self.cursor[0] and self.mouse.on_click:

            delta_x = self.mouse.x - self._cursor_offx
            delta_y = self.mouse.y - self._cursor_offy

            # se il cursore esce dall'area del widget
            x2 = delta_x * delta_x
            y2 = delta_y * delta_y
            r2 = self._rHole * self._rHole
            if x2 + y2 > r2:
                try:
                    # prima Y perchè ho risolto per Y(x)
                    self._cursor_posy = sign(delta_y) * sqrt(r2 / (1 + x2 / y2))
                    self._cursor_posx = self._cursor_posy * delta_x / delta_y
                except ZeroDivisionError:
                    pass
            else:
                self._cursor_posy = delta_y
                self._cursor_posx = delta_x

            # aggiorna la velocità della camera
            self._flag_update = True
            self._camera_x = 0.9 * self._cursor_posx /  self._rHole
            self._camera_y = 0.9 * - self._cursor_posy /  self._rHole
            # 
            if abs(self._camera_x) < 0.1 and abs(self._camera_y) > 0.5 : self._camera_x = 0.0
            if abs(self._camera_y) < 0.1 and abs(self._camera_x) > 0.5 : self._camera_y = 0.0
            self.on_resize_cursor()

    def on_resize_cursor(self):
        w, h = self.winfo_width(), self.winfo_height()
        off = 10
        rc = self._rHole - off
        # viene riposizionato il cursore con le nuove coordinate
        self.coords(self.cursor[0],
                    (0.5 * w + self._cursor_posx - rc, 0.5 * h + self._cursor_posy - rc,
                     0.5 * w + self._cursor_posx + rc, 0.5 * h + self._cursor_posy + rc))

    def on_resize(self, *args, **kwargs):
        w,h = super(Joystick, self).on_resize(*args, **kwargs)

        off = 10
        shift = 7

        # draw dei 4 settori direzionali
        for item in self.background['outer']:
            self.coords(item,
                        (off, off, w - off, h - off))

        #draw del foro centrale
        self.coords(self.background['inner'],
                    (shift * off, shift * off, w - shift * off, h - shift * off))

        self.coords(self.background['hole'],
                    (0.5 * w - self._rHole, 0.5 * h - self._rHole,
                     0.5 * w + self._rHole, 0.5 * h + self._rHole))

        #draw del cursore
        self.on_resize_cursor()

    def on_mouse_press(self, *event):
        super(Joystick, self).on_mouse_press(*event)

        # viene premuto il cursore centrale
        if self.current and self.current[0] == self.cursor[0]:
            self._flag_update = True
            # reset dell'offset del mouse. on_motion() calcola la differenza
            self._cursor_offx = self.mouse.x
            self._cursor_offy = self.mouse.y
            self.itemconfig(self.cursor[0],
                            fill=Palette.RED
                            )
            return

        # viene premuto uno dei 4 settori direzionali
        arcs = [ arc for arc in self.background['outer'] if arc == self.current[0] ]
        if arcs:
            self._flag_update = True
            self.itemconfig(
                arcs[0],
                fill=Palette.RED
            )
            if arcs[0] == self.background['outer'][0]:
                self._camera_y = 1.0
            elif arcs[0] == self.background['outer'][1]:
                self._camera_x = -1.0
            elif arcs[0] == self.background['outer'][2]:
                self._camera_y = -1.0
            elif arcs[0] == self.background['outer'][3]:
                self._camera_x = 1.0

    def on_mouse_release(self, *event):
        super(Joystick, self).on_mouse_release(*event)

        # stop al brandeggio
        self._camera_x = 0.0
        self._camera_y = 0.0
        self._flag_update = True

        if self.current and self.current[0] == self.cursor[0]:
            # reset posizione cursore
            self._cursor_posx = 0.0
            self._cursor_posy = 0.0
            self.itemconfig(self.cursor[0],
                            fill=Palette.WHITE
                            )
            self.on_resize_cursor()

            #questo aggiorna l'id dell'oggetto sotto il mouse
            self.current = []
            self.on_motion()
            return

        ids = [ arc for arc in self.background['outer'] if arc == self.current[0] ]
        if ids:
            self.itemconfig(
                ids[0],
                fill=Palette.BLACK
            )
