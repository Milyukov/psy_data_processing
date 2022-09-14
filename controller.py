class Controller:

    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def run(self, filename):
        self.model.process(filename, 'result.xlsx')
