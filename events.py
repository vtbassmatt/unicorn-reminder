from enum import Enum


class EventKind(Enum):
    NOTHING = 0
    ALERT = 1
    REMIND = 2
    CALM = 3


class ScheduledEventError(RuntimeError):
    pass
