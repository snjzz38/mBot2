import time, event, cyberpi
import mbuild, mbot2

step = 0
target = 4

rows = [
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1]    
]

columns = [
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1],
    [-1, -1, -1]
]

rowMatrixRowIndex = -1
rowMatrixColIndex = -1
colMatrixRowIndex = 6
colMatrixColIndex = 2
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


def back_to_base(path):
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
            cyberpi.console.println(diff)
            follow_the_line(diff)
    
    cyberpi.led.set_bri(500)
    cyberpi.led.play("flash_red")
    cyberpi.audio.set_vol(50)
    cyberpi.audio.play("wow")
    time.sleep(3)
    cyberpi.led.off(id = "all")
    cyberpi.audio.set_vol(0)


def detect_obstacles():
    global x, y, rows, columns, direction
    distance = mbuild.ultrasonic2.get(1)
    if distance == 300.0:
        mbot2.straight(-8)
        distance = mbuild.ultrasonic2.get(1)
        mbot2.straight(8)
    cyberpi.console.println(distance)
    offset = -1
    if distance > 0 and distance < 25.6:
        offset = 0
    elif distance > 25.6 and distance < 61.8:
        offset = 1
    elif distance > 61.8 and distance < 98:
        offset = 2
    elif distance > 98 and distance < 134.2 and direction <= 1: 
        offset = 3
    elif distance > 134.2 and distance < 170.4 and direction <= 1:
        offset = 4
    elif distance > 170.4 and distance < 206.6 and direction <= 1:
        offset = 5
 
    if direction == 0:
        if offset == -1:
            for i in range(6-x):
                rows[y][x+i] = 0
        elif offset >= 0 and x+offset < 6:
            for i in range(offset+1):
                if i < offset:
                    rows[y][i+x] = 0
                else:
                    rows[y][i+x] = 1
        elif x+offset >= 6:
            offset = -1
            for i in range(6-x):
                rows[y][x+i] = 0

    elif direction == 1:
        if offset == -1:
            for i in range(x):
                rows[y][i] = 0
        elif offset >= 0 and offset < x:
            for i in range(offset+1):
                if i < offset:
                    rows[y][x-i-1] = 0
                else:
                    rows[y][x-i-1] = 1
        elif offset >= x:
            offset = -1
            for i in range(x):
                rows[y][i] = 0

    elif direction == 2:
        if offset == -1:
            for i in range(y):
                columns[x][i] = 0
        elif offset >= 0 and offset < y:
            for i in range(offset+1):
                if i < offset:
                    columns[x][y-i-1] = 0
                else:
                    columns[x][y-i-1] = 1
        elif offset >= y:
            offset = -1
            for i in range(y):
                columns[x][i] = 0

    elif direction == 3:
        if offset == -1:
            for i in range(3-y):
                columns[x][y+i] = 0
        elif offset >= 0 and y+offset < 3:
            for i in range(offset+1):
                if i < offset:
                    columns[x][y+i] = 0
                else:
                    columns[x][y+i] = 1
        elif y+offset >= 3:
            offset = -1
            for i in range(3-y):
                columns[x][y+i] = 0

    cyberpi.console.println(offset)


def maketurn(new_direction):
    global direction
    cyberpi.console.print(direction)
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
        cyberpi.led.set_bri(500)
        cyberpi.led.play("meteor_green")
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


def find_survivor_group(x, y, level):
    global path, rows, columns
    path.append((x, y))
    
    if pick_up_group(x, y) == True:
        cyberpi.console.println(path)
        # newPath = path_processing(path)
        back_to_base(path)
        return 1

    #right    
    if (x < 6):
        if rows[y][x] == -1:
            maketurn(0)
            detect_obstacles()
        if rows[y][x] == 0:
            follow_the_line(1) 
            if (x+1, y) not in path:
                #cyberpi.console.println("-> Right")
                if find_survivor_group(x+1, y, level+1) == 1:
                    return 1

    #down
    if (y < 3):
        if columns[x][y] == -1:
            maketurn(3)
            cyberpi.console.println("ghjsz")
            detect_obstacles()
        if columns[x][y] == 0:
            follow_the_line(1)
            if (x, y+1) not in path:
                #cyberpi.console.println("-> Down")
                if find_survivor_group(x, y+1, level+1) == 1:
                    return 1

    #left
    if (x > 0):
        if rows[y][x-1] == -1:
            maketurn(1)
            detect_obstacles()
        if rows[y][x-1] == 0:
            follow_the_line(1)
            if (x-1, y) not in path:
                #cyberpi.console.println("-> Left")
                if find_survivor_group(x-1, y, level+1) == 1:
                    return 1

    #up
    if (y > 0):
        if columns[x][y-1] == -1:
            maketurn(2)
            detect_obstacles()
        if columns[x][y-1] == 0:
            follow_the_line(1)
            if (x, y-1) not in path:
                #cyberpi.console.println("-> Up")
                if find_survivor_group(x, y-1, level+1) == 1:
                    return 1

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
    cyberpi.console.println('Stop Line Follower...')
    cyberpi.mbot2.drive_power(0, 0)







