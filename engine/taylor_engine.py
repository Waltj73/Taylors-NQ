from .rally import calculate as rally
from .decline import calculate as decline


class TaylorEngine:

    def __init__(self, df):
        self.df = df.copy()

    def calculate(self):

        self.df = rally(self.df)

        self.df = decline(self.df)

        return self.df
