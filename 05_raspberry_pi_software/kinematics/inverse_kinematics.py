import math
from dataclasses import dataclass


@dataclass
class Geometry:
    base_height_mm: float = 120.0
    shoulder_link_mm: float = 220.0
    elbow_link_mm: float = 220.0
    wrist_link_mm: float = 90.0
    tongue_tool_offset_mm: float = 80.0


@dataclass
class JointAngles:
    base: float
    shoulder: float
    elbow: float
    wrist: float
    tool: float = 0.0

    def as_list(self) -> list[float]:
        return [self.base, self.shoulder, self.elbow, self.wrist, self.tool]


class KinematicsError(ValueError):
    pass


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def xyz_to_joints(x_mm: float, y_mm: float, z_mm: float, geom: Geometry = Geometry(), tool_pitch_deg: float = 0.0) -> JointAngles:
    """Упрощённая обратная кинематика для Moveo-подобной руки.

    Модель: база + плечо + локоть + запястье. Конечный инструмент — "язычок".
    Для MVP считаем, что язычок направлен примерно вдоль последнего звена,
    поэтому целевая точка запястья смещается на tool_offset.

    Возвращает углы в градусах.
    """
    base_angle = math.degrees(math.atan2(y_mm, x_mm))
    r = math.hypot(x_mm, y_mm)

    # Компенсация длины язычка/инструмента.
    pitch_rad = math.radians(tool_pitch_deg)
    wrist_r = r - (geom.wrist_link_mm + geom.tongue_tool_offset_mm) * math.cos(pitch_rad)
    wrist_z = z_mm - geom.base_height_mm - (geom.wrist_link_mm + geom.tongue_tool_offset_mm) * math.sin(pitch_rad)

    l1 = geom.shoulder_link_mm
    l2 = geom.elbow_link_mm
    d = math.hypot(wrist_r, wrist_z)
    if d > l1 + l2 or d < abs(l1 - l2):
        raise KinematicsError(f"Target is unreachable: x={x_mm}, y={y_mm}, z={z_mm}, distance={d:.1f} mm")

    cos_elbow = clamp((wrist_r**2 + wrist_z**2 - l1**2 - l2**2) / (2 * l1 * l2), -1.0, 1.0)
    elbow = math.atan2(math.sqrt(1 - cos_elbow**2), cos_elbow)

    k1 = l1 + l2 * math.cos(elbow)
    k2 = l2 * math.sin(elbow)
    shoulder = math.atan2(wrist_z, wrist_r) - math.atan2(k2, k1)

    wrist = pitch_rad - shoulder - elbow

    return JointAngles(
        base=base_angle,
        shoulder=math.degrees(shoulder),
        elbow=math.degrees(elbow),
        wrist=math.degrees(wrist),
        tool=0.0,
    )
