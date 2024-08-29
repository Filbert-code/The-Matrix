from pygame import Rect


def to_pygame_coords(coords, height):
    """Convert coordinates into pygame coordinates (lower-left => top left)."""
    return (coords[0], height - coords[1])


def to_pygame_rect(rect, height):
    """Convert a rectangle from normal coordinates to pygame coordinates."""
    return Rect(rect.x, height - rect.y - rect.height, rect.width, rect.height)

# def from_screen_to_world_coords(coord):
#