"""
    Spike_Firmware_Rig.py
    Date: 10/28/24
    Author: Tufts CEEO - William Goldman
    Purpose: Run multiple tests on the LEGO SPIKE to ensure that sensors and motors run properly with new firmware
"""

# Motor pair in C, E
# Light Matrix in A
# Distance Sensor in D
# Force Sensor in B
# Color Sensor in F

import motor, time, runloop, motor_pair, random, color, sys, device, color_sensor, color_matrix
import distance_sensor as ds
import force_sensor as fs
from hub import light_matrix, port, button, light, motion_sensor, sound

motor_left, motor_right, dis, forceS, sensor, matrix = 0, 0, 0, 0, 0, 0

result_array = [0] * 10 


"""
    Function Name: intro
    Function Purpose: Initializes the test environment and prompts the user to begin testing.
"""
def intro(z):
    global result_array

    try:
        sound.beep(550, 500, 100)
        light.color(light.POWER, color.GREEN)
    except Exception as e:
        print('There is something wrong with the sound or color system')
        print('\nTEST FAILED:', e)
        return
    
    ready = input("""
    *****************************SPIKE FIRMWARE TEST***************************
    * Tests to be completed: Hub Buttons, Hub Display, Hub IMU, Color Sensor, *
    *                        Light Matrix, Force Sensor, Distance Sensor,     *
    *                        Motors (Parallel, Independent), Gyroscope (TBD)  *
    *                                                                         *
    * Before Starting Tests, ensure testing rig is on a flat surface, away    *
    * from impeding objects.                                                  *
    *                                                                         *
    *                                                                         *
    *                   ARE YOU READY TO BEGIN TESTING? (y/n)                 *
    ***************************************************************************
    """)
    print('\n')
    
    while (not((ready.lower() == 'y') or (ready.lower() == 'n'))):
        print ("You DID NOT respond with a valid character")
        ready = input('ARE YOU READY TO BEGIN TESTING? (y/n)\n')
            
    if ready.lower() == 'n':
        print("You chose to exit the program. Terminating...")
        sys.exit()
    elif ready.lower() == 'y':
        print("Running tests...")
        
    result_array[z] = 1
    print('TEST PASSED: Moving onto port test...')



"""
    Function Name: hub_port_test
    Function Purpose: Test the ports of the LEGO SPIKE to ensure that the correct 
    devices are connected to the correct ports.
"""
def hub_port_test(z):
    global result_array
    print('\nRunning...')
    
    try: 
        light.color(light.POWER, color.RED)
#         device.id(port.A)
#         pwm = device.get_duty_cycle(port.A)
#         device.set_duty_cycle(port.A, pwm)   # pwm 0-10,000
#         device.ready(port.F)  # use for startup test
#         device.data(port.A)   # aw LPF-2 data from a device.

        device_type = {'61':'light', '62': 'dist', '63': 'force', '64': 'color_matrix',
                       '65': 'essentials motor', '48': 'medium motor', '49': 'large motor'}
        
        ports = [
                ['64', 'WRONG DEVICE IN PORT A: Please replace with the color matrix!', 'A'],
                ['63', 'WRONG DEVICE IN PORT B: Please replace with the force sensor!', 'B'],
                ['48', 'WRONG DEVICE IN PORT C: Please replace with a medium motor!', 'C'],
                ['62', 'WRONG DEVICE IN PORT D: Please replace with the distance sensor!', 'D'],
                ['48', 'WRONG DEVICE IN PORT E: Please replace with a medium motor!', 'E'],
                ['61', 'WRONG DEVICE IN PORT F: Please replace with the color sensor!', 'F']
            ]
    
        port_error = True

        def run_test():
            
            global port_error
            port_error = False
            
            for i in range(6):
                r = device.ready(i)
                if r:
                    if(str(device.id(i)) != ports[i][0]):
                        print(f"- {ports[i][1]}")
                        port_error = True
                else:
                    print(f"- NO DEVICE DETECTED IN PORT {ports[i][2]}")
                    port_error = True
            
            return port_error
            
            
        while port_error:
            if run_test():
                print("""
    ***********************************************************
    Please address the port assignment errors before continuing
    ***********************************************************
            """)
                print("Pausing for 5 seconds to allow for port reallocation...")
                time.sleep(5)
            else:
                result_array[z] = 1
                light.color(light.POWER, color.GREEN)
                print('TEST PASSED: Moving onto Hub Button test...')
                global motor_left, motor_right, dis, forceS, sensor, matrix
                motor_left, motor_right = port.C, port.E
                dis = port.D
                forceS = port.B
                sensor = port.F
                matrix = port.A
                motor_pair.pair(motor_pair.PAIR_1, motor_left, motor_right)
                
                break
        
        
    except Exception as e:
        print('TEST FAILED:', e)
        return
             

