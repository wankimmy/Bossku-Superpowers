"""Helpers for a tiny in-memory job scheduler."""


def make_job_id(prefix, n):
    """Build a simple deterministic job id, like 'job-3'."""
    return f"{prefix}-{n}"


class Job:
    def __init__(self, job_id, name, run_at):
        self.job_id = job_id
        self.name = name
        self.run_at = run_at


class Scheduler:
    def __init__(self):
        self._jobs = {}
        self._recurring_ms = {}

    def add_job(self, job):
        self._jobs[job.job_id] = job

    def due_jobs(self, now):
        return sorted(
            (job for job in self._jobs.values() if job.run_at <= now),
            key=lambda job: job.run_at,
        )

    def cancel_job(self, job_id):
        self._jobs.pop(job_id, None)
        self._recurring_ms.pop(job_id, None)

    def next_job(self, now):
        upcoming = [job for job in self._jobs.values() if job.run_at > now]
        if not upcoming:
            return None
        return min(upcoming, key=lambda job: job.run_at)

    def add_recurring_job(self, job, interval_ms):
        self.add_job(job)
        self._recurring_ms[job.job_id] = interval_ms

    def run_due(self, now):
        fired = self.due_jobs(now)
        for job in fired:
            if job.job_id in self._recurring_ms:
                job.run_at = job.run_at + self._recurring_ms[job.job_id]
            else:
                self._jobs.pop(job.job_id, None)
        return fired

    def mark_failed(self, job_id, retry_delay_ms):
        job = self._jobs.get(job_id)
        if job is not None:
            job.run_at = job.run_at + retry_delay_ms
