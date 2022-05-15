class Quiz:

    def __init__(self, start_col, count) -> None:
        self.sc = start_col
        self.count = count
        self.ec = start_col + count

    def eval(self, data):
        pass

    def format(self):
        pass

    def get_cols(self, cols):
        return cols[self.sc:self.ec]
