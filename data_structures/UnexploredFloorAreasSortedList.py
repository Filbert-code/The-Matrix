from typing import List

from sortedcontainers import SortedList


class UnexploredFloorArea:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def __lt__(self, other):
        if type(other) is UnexploredFloorArea:
            return self.x1 < other.x1
        elif type(other) is int:
            return self.x2 < other

    def overlapping(self, other):
        return other.x1 < self.x1 < other.x2 or other.x1 < self.x2 < other.x2

    def __str__(self):
        return f'({self.x1}, {self.x2})'

    def __repr__(self):
        return f'({self.x1}, {self.x2})'


# need a data structure that allows us to insert UnexploredFloorAreas into an ordered list, and find the closest
# UnexploredFloorArea to any given x-position
# Insertions are O(n) (unfortunately)
# Finding is O(log(n))
class UnexploredFloorAreasSortedList:
    def __init__(self, floor_size, unexplored_floor_areas: List[UnexploredFloorArea] = None, building_horizontal_padding=0):
        self.floor_size = floor_size
        self.sorted_list = SortedList()
        if unexplored_floor_areas:
            self.add_unexplored_floor_areas(unexplored_floor_areas)
        else:
            self.sorted_list.add(UnexploredFloorArea(building_horizontal_padding, self.floor_size - building_horizontal_padding))

    def add_unexplored_floor_areas(self, unexplored_floor_areas):
        for unexplored_floor_area in unexplored_floor_areas:
            self.sorted_list.add(unexplored_floor_area)

    def find_closest_unexplored_floor_area(self, x_pos) -> UnexploredFloorArea | None:
        if len(self.sorted_list) == 0:
            return None

        # find the closest floor area
        closest_floor_area_index = self.sorted_list.bisect_left(x_pos)

        if closest_floor_area_index >= len(self.sorted_list):
            return self.sorted_list[len(self.sorted_list) - 1]

        next_unexplored_area = self.sorted_list[closest_floor_area_index]
        prev_unexplored_area = self.sorted_list[closest_floor_area_index - 1]

        dist_to_next = abs(next_unexplored_area.x1 - x_pos)
        dist_to_prev = abs(prev_unexplored_area.x2 - x_pos)

        return next_unexplored_area if dist_to_next < dist_to_prev else prev_unexplored_area

    def __len__(self):
        return len(self.sorted_list)

    def bisect_left(self, other):
        self.sorted_list.bisect_left(other)


if __name__ == '__main__':
    unexplored_areas = [
        UnexploredFloorArea(30, 100),
        UnexploredFloorArea(120, 170),
        UnexploredFloorArea(200, 210)
    ]
    sorted_list = UnexploredFloorAreasSortedList(unexplored_areas)
    player_pos = 186

    # print(sorted_list.find_closest_floor_area(player_pos))

