# Проверка строк команд, которые Raspberry Pi отправляет микроконтроллеру.

def move_joint(axis, angle, speed_us=700):
    return f"MOVE_JOINT {axis} {angle:.3f} {speed_us}"

def move_steps(axis, steps, speed_us=700):
    return f"MOVE_STEPS {axis} {steps} {speed_us}"

assert move_joint(0, 45) == "MOVE_JOINT 0 45.000 700"
assert move_steps(2, -1000, 900) == "MOVE_STEPS 2 -1000 900"

print("OK: протокол команд сформирован корректно")
