from errno import EREMOTE
from model.quiz import Quiz
import pandas as pd
import numpy as np

class Ed(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

        self.replace_answers_dict = {
            'никогда': 0,
            'редко': 1,
            'изредка': 2,
            'иногда': 3,
            'часто': 4,
            'очень часто': 5,
            'всегда': 6
        }

        self.questions_to_codes = {}
        self.codes_to_questions = {}

        for number, q in enumerate(self.cols):
            self.questions_to_codes[q] = '{}_{}'.format('ed15', number + 1)
            self.codes_to_questions['{}_{}'.format('ed15', number + 1)] = q

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['ED-15'])


        scale_name = 'Озабоченность весом и формой тела'
        cols = ['ED15_2', 'ED15_4', 'ED15_5', 'ED15_6', 'ED15_9', 'ED15_10']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)

        scale_name = 'Озабоченность питанием'
        cols = ['ED15_1', 'ED15_3', 'ED15_7', 'ED15_8']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)

        scale_name = 'Общий балл'
        cols = ['ED15_1', 'ED15_2', 'ED15_3', 'ED15_4', 'ED15_5', 'ED15_6', 'ED15_7', 'ED15_8', 'ED15_9', 'ED15_10']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)

        replace_answers_dict_ed15_back = {val: key for (key, val) in self.replace_answers_dict.items()}

        def format_ed15_cell(x, index):
            x = str(x)
            if x == '' or x == 'nan':
                return ''
            if 'например' in x:
                return '0'
            if index < 10:
                if '.' in x:
                    x = float(x)
                return str(replace_answers_dict_ed15_back[int(x)])
            else:
                return x

        cols = ['ed15_{}'.format(i) for i in range(1, 16)]
        for index, c in enumerate(cols):
            question = self.codes_to_questions[c]
            question = question[0].upper() + question[1:]
            self.codes_to_questions[c] = question
            self.data_frame[self.codes_to_questions[c]] = data[c].apply(lambda x: format_ed15_cell(x, index))

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()
        for scale_name in ['Озабоченность весом и формой тела', 'Озабоченность питанием', 'Общий балл']:
            data_frame[scale_name] = data_frame[scale_name].apply(lambda x: '{:.2f}'.format(x) if not np.isnan(x) else '')
        return data_frame
