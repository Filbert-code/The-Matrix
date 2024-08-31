

class Room:
    def __init__(self, door_rect, room_rect, room_number):
        self.door_rect = door_rect
        self.room_rect = room_rect
        self.room_number = room_number
        self.fully_explored = False
        self.assigned_agent = None

    def update(self):
        pass

    def draw(self, screen):
        pass
