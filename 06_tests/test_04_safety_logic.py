class SafetyState:
    def __init__(self):
        self.estop = False
        self.limit_triggered = False

    def can_move(self):
        return not self.estop and not self.limit_triggered


s = SafetyState()
assert s.can_move() is True

s.estop = True
assert s.can_move() is False

s.estop = False
s.limit_triggered = True
assert s.can_move() is False

print("OK: safety logic")