"""
    Function Name: hub_button_test
    Function Purpose: Test the buttons on the hub to ensure that they are 
    functioning properly.
"""
def hub_button_test(z):
    global result_array
    print('\nRunning...')

    try:
        light.color(light.POWER, color.RED)

        btn = {
            0:'left',
            1:'power',
            2:'right',
            3:'connect/bluetooth',
        }
        
        for num, name in btn.items():
            print('Press the', name, 'button')
            while not button.pressed(num): # Wait for the button to be pressed 
                pass
    #         print('pressed for %d msec'% (i))

        result_array[z] = 1
        light.color(light.POWER, color.GREEN)
        print('TEST PASSED: Moving onto hub display test...')
    except Exception as e:
        print('TEST FAILED:', e)
        return
        

"""
    Function Name: hub_display_test
    Function Purpose: Test the light matrix on the LEGO SPIKE by displaying a 
    series of images and text on the hub.
"""
def hub_display_test(z):
    global result_array
    print('\nRunning...')
    try:
        # Change the power button light to red (light.CONNECT gives the BLE btn)
        light.color(light.POWER, color.RED)

        light_matrix.clear()
        light_matrix.write("LEGO")
        # added to see full "Lego" printed
        time.sleep(2)   

        row,col,bright = 1,2,100
        light_matrix.set_pixel(col,row,bright)
#         print(light_matrix.get_pixel(row,col))

        images = [light_matrix.CANCELLED,
                    light_matrix.IMAGE_ANGRY,
                    light_matrix.IMAGE_ARROW_E,
                    light_matrix.IMAGE_ARROW_N,
                    light_matrix.IMAGE_ARROW_NE,
                    light_matrix.IMAGE_ARROW_NW,
                    light_matrix.IMAGE_ARROW_S,
                    light_matrix.IMAGE_ARROW_SE,
                    light_matrix.IMAGE_ARROW_SW,
                    light_matrix.IMAGE_ARROW_W,
                    light_matrix.IMAGE_ASLEEP,
                    light_matrix.IMAGE_BUTTERFLY,
                    light_matrix.IMAGE_CHESSBOARD,
                    light_matrix.IMAGE_CLOCK1,
                    light_matrix.IMAGE_CLOCK2,
                    light_matrix.IMAGE_CLOCK3,
                    light_matrix.IMAGE_CLOCK4,
                    light_matrix.IMAGE_CLOCK5,
                    light_matrix.IMAGE_CLOCK6,
                    light_matrix.IMAGE_CLOCK7,
                    light_matrix.IMAGE_CLOCK8,
                    light_matrix.IMAGE_CLOCK9,
                    light_matrix.IMAGE_CLOCK10,
                    light_matrix.IMAGE_CLOCK11,
                    light_matrix.IMAGE_CLOCK12,
                    light_matrix.IMAGE_CONFUSED,
                    light_matrix.IMAGE_COW,
                    light_matrix.IMAGE_DIAMOND,
                    light_matrix.IMAGE_DIAMOND_SMALL,
                    light_matrix.IMAGE_DUCK,
                    light_matrix.IMAGE_FABULOUS,
                    light_matrix.IMAGE_GHOST,
                    light_matrix.IMAGE_GIRAFFE,
                    light_matrix.IMAGE_GO_DOWN,
                    light_matrix.IMAGE_GO_LEFT,
                    light_matrix.IMAGE_GO_RIGHT,
                    light_matrix.IMAGE_GO_UP,
                    light_matrix.IMAGE_HAPPY,
                    light_matrix.IMAGE_HEART,
                    light_matrix.IMAGE_HEART_SMALL,
                    light_matrix.IMAGE_HOUSE,
                    light_matrix.IMAGE_MEH,
                    light_matrix.IMAGE_MUSIC_CROTCHET,
                    light_matrix.IMAGE_MUSIC_QUAVER,
                    light_matrix.IMAGE_MUSIC_QUAVERS,
                    light_matrix.IMAGE_NO,
                    light_matrix.IMAGE_PACMAN,
                    light_matrix.IMAGE_PITCHFORK,
                    light_matrix.IMAGE_RABBIT,
                    light_matrix.IMAGE_ROLLERSKATE,
                    light_matrix.IMAGE_SAD,
                    light_matrix.IMAGE_SILLY,
                    light_matrix.IMAGE_SKULL,
                    light_matrix.IMAGE_SMILE,
                    light_matrix.IMAGE_SNAKE,
                    light_matrix.IMAGE_SQUARE,
                    light_matrix.IMAGE_SQUARE_SMALL,
                    light_matrix.IMAGE_STICKFIGURE,
                    light_matrix.IMAGE_SURPRISED,
                    light_matrix.IMAGE_SWORD,
                    light_matrix.IMAGE_TARGET,
                    light_matrix.IMAGE_TORTOISE,
                    light_matrix.IMAGE_TRIANGLE,
                    light_matrix.IMAGE_TRIANGLE_LEFT,
                    light_matrix.IMAGE_TSHIRT,
                    light_matrix.IMAGE_UMBRELLA,
                    light_matrix.IMAGE_XMAS,
                    light_matrix.IMAGE_YES]
                    
        for i,image in enumerate(images):
