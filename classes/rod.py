from .v2 import V2
from .node import Node
from .coord_canvas import CoordCanvas
import tkinter as tk

class Rod:
    nodes: list[Node]
    is_selected: bool

    # vector of inner force directed by delta nodes position
    inner_force: V2
    inner_force_defined: bool

    def __init__(self, node1: Node, node2: Node):
        self.is_selected = False
        self.nodes = [node1, node2]
        self.flush_force()

    def __str__(self):
        return "Rod: from {} to {}. Inner force {} defined: {}".format(self.nodes[0], self.nodes[1], self.inner_force, self.inner_force_defined)
    
    def flush_force(self):
        self.inner_force = self.nodes[1].position - self.nodes[0].position
        self.inner_force_defined = False

    def draw(self, canvas: CoordCanvas):
        pos1 = canvas.toCanvasCoords(self.nodes[0].position)
        pos2 = canvas.toCanvasCoords(self.nodes[1].position)
        width = 4 if self.is_selected else 1
        canvas.create_line(pos1.x, pos1.y, pos2.x, pos2.y, width=width)

    def get_info_frame(self, parent: tk.Misc, callback = lambda: 1) -> tk.Frame:
        frame: tk.Frame = tk.Frame(parent)
        frame.pack(side=tk.TOP)
        text="Стержень от {} к {}\nУсилие {} определено".format(self.nodes[0].title, self.nodes[1].title, "" if self.inner_force_defined else "не")
        if self.inner_force_defined:
            text += '\nУсилие: {}'.format(round(self.inner_force.norm(), 4))
        
        label = tk.Label(frame, text=text)
        label.pack(side=tk.TOP)

        return frame