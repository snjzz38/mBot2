import time, event, cyberpi
import mbuild, mbot2

step = 0
target = 4

path = [(0,0), (1,0), (1,3), (3,3), (3,2), (4,2), (4,3), (5,3)]
direction = 0

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

def follow_the_line(num):
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
            cyberpi.console.print('.')
            #cyberpi.console.println(counter)
            counter = 0
            
        elif counter >= 400:
            cyberpi.console.print('#')
            step += 1
            counter -= avg

        elif mbuild.ultrasonic2.get(1) < 10:
            break
            
    mbot2.drive_power(0, 0)
    cyberpi.console.println(step)

def get_grid_distance():
    distance = mbuild.ultrasonic2.get(1)
    if distance == 300.0:
        mbot2.straight(-8)
        distance = mbuild.ultrasonic2.get(1)
        mbot2.straight(8)
    cyberpi.console.println(distance)   
    if distance > 0 and distance < 25.6:
        return 0
    elif distance > 25.6 and distance < 61.8:
        return 1
    elif distance > 61.8 and distance < 98:
        return 2
    elif distance > 98 and distance < 134.2:
        return 3
    elif distance > 134.2 and distance < 170.4:
        return 4
    elif distance > 170.4 and distance < 206.6:
        return 5
    else:
        return -1

@event.start
def on_start():
    cyberpi.console.println('A to start')
    cyberpi.console.println('B to stop')

@event.is_press('a')
def a_is_pressed():
    global target
    cyberpi.stop_other()
    back_to_base(path)

@event.is_press('b')
def b_is_pressed():
    cyberpi.stop_other()
    cyberpi.console.println('Stop Line Follower...')
    cyberpi.mbot2.drive_power(0, 0)
    h_distance = get_grid_distance()
    cyberpi.console.println(h_distance)
    mbot2.turn(90)
    v_distance = get_grid_distance()
    cyberpi.console.println(v_distance)
    mbot2.turn(-90)



