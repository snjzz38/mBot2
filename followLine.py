import time, event, cyberpi
import mbuild, mbot2

step = 0
target = 4

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

@event.start
def on_start():
    cyberpi.console.println('A to start')
    cyberpi.console.println('B to stop')

@event.is_press('a')
def a_is_pressed():
    global target
    cyberpi.stop_other()
    follow_the_line(target)

@event.is_press('b')
def b_is_pressed():
    cyberpi.stop_other()
    cyberpi.console.println('Stop Line Follower...')
    cyberpi.mbot2.drive_power(0, 0)
    h = mbuild.ultrasonic2.get(1)
    cyberpi.console.println(h)
    mbot2.turn(90)
    v = mbuild.ultrasonic2.get(1)
    cyberpi.console.println(v)
    mbot2.turn(-90)

