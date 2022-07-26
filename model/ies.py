from model.quiz import Quiz
import pandas as pd

class Ies(Quiz):

    def __init__(self, start_col, count, columns, workbook, worksheet) -> None:
        super().__init__(start_col, count, columns, worksheet)
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
            'minimum': 2.8,
            'maximum': 4.2,
            'format': outlier_format
        }

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Шкала интуитивного питания  (IES-23)'])
        cols = ['IES_1', 'IES_2', 'IES_3', 'IES_4', 'IES_5', 'IES_6']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Безусловное разрешение есть'] = data[cols].replace('', 0).mean(axis=1)

        cols = ['IES_7', 'IES_8', 'IES_9', 'IES_10', 'IES_11', 'IES_12', 'IES_13', 'IES_14']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Прием пищи по физическим, а не эмоциональным причинам'] = data[cols].replace('', 0).mean(axis=1)

        cols = ['IES_15', 'IES_16', 'IES_17', 'IES_18', 'IES_19', 'IES_20']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Доверие внутренним ощущениям голода и сытости'] = data[cols].replace('', 0).mean(axis=1)


        cols = ['IES_21', 'IES_22', 'IES_23']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Конгруэнтность "Тело/Выбор еды"'] = data[cols].replace('', 0).mean(axis=1)

        cols = ['ies_{}'.format(i) for i in range(1, self.count + 1)]
        self.data_frame['IES_Общий балл'] = data[cols].mean(axis=1)

    def format(self):
        row_index = 24
        self.worksheet.set_row(row_index, None, self.header_format)
        
        self.options['minimum'] = 2.8
        self.options['maximum'] = 4.2
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 2.33
        self.options['maximum'] = 4.03
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 2.91
        self.options['maximum'] = 4.23
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 2.49
        self.options['maximum'] = 4.09
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)

        self.options['minimum'] = 2.9
        self.options['maximum'] = 3.86
        row_index += 1
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
        self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)
