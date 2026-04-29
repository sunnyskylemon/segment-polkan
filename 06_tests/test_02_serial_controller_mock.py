import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "05_raspberry_pi_software"))

from controller_bridge.serial_controller import SerialControllerMock

controller = SerialControllerMock()

assert controller.enable() == "OK MOCK"
assert controller.move_joint(1, 45.0) == "OK MOCK"
assert controller.stop() == "OK MOCK"

assert controller.commands == [
    "ENABLE",
    "MOVE_JOINT 1 45.000 700",
    "STOP",
]

print("OK: serial controller mock")
