from copy import deepcopy 

def fill_puzzle(puzzle,sol):
    copia=deepcopy(puzzle)
    for s in sol:
        if isinstance(sol[s],int):
            xy=s.split('_')
            x=int(xy[1])
            y=int(xy[2])
            copia[y][x]='@' if sol[s] else '~'
    return copia
    
def puzzle_display(puzzle):
    compy=len(puzzle)
    compx=len(puzzle[0])
    for y in range(compy):
        for x in range(compx):
            print(puzzle[y][x],end=' ')
        print()