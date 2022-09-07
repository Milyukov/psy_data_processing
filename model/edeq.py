from model.quiz import Quiz
import pandas as pd

class Edeq(Quiz):

    def __init__(self, start_col, count, columns, workbook, worksheet, transposed_worksheet=None) -> None:
        super().__init__(start_col, count, columns, worksheet, transposed_worksheet)
        self.header_format = workbook.add_format({'bg_color': 'yellow'})
        outlier_format = workbook.add_format({'bg_color': '#FAA9A5', 'align': 'left'})
        blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
        self.blank = {
            'type': 'blanks', 
            'stop_if_true': True, 
            'format': blank_format
            }

        self.options = {
            'type': 'cell',
            'criteria': 'not between',
            'minimum': -0.07,
            'maximum': 2.57,
            'format': outlier_format
        }

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

    def format(self):
        row_index = 3
        self.worksheet.set_row(row_index, None, self.header_format)

        self.options['minimum'] = -0.07
        self.options['maximum'] = 2.57
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = -0.24
        self.options['maximum'] = 1.48
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 0.55
        self.options['maximum'] = 3.75
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 0.22
        self.options['maximum'] = 2.96
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 0.34
        self.options['maximum'] = 2.77
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        if self.transposed_worksheet is not None:
            col_index = 3
            self.options['minimum'] = -0.07
            self.options['maximum'] = 2.57
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.blank)
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.options)

            self.options['minimum'] = -0.24
            self.options['maximum'] = 1.48
            col_index += 1
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.blank)
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.options)

            self.options['minimum'] = 0.55
            self.options['maximum'] = 3.75
            col_index += 1
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.blank)
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.options)

            self.options['minimum'] = 0.22
            self.options['maximum'] = 2.96
            col_index += 1
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.blank)
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.options)

            self.options['minimum'] = 0.34
            self.options['maximum'] = 2.77
            col_index += 1
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.blank)
            self.transposed_worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, self.options)
