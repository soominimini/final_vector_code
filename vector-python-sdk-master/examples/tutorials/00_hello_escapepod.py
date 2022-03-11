import sys
import time
import anki_vector
from anki_vector.util import degrees
from anki_vector.connection import ControlPriorityLevel


def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial,behavior_control_level=ControlPriorityLevel.OVERRIDE_BEHAVIORS_PRIORITY) as robot:
        head_angle = 2  # variable for the angle of Vector's head
        x_bound_high = 50  # variable to determine the lower bound for x positive values
        x_bound_low = -50  # variable to determine the upper bound for x negative values
        x_bound_bal_low = -75  # variable to determine the lower bound of x balanced range condition
        x_bound_bal_high = 75  # variable to determine the upper bound of x balanced range condition
        x_bound_for_low = 300  # variable to determine the lower bound for x values for drive forward condition
        y_bound_high = -90  # variable to determine the lower bound for y positive values
        y_bound_low = -190  # variable to determine the upper bound for y negative values
        y_bound_bal_high = -65  # variable to determine the upper bound of y balanced range condition
        y_bound_bal_low = -215  # variable to determine the lower bound of y balanced range condition
        z_bound_move_low = 10000  # variable to determine the lower bound of z value to make a movement, over 10000
        # includes all possible values
        z_bound_bal_low = 9920  # variable to determine the lower bound of z value for balance condition

        robot.behavior.set_head_angle(degrees(head_angle))
        robot.motors.set_wheel_motors(0, 0)
        time.sleep(2)
        robot.motors.set_lift_motor(10)
        robot.behavior.say_text("Pick me up!")
        pickup_countdown = 20  # Time in seconds for Vector to wait to get picked up
        print("Waiting for Vector to be picked up, press ctrl+c to exit")

        # loop to determinate if vector has been, or not, picked up and then laid down.
        try:

            #  Count down when Vector is waiting to get picked up
            while not robot.status.is_picked_up and pickup_countdown:
                time.sleep(1)
                pickup_countdown -= 1

            # if Vector doesnt get picked up during countdown exit program
            if not pickup_countdown:
                print("Did not get picked up")
                sys.exit()

            # When vector is picked up
            while robot.status.is_picked_up:
                print("Vector is picked up...")
                robot.behavior.say_text("Put Me Down")
                print("Waiting for Vector to be put down...")
                time.sleep(1)

            # when Vector is placed down. Contains the main functions of the programme.
            while not robot.status.is_picked_up:
                robot.motors.set_lift_motor(-1)
                print("Action 1")
                x_accel = robot.accel.x
                y_accel = robot.accel.y
                z_accel = robot.accel.z
                print("x=", x_accel)
                print("y=", y_accel)
                print("z=", z_accel)
                time.sleep(0.05)

                # Secondary loop options when after Vector has been placed down
                try:
                    # When uphill is in vectors back-right quadrant
                    while y_accel < y_bound_low \
                            and x_accel < x_bound_low \
                            and z_accel < z_bound_move_low:
                        print("Turn Right")
                        robot.motors.set_wheel_motors(20, -30)
                        time.sleep(2)
                        robot.behavior.set_head_angle(degrees(head_angle))
                        robot.motors.set_wheel_motors(0, 0)
                        time.sleep(1)
                        break

                    # When uphill is in vectors back-left quadrant
                    while y_bound_high < y_accel \
                            and x_accel < x_bound_low \
                            and z_accel < z_bound_move_low:
                        print("Turn Left")
                        robot.motors.set_wheel_motors(-30, 20)
                        time.sleep(2)
                        robot.behavior.set_head_angle(degrees(head_angle))
                        robot.motors.set_wheel_motors(0, 0)
                        time.sleep(1)
                        break

                    # When uphill is in vectors front-left quadrant
                    while y_bound_high < y_accel \
                            and x_bound_high < x_accel \
                            and z_accel < z_bound_move_low:
                        print("Forward Left")
                        robot.motors.set_wheel_motors(20, 60)
                        time.sleep(1)
                        robot.behavior.set_head_angle(degrees(head_angle))
                        robot.motors.set_wheel_motors(0, 0)
                        time.sleep(1)
                        break

                    # When uphill is in vectors front-right quadrant
                    while y_accel < y_bound_low \
                            and x_bound_high < x_accel \
                            and z_accel < z_bound_move_low:
                        print("Forward Right")
                        robot.motors.set_wheel_motors(60, 20)
                        time.sleep(1)
                        robot.behavior.set_head_angle(degrees(head_angle))
                        robot.motors.set_wheel_motors(0, 0)
                        time.sleep(1)
                        break

                    # When Vector is facing uphill
                    while y_bound_low < y_accel < y_bound_high \
                            and x_bound_for_low < x_accel \
                            and z_accel < z_bound_move_low:
                        robot.behavior.say_text("Forward")
                        print("Forward")
                        robot.motors.set_wheel_motors(45, 45)
                        time.sleep(1)
                        robot.behavior.set_head_angle(degrees(head_angle))
                        robot.motors.set_wheel_motors(0, 0)
                        time.sleep(1)
                        break

                    # When Vector's x, y and z values are met for the balance condition
                    while y_bound_bal_low < y_accel < y_bound_bal_high \
                            and x_bound_bal_low < x_accel < x_bound_bal_high \
                            and z_bound_bal_low < z_accel:
                        robot.behavior.say_text("Balanced")
                        print("Balanced")
                        robot.motors.set_lift_motor(1)  # Vector celebrates
                        time.sleep(2)
                        robot.motors.set_lift_motor(-0.5)  # Vector need to get balanced again
                        robot.behavior.set_head_angle(degrees(head_angle))
                        time.sleep(8)  # Wait before returning to accelerometer reading
                        break

                except KeyboardInterrupt:
                    pass

        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
