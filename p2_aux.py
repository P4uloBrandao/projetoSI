def line(x, y, dx, dy, length):
    """Uma linha de células de comprimento 'length' começando em (x, y) na direcção (dx, dy)."""
    return {(x + i * dx, y + i * dy) for i in range(length)}

def quadro(x, y, length):
    """Uma moldura quadrada de células de comprimento 'length' começando no topo esquerdo (x, y)."""
    return line(x,y,0,1,length) | line(x+length-1,y,0,1,length) | line(x,y,1,0,length) | line(x,y+length-1,1,0,length)

def manhatan(p,q):
    (x1,y1) = p
    (x2,y2) = q
    return abs(x1-x2) + abs(y1-y2)


def display(pacman,pastilha,obstaculos,path=[]):
    """ print the state please"""
    osXs={x for (x,_) in obstaculos | {pastilha, pacman}}
    minX=min(osXs)
    maxX=max(osXs)
    osYs={y for (_,y) in obstaculos | {pastilha, pacman}}
    minY=min(osYs)
    maxY=max(osYs)
    output=""
    for j in range(minY,maxY+1):
        for i in range(minX,maxX+1):
            if pacman ==(i,j):
                ch = '@'
            elif pastilha==(i,j):
                ch = "*"
            elif (i,j) in obstaculos:
                ch = "#"
            elif (i,j) in path:
                ch = '+'
            else:
                ch = "."
            output += ch + " "
        output += "\n"
    print(output)
