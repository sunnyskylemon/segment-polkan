from controller_bridge.serial_controller import RobotController
from kinematics.inverse_kinematics import xyz_to_joints, Geometry
from robot_core.safety import SafetyManager


class SegmentPolkanRobot:
    def __init__(self, controller: RobotController, geometry: Geometry | None = None):
        self.controller = controller
        self.geometry = geometry or Geometry()
        self.safety = SafetyManager()

    def enable(self):
        return self.controller.enable(True)

    def disable(self):
        return self.controller.enable(False)

    def stop(self):
        return self.controller.stop()

    def home(self):
        return self.controller.home()

    def move_joint(self, joint: int, angle_deg: float, speed_us: int = 700):
        self.safety.assert_safe()
        return self.controller.move_joint(joint, angle_deg, speed_us)

    def move_to_xyz(self, x: float, y: float, z: float, tool_pitch_deg: float = 0.0, speed_us: int = 700):
        self.safety.assert_safe()
        angles = xyz_to_joints(x, y, z, self.geometry, tool_pitch_deg)
        return self.controller.move_joints(angles.as_list(), speed_us)

    def tongue_touch(self):
        # Канал и угол заменить по фактическому сервоприводу язычка.
        return self.controller.servo(0, 90)

    def tongue_release(self):
        return self.controller.servo(0, 0)

    def status(self):
        return self.controller.status()