#             print(i, image)
            light_matrix.show_image(image)
            time.sleep(0.1)     
            
        orientation={'up': 0, 'left': 1, 'down':2, 'right': 3}
            
        for o in orientation:
#             print(orientation[o])
            light_matrix.set_orientation(orientation[o])
            time.sleep(1)

        if not (light_matrix.get_orientation() == orientation['up']): 
            light_matrix.set_orientation(orientation['up'])


        # added for testing
        light_matrix.write(str(light_matrix.get_orientation()))
        time.sleep(1)   
        light_matrix.set_orientation(orientation['left'])
        light_matrix.write(str(light_matrix.get_orientation()))
        
        result_array[z] = 1
        light.color(light.POWER, color.GREEN)
        print('TEST PASSED: Moving onto hub IMU test...')
    except Exception as e:
        print('TEST FAILED:', e)
        return


"""
    Function Name: hub_imu_test
    Function Purpose: Test the Inertial Measurement Unit (IMU) by checking the
    tap count on the hub.
"""
def hub_imu_test(z):
    global result_array
    print('\nRunning...')

    try:
        light.color(light.POWER, color.RED)

        faces = {
            0:'HUB_FACE_TOP',
            1:'HUB_FACE_FRONT',
            2:'HUB_FACE_RIGHT',
            3:'HUB_FACE_BOTTOM',
            4:'HUB_FACE_BACK',
            5:'HUB_FACE_LEFT',
        }
        
        gestures = [
            motion_sensor.TAPPED,
            motion_sensor.DOUBLE_TAPPED,
            motion_sensor.SHAKEN,
            motion_sensor.FALLING,
            motion_sensor.UNKNOWN,
        ]
        
        Yaw_Face = [
            motion_sensor.TOP,    # The SPIKE Prime hub face with the USB charging port.
            motion_sensor.FRONT,  # The SPIKE Prime hub face with the Light Matrix.
            motion_sensor.RIGHT,  # The right side of the SPIKE Prime hub when facing the front hub face.
            motion_sensor.BOTTOM, # The side of the SPIKE Prime hub where the battery is.
            motion_sensor.BACK,   # The SPIKE Prime hub face where the speaker is.
            motion_sensor.LEFT,   # The left side of the SPIKE Prime hub when facing the front hub face.
        ]

        motion_sensor.get_yaw_face()
        motion_sensor.stable()  # True means not moving
        motion_sensor.gesture()
        motion_sensor.tilt_angles() # yaw pitch and roll values as integers. Values are decidegrees
        faces[motion_sensor.up_face()]
        motion_sensor.quaternion()
        motion_sensor.acceleration() #The values are mili G, so 1 / 1000 G
        motion_sensor.angular_velocity() # The values are decidegrees per second

        def run_test():
            motion_sensor.reset_tap_count()
            print('Tap the top of the SPIKE (Record the number of taps)')
            time.sleep(5)
        
        num_tests = 0
        
        while True:
            run_test()
            response = input('Was this the number of taps: %s? (y/n)\n' % (motion_sensor.tap_count()))
            
            while (not((response.lower() == 'y') or (response.lower() == 'n'))):
                print ("You DID NOT respond with a valid character")
                response = input('Was this the number of taps: %s? (y/n)\n' % (motion_sensor.tap_count()))
                
            if response.lower() == 'n':
                if num_tests < 2:
                    print("Try again...")
                    num_tests += 1
                else:
                    print("ERROR: Hub IMU malfunction determined by user testing.")
                    return
            elif response.lower() == 'y':
                result_array[z] = 1
                light.color(light.POWER, color.GREEN)
                print('TEST PASSED: Moving onto Distance Sensor test...')
                break
        
    except Exception as e:
        print('TEST FAILED:', e)
        return
     

