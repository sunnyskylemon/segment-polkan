# Segment-Polkan Master

Проект ПО для роботизированного манипулятора «Сегмент-Полкан» на базе конструкции BCN3D Moveo.

Состав:
- firmware микроконтроллера для STEP/DIR, PWM, концевиков и E-Stop;
- ПО Raspberry Pi для оператора, видеотрансляции и телеметрии;
- обратная кинематика для Moveo-подобной руки с язычком;
- модуль управления СИП и первичной обработки спектров;
- тестовые скрипты.

## Быстрый запуск Raspberry Pi ПО

```bash
cd 05_raspberry_pi_software
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn operator_ui.app:app --host 0.0.0.0 --port 8000
```

Открыть: `http://<ip-raspberry-pi>:8000`

## Firmware

Открыть `04_firmware/pico_or_arduino_motor_controller/src/main.cpp` в Arduino IDE / PlatformIO и прошить микроконтроллер.

