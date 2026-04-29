# Тест математики преобразования угла сервопривода в PWM tick.
# Можно запускать на ПК без Raspberry Pi.

def angle_to_tick(angle, min_us=500, max_us=2500, freq_hz=50):
    angle = max(0, min(180, angle))
    pulse_us = min_us + (max_us - min_us) * angle / 180.0
    period_us = 1_000_000 / freq_hz
    return int(4096 * pulse_us / period_us)

assert 90 <= angle_to_tick(0) <= 110
assert 290 <= angle_to_tick(90) <= 320
assert 500 <= angle_to_tick(180) <= 530

print("OK: PCA9685 angle_to_tick работает корректно")
