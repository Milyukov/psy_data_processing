from model.quiz import Quiz
import pandas as pd
import numpy as np

class Ders(Quiz):

    def __init__(self, start_col, count, columns, workbook, worksheet, show_reference) -> None:
        super().__init__(start_col, count, columns, worksheet)
        self.header_format = workbook.add_format({'bg_color': 'yellow'})
        outlier_format = workbook.add_format({'align': 'left'})
        self.options = {
            'format': outlier_format
            }
        blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
        self.blank = {
            'type': 'blanks', 
            'stop_if_true': True, 
            'format': blank_format,
            }
        self.show_reference = show_reference

    def eval(self, data):


        def format_cell(x):
            if x == '':
                return x
            elif np.isnan(x):
                return ''
            elif self.show_reference:
                return f'{x:.0f} из 15'
            else:
                return f'{x:.0f}'

        def format_cell_general(x):
            if x == '':
                return x
            elif np.isnan(x):
                return ''
            else:
                return f'{x:.0f}'

        self.data_frame = pd.DataFrame([''] * len(data), columns=['Шкала трудностей эмоциональной регуляции (DERS-18)'])
        scale_name = 'Осозанность'
        cols = 'DERS_1+DERS_4+DERS_6'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(format_cell)

        scale_name = 'Ясность'
        cols = 'DERS_2+DERS_3+DERS_5'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(format_cell)

        scale_name = 'Целенаправленность'
        cols = 'DERS_8+DERS_12+DERS_15'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(format_cell)

        scale_name = 'Управление импульсами'
        cols = 'DERS_9+DERS_16+DERS_18'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(format_cell)

        scale_name = 'Непринятие эмоциональных реакций'
        cols = 'DERS_7+DERS_13+DERS_14'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(format_cell)

        scale_name = 'Стратегии'
        cols = 'DERS_10+DERS_11+DERS_17'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(format_cell)

        cols = ['ders_{}'.format(i) for i in range(1, self.count + 1)]
        self.data_frame['DERS_Общий балл'] = data[cols].sum(axis=1, skipna=False).apply(format_cell_general)

    def format(self):
        initial_row_index = 40
        self.worksheet.set_row(initial_row_index, None, self.header_format)

        initial_row_index += 1
        for row_index in range(initial_row_index, initial_row_index + 7):
            self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.blank)
