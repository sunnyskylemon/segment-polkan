from dataclasses import dataclass


@dataclass
class SafetyState:
    emergency_stop: bool = False
    limit_triggered: bool = False
    controller_connected: bool = False
    last_error: str | None = None


class SafetyManager:
    def __init__(self):
        self.state = SafetyState()

    def assert_safe(self) -> None:
        if self.state.emergency_stop:
            raise RuntimeError("Emergency stop is active")
        if self.state.limit_triggered:
            raise RuntimeError("Limit switch is triggered")

    def set_error(self, error: str) -> None:
        self.state.last_error = error

    def clear_error(self) -> None:
        self.state.last_error = None
