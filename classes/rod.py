from .v2 import V2
from .node import Node
from .coord_canvas import CoordCanvas

class Rod:
    nodes: list[Node]
    is_selected: bool

    def __init__(self, node1: V2, node2: V2):
        self.is_selected = False
        self.nodes = [node1, node2]

    def draw(self, canvas: CoordCanvas):
        pos1 = canvas.toCanvasCoords(self.nodes[0].position)
        pos2 = canvas.toCanvasCoords(self.nodes[1].position)
        width = 4 if self.is_selected else 1
        canvas.create_line(pos1.x, pos1.y, pos2.x, pos2.y, width=width)