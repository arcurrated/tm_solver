from reportlab.pdfgen import canvas
from classes import V2, Node, Rod, Force


def make_report(fname, nodes: list[Node], rods: list[Rod], forces: list[Force]):
    if len(nodes) == 0:
        return
    
    w: int = 500
    h: int = 700
    c: canvas.Canvas = canvas.Canvas(fname, bottomup=0, pagesize=(w, h))
    c.setAuthor('@arcurrated')

    px: int = 50 # padding
    py: int = 50
    cursor: int = px # next element will be displayed on Y = cursor

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
    imgH = 300
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
        c.circle(posX, posY, 5, fill=1)
        c.drawString(posX-20, posY, node.title)

    for force in forces:
        source_pos = V2(cPosX(force.node.position.x), cPosY(force.node.position.y))
        arrow_pos, title_pos = force.get_relative_coords_for_drawing(30, 10)
        to_pos = source_pos + arrow_pos
        title_pos = source_pos + title_pos

        c.setLineWidth(4)
        c.line(source_pos.x, source_pos.y, to_pos.x, to_pos.y,)
        c.circle(to_pos.x, to_pos.y, 6, fill=1)
        c.setLineWidth(1)
        c.drawString(title_pos.x, title_pos.y, force.title)


    # 4. print forces data
    # 5. print rods data

    cursor += imgH

    c.line(0, cursor, 100, cursor+100)
    c.circle(10, cursor+20, 5)
    c.drawString(50, cursor+10, 'hehe')

    c.save()
    