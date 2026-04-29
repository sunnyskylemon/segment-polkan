import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2] / '05_raspberry_pi_software'))

from kinematics.inverse_kinematics import xyz_to_joints
from analyzer_sip.sip_client import SIPAnalyzer
from analyzer_sip.spectra_processing import process_spectrum

print('IK:', xyz_to_joints(250, 0, 180).as_list())
an = SIPAnalyzer(mock=True)
an.start_measurement()
s = an.read_spectrum()
print('Spectrum:', process_spectrum(s))
