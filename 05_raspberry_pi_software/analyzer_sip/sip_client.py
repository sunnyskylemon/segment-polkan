import random
from typing import Sequence

try:
    import serial
except ImportError:
    serial = None


class SIPAnalyzer:
    """Клиент СИП/анализатора.

    Пока протокол СИП не финализирован, класс умеет работать в mock-режиме.
    После уточнения интерфейса заменить команды START/STATUS/READ на реальные.
    """

    def __init__(self, port: str | None = None, baudrate: int = 115200, mock: bool = True):
        self.mock = mock or port is None or serial is None
        self.status = "idle"
        if self.mock:
            self.ser = None
        else:
            self.ser = serial.Serial(port, baudrate, timeout=1)

    def start_measurement(self) -> str:
        self.status = "measuring"
        if self.mock:
            return "MOCK_ANALYZER_STARTED"
        self.ser.write(b"START\n")
        return self.ser.readline().decode(errors="replace").strip()

    def read_spectrum(self) -> list[float]:
        self.status = "done"
        if self.mock:
            # имитация спектра: фон + 2 пика
            spectrum = []
            for i in range(256):
                peak1 = 120 * pow(2.71828, -((i - 80) ** 2) / (2 * 8 ** 2))
                peak2 = 80 * pow(2.71828, -((i - 170) ** 2) / (2 * 12 ** 2))
                noise = random.uniform(-3, 3)
                spectrum.append(max(0.0, 10 + peak1 + peak2 + noise))
            return spectrum
        self.ser.write(b"READ\n")
        raw = self.ser.readline().decode(errors="replace").strip()
        return [float(x) for x in raw.split(",") if x]
