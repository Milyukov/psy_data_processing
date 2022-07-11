from model.quiz import Quiz
import pandas as pd
import numpy as np

class Debq(Quiz):

    def __init__(self, start_col, count, columns, workbook, worksheet) -> None:
        super().__init__(start_col, count, columns, worksheet)
        self.header_format = workbook.add_format({'bg_color': 'yellow'})
        outlier_format = workbook.add_format({'align': 'left'})
        self.options = {
            'format': outlier_format
            }

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Опросник стиля пищевого поведения / Голладский пищевой опросник (DEBQ)'])
        scale_name = 'Ограничительный'
        cols = ['DEBQ_1', 'DEBQ_2', 'DEBQ_3', 'DEBQ_4', 'DEBQ_5', 'DEBQ_6', 'DEBQ_7', 'DEBQ_8', 'DEBQ_9', 'DEBQ_10']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(
            lambda x: '{:.2f}'.format(x) + " (норма: 2.4)" if not np.isnan(x) else '')

        scale_name = 'Эмоциональный'
        cols = ['DEBQ_11', 'DEBQ_12', 'DEBQ_13', 'DEBQ_14', 'DEBQ_15', 'DEBQ_16', 'DEBQ_17', 'DEBQ_18', 'DEBQ_19', 'DEBQ_20', 'DEBQ_21', 'DEBQ_22', 'DEBQ_23']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(
            lambda x: '{:.2f}'.format(x) + " (норма: 1.8)" if not np.isnan(x) else '')

        scale_name = 'Экстернальный'
        cols = ['DEBQ_24', 'DEBQ_25', 'DEBQ_26', 'DEBQ_27', 'DEBQ_28', 'DEBQ_29', 'DEBQ_30', 'DEBQ_31', 'DEBQ_32', 'DEBQ_33']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        self.data_frame[scale_name] = self.data_frame[scale_name].apply(
            lambda x: '{:.2f}'.format(x) + " (норма: 2.7)" if not np.isnan(x) else '')

    def format(self):
        initial_row_index = 30
        self.worksheet.set_row(initial_row_index, None, self.header_format)

        initial_row_index += 1
        for row_index in range(initial_row_index, initial_row_index + 3):
            self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, self.options)
