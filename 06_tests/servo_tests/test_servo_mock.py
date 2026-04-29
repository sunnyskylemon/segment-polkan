import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / '05_raspberry_pi_software'))

from controller_bridge.serial_controller import RobotController

c = RobotController(mock=True)
for angle in [0, 45, 90, 135, 180]:
    print(c.servo(0, angle))
