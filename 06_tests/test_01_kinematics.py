import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "05_raspberry_pi_software"))

from kinematics.inverse_kinematics import xyz_to_joints, ArmGeometry

geom = ArmGeometry(
    base_height_mm=120,
    link_1_mm=220,
    link_2_mm=220,
    wrist_mm=100,
    tongue_length_mm=80,
)

joints = xyz_to_joints(260, 0, 160, geom)

assert "joint_0" in joints
assert "joint_1" in joints
assert "joint_2" in joints
assert "joint_3" in joints

print("OK: inverse kinematics")
print(joints)
