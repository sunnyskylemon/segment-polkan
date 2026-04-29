import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "05_raspberry_pi_software"))

from controller_bridge.serial_controller import SerialControllerMock
from analyzer_sip.sip_client import SipAnalyzerClient

controller = SerialControllerMock()
analyzer = SipAnalyzerClient()

controller.enable()
controller.home()
controller.move_joint(0, 20)
controller.move_joint(1, 35)
controller.move_joint(2, 60)

analyzer.start_measurement()
spectrum = analyzer.read_spectrum()
result = analyzer.process_spectrum(spectrum)

controller.stop()

assert result["peak_intensity"] > 0
assert controller.commands[0] == "ENABLE"
assert controller.commands[-1] == "STOP"

print("OK: full mock scenario")
print(result)
