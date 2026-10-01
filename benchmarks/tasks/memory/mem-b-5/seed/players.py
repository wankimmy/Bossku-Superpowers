"""Static roster of players tracked by the stat sheet."""

KNOWN_PLAYERS = {"amy", "bo", "cy"}


def is_known_player(name):
    return name in KNOWN_PLAYERS
