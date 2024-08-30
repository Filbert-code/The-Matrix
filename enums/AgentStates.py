from enum import Enum


class AgentStates(Enum):
    FLOOR_CLEARING = 1
    CHANGING_FLOORS = 2
    HUNTING_NEO = 3
    DONE = 4