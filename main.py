import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from classes import V2, Node, Rod, CoordCanvas, AppConfig, Force
from canvas_utils import draw_grid
from calculator import calculate_simple
from forces_table import update_forces_table

class MainWindow:
    nodes: list[Node]
    rods: list[Rod]
    forces: list[Force]

    selectedItem: Node | Rod = None
    
    canvas_width: int = 900
    canvas_height: int = 700
    last_drag_position: V2
    config: AppConfig

    workspace_mode: int = 0
    '''
        0 - selection
        1 - insert nodes
        2 - insert rods
        3 - insert force
    '''

    def __init__(self):
        root = tk.Tk()
        root.title("Теормех.СТАТИКА")
        
        top_bar = tk.Frame(root, pady=10)
        top_bar.pack(side=tk.TOP)

        canvas_frame = tk.Frame(root)
        canvas_frame.pack(side=tk.TOP)

        mode_label = tk.Label(top_bar, text="")
        mode_label.pack(side=tk.LEFT)
        self.mode_label = mode_label

        selection_btn = tk.Button(top_bar, text="Выделение", command=self.register_switch_mode_handler(0))
        selection_btn.pack(side=tk.LEFT)

        add_node_btn = tk.Button(top_bar, text="+ Узел", command=self.register_switch_mode_handler(1))
        add_node_btn.pack(side=tk.LEFT)

        add_rod_btn = tk.Button(top_bar, text='+ Стержень', command=self.register_switch_mode_handler(2))
        add_rod_btn.pack(side=tk.LEFT)

        add_force_btn = tk.Button(top_bar, text='+ Сила', command=self.register_switch_mode_handler(3))
        add_force_btn.pack(side=tk.LEFT)

        clear_space_btn = tk.Button(top_bar, text='Очистить область', command=self.handle_clear_space_btn)
        clear_space_btn.pack(side=tk.LEFT)

        calc_btn = tk.Button(top_bar, default='active', text='Рассчитать', command=self.calculate_schema)
        calc_btn.pack(side=tk.RIGHT)

        O_position=V2(self.canvas_width/2, self.canvas_height/2)
        canvas = CoordCanvas(canvas_frame, width=self.canvas_width, height=self.canvas_height, O_position=O_position, scale=1)
        canvas.bind("<Button-1>", self.canvas_clicked)
        canvas.bind('<B1-Motion>', self.on_drag)
        canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        #canvas.grid(column=0, row=0)

        canvas.pack(side=tk.LEFT)
        self.canvas = canvas

        info_frame = tk.Frame(canvas_frame)
        info_frame.pack()

        columns = ('title', 'X_proj', 'Y_proj')
        tree = ttk.Treeview(info_frame, columns=columns, show='headings')
        for col in columns:
            tree.column(col, width=100)
        # define headings
        tree.heading('title', text='Название')
        tree.heading('X_proj', text='Проекция на X')
        tree.heading('Y_proj', text='Проекция на Y')
        tree.pack(side=tk.TOP)
        self.forces_table = tree

        info_label = tk.Label(info_frame, text="Информация об объекте", padx=5)
        info_label.pack(side=tk.TOP)

        info_rewriteable_frame = tk.Frame(info_frame)
        info_rewriteable_frame.pack(side=tk.TOP)
        
        self.selected_obj_info_frame = info_rewriteable_frame
        
        self.nodes = []
        self.rods = []
        self.forces = []
        self.last_drag_position = V2(0, 0)
        self.config = AppConfig(selectionThreshold=10)

        self.root = root
        self.canvas_frame = canvas_frame

    def run(self):
        self.update_info_column()
        self.redraw_canvas()
        self.update_mode_label()
        self.root.mainloop()

    def on_mouse_wheel(self, event: tk.Event):
        self.canvas.scale *= 1 + (event.delta/10)
        self.redraw_canvas()

    def on_drag(self, event: tk.Event):
        pos: V2 = V2(event.x, event.y)
        if (pos - self.last_drag_position).norm() < 25:
            self.canvas.O_position = self.canvas.O_position + pos - self.last_drag_position
        
        self.last_drag_position = pos
        self.redraw_canvas()

    def canvas_clicked(self, event: tk.Event):
        click_pos: V2 = V2(event.x, event.y) # canvas coords

        # lets find global coords
        global_click_pos: V2 = self.canvas.toGlobalCoords(click_pos)
        '''
            Workspace modes
            0 - selection
            1 - insert nodes
            2 - insert rods
            3 - insert force
        '''
        if self.workspace_mode == 0:
            # detect nearest object
            finded_force = None
            minD = self.config.selectionThreshold+1
            for force in self.forces:
                force.is_selected = False
                dist = (force.arrow_canvas_coordinates-click_pos).norm()
                if dist < minD:
                    minD = dist
                    finded_force = force
            self.selectedItem = None
            if finded_force is not None:
                finded_force.is_selected = True
                self.selectedItem = finded_force

            index, alreadySelectedIndex = self.get_hearest_node(global_click_pos)
            if alreadySelectedIndex is not None:
                self.nodes[alreadySelectedIndex].is_selected = False
                self.selectedItem = None
            if index is not None:
                self.selectedItem = None # deselect
                if alreadySelectedIndex != index:
                    self.nodes[index].is_selected = True
                    self.selectedItem = self.nodes[index]
            

        elif self.workspace_mode == 1:
            self.nodes.append(Node(global_click_pos))
        elif self.workspace_mode == 2:
            index, alreadySelectedIndex = self.get_hearest_node(global_click_pos)
            
            if index is not None:
                self.nodes[index].is_selected = True
                if alreadySelectedIndex is not None and alreadySelectedIndex != index:
                    self.rods.append(Rod(self.nodes[index], self.nodes[alreadySelectedIndex]))
                    self.nodes[index].is_selected = False
                    self.nodes[alreadySelectedIndex].is_selected = False
                elif alreadySelectedIndex is not None:
                    self.nodes[index].is_selected = False
        elif self.workspace_mode == 3:
            # add force
            index, _ = self.get_hearest_node(global_click_pos)
            if index is not None:
                self.forces.append(Force(node=self.nodes[index], x=0, y=-10))

        self.redraw_canvas()
        self.update_info_column()

    def get_hearest_node(self, global_pos: V2):
        '''
            i. e: selected_index, already_selected_index = get_hearest_node(V2(...));
            if selected_index not exists - None;
            if already_selected_index not exits - None;
        '''
        index = None
        minDist = self.config.selectionThreshold + 1
        alreadySelectedIndex = None
        for (i, node) in enumerate(self.nodes):
            if node.is_selected:
                alreadySelectedIndex = i

            pos1 = global_pos
            pos2 = node.position
            dist = ((pos1.x-pos2.x)**2 + (pos1.y-pos2.y)**2)**(1/2)
            if dist <= self.config.selectionThreshold and dist < minDist:
                minDist = dist
                index = i
        return index, alreadySelectedIndex
    
    def calculate_schema(self):
        res = calculate_simple(self.forces)
        if not res:
            messagebox.showerror("Ошибка при рассчете", "Ошибка при рассчете: Неопределенных сил должно быть 3")
        else:
            self.update_info_column()

        self.redraw_canvas()

    def register_switch_mode_handler(self, mode: int):
        def handler():
            self.workspace_mode = mode
            self.update_mode_label()
        return handler
            
    def handle_clear_space_btn(self):
        self.selectedItem = None
        self.update_info_column()
        self.nodes.clear()
        self.rods.clear()
        self.forces.clear()
        self.redraw_canvas()

    def update_info_column(self):
        update_forces_table(self.forces_table, self.forces)
        for child in self.selected_obj_info_frame.winfo_children():
            child.destroy()
        
        frame = self.selected_obj_info_frame
        if self.selectedItem is None:
            text = "Ничего не выделено"
            label = tk.Label(frame, text=text)
            label.pack(side=tk.TOP)
        else:
            item_frame = self.selectedItem.get_info_frame(frame, self.redraw_canvas)
            item_frame.pack(side=tk.TOP)

        self.root.update()

    def update_mode_label(self):
        mode_str: str = ''
        mode = self.workspace_mode
        if mode == 0:
            mode_str = 'выделение'
        elif mode == 1:
            mode_str = '+ узел'
        elif mode == 2:
            mode_str = '+ стержень'
        else:
            mode_str = 'неопределен'
        self.mode_label.config(text='Режим: {}'.format(mode_str))
        self.root.update()

    def redraw_canvas(self):
        self.canvas.delete("all")
        self.canvas.update()
        draw_grid(self.canvas)

        self.forces = [f for f in self.forces if f.norm() != 0]

        for rod in self.rods:
            rod.draw(self.canvas)
        for node in self.nodes:
            node.draw(self.canvas)
        for force in self.forces:
            force.draw(self.canvas)
        self.root.update()


if __name__ == '__main__':
    window = MainWindow()
    window.run()