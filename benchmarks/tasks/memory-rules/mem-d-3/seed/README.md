# Tiny Scheduler

Prototype in-memory job scheduler. Time is just an opaque, monotonically
increasing integer "tick" supplied by the caller -- there's no real wall
clock involved anywhere in this package.

Run tests: `python -m unittest discover -s tests`
