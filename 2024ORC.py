rows = [
    [0, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 1],
    [1, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 0, 0]    
]

columns = [
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0],
    [0, 0, 0]
]

rowMatrixRowIndex = -1
rowMatrixColIndex = -1
colMatrixRowIndex = 6
colMatrixColIndex = 2
onRow = False

x = 0
y = 0
direction = 0
level = 0
path = []

if colMatrixRowIndex == -1 and colMatrixColIndex == -1:
    onRow = True
    targetX = [rowMatrixColIndex, rowMatrixColIndex+1]
    targetY = rowMatrixRowIndex
    print("targetX=", targetX, "targetY=", targetY)
else:
    onRow = False
    targetX = colMatrixRowIndex
    targetY = [colMatrixColIndex, colMatrixColIndex+1]
    print("targetX=", targetX, "targetY=", targetY)

def find_survivor_group(x, y, level):
    global targetX, targetY, path, onRow
    path.append((x, y))
    
    if onRow:
        if x in targetX and y == targetY:
            print("Find Row", level)
            print(path)
            return 1
    else:
        if x == targetX and y in targetY:
            print("Find Column", level)
            print(path)
            return 1
    
    #right    
    if (x < 6 and rows[y][x] == 0):
        if (x+1, y) not in path:
            print("X=", x,"Y=", y, "move right")
            if find_survivor_group(x+1, y, level+1) == 1:
                return 1
        
    #down
    if (y < 3 and columns[x][y] == 0):
        if (x, y+1) not in path:
            print("X=", x,"Y=", y, "move down")
            if find_survivor_group(x, y+1, level+1) == 1:
                return 1

    #up
    if (y > 0 and columns[x][y-1] == 0):
        if (x, y-1) not in path:
            print("X=", x,"Y=", y, "move up")
            if find_survivor_group(x, y-1, level+1) == 1:
                return 1

    #left
    if (x > 0 and rows[y][x-1] == 0):
        if (x-1, y) not in path:
            print("X=", x,"Y=", y, "move left")
            if find_survivor_group(x-1, y, level+1) == 1:
                return 1

    path.pop()
    return 0
    
print("START")
if find_survivor_group(x, y, level) == 0:
    print("NO ANSWER")
else:
    print("PASSED")
        

