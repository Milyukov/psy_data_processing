from model.quiz import Quiz
import pandas as pd

class NVM(Quiz):

    def __init__(self, start_col, count, columns) -> None:
        super().__init__(start_col, count, columns)

    def eval(self, data):
        self.data_frame = pd.DataFrame([''] * len(data), columns=['NVM - Нидерландский личностный опросник'])
        cols = 'NVM_4+NVM_6+NVM_9+NVM_10+NVM_16+NVM_21+NVM_22+NVM_24+NVM_31+NVM_32+NVM_33+NVM_38+NVM_43+NVM_48+NVM_49+NVM_51+NVM_58+NVM_59+NVM_69+NVM_70+NVM_80+NVM_82'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Негативизм'] = data[cols].replace('', 0).sum(axis=1, skipna=False)

        cols = 'NVM_1+NVM_2+NVM_3+NVM_5+NVM_7+NVM_11+NVM_12+NVM_13+NVM_14+NVM_15+NVM_17+NVM_19+NVM_25+NVM_27+NVM_30+NVM_35+NVM_37+NVM_41+NVM_52+NVM_54'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Соматизация'] = data[cols].replace('', 0).sum(axis=1, skipna=False)

        cols = 'NVM_20+NVM_36+NVM_39+NVM_42+NVM_45+NVM_55+NVM_60+NVM_63+NVM_64+NVM_65+NVM_68+NVM_71+NVM_73+NVM_79+NVM_81'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Застенчивость'] = data[cols].replace('', 0).sum(axis=1, skipna=False)

        cols = 'NVM_8+NVM_18+NVM_26+NVM_28+NVM_29+NVM_34+NVM_44+NVM_57+NVM_61+NVM_66+NVM_67+NVM_74+NVM_75'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Психопатология'] = data[cols].replace('', 0).sum(axis=1, skipna=False)

        cols = 'NVM_23+NVM_40+NVM_46+NVM_47+NVM_50+NVM_53+NVM_56+NVM_62+NVM_72+NVM_76+NVM_77+NVM_78+NVM_83'
        cols = cols.split('+')
        for i, col in enumerate(cols):
            cols[i] = col.lower()
        self.data_frame['Экстраверсия'] = data[cols].replace('', 0).sum(axis=1, skipna=False)

    def format(self, original_data_frame, show_reference):
        data_frame = original_data_frame.copy()
        return data_frame
