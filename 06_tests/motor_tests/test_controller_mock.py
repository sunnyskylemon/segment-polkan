import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / '05_raspberry_pi_software'))

from controller_bridge.serial_controller import RobotController

c = RobotController(mock=True)
print(c.ping())
print(c.enable(True))
print(c.move_steps(0, 100, 700))
print(c.move_joint(1, 45, 700))
print(c.status())
