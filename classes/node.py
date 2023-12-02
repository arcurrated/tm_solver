from .v2 import V2
from .coord_canvas import CoordCanvas
import tkinter as tk

class Node:
    position: V2
    is_selected: bool
    title: str

    def __init__(self, position: V2, title = ''):
        self.position = position
        self.is_selected = False
        self.title = title

    def draw(self, canvas: CoordCanvas):
        pos = canvas.toCanvasCoords(self.position)

        width = 4 if self.is_selected else 1
        canvas.create_oval(pos.x-5, pos.y-5, pos.x+5, pos.y+5, width=width, fill='#444')
        canvas.create_text(pos.x-8, pos.y, anchor=tk.E, text=self.title)

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
        
        x_input_group = tk.Frame(frame, pady=5)
        
        x_label = tk.Label(x_input_group, text='X: ')
        x_label.pack(side=tk.LEFT)

        x_entry = tk.Entry(x_input_group, width=10)
        x_entry.insert(0, str(self.position.x))
        x_entry.pack(side=tk.LEFT)

        x_input_group.pack(side=tk.TOP)

        ## y
        y_input_group = tk.Frame(frame, pady=5)
        
        y_label = tk.Label(y_input_group, text='Y: ')
        y_label.pack(side=tk.LEFT)

        y_entry = tk.Entry(y_input_group, width=10)
        y_entry.insert(0, str(self.position.y))
        y_entry.pack(side=tk.LEFT)

        y_input_group.pack(side=tk.TOP)

        def save():
            self.position.x = float(x_entry.get())
            self.position.y = float(y_entry.get())
            self.title = title_entry.get()
            callback()
        save_btn = tk.Button(frame, text="Сохранить", default='active', command=save)
        save_btn.pack(side=tk.TOP)

        return frame