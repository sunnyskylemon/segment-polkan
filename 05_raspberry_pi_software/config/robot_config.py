from dataclasses import dataclass

@dataclass(frozen=True)
class SerialConfig:
    port: str = "/dev/ttyACM0"
    baudrate: int = 115200
    timeout: float = 1.0

@dataclass(frozen=True)
class ArmGeometry:
    # Размеры примерные. Их нужно заменить после финальной механики Moveo/Полкан.
    base_height_mm: float = 120.0
    shoulder_link_mm: float = 220.0
    elbow_link_mm: float = 220.0
    wrist_link_mm: float = 90.0
    tongue_tool_offset_mm: float = 80.0

@dataclass(frozen=True)
class JointLimits:
    base_min_deg: float = -160
    base_max_deg: float = 160
    shoulder_min_deg: float = -45
    shoulder_max_deg: float = 120
    elbow_min_deg: float = -120
    elbow_max_deg: float = 120
    wrist_min_deg: float = -120
    wrist_max_deg: float = 120
    tool_min_deg: float = -180
    tool_max_deg: float = 180

SERIAL = SerialConfig()
GEOMETRY = ArmGeometry()
LIMITS = JointLimits()
