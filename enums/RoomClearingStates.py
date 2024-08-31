from enum import Enum


class RoomClearingStates(Enum):
    MOVING_TO_ROOM = 1
    CLEARING_ROOM = 2
    LEAVING_ROOM = 3