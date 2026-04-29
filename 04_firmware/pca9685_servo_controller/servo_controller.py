from pca9685 import PCA9685

class ServoController:
    def __init__(self):
        self.pwm = PCA9685()

    def set_angle(self, channel, angle):
        pulse = int(150 + (angle / 180.0) * 450)
        self.pwm.set_pwm(channel, 0, pulse)

    def tongue_down(self):
        self.set_angle(0, 120)

    def tongue_up(self):
        self.set_angle(0, 30)