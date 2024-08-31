from enum import Enum


class AgentStates(Enum):
    FLOOR_CLEARING = 1
    ROOM_CLEARING = 2
    CHANGING_FLOORS = 3
    HUNTING_NEO = 4
    DONE = 5
