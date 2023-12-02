from .v2 import V2
import tkinter as tk

class CoordCanvas(tk.Canvas):
    O_position: V2
    scale: float
    width: int
    height: int
    def __init__(self, *args, **kwargs):
        self.O_position = kwargs['O_position']
        self.scale = float(kwargs['scale'])
        # self.width = kwargs['width']
        # self.height = kwargs['height']
        del kwargs['O_position']
        del kwargs['scale']
        super().__init__(*args, **kwargs)

    def update(self):
        self.width = self.winfo_width()
        self.height = self.winfo_height()
    

    def toGlobalCoords(self, canvas_coords: V2) -> V2:
        tmp: V2 = canvas_coords - self.O_position
        tmp.y *= -1 # так как для холста положительное направление - вниз, для глобальных - вверх
        tmp = tmp * self.scale
        return tmp
    
    def toCanvasCoords(self, global_coords: V2) -> V2:
        tmp: V2 = V2(global_coords.x/self.scale, global_coords.y/self.scale)
        tmp.y *= -1
        tmp = tmp + self.O_position
        return tmp
    
    def globalCoordsInViewPort(self, global_coords: V2) -> bool:
        canvas_coords = self.toCanvasCoords(global_coords)
        if canvas_coords.x < 0 or canvas_coords.y < 0 \
            or canvas_coords.x > self.width or canvas_coords.y > self.height:
            return False
        return True