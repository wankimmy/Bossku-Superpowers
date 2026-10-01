"""Static catalog of desk ids that exist in the space."""

DESK_IDS = {"A1", "A2", "A3", "B1", "B2"}


def is_known_desk_id(desk_id):
    return desk_id in DESK_IDS