"""
    Function Name: distance_sensor_test
    Function Purpose: Check the lights and distance readings on the distance sensor.
"""
def distance_sensor_test(z):
    global result_array
    print('\nRunning...')

    try:
        light.color(light.POWER, color.RED)
        # Get distance from object of distance sensor connected to port D
        for i in range(10):
            distance_var = ds.distance(dis)
            # print(ds.distance(dis))
            time.sleep(0.1)
            
        # messing around with the lights on the distance sensor

        ds.clear(dis)

        max_bright = 100
        ds.show(dis, [max_bright]*4)

        row,col = 1,0  # 2 rows, 2 cols
        ds.get_pixel(dis,row,col)
        ds.set_pixel(dis,row,col,80)

        for b in range(50):
            ds.show(dis, [b]*4)
            time.sleep(0.1)
    except Exception as e:
        print('TEST FAILED:', e)
        return
    
    result_array[z] = 1
    light.color(light.POWER, color.GREEN)
    print('TEST PASSED: Moving onto Parallel Motor test...')


"""
    Function Name: motor_parallel_test
    Function Purpose: Run the two motors together both extents of the rig to check 
    behavior when skipping and stopping.
"""
def motor_parallel_test(z):
    global result_array
    print('\nRunning...')

    print('BEFORE THIS TEST BEGINS, ENGAGE THE PARALLEL MOTOR LOCK')
    response = input('Did you engage the lock? (y/n)\n')
    while (not(response.lower() == 'y')):
        if response.lower() == 'n':
            print("You MUST engage the lock to continue.")
        else:
            print ("You DID NOT respond with a valid character")
        response = input('Did you engage the lock? (y/n)\n')

    distance = ds.distance(dis)
    try:        
        light.color(light.POWER, color.RED)
        # Move the motors to the extremes of the rig
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 
                            -10,                 # degrees (relative)
                            100,                # left speed (deg/sec)
                            100)               # right speed (deg/sec)
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 10, 100, 100)
        
        while (distance > 40):
            distance = ds.distance(dis)
#             print(ds.distance(dis))
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -10, 100, 100)
            time.sleep(0.1)
            
        while (distance < 57):
            distance = ds.distance(dis)
#             print(ds.distance(dis))
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 10, 100, 100)
            time.sleep(0.1)
        
    except Exception as e:
        print('TEST FAILED:', e)
        return
    
    result_array[z] = 1
    light.color(light.POWER, color.GREEN)
    print('TEST PASSED: Moving onto Force Sensor test...')


