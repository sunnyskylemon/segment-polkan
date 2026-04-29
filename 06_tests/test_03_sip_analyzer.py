import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "05_raspberry_pi_software"))

from analyzer_sip.sip_client import SipAnalyzerClient

analyzer = SipAnalyzerClient()

assert analyzer.start_measurement()["status"] == "started"

spectrum = analyzer.read_spectrum()
result = analyzer.process_spectrum(spectrum)

assert 400 <= result["peak_wavelength_nm"] <= 900
assert result["peak_intensity"] > 0

print("OK: SIP analyzer")
print(result)
