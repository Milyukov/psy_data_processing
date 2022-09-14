from model.quiz import Quiz
import pandas as pd
import numpy as np

class Dass(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Шкала депрессии, тревоги и стресса (DASS-21)'])
        cols = ['DASS_3', 'DASS_5', 'DASS_10', 'DASS_13', 'DASS_16', 'DASS_17', 'DASS_21']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Депрессия'] = 2 * data[cols].sum(axis=1, skipna=False)

        cols = ['DASS_2', 'DASS_4', 'DASS_7', 'DASS_9', 'DASS_15', 'DASS_19', 'DASS_20']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Тревога'] = 2 * data[cols].sum(axis=1, skipna=False)

        cols = ['DASS_1', 'DASS_6', 'DASS_8', 'DASS_11', 'DASS_12', 'DASS_14', 'DASS_18']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Стресс'] = 2 * data[cols].sum(axis=1, skipna=False)

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()

        def format_answer(x, suffix):
            if np.isnan(x):
                return ''
            if show_reference:
                return f'{x:.0f} ({suffix})'
            return f'{x:.0f}'


        min_vals = [0, 10, 14, 21, 28]
        max_vals = [9, 13, 20, 27, 10000]
        suffixes = ['Нормативно', 'Неявно выражено', 'Средне выражено', 'Явно выражено', 'Крайне тяжело']
        locs = []
        for min_val, max_val in zip(min_vals, max_vals):
            locs.append(data_frame['Депрессия'].replace('', 20000).between(min_val, max_val).values)
        for index, loc in enumerate(locs):
            data_frame.loc[loc, 'Депрессия'] = data_frame.loc[loc, 'Депрессия'].apply(lambda x: format_answer(x, suffixes[index]))

        min_vals = [0, 8, 10, 15, 20]
        max_vals = [7, 9, 14, 19, 10000]
        locs = []
        for min_val, max_val in zip(min_vals, max_vals):
            locs.append(data_frame['Тревога'].replace('', 20000).between(min_val, max_val).values)
        for index, loc in enumerate(locs):
            data_frame.loc[loc, 'Тревога'] = data_frame.loc[loc, 'Тревога'].apply(lambda x: format_answer(x, suffixes[index]))        

        min_vals = [0, 15, 19, 26, 34]
        max_vals = [14, 18, 25, 33, 10000]
        locs = []
        for min_val, max_val in zip(min_vals, max_vals):
            locs.append(data_frame['Стресс'].replace('', 20000).between(min_val, max_val).values)
        for index, loc in enumerate(locs):
            data_frame.loc[loc, 'Стресс'] = data_frame.loc[loc, 'Стресс'].apply(lambda x: format_answer(x, suffixes[index]))

        return data_frame
