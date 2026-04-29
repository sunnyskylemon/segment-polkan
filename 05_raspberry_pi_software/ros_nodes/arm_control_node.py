"""Минимальная ROS2-заготовка. Требует установленный rclpy.

Назначение: принимать высокоуровневые команды и передавать их в RobotController.
Это skeleton, чтобы проект соответствовал требованию ROS, но MVP может работать без ROS.
"""

try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import String
except ImportError:
    rclpy = None

from controller_bridge.serial_controller import RobotController


if rclpy is not None:
    class ArmControlNode(Node):
        def __init__(self):
            super().__init__('segment_polkan_arm_control')
            self.controller = RobotController(mock=True)
            self.sub = self.create_subscription(String, 'arm_command', self.on_command, 10)
            self.pub = self.create_publisher(String, 'arm_status', 10)

        def on_command(self, msg: String):
            try:
                response = self.controller.send(msg.data)
            except Exception as exc:
                response = f"ERR {exc}"
            out = String()
            out.data = response
            self.pub.publish(out)


def main():
    if rclpy is None:
        raise RuntimeError("ROS2/rclpy is not installed")
    rclpy.init()
    node = ArmControlNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
