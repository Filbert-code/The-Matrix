from typing import List

from sortedcontainers import SortedList


class UnexploredRoomArea:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def __lt__(self, other):
        if type(other) is UnexploredRoomArea:
            return self.x1 < other.x1
        elif type(other) is int:
            return self.x2 < other

    def overlapping(self, other):
        return other.x1 < self.x1 < other.x2 or other.x1 < self.x2 < other.x2

    def __str__(self):
        return f'({self.x1}, {self.x2})'

    def __repr__(self):
        return f'({self.x1}, {self.x2})'


# same logic for finding the closest unexplored area for floors, but for rooms instead
class UnexploredRoomAreasSortedList:
    def __init__(self, room_size, unexplored_room_areas: List[UnexploredRoomArea] = None):
        self.room_size = room_size
        self.sorted_list = SortedList()
        if unexplored_room_areas:
            self.add_unexplored_room_areas(unexplored_room_areas)
        else:
            self.sorted_list.add(UnexploredRoomArea(0, self.room_size))

    def add_unexplored_room_areas(self, unexplored_room_areas):
        for unexplored_room_area in unexplored_room_areas:
            self.sorted_list.add(unexplored_room_area)

    def find_closest_unexplored_room_area(self, x_pos) -> UnexploredRoomArea | None:
        if len(self.sorted_list) == 0:
            return None

        # find the closest room area
        closest_room_area_index = self.sorted_list.bisect_left(x_pos)

        if closest_room_area_index >= len(self.sorted_list):
            return self.sorted_list[len(self.sorted_list) - 1]

        next_unexplored_area = self.sorted_list[closest_room_area_index]
        prev_unexplored_area = self.sorted_list[closest_room_area_index - 1]

        dist_to_next = abs(next_unexplored_area.x1 - x_pos)
        dist_to_prev = abs(prev_unexplored_area.x2 - x_pos)

        return next_unexplored_area if dist_to_next < dist_to_prev else prev_unexplored_area

    def __len__(self):
        return len(self.sorted_list)

    def bisect_left(self, other):
        self.sorted_list.bisect_left(other)


if __name__ == '__main__':
    unexplored_areas = [
        UnexploredRoomArea(30, 100),
        UnexploredRoomArea(120, 170),
        UnexploredRoomArea(200, 210)
    ]
    sorted_list = UnexploredRoomAreasSortedList(unexplored_areas)
    player_pos = 186
