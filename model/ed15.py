from model.quiz import Quiz
import pandas as pd
import numpy as np

class Ed(Quiz):

    def __init__(self, start_col, count, columns, workbook, worksheet, transposed_worksheet=None) -> None:
        super().__init__(start_col, count, columns, worksheet, transposed_worksheet)
        self.header_format = workbook.add_format({'bg_color': 'yellow'})
        outlier_format = workbook.add_format({'bg_color': '#FAA9A5', 'align': 'left'})
        self.options = {
            'format': outlier_format
            }

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


        scale_name = 'Озабоченность весом и формой тела '
        cols = ['ED15_2', 'ED15_4', 'ED15_5', 'ED15_6', 'ED15_9', 'ED15_10']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(
            lambda x: '{:.2f}'.format(x) if not np.isnan(x) else '')

        scale_name = 'Озабоченность питанием '
        cols = ['ED15_1', 'ED15_3', 'ED15_7', 'ED15_8']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(
            lambda x: '{:.2f}'.format(x) if not np.isnan(x) else '')

        scale_name = 'Общий балл'
        cols = ['ED15_1', 'ED15_2', 'ED15_3', 'ED15_4', 'ED15_5', 'ED15_6', 'ED15_7', 'ED15_8', 'ED15_9', 'ED15_10']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(
            lambda x: '{:.2f}'.format(x) if not np.isnan(x) else '')

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

    def format(self):
        initial_row_index = 48
        self.worksheet.set_row(initial_row_index, None, self.header_format)

        initial_row_index += 1
        for row_index in range(initial_row_index, initial_row_index + 3):
            self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        if self.transposed_worksheet is not None:
            initial_col_index = 48 - 6
            for col_index in range(initial_col_index, initial_col_index + 3):
                self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.options)
