class Controller:

    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view

    def run(self, filename, config_name):
        self.model.process(filename, 'result.xlsx', config_name)
