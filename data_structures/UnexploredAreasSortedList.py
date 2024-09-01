from typing import List

from sortedcontainers import SortedList

from util.common import is_segments_overlapping


class UnexploredArea:
    def __init__(self, x1, x2):
        self.x1 = x1
        self.x2 = x2

    def __lt__(self, other):
        if type(other) is UnexploredArea:
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
class UnexploredAreasSortedList:
    def __init__(self, x_boundaries, unexplored_floor_areas: List[UnexploredArea] = None, building_horizontal_padding=0):
        self.x_left_boundary, self.x_right_boundary = x_boundaries
        self.sorted_list = SortedList()
        if unexplored_floor_areas:
            self.add_unexplored_floor_areas(unexplored_floor_areas)
        else:
            self.sorted_list.add(UnexploredArea(self.x_left_boundary + building_horizontal_padding, self.x_right_boundary - building_horizontal_padding))

    def add_unexplored_floor_areas(self, unexplored_floor_areas):
        for unexplored_floor_area in unexplored_floor_areas:
            self.sorted_list.add(unexplored_floor_area)

    def find_closest_unexplored_area(self, x_pos) -> UnexploredArea | None:
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

    def update_unexplored_area(self, agent):
        # LOGIC FOR UPDATING THE LEVEL'S SORTED UNEXPLORED AREA DATA STRUCTURE
        # Check if vision vector overlaps with any unexplored areas
        # If it does, update the overlapped area to reduce its range
        for unexplored_area in self.sorted_list:
            agent_x1, agent_x2 = min(agent.rect.centerx, int(agent.vision_vector[0])), max(agent.rect.centerx, int(agent.vision_vector[0]))

            if agent_x1 <= unexplored_area.x1 <= agent_x2 and agent_x1 <= unexplored_area.x2 <= agent_x2:
                # area is within the vision area
                self.sorted_list.remove(unexplored_area)

            # if agent does not overlap with unexplored area, skip
            if not is_segments_overlapping((unexplored_area.x1, unexplored_area.x2), (agent_x1, agent_x2)):
                continue

            if agent_x1 >= unexplored_area.x1 and agent_x2 <= unexplored_area.x2:
                # the agent has unexplored area forwards and backwards. Need to split the unexplored area into 2
                new_unexplored_area = UnexploredArea(agent_x2, unexplored_area.x2)
                self.sorted_list.add(new_unexplored_area)
                unexplored_area.x2 = agent_x1
                # break here because we know our vision is completely within this unexplored area and none others
                break

            if agent_x1 >= unexplored_area.x1 and agent_x2 >= unexplored_area.x2:
                unexplored_area.x2 = agent_x1
                if abs(unexplored_area.x2 - unexplored_area.x1) < 5:
                    try:
                        self.sorted_list.remove(unexplored_area)
                    except ValueError as e:
                        print(e)
            elif agent_x1 <= unexplored_area.x1 and agent_x2 <= unexplored_area.x2:
                unexplored_area.x1 = agent_x2
                if abs(unexplored_area.x2 - unexplored_area.x1) < 5:
                    try:
                        self.sorted_list.remove(unexplored_area)
                    except ValueError as e:
                        print(e)


if __name__ == '__main__':
    unexplored_areas = [
        UnexploredArea(30, 100),
        UnexploredArea(120, 170),
        UnexploredArea(200, 210)
    ]
    sorted_list = UnexploredAreasSortedList(unexplored_areas)
    player_pos = 186

    # print(sorted_list.find_closest_floor_area(player_pos))

