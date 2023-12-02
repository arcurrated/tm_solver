from classes import Force
from tkinter import ttk
import tkinter as tk

def update_forces_table(table: ttk.Treeview, forces: list[Force]):
    table.delete(*table.get_children())

    for force in forces:
        vals = (force.title, '-' if not force.defined else force.x , '-' if not force.defined else force.y)
        table.insert('', tk.END, values=vals)