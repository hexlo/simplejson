import random
import string

from BaseFuzzer import BaseFuzzer


class RandomFuzzer(BaseFuzzer):
    def __init__(self, min_length: int = 0, max_length: int = 20):
        super().__init__()
        self.min_length = min_length
        self.max_length = max_length

    def fuzz(self):
        """Generate a random string to fuzz json parser. String has length between `min_length` and `max_length`"""
        length = random.randrange(self.min_length, self.max_length)
        return "".join([random.choice(string.printable) for _ in range(length)])
