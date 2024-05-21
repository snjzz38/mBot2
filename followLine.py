import time, event, cyberpi
import mbuild, mbot2

step = 0
target = 4

rows = [[-1 for j in range(6)] for i in range(4)]
columns = [[-1 for j in range(3)] for i in range(7)]

rowMatrixRowIndex = -1
rowMatrixColIndex = -1
colMatrixRowIndex = 4
colMatrixColIndex = 2

xBoundary = 5

targetX = -1
targetY = -1 
onRow = False

x = 0
y = 0
direction = 0
level = 0
path = []


def init():
    global colMatrixColIndex, colMatrixRowIndex, rowMatrixRowIndex, rowMatrixColIndex, targetX, targetY, onRow
    if colMatrixRowIndex == -1 and colMatrixColIndex == -1:
        onRow = True
        targetX = [rowMatrixColIndex, rowMatrixColIndex+1]
        targetY = rowMatrixRowIndex
    else:
        onRow = False
        targetX = colMatrixRowIndex
        targetY = [colMatrixColIndex, colMatrixColIndex+1]

def follow_the_line(num):
    global direction, x, y
    sensor = 0
    base_power = 30
    kp = 0.1
    avg = 310
    counter = 0
    step = 0
    while step < num:
        counter += 1
        deviation = mbuild.quad_rgb_sensor.get_offset_track(index=1)
        left_power = base_power-kp*deviation
        right_power = -base_power-kp*deviation
        mbot2.drive_power(left_power, right_power)
        sensor = mbuild.quad_rgb_sensor.get_line_sta(index=1)
        if (counter > 300 and counter < 400) and (sensor == 15 or sensor == 7 or sensor == 14):
            step += 1
            if step == num:
                mbot2.straight(8)
            #cyberpi.console.print('.')
            #cyberpi.console.println(counter)
            counter = 0
            
        elif counter >= 400:
            cyberpi.console.print('#')
            step += 1
            counter -= avg
            
    mbot2.drive_power(-1, 0)
    #cyberpi.console.println(step)
    if direction == 0:
        x += num
    elif direction == 1:
        x -= num
    elif direction == 2:
        y -= num
    elif direction == 3:
        y += num
    #cyberpi.console.print("X=")
    #cyberpi.console.print(x)
    #cyberpi.console.print(", Y=")
    #cyberpi.console.println(y)

def back_to_path(path):
    global direction
    route = path[::-1]
    for i in range(len(route)-1):
        if route[i][0] == route[i+1][0]:
            diff = abs(route[i][1] - route[i+1][1])
            if route[i][1] < route[i+1][1]:
                if direction == 0:
                    mbot2.turn(90)
                elif direction == 1:
                    mbot2.turn(-90)
                elif direction == 2:
                    mbot2.turn(180)
                direction = 3
            elif route[i][1] > route[i+1][1]:
                if direction == 0:
                    mbot2.turn(-90)
                elif direction == 1:
                    mbot2.turn(90)
                elif direction == 3:
                    mbot2.turn(180)
                direction = 2
            follow_the_line(diff)
        
        elif route[i][1] == route[i+1][1]:
            diff = abs(route[i][0] - route[i+1][0])
            if route[i][0] < route[i+1][0]:
                if direction == 1:
                    mbot2.turn(180)
                elif direction == 2:
                    mbot2.turn(90)
                elif direction == 3:
                    mbot2.turn(-90)
                direction = 0
            elif route[i][0] > route[i+1][0]:
                if direction == 0:
                    mbot2.turn(180)
                elif direction == 2:
                    mbot2.turn(-90)
                elif direction == 3:
                    mbot2.turn(90)
                direction = 1
            #cyberpi.console.println(diff)
            follow_the_line(diff)
    
    if route[-1] == (0,0):
        cyberpi.led.set_bri(500)
        cyberpi.led.play("flash_red")
        cyberpi.audio.set_vol(50)
        cyberpi.audio.play("wow")
        time.sleep(3)
        cyberpi.led.off(id = "all")
        cyberpi.audio.set_vol(0)

def detect_obstacles():
    global x, y, rows, columns, direction
    for i in range(5):
        distance = mbuild.ultrasonic2.get(1)
    if distance == 300.0:
        mbot2.straight(-5)
        for i in range(5):
            distance = mbuild.ultrasonic2.get(1)
        mbot2.straight(5)
    #cyberpi.console.println(distance)
    offset = 0
    if distance > 0 and distance < 25.6:
        offset = 1
    if direction == 0:
        rows[y][x] = offset
    elif direction == 1:
        rows[y][x-1] = offset
    elif direction == 2:
        columns[x][y-1] = offset
    elif direction == 3:
        columns[x][y] = offset
    return offset

