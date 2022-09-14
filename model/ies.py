from model.quiz import Quiz
import pandas as pd

class Ies(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

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

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()
        return data_frame
