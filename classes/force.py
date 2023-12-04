from .v2 import V2
from .node import Node
from .coord_canvas import CoordCanvas
import tkinter as tk

class Force(V2):
    node: Node
    defined: bool
    is_selected: bool
    title: str
    
    arrow_canvas_coordinates: V2

    def __init__(self, node: Node, x: float, y: float, defined: bool = True, title: str = ''):
        self.defined = defined
        self.is_selected = False
        self.arrow_canvas_coordinates = None
        self.title = title

        super().__init__(x, y)
        self.node = node
    
    def __str__(self):
        return "x: {}, y: {}, norm: {}, defined: {}".format(self.x, self.y, self.norm(), self.defined)

    def draw(self, canvas: CoordCanvas):
        pos = canvas.toCanvasCoords(self.node.position)
        arrow_length = 50

        cos = self.x/self.norm()
        sin = -self.y/self.norm()

        to = pos + V2(
            arrow_length*cos,
            arrow_length*sin
        )

        self.arrow_canvas_coordinates = to # for handle clicks

        title_pos = to + V2(
            15*sin, -15*cos
        )
        color = '#F9CE5F' if self.defined else '#bbb'

        width = 4 if self.is_selected else 2
        canvas.create_oval(pos.x-width, pos.y-width, pos.x+width, pos.y+width, fill=color, outline="")
        canvas.create_line(pos.x, pos.y, to.x, to.y, width=width, fill=color, arrow='last')
        canvas.create_text(title_pos.x, title_pos.y, text=self.title, justify=tk.CENTER)

    def get_info_frame(self, parent: tk.Misc, callback = lambda: 1) -> tk.Frame:
        frame: tk.Frame = tk.Frame(parent)
        frame.pack(side=tk.TOP)

        title_input_group = tk.Frame(frame, pady=5)
        title_label = tk.Label(title_input_group, text='Имя: ')
        title_label.pack(side=tk.LEFT)

        title_entry = tk.Entry(title_input_group, width=10)
        title_entry.insert(0, self.title)
        title_entry.pack(side=tk.LEFT)
        title_input_group.pack(side=tk.TOP)

        label = tk.Label(frame, text="Составляющие силы")
        label.pack(side=tk.TOP)
        
        x_input_group = tk.Frame(frame, pady=5)
        
        x_label = tk.Label(x_input_group, text='X: ')
        x_label.pack(side=tk.LEFT)

        x_entry = tk.Entry(x_input_group, width=10)
        x_entry.insert(0, str(self.x))
        x_entry.pack(side=tk.LEFT)

        #x_input_group.grid(column=0, row=0)
        x_input_group.pack(side=tk.TOP)

        ## y
        y_input_group = tk.Frame(frame, pady=5)
        
        y_label = tk.Label(y_input_group, text='Y: ')
        y_label.pack(side=tk.LEFT)

        y_entry = tk.Entry(y_input_group, width=10)
        y_entry.insert(0, str(self.y))
        y_entry.pack(side=tk.LEFT)

        #y_input_group.grid(column=0, row=1)
        y_input_group.pack(side=tk.TOP)

        tmp_defined = tk.BooleanVar(value=self.defined)
        defined_checkbox = tk.Checkbutton(frame, variable=tmp_defined, text='Определена', onvalue=True, offvalue=False)
        defined_checkbox.pack(side=tk.TOP)

        def save():
            self.x = float(x_entry.get())
            self.y = float(y_entry.get())
            self.defined = tmp_defined.get()
            self.title = title_entry.get()
            callback()
        save_btn = tk.Button(frame, text="Сохранить", default='active', command=save)
        #save_btn.grid(column=0, row=2)
        save_btn.pack(side=tk.TOP)

        return frame