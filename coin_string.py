import random
import itertools


class RandomCoinString:
    bin_str: str

    @staticmethod
    def get_generator():
        while True:
            yield RandomCoinString()

    def __init__(self):
        self.bin_str = ""

    def __getitem__(self, item):
        try:
            # noinspection PyStatementEffect
            self.bin_str[item.stop]
            return self.bin_str[item]
        except IndexError:
            self.bin_str += "".join(random.choices(["1", "0"], k=len(self.bin_str) + 10))
            return self[item]

    def __repr__(self):
        return self.bin_str

    def find_first_occurrence(self, targets):
        for coin_index in itertools.count():
            for target in targets:
                if self[coin_index:coin_index + len(target)] == target:
                    return coin_index,target
