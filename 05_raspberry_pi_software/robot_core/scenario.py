from dataclasses import dataclass
from robot_core.robot import SegmentPolkanRobot
from analyzer_sip.sip_client import SIPAnalyzer
from analyzer_sip.spectra_processing import process_spectrum


@dataclass
class Point3D:
    x: float
    y: float
    z: float


class RobotScenario:
    def __init__(self, robot: SegmentPolkanRobot, analyzer: SIPAnalyzer):
        self.robot = robot
        self.analyzer = analyzer

    def collect_and_analyze(self, sample_point: Point3D, analyzer_point: Point3D) -> dict:
        """Сценарий: подойти к материалу -> коснуться язычком -> перенести к СИП -> анализ."""
        self.robot.enable()
        self.robot.home()

        safe_z = max(sample_point.z + 120, 180)
        self.robot.move_to_xyz(sample_point.x, sample_point.y, safe_z)
        self.robot.move_to_xyz(sample_point.x, sample_point.y, sample_point.z)
        self.robot.tongue_touch()
        self.robot.move_to_xyz(sample_point.x, sample_point.y, safe_z)

        self.robot.move_to_xyz(analyzer_point.x, analyzer_point.y, max(analyzer_point.z + 120, 180))
        self.robot.move_to_xyz(analyzer_point.x, analyzer_point.y, analyzer_point.z)
        self.analyzer.start_measurement()
        spectrum = self.analyzer.read_spectrum()
        result = process_spectrum(spectrum)

        self.robot.move_to_xyz(analyzer_point.x, analyzer_point.y, max(analyzer_point.z + 120, 180))
        return {"status": "ok", "spectrum_result": result}
