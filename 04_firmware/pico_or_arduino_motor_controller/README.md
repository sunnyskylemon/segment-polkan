# Firmware контроллера приводов

Команды принимаются по USB Serial на скорости 115200.

Примеры:

```text
PING
ENABLE 1
HOME
MOVE_STEPS 0 1000 700
MOVE_JOINT 1 45 700
SERVO 0 90
STATUS
STOP
```

Назначение firmware — не выполнять бизнес-логику, а безопасно и точно управлять приводами.