# def detect_obstacles():
#     global x, y, rows, columns, direction
#     cyberpi.console.print("DIR=")
#     cyberpi.console.println(direction)
#     cyberpi.console.print("dis=")
#     for i in range(10):
#         distance = mbuild.ultrasonic2.get(1)
#     if distance == 300.0:
#         mbot2.straight(-5)
#         for i in range(10):
#             distance = mbuild.ultrasonic2.get(1)
#         mbot2.straight(5)
#     cyberpi.console.println(distance)
#     offset = -1
#     if distance > 0 and distance < 25.6:
#         offset = 0
#     elif distance > 25.6 and distance < 61.8:
#         offset = 1
#     elif distance > 61.8 and distance < 98:
#         offset = 2
#     elif distance > 98 and distance < 134.2 and direction <= 1: 
#         offset = 3
#     elif distance > 134.2 and distance < 170.4 and direction <= 1:
#         offset = 4
#     elif distance > 170.4 and distance < 206.6 and direction <= 1:
#         offset = 5
 
#     if direction == 0:
#         if offset == -1:
#             for i in range(6-x):
#                 rows[y][x+i] = 0
#         elif offset >= 0 and x+offset < 6:
#             for i in range(offset+1):
#                 if i < offset:
#                     rows[y][i+x] = 0
#                 else:
#                     rows[y][i+x] = 1
#         elif x+offset >= 6:
#             offset = -1
#             for i in range(6-x):
#                 rows[y][x+i] = 0

#     elif direction == 1:
#         if offset == -1:
#             for i in range(x):
#                 rows[y][i] = 0
#         elif offset >= 0 and offset < x:
#             for i in range(offset+1):
#                 if i < offset:
#                     rows[y][x-i-1] = 0
#                 else:
#                     rows[y][x-i-1] = 1
#         elif offset >= x:
#             offset = -1
#             for i in range(x):
#                 rows[y][i] = 0

#     elif direction == 2:
#         if offset == -1:
#             for i in range(y):
#                 columns[x][i] = 0
#         elif offset >= 0 and offset < y:
#             for i in range(offset+1):
#                 if i < offset:
#                     columns[x][y-i-1] = 0
#                 else:
#                     columns[x][y-i-1] = 1
#         elif offset >= y:
#             offset = -1
#             for i in range(y):
#                 columns[x][i] = 0

#     elif direction == 3:
#         if offset == -1:
#             for i in range(3-y):
#                 columns[x][y+i] = 0
#         elif offset >= 0 and y+offset < 3:
#             for i in range(offset+1):
#                 if i < offset:
#                     columns[x][y+i] = 0
#                 else:
#                     columns[x][y+i] = 1
#         elif y+offset >= 3:
#             offset = -1
#             for i in range(3-y):
#                 columns[x][y+i] = 0

#     cyberpi.console.println(offset)


def maketurn(new_direction):
    global direction
    if direction == new_direction:
        return
    
    if new_direction == 0:
        if direction == 1:
            mbot2.turn(180)
        elif direction == 2:
            mbot2.turn(90)
        elif direction == 3:
            mbot2.turn(-90)

    elif new_direction == 1:
        if direction == 0:
            mbot2.turn(180)
        elif direction == 2:
            mbot2.turn(-90)
        elif direction == 3:
            mbot2.turn(90)

    elif new_direction == 2:
        if direction == 0:
            mbot2.turn(-90)
        elif direction == 1:
            mbot2.turn(90)
        elif direction == 3:
            mbot2.turn(180)

    elif new_direction == 3:
        if direction == 0:
            mbot2.turn(90)
        elif direction == 1:
            mbot2.turn(-90)
        elif direction == 2:
            mbot2.turn(180)

    direction = new_direction

def pick_up_group(x, y):
    global targetX, targetY, direction, onRow
    found = False

    if onRow:
        if x == targetX[0] and y == targetY:
            if direction == 2:
                mbot2.turn(90)
            elif direction == 3:
                mbot2.turn(-90)
            direction = 0
            found = True
        elif x == targetX[1] and y == targetY:
            if direction == 2:
                mbot2.turn(-90)
            elif direction == 3:
                mbot2.turn(90)
            direction = 1
            found = True
    else:
        if x == targetX and y == targetY[0]:
            if direction == 0:
                mbot2.turn(90)
            elif direction == 1:
                mbot2.turn(-90)
            direction = 3
            found = True
        elif x == targetX and y == targetY[1]:
            if direction == 0:
                mbot2.turn(-90)
            elif direction == 1:
                mbot2.turn(90)
            direction = 2
            found = True
    if found:
        cyberpi.led.set_bri(100)
        cyberpi.led.show("green green green green green")
        cyberpi.audio.set_vol(75)
        cyberpi.audio.play("yeah")
        time.sleep(3)
        cyberpi.led.off(id = "all")
        cyberpi.audio.set_vol(0)

    return found 

