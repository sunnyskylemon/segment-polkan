import time
from typing import Optional

try:
    import serial
except ImportError:  # позволяет запускать тесты без железа
    serial = None


class RobotControllerError(RuntimeError):
    pass


class RobotController:
    """Мост Raspberry Pi -> микроконтроллер.

    Этот класс не должен считать кинематику. Он только отправляет команды firmware
    и читает ответы.
    """

    def __init__(self, port: str = "/dev/ttyACM0", baudrate: int = 115200, timeout: float = 1.0, mock: bool = False):
        self.mock = mock or serial is None
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self._last_status = "not_connected"
        if self.mock:
            self.ser = None
        else:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)

    def send(self, command: str) -> str:
        command = command.strip()
        if not command:
            raise ValueError("Empty command")
        if self.mock:
            self._last_status = f"MOCK_OK {command}"
            return self._last_status
        assert self.ser is not None
        self.ser.write((command + "\n").encode("utf-8"))
        response = self.ser.readline().decode("utf-8", errors="replace").strip()
        self._last_status = response
        if response.startswith("ERR"):
            raise RobotControllerError(response)
        return response

    def ping(self) -> str:
        return self.send("PING")

    def enable(self, enabled: bool = True) -> str:
        return self.send(f"ENABLE {1 if enabled else 0}")

    def stop(self) -> str:
        return self.send("STOP")

    def status(self) -> str:
        return self.send("STATUS")

    def home(self) -> str:
        return self.send("HOME")

    def move_steps(self, axis: int, steps: int, speed_us: int = 700) -> str:
        return self.send(f"MOVE_STEPS {axis} {steps} {speed_us}")

    def move_joint(self, joint: int, angle_deg: float, speed_us: int = 700) -> str:
        return self.send(f"MOVE_JOINT {joint} {angle_deg:.3f} {speed_us}")

    def move_joints(self, angles_deg: list[float], speed_us: int = 700) -> list[str]:
        responses = []
        for joint, angle in enumerate(angles_deg):
            responses.append(self.move_joint(joint, angle, speed_us))
        return responses

    def servo(self, channel: int, angle_deg: int) -> str:
        return self.send(f"SERVO {channel} {angle_deg}")

    @property
    def last_status(self) -> str:
        return self._last_status
