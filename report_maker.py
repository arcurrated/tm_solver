from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from classes import V2, Node, Rod, Force


def make_report(fname, nodes: list[Node], rods: list[Rod], forces: list[Force]):
    if len(nodes) == 0:
        return
    
    w: int = 500
    h: int = 700
    c: canvas.Canvas = canvas.Canvas(fname, bottomup=0, pagesize=(w, h))
    c.setAuthor('@arcurrated')

    # for UTF-8 support
    pdfmetrics.registerFont(TTFont('FreeSans','fonts/FreeSans.ttf'))
    tblstyle = TableStyle([('FONT', (0, 0), (-1, 1), 'FreeSans', 9)])
    c.setFont('FreeSans', 12)

    px: int = 50 # padding
    py: int = 50
    cursor: int = py # next element will be displayed on Y = cursor

    c.drawString(px, cursor, 'Схема: ')
    cursor += 20

    # 1. detect bounding rect of image (minX, maxX, minY, maxY)
    minX = None
    maxX = None
    minY = None
    maxY = None
    for node in nodes:
        if minX is None or node.position.x < minX:
            minX = node.position.x
        if maxX is None or node.position.x > maxX:
            maxX = node.position.x
        if minY is None or node.position.y < minY:
            minY = node.position.y
        if maxY is None or node.position.y > maxY:
            maxY = node.position.y
    # 2. calc scale and offset
    imgW = w-2*px # schema size on PDF
    imgH = 250
    #c.rect(px, cursor, imgW, imgH)

    offset: V2 = V2(-minX, -minY)
    dX = abs(maxX - minX)
    dY = abs(maxY - minY)
    scX = 0
    scY = 0
    if dX != 0:
        scX = imgW/dX
    if dY != 0:
        scY = imgH/dY
    scale: float = scX if scX < scY else scY

    # recalc imgH with scale and dY
    imgH = dY*scale

    cPosX = lambda x: px + (x + offset.x) * scale # canvas X position
    cPosY = lambda y: cursor+imgH-(y + offset.y) * scale # canvas Y position

    # 3. draw with this scale and offset
    for rod in rods:
        pos1: V2 = V2(0, 0)
        pos2: V2 = V2(0, 0)

        pos1.x = cPosX(rod.nodes[0].position.x)
        pos1.y = cPosY(rod.nodes[0].position.y)
        
        pos2.x = cPosX(rod.nodes[1].position.x)
        pos2.y = cPosY(rod.nodes[1].position.y)

        c.line(pos1.x, pos1.y, pos2.x, pos2.y)

    for node in nodes:
        posX = cPosX(node.position.x)
        posY = cPosY(node.position.y)
        c.setFillGray(0.8)
        c.circle(posX, posY, 5, fill=1)
        c.setFillGray(0)
        c.drawCentredString(posX-20, posY, node.title)

    for force in forces:
        source_pos = V2(cPosX(force.node.position.x), cPosY(force.node.position.y))
        arrow_pos, title_pos = force.get_relative_coords_for_drawing(30, 15)
        to_pos = source_pos + arrow_pos
        title_pos = source_pos + title_pos

        c.setLineWidth(2)
        c.line(source_pos.x, source_pos.y, to_pos.x, to_pos.y,)
        c.circle(to_pos.x, to_pos.y, 3, fill=1)
        c.setLineWidth(1)
        c.drawCentredString(title_pos.x, title_pos.y, force.title)
    cursor += imgH + 50

    # 4. print forces data
    t_width = (w-2*px)/2 - 10 # ширина одной таблицы
    rods_table_x = px+t_width + 10
    table_header_y = cursor

    c.drawString(px, table_header_y, 'Силы: ')
    cursor += 20

    forces_data = [('Имя', 'X проек.', 'Y проек.', 'Знач.')]
    for force in forces:
        forces_data.append((
            force.title, 
            round(force.x, 4) if force.defined else '-', 
            round(force.y, 4) if force.defined else '-',
            round(force.norm(), 4) if force.defined else '-'))

    # костыль для того, чтобы корректно везде отрисовывался UTF-8,
    # иначе читаются только две строчки, остальные - черные квадраты
    for i, el in enumerate(forces_data): 
        tmp = Table([el], style=tblstyle, colWidths=(t_width/len(el)))
        tmp.wrapOn(c, t_width, 20) # width, height
        tmp.drawOn(c, px, cursor+20*i, 1)

    # 5. print rods data
    c.drawString(rods_table_x, table_header_y, 'Стержни: ')
    rods_data = [('Нач.', 'Кон.', 'Усилие')]
    for rod in rods:
        rods_data.append((
            rod.nodes[0].title, rod.nodes[1].title,
            # round(rod.inner_force.x, 4) if rod.inner_force_defined else '-',
            # round(rod.inner_force.y, 4) if rod.inner_force_defined else '-',
            round(rod.inner_force.norm(), 4) * \
                (-1 if min(rod.inner_force.x, rod.inner_force.y) < 0 else 1) \
                    if rod.inner_force_defined else '-'
            # from A to B Value -10 means force directed opposite
        ))
    
    for i, el in enumerate(rods_data): 
        tmp = Table([el], style=tblstyle, colWidths=(t_width/len(el)))
        tmp.wrapOn(c, t_width, 20)
        tmp.drawOn(c, rods_table_x, cursor+20*i, 1)

    c.save()
    