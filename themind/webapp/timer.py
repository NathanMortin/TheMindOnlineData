import time
from datetime import date, datetime


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class Timer:
    timers = {}

    def __init__(
        self,
        name=None,
        text="Elapsed time: {:0.4f} seconds",
        logger=print,
    ):
        self._start_time = None
        self.name = name
        self.text = text
        self.logger = logger

        # Add new named timers to dictionary of timers
        if name:
            self.timers.setdefault(name, 0)

        self.timers[name] = 0

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None

        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time

        return elapsed_time

    @staticmethod
    def get_current_date():
        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        return d4

    @staticmethod
    def get_current_time():
        now = datetime.now()
        current_time = now.strftime("%H-%M-%S")
        return current_time



