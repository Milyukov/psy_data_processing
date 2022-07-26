class Controller:

    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def run(self, filename, mode):
        self.model.process(filename, 'result.xlsx', mode)