"""
    Function Name: fofce_sensor_test
    Function Purpose: Ensure force sensor functionality by pressing it
"""
def force_sensor_test(z):
    global result_array
    print('\nRunning...')
    
    distance = ds.distance(dis)
    try:
        light.color(light.POWER, color.RED)

        while (distance > 40):
            distance = ds.distance(dis)
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -10, 100, 100)
            time.sleep(0.1)

        fs.pressed(forceS)
#         print(fs.raw(port.B))
        
        force = fs.force(forceS)
        for i in range(10):
            force = fs.force(forceS)
#             print(fs.force(forceS))
            time.sleep(0.1)
        
        while (distance < 57):
#             print(fs.force(forceS))
            distance = ds.distance(dis)
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 10, 100, 100)
            time.sleep(0.1)
            
    except Exception as e:
        print('TEST FAILED:', e)
        return
    
    result_array[z] = 1
    light.color(light.POWER, color.GREEN)
    print('TEST PASSED: Moving onto Color Sensor and Light Matrix test...')


"""
    Function Name: color_sensor_light_matrix_test
    Function Purpose: Test the color sensor and light matrix by displaying colors 
    reading and displaying 'slide' colors on the light matrix.
"""
def color_sensor_light_matrix_test(z):
    global result_array
    print('\nRunning...')

    try:
        light.color(light.POWER, color.RED)
        # Get color - see Defines.py for the list of colors
        colors = {
            -1:'ERR',
            0:"LEGO_BLACK",
            1:"LEGO_MAGENTA",
            2:"LEGO_PURPLE",
            3:"LEGO_BLUE",
            4:"LEGO_AZURE",
            5:"LEGO_TURQUOISE",
            6:"LEGO_GREEN",
            7:"LEGO_YELLOW",
            8:"LEGO_ORANGE",
            9:"LEGO_RED",
            10:"LEGO_WHITE",
            11:"LEGO_DIM_WHITE",
        }
        
        # light matrix test run first
        color_matrix.clear(0)  
        (row, col, brightness) = (2, 0, 10)
        
        for colorA in range(len(colors) - 2):
            if colorA > -1:
                col = colorA % 3
                row = int(colorA/3) if colorA < 9 else int((colorA-9)/3)
                color_matrix.set_pixel(matrix, col, row, (colorA, brightness))
                time.sleep(0.1)

        # Begin color sensor reading onto light matrix
        i_see = colors[color_sensor.color(sensor)]
        color_sensor.reflection(sensor)
        color_sensor.rgbi(sensor)  #RGBI
        # print(color_sensor.rgbi(sensor))
        # print(color_sensor.reflection(sensor))
        
        color_matrix.clear(0)
        for i in range(3):
            color_matrix.set_pixel(matrix, i, 0, (10, brightness))
        for i in range(3):
            color_matrix.set_pixel(matrix, i, 2, (10, brightness))
        
        for i in range(2):
            color_matrix.set_pixel(matrix, i, 1, (color_sensor.color(sensor), brightness))
            time.sleep(1)
            motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -65, 100, 100)
            time.sleep(1)
        color_matrix.set_pixel(matrix, 2, 1, (color_sensor.color(sensor), brightness))
        
        response = input('Do the colors on the light matrix match your color slide? (y/n)\n')
        while (not((response.lower() == 'y') or (response.lower() == 'n'))):
            print ("You DID NOT respond with a valid character")
            response = input('Do the colors on the light matrix match your color slide? (y/n)\n')
            
        if response.lower() == 'n':
            print('TEST FAILED: Moving onto Independent Motor test...')
            return
        
    except Exception as e:
        print('TEST FAILED:', e)
        return
    
    result_array[z] = 1
    light.color(light.POWER, color.GREEN)
    print('TEST PASSED: Moving onto Independent Motor test...')
    
    
