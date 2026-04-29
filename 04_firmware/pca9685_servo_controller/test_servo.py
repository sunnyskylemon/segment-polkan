import time
from servo_controller import ServoController

servo = ServoController()

while True:
    print("Down")
    servo.tongue_down()
    time.sleep(2)

    print("Up")
    servo.tongue_up()
    time.sleep(2)