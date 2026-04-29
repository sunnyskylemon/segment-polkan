# Распиновка MVP

## Raspberry Pi 5

| Интерфейс | Назначение |
|---|---|
| USB | связь с микроконтроллером |
| CSI/USB | камера |
| Wi-Fi/Ethernet | операторский интерфейс |

## Микроконтроллер

См. `04_firmware/pico_or_arduino_motor_controller/include/pinout.md`.

## DM865C

| Контакт драйвера | Куда подключать |
|---|---|
| PUL+/PUL- | STEP через level shifter/опторазвязку по необходимости |
| DIR+/DIR- | DIR через level shifter/опторазвязку по необходимости |
| ENA+/ENA- | ENABLE |
| V+/V- | 24V/GND силового питания |
| A+/A-/B+/B- | обмотки шагового двигателя |
