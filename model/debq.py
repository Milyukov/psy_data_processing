from model.quiz import Quiz
import pandas as pd
import numpy as np

class Debq(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

    def eval(self, data):

        
        
        self.data_frame = pd.DataFrame([''] * len(data), columns=['Опросник стиля пищевого поведения / Голладский пищевой опросник (DEBQ)'])
        scale_name = 'Ограничительный'
        cols = ['DEBQ_1', 'DEBQ_2', 'DEBQ_3', 'DEBQ_4', 'DEBQ_5', 'DEBQ_6', 'DEBQ_7', 'DEBQ_8', 'DEBQ_9', 'DEBQ_10']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)
        

        scale_name = 'Эмоциональный'
        cols = ['DEBQ_11', 'DEBQ_12', 'DEBQ_13', 'DEBQ_14', 'DEBQ_15', 'DEBQ_16', 'DEBQ_17', 'DEBQ_18', 'DEBQ_19', 'DEBQ_20', 'DEBQ_21', 'DEBQ_22', 'DEBQ_23']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)

        scale_name = 'Экстернальный'
        cols = ['DEBQ_24', 'DEBQ_25', 'DEBQ_26', 'DEBQ_27', 'DEBQ_28', 'DEBQ_29', 'DEBQ_30', 'DEBQ_31', 'DEBQ_32', 'DEBQ_33']
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame[scale_name] = data[cols].replace('', 0).mean(axis=1)

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()
        
        def format_answer(x, suffix):
            if np.isnan(x):
                return ''
            if show_reference:
                return f'{x:.2f} {suffix}'
            return f'{x:.2f}'

        scale_name = 'Ограничительный'
        data_frame[scale_name] = data_frame[scale_name].apply(lambda x: format_answer(x, '(норма: 2.4)'))
        scale_name = 'Эмоциональный'
        data_frame[scale_name] = data_frame[scale_name].apply(lambda x: format_answer(x, '(норма: 1.8)'))
        scale_name = 'Экстернальный'
        data_frame[scale_name] = data_frame[scale_name].apply(lambda x: format_answer(x, '(норма: 2.7)'))
        return data_frame
