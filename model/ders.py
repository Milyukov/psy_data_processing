from model.quiz import Quiz
import pandas as pd
import numpy as np

class Ders(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Шкала трудностей эмоциональной регуляции (DERS-18)'])
        scale_name = 'Осозанность'
        cols = 'DERS_1+DERS_4+DERS_6'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)

        scale_name = 'Ясность'
        cols = 'DERS_2+DERS_3+DERS_5'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)
        scale_name = 'Целенаправленность'
        cols = 'DERS_8+DERS_12+DERS_15'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)

        scale_name = 'Управление импульсами'
        cols = 'DERS_9+DERS_16+DERS_18'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)

        scale_name = 'Непринятие эмоциональных реакций'
        cols = 'DERS_7+DERS_13+DERS_14'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)

        scale_name = 'Стратегии'
        cols = 'DERS_10+DERS_11+DERS_17'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].sum(axis=1, skipna=False)

        cols = ['ders_{}'.format(i) for i in range(1, self.count + 1)]
        self.data_frame['DERS_Общий балл'] = data[cols].sum(axis=1, skipna=False)

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()

        def format_cell(x):
            if x == '':
                return x
            elif np.isnan(x):
                return ''
            elif show_reference:
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
        
        for scale_name in ['Осозанность', 'Ясность', 'Целенаправленность', 'Управление импульсами', 'Непринятие эмоциональных реакций', 'Стратегии']:
            data_frame[scale_name] = data_frame[scale_name].apply(format_cell)
        data_frame['DERS_Общий балл'] = data_frame['DERS_Общий балл'].apply(format_cell_general)

        return data_frame
