from classes import CoordCanvas, V2
import tkinter as tk

def draw_grid(canvas: CoordCanvas):
    center: V2 = canvas.toCanvasCoords(V2(0, 0))
    # canvas.create_oval(center.x-10, center.y-10, center.x+10, center.y+10)
    
    top_left_corner = canvas.toGlobalCoords(V2(0, 0))
    bottom_right_corner = canvas.toGlobalCoords(V2(canvas.width, canvas.height))

    step = round(canvas.scale * 60, 2)
    if step == 0:
        return
    grid_color = "#777"
    text_color = "#aaa"
    canvas.create_text(center.x-10, center.y+10, text="0", fill=text_color)
    if top_left_corner.x < 0 and bottom_right_corner.x > 0:
        canvas.create_line(center.x, 0, center.x, canvas.height, fill='#FA6060')
        # draw from center both
        curr_x = step
        while True:
            canvas_curr_x = canvas.toCanvasCoords(V2(curr_x, 0)).x
            canvas.create_line(canvas_curr_x, 0, canvas_curr_x, canvas.height, fill=grid_color)
            canvas.create_text(canvas_curr_x, center.y+10, text=str(round(curr_x, 2)), fill=text_color)
            if canvas_curr_x > canvas.width:
                break
            curr_x += step
        curr_x = -step
        while True:
            canvas_curr_x = canvas.toCanvasCoords(V2(curr_x, 0)).x
            canvas.create_line(canvas_curr_x, 0, canvas_curr_x, canvas.height, fill=grid_color)
            canvas.create_text(canvas_curr_x, center.y+10, text=str(round(curr_x, 2)), fill=text_color)
            if canvas_curr_x < 0:
                break
            curr_x -= step
        
    elif top_left_corner.x > 0:
        # draw from center to right
        curr_x = step
        while True:
            canvas_curr_x = canvas.toCanvasCoords(V2(curr_x, 0)).x
            if canvas_curr_x < 0:
                curr_x += step
                continue

            canvas.create_line(canvas_curr_x, 0, canvas_curr_x, canvas.height, fill=grid_color)
            canvas.create_text(canvas_curr_x, center.y+10, text=str(round(curr_x, 2)), fill=text_color)
            if canvas_curr_x > canvas.width:
                break
            curr_x += step
    else:
        curr_x = -step
        while True:
            canvas_curr_x = canvas.toCanvasCoords(V2(curr_x, 0)).x
            if canvas_curr_x > canvas.width:
                curr_x -= step
                continue
            canvas.create_line(canvas_curr_x, 0, canvas_curr_x, canvas.height, fill=grid_color)
            canvas.create_text(canvas_curr_x, center.y+10, text=str(round(curr_x, 2)), fill=text_color)
            if canvas_curr_x < 0:
                break
            curr_x -= step
        # draw from center to left

    if top_left_corner.y > 0 and bottom_right_corner.y < 0:
        canvas.create_line(0, center.y, canvas.width, center.y, fill='#FA6060')
        # draw from center both
        curr_y = step
        while True:
            canvas_curr_y = canvas.toCanvasCoords(V2(0, curr_y)).y
            canvas.create_line(0, canvas_curr_y, canvas.width, canvas_curr_y, fill=grid_color)
            canvas.create_text(center.x-10, canvas_curr_y, text=str(round(curr_y, 2)), anchor=tk.E, fill=text_color)
            if canvas_curr_y < 0:
                break
            curr_y += step
        curr_y = -step
        while True:
            canvas_curr_y = canvas.toCanvasCoords(V2(0, curr_y)).y
            canvas.create_line(0, canvas_curr_y, canvas.width, canvas_curr_y, fill=grid_color)
            canvas.create_text(center.x-10, canvas_curr_y, text=str(round(curr_y, 2)), anchor=tk.E, fill=text_color)
            if canvas_curr_y > canvas.height:
                break
            curr_y -= step
        
    elif top_left_corner.y < 0:
        # draw from center to bottom
        curr_y = -step
        while True:
            canvas_curr_y = canvas.toCanvasCoords(V2(0, curr_y)).y
            if canvas_curr_y < 0:
                curr_y -= step
                continue

            canvas.create_line(0, canvas_curr_y, canvas.width, canvas_curr_y, fill=grid_color)
            canvas.create_text(center.x-10, canvas_curr_y, text=str(round(curr_y, 2)), anchor=tk.E, fill=text_color)
            if canvas_curr_y > canvas.height:
                break
            curr_y -= step
    else:
        curr_y = step
        while True:
            canvas_curr_y = canvas.toCanvasCoords(V2(0, curr_y)).y
            if canvas_curr_y > canvas.height:
                curr_y += step
                continue
            canvas.create_line(0, canvas_curr_y, canvas.width, canvas_curr_y, fill=grid_color)
            canvas.create_text(center.x-10, canvas_curr_y, text=str(round(curr_y, 2)), anchor=tk.E, fill=text_color)
            if canvas_curr_y < 0:
                break
            curr_y += step
        # draw from center to left
