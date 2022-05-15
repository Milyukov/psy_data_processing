from model.quiz import Quiz
import pandas as pd
import numpy as np

class Ders(Quiz):

    def __init__(self, start_col, count, workbook) -> None:
        super().__init__(start_col, count)
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

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Шкала трудностей эмоциональной регуляции (DERS-18)'])
        scale_name = 'Осозанность'
        cols = 'DERS_1+DERS_4+DERS_6'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

        scale_name = 'Ясность'
        cols = 'DERS_2+DERS_3+DERS_5'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

        scale_name = 'Целенаправленность'
        cols = 'DERS_8+DERS_12+DERS_15'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

        scale_name = 'Управление импульсами'
        cols = 'DERS_9+DERS_16+DERS_18'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

        scale_name = 'Непринятие эмоциональных реакций'
        cols = 'DERS_7+DERS_13+DERS_14'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

        scale_name = 'Стратегии'
        cols = 'DERS_10+DERS_11+DERS_17'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

        cols = ['ders_{}'.format(i) for i in range(1, self.count + 1)]
        self.data_frame['DERS_Общий балл'] = data[cols].sum(axis=1, skipna=False).apply(lambda x: '{:.0f}'.format(x) if not np.isnan(x) else '')

    def format(self, worksheet, general_res):
        initial_row_index = 40
        worksheet.set_row(initial_row_index, None, self.header_format)

        initial_row_index += 1
        for row_index in range(initial_row_index, initial_row_index + 7):
            worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, self.blank)
