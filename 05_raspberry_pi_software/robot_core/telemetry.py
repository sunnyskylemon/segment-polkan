from dataclasses import dataclass, asdict
from time import time


@dataclass
class Telemetry:
    timestamp: float
    controller_status: str
    video_enabled: bool
    analyzer_status: str
    last_error: str | None = None

    def to_dict(self):
        return asdict(self)


def build_telemetry(controller_status: str, analyzer_status: str = "idle", video_enabled: bool = False, last_error: str | None = None):
    return Telemetry(time(), controller_status, video_enabled, analyzer_status, last_error)
