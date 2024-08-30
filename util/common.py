from pygame import Rect


def to_pygame_coords(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], height - coords[1])


def to_pygame_rect(rect, height):
    """Convert a rectangle from normal coordinates to pygame coordinates."""
    return Rect(rect.x, height - rect.y - rect.height, rect.width, rect.height)


def is_segments_overlapping(seg_one, seg_two):
    return seg_one[0] <= seg_two[0] <= seg_one[1] or seg_one[0] <= seg_two[1] <= seg_one[1]