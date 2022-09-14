from model.quiz import Quiz
import pandas as pd

class Edeq(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Опросник питания (EDEQ)'])
        cols = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 'EDEQ_4', 'EDEQ_5']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Ограничения питания'] = data[cols].replace('', 0).mean(axis=1, skipna=False)

        cols = ['EDEQ_7', 'EDEQ_9', 'EDEQ_19', 'EDEQ_20', 'EDEQ_21']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Беспокойство о питании'] = data[cols].replace('', 0).mean(axis=1, skipna=False)

        cols = ['EDEQ_6', 'EDEQ_8', 'EDEQ_10', 'EDEQ_11', 'EDEQ_23', 'EDEQ_26', 'EDEQ_27', 'EDEQ_28']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Беспокойство о фигуре'] = data[cols].replace('', 0).mean(axis=1, skipna=False)

        cols = ['EDEQ_8', 'EDEQ_12', 'EDEQ_22', 'EDEQ_24', 'EDEQ_25']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Беспокойство о весе'] = data[cols].replace('', 0).mean(axis=1, skipna=False)

        cols = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 'EDEQ_4', 'EDEQ_5', 'EDEQ_6', 'EDEQ_7', 'EDEQ_8', 
        'EDEQ_9', 'EDEQ_10', 'EDEQ_11', 'EDEQ_12', 'EDEQ_19', 'EDEQ_20', 'EDEQ_21', 'EDEQ_22', 
        'EDEQ_23', 'EDEQ_24', 'EDEQ_25', 'EDEQ_26', 'EDEQ_27', 'EDEQ_28']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['EDEQ_Общий балл'] = data[cols].replace('', 0).mean(axis=1, skipna=False)

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()
        return data_frame