def path_processing(path):
    newPath = []

    for i in range(len(path)):
        if i == 0 or i == len(path)-1:
            newPath.append(path[i])
        elif (path[i-1][0] == path[i][0] and path[i][0] != path[i+1][0]) or (path[i-1][1] == path[i][1] and path[i][1] != path[i+1][1]):
            newPath.append(path[i])
    return newPath

def find_shortcut(x, y):
    global targetX, targetY, direction, onRow
    originalDirection = direction
    newDirection = -1
    if onRow:
        if x==targetX[0] and y == targetY-1:
            maketurn(3)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 3
        elif x==targetX[0]-1 and y==targetY:
            maketurn(0)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 0
        elif x==targetX[0] and y == targetY+1:
            maketurn(2)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 2
        elif x==targetX[1] and y==targetY-1:
            maketurn(3)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 3
        elif x==targetX[1]+1 and y==targetY:
            maketurn(1)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 1
        elif x==targetX[1] and y==targetY+1:
            maketurn(2)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 2
    else:
        if x==targetX and y==targetY[0]-1:
            maketurn(3)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 3
        elif x==targetX-1 and y==targetY[0]:
            maketurn(0)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 0
        elif x==targetX+1 and y==targetY[0]:
            maketurn(1)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 1
        elif x==targetX and y==targetY[1]+1:
            maketurn(2)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 2
        elif x==targetX-1 and y==targetY[1]:
            maketurn(0)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 0
        elif x==targetX+1 and y==targetY[1]:
            maketurn(1)
            if detect_obstacles()==1:
                maketurn(originalDirection)
            else:
                newDirection = 1
    if newDirection != -1:
        follow_the_line(1)
    return newDirection

def find_survivor_group(x, y, level):
    global path, rows, columns
    path.append((x, y))
    
    if pick_up_group(x, y) == True:
        #cyberpi.console.println(path)
        #newPath = path_processing(path)
        back_to_path(path)
        return 1

    shortcut = find_shortcut(x, y)
    if shortcut == 0:
        if find_survivor_group(x+1, y, level+1) == 1:
            return 1
    elif shortcut == 1:
        if find_survivor_group(x-1, y, level+1) == 1:
            return 1
    elif shortcut == 2:
        if find_survivor_group(x, y-1, level+1) == 1:
            return 1
    elif shortcut == 3:
        if find_survivor_group(x, y+1, level+1) == 1:
            return 1

    #right    
    if (x < xBoundary):
        if (x+1, y) not in path:
            if rows[y][x] == -1:
                maketurn(0)
                detect_obstacles()
            if rows[y][x] == 0:
                maketurn(0)
                #cyberpi.console.println("-> Right")
                follow_the_line(1)            
                if find_survivor_group(x+1, y, level+1) == 1:
                    return 1

    #down
    if (y < 3):
        if (x, y+1) not in path:
            if columns[x][y] == -1:
                maketurn(3)
                detect_obstacles()
            if columns[x][y] == 0:
                maketurn(3)
                #cyberpi.console.println("-> Down")
                follow_the_line(1)
                if find_survivor_group(x, y+1, level+1) == 1:
                    return 1

    #up
    if (y > 0):
        if (x, y-1) not in path:
            if columns[x][y-1] == -1:
                maketurn(2)
                detect_obstacles()
            if columns[x][y-1] == 0:
                maketurn(2)
                #cyberpi.console.println("-> Up")
                follow_the_line(1)
                if find_survivor_group(x, y-1, level+1) == 1:
                    return 1

    #left
    if (x > 0):
        if (x-1, y) not in path:
            if rows[y][x-1] == -1:
                maketurn(1)
                detect_obstacles()
            if rows[y][x-1] == 0:
                maketurn(1)
                #cyberpi.console.println("-> Left")
                follow_the_line(1)
                if find_survivor_group(x-1, y, level+1) == 1:
                    return 1

    temp = []
    temp.append(path[-2])
    temp.append(path[-1])
    #cyberpi.console.println(temp)
    back_to_path(temp)
    cyberpi.audio.play("drop")
    path.pop()
    return 0

@event.start
def on_start():
    cyberpi.console.println('A to start')
    cyberpi.console.println('B to stop')
    init()

@event.is_press('a')
def a_is_pressed():
    global x, y, level
    cyberpi.stop_other()
    find_survivor_group(x, y, level)

@event.is_press('b')
def b_is_pressed():
    cyberpi.stop_other()
    cyberpi.console.println('Stop ...')
    cyberpi.mbot2.drive_power(0, 0)