"""
    Function Name: motor_independent_test
    Function Purpose: Test the motors by running them in independtly of eachother
    and ensuring that after the tests they return to the same position.
"""
def motor_independent_test(z):
    global result_array
    print('\nRunning...')

    print('BEFORE THIS TEST BEGINS, RELEASE THE PARALLEL MOTOR LOCK')
    response = input('Did you release the lock? (y/n)\n')
    while (not(response.lower() == 'y')):
        if response.lower() == 'n':
            print("You MUST release the lock to continue.")
        else:
            print ("You DID NOT respond with a valid character")
        response = input('Did you release the lock? (y/n)\n')
        
    motors = [motor_left, motor_right]
    speed = 250
    degrees = 90
    
    def test3():
        for m in motors: 
            motor.run_for_degrees(m, degrees, speed)
            time.sleep(1)
        
    def test5(amplitude = 35, duration = 4):
        
        for m in motors:
            start = motor.absolute_position(m)
            for i in range(25):
                dx = random.uniform(-amplitude, amplitude)
                motor.run_to_relative_position(m, int(dx), speed)
                time.sleep(0.1)
        
        # Return to starting position
        for m in motors:
            motor.run_to_absolute_position(motors[0], start, speed)
            time.sleep(0.2)
        
    def test6():
        for m in motors:
            while (motor.absolute_position(m)) != 0:
                motor.run_to_absolute_position(m, 0, 500)
            motor.reset_relative_position(m)
            
    def test7():
        #print('part 1')
        for m in motors:
            motor.run_to_absolute_position(m, 0, 180)
        time.sleep(2)
        
        #print('part 2')
        motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 5000, 1000, 1000)
        time.sleep(5)
        
        #print('part 3')
        for m in motors:
            motor.run_to_absolute_position(m, 0, 180)
        time.sleep(2)
        
        #print('part 4')
        motor.run_for_degrees(motor_left, 5000, 1000)
        motor.run_for_degrees(motor_right, -5000, 1000)
        time.sleep(4)
        
    try:
        light.color(light.POWER, color.RED)
        test3()
        time.sleep(1)
        test5()
        time.sleep(1)
        test6()
        time.sleep(1)
        test7()
        time.sleep(1)
        
        while True:
            response = input('Do the green motor position markers align? (y/n)\n')
            
            while (not((response.lower() == 'y') or (response.lower() == 'n'))):
                print ("You DID NOT respond with a valid character")
                response = input('Do the green motor position markers align? (y/n)\n')
                
            if response.lower() == 'n':
                print("ERROR: Motor malfunction determined by user testing.")
                return
            elif response.lower() == 'y':
                break
    except Exception as e:
        print('TEST FAILED:', e)  
        return

    # ---------------------------------
        
    # TODO: print('TEST PASSED: Moving onto Gyroscope Motor test...')

    # ---------------------------------
    
    result_array[z] = 1
    light.color(light.POWER, color.GREEN)
    print('TEST PASSED: TESTING COMPLETE!')


"""
    Function Name: print_results
    Function Purpose: Print the results of the tests to the console.
"""
def print_results():
    global result_array
    print('\n\n*****************************RESULTS***************************\n')
    
    errors = ["Hub Port Error", "Hub Button Error", "Hub Display Error", 
              "Hub IMU Error", "Distance Sensor Error", "Parallel Motor Error",
              "Force Sensor Error", "Color Sensor Error", "Independent Motor Error"]

    for i in range(1, 10):
        if result_array[i] == 1:
            print(f'* Test {i} PASSED')
        else:
            print(f'* * Test {i} FAILED * --> {errors[i-1]}')
            
    print('\n***************************************************************')

async def main():
    intro(0)
    time.sleep(1)
    
    hub_port_test(1)
    time.sleep(1)
    
    hub_button_test(2)
    time.sleep(1)
    
    hub_display_test(3)
    time.sleep(1)
    
    hub_imu_test(4)
    time.sleep(1)
    
    distance_sensor_test(5)
    time.sleep(1)
    
    motor_parallel_test(6)
    time.sleep(1)
    
    force_sensor_test(7)
    time.sleep(1)
    
    color_sensor_light_matrix_test(8)
    time.sleep(1)
    
    motor_independent_test(9)
    time.sleep(1)
    
    print_results()
    
runloop.run(main())
