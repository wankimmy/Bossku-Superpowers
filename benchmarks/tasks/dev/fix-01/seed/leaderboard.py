"""A simple in-memory game leaderboard."""


class Leaderboard:
    def __init__(self):
        self._scores = {}
        self._rank_cache = None

    def add_player(self, name, score=0):
        if name in self._scores:
            raise ValueError(f"{name} is already on the leaderboard")
        self._scores[name] = score
        self._rank_cache = None

    def remove_player(self, name):
        if name not in self._scores:
            raise KeyError(name)
        del self._scores[name]

    def record_score(self, name, points):
        if name not in self._scores:
            raise KeyError(name)
        self._scores[name] += points

    def reset_player(self, name):
        if name not in self._scores:
            raise KeyError(name)
        self._scores[name] = 0
        self._rank_cache = None

    def score_of(self, name):
        if name not in self._scores:
            raise KeyError(name)
        return self._scores[name]

    def rankings(self):
        if self._rank_cache is None:
            self._rank_cache = sorted(self._scores, key=lambda n: (-self._scores[n], n))
        return list(self._rank_cache)

    def top(self, n):
        return self.rankings()[:n]
