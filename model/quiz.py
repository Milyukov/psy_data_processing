class Quiz:

    def __init__(self, start_col, count, columns, worksheet) -> None:
        self.sc = start_col
        self.count = count
        self.ec = start_col + count
        self.worksheet = worksheet
        self.cols = columns[start_col:start_col + count]

    def eval(self, data):
        pass

    def format(self):
        pass

    def get_cols(self):
        return self.cols
