import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scheduler import make_job_id


class SchedulerTests(unittest.TestCase):
    def test_make_job_id(self):
        self.assertEqual(make_job_id("job", 3), "job-3")


if __name__ == "__main__":
    unittest.main()
