from copy import deepcopy
import pandas as pd
import numpy as np
from model.edeq import Edeq
from model.dass import Dass
from model.ies import Ies
from model.debq import Debq
from model.nvm import NVM
from model.ders import Ders
from model.ed15 import Ed

from model.sheet.general import GeneralInfo
from model.sheet.transposed import TransposedGeneralInfo

import tests.utils.tables as utils
import re

class Model:

    def __init__(self) -> None:
        self.replace_answers_dict_edeq = {
            # EDEQ
            'ни одного': 0,
            '1-5 дней':	1,
            '6-12 дней': 2,
            '13-15 дней': 3,
            '16-22 дней': 4,
            '23-27 дней': 5,
            'каждый день': 6,
            'несколько': 1,
            'менее половины':2,
            'половина': 3,
            'более половины': 4,
            'большинство': 5,
            'все': 6,
            'совсем нет': 0,
            'слегка': 2,
            'умеренно': 4,
            'существенно': 6,
            np.nan: '',
            'nan': '',
            'NaN': '',
            'мой ответ': 0
        }
        
        self.replace_answers_dict_dass = {
            # DASS
            'вообще не относится ко мне': 0,
            'относилось ко мне до некоторой степени или некоторое время': 1,
            'относилось ко мне в значительной мере или значительную часть времени': 2,
            'относилось ко мне полностью или большую часть времени': 3,
            np.nan: '',
            'nan': '',
            'NaN': ''
        }
        self.replace_answers_dict_ies = {
            # IES
            'полностью не согласен': 1,
            'не согласен': 2,
            'ни то, ни другое': 3,
            'согласен': 4,
            'полностью согласен': 5
        }
        self.replace_answers_dict_debq = {
            # DEBQ
            'никогда': 1,
            'очень редко': 2,
            'иногда': 3,
            'часто': 4,
            'очень часто': 5
        }
        self.replace_answers_dict_nvm = {
            # NVM
            'неверно': 0,
            'затрудняюсь ответить': 1,
            'верно': 2,
            np.nan: '',
            'nan': '',
            'NaN': ''
        }

        self.replace_answers_dict_ders = {
            # DERS
            'почти никогда (0-10%)': 1,
            'иногда (11-35%)': 2,
            'примерно половину времени (36-65%)': 3,
            'большую часть времени (66-90%)': 4,
            'почти всегда (91-100%)': 5,
            np.nan: '',
            'nan': '',
            'NaN': ''
        }

        self.replace_answers_dict_ed15 = {
            'никогда': 0,
            'редко': 1,
            'изредка': 2,
            'иногда': 3,
            'часто': 4,
            'очень часто': 5,
            'всегда': 6
        }

        self.replace_answers_dict_ed15_back = {val: key for (key, val) in self.replace_answers_dict_ed15.items()}

        self.age_col = 'Возраст (ДАННЫЕ ПАЦИЕНТА)'.lower()
        self.name_col = 'ФИО (EDE-Q (ПИЩЕВОЕ ПОВЕДЕНИЕ))'.lower()

    @staticmethod
    def upper_first_letters(s):
        if not isinstance(s, str):
            if np.isnan(s):
                return ''
            s = str(s)
        words = s.split()
        new_words = []
        for word in words:
            new_words.append(word[0].upper() + word[1:])
        return ' '.join(new_words)

    @staticmethod
    def format_weight(val):
        val_str = '{}'.format(val)
        res = re.findall('\d*\.?,?\d+',val_str)
        if len(res) > 0:
            res = res[0].replace(',', '.')
            return float(res)
        return 0.0

    @staticmethod
    def format_height(val):
        val_str = '{}'.format(val)
        res = re.findall('\d*\.?,?\d+',val_str)
        if len(res) > 0:
            res = res[0].replace(',', '.')
            if '.' in res:
                integer_part, fraction = res.split('.')
                if float(integer_part) >= 100:
                    return float(res) / 100.0
                return float(res)
            else:
                return float(res) / 100.0
        return 0.0

    def process_data_frame(self):
        # get questions names
        question_cols = []
        questions = {}
        for q in self.quizes:
            cols = self.quizes[q].get_cols()
            questions[q] = cols
            question_cols.extend(cols)

        additional_info = [self.name_col, 'название клиента', self.age_col]
        self.original_data = self.original_data[additional_info + question_cols]

        # generate new question names
        self.questions_to_codes = {}
        self.codes_to_questions = {}

        for key in questions:
            for number, q in enumerate(questions[key]):
                self.questions_to_codes[q] = '{}_{}'.format(key, number + 1)
                self.codes_to_questions['{}_{}'.format(key, number + 1)] = q

        data = utils.replace_questions(self.original_data, self.questions_to_codes)

        # generate new answers names
        inverted_columns = ['IES_1', 'IES_2', 'IES_3', 'IES_7', 'IES_8', 'IES_9', 'IES_10', 'DEBQ_31', 'DERS_1', 'DERS_4', 'DERS_6']
        for index, col in enumerate(inverted_columns):
            inverted_columns[index] = col.lower()

        edeq_data = utils.replace_answers(data[['edeq_{}'.format(i) for i in range(1, self.quizes['edeq'].count + 1)]], self.replace_answers_dict_edeq)
        dass_data = utils.replace_answers(data[['dass_{}'.format(i) for i in range(1, self.quizes['dass'].count + 1)]], self.replace_answers_dict_dass)
        ies_data = utils.replace_answers(data[['ies_{}'.format(i) for i in range(1, self.quizes['ies'].count + 1)]], self.replace_answers_dict_ies)
        debq_data = utils.replace_answers(data[['debq_{}'.format(i) for i in range(1, self.quizes['debq'].count + 1)]], self.replace_answers_dict_debq)
        nvm_data = utils.replace_answers(data[['nvm_{}'.format(i) for i in range(1, self.quizes['nvm'].count + 1)]], self.replace_answers_dict_nvm)
        ders_data = utils.replace_answers(data[['ders_{}'.format(i) for i in range(1, self.quizes['ders'].count + 1)]], self.replace_answers_dict_ders)
        ed15_data = utils.replace_answers(data[['ed15_{}'.format(i) for i in range(1, self.quizes['ed15'].count + 1)]], self.replace_answers_dict_ed15)

        self.data = pd.concat([edeq_data, dass_data, ies_data, debq_data, nvm_data, ders_data, ed15_data], axis=1)
        self.data['возраст'] = self.original_data[self.age_col].fillna(0).astype(int)

        names = self.original_data[[self.name_col, 'название клиента']].apply(lambda x: x[x.first_valid_index()], axis=1)
        self.data.insert(0, 'фио', names)

        replace_inverted_answers_dict = {
            1: 5,
            2: 4,
            4: 2,
            5: 1
        }

        self.data[inverted_columns] = utils.replace_answers(self.data[inverted_columns], replace_inverted_answers_dict)

        client_data = pd.DataFrame()
        client_data.insert(0, 'Возраст', self.data['возраст'])
        weight = self.data['edeq_29'].fillna(0).apply(self.format_weight)
        height = self.data['edeq_30'].fillna(0).apply(self.format_height)
        client_data.insert(1, 'ИМТ', weight.div(height.apply(lambda x: x ** 2)).apply(lambda x: f'{x:.2f}'))
        return client_data

    def post_process_data(self):
        self.general_res = self.general_res.replace(np.nan, '')
        self.general_res = self.general_res.replace('nan', '')
        self.data['фио'] = self.data['фио'].apply(self.upper_first_letters)
        self.general_res.set_axis(self.data['фио'], inplace=True)

        self.general_res_transposed = self.general_res_transposed.replace(np.nan, '')
        self.general_res_transposed = self.general_res_transposed.replace('nan', '')
        self.general_res_transposed.set_axis(self.data['фио'], inplace=True)

        self.general_res_transposed_with_info = self.general_res_transposed_with_info.replace(np.nan, '')
        self.general_res_transposed_with_info = self.general_res_transposed_with_info.replace('nan', '')
        self.general_res_transposed_with_info.set_axis(self.data['фио'], inplace=True)
        # edeq_cols = self.general_res_transposed.iloc[:, 4:8].columns.values
        # self.general_res_transposed[edeq_cols] = self.general_res_transposed[edeq_cols].apply(lambda x: f'{x:.2f}')

    def add_info_for_ed15(self, workbook, worksheet):
        # additional info for ED-15
        # head
        cell_format = workbook.add_format(
            {
                'font_color': 'red', 
                'bold': True,
                'font_size': 11,
                'font_name': 'Calibri'
                }
                )
        worksheet.write('A70', 'Нормы для ED-15', cell_format)

        cell_format = workbook.add_format({'bold': True, 'align': 'center'})
        worksheet.merge_range('B70:C70', 'Здоровые', cell_format)
        worksheet.merge_range('D70:E70', 'Здоровые', cell_format)
        worksheet.merge_range('F70:G70', 'Нервная анорексия', cell_format)
        worksheet.merge_range('H70:I70', 'Нервная анорексия', cell_format)
        worksheet.merge_range('J70:K70', 'Булимия', cell_format)
        worksheet.merge_range('L70:M70', 'Булимия', cell_format)
        worksheet.merge_range('N70:O70', 'НРПП', cell_format)
        worksheet.merge_range('P70:Q70', 'НРПП', cell_format)

        cell_format = workbook.add_format()
        # first row
        worksheet.write('B71', 'Среднее', cell_format)
        worksheet.write('C71', 'СКО', cell_format)
        worksheet.write('D71', 'Нижняя граница', cell_format)
        worksheet.write('E71', 'Верхняя граница', cell_format)
        worksheet.write('F71', 'Среднее', cell_format)
        worksheet.write('G71', 'СКО', cell_format)
        worksheet.write('H71', 'Нижняя граница', cell_format)
        worksheet.write('I71', 'Верхняя граница', cell_format)
        worksheet.write('J71', 'Среднее', cell_format)
        worksheet.write('K71', 'СКО', cell_format)
        worksheet.write('L71', 'Нижняя граница', cell_format)
        worksheet.write('M71', 'Верхняя граница', cell_format)
        worksheet.write('N71', 'Среднее', cell_format)
        worksheet.write('O71', 'СКО', cell_format)
        worksheet.write('P71', 'Нижняя граница', cell_format)
        worksheet.write('Q71', 'Верхняя граница', cell_format)

        # second row
        worksheet.write('A72', 'Озабоченность весом и формой тела', cell_format)
        worksheet.write('B72', '1,79', cell_format)
        worksheet.write('C72', '1,49', cell_format)
        worksheet.write('D72', '0,3', cell_format)
        worksheet.write('E72', '3,28', cell_format)
        worksheet.write('F72', '3,93', cell_format)
        worksheet.write('G72', '1,35', cell_format)
        worksheet.write('H72', '2,58', cell_format)
        worksheet.write('I72', '5,28', cell_format)
        worksheet.write('J72', '4,58', cell_format)
        worksheet.write('K72', '0,87', cell_format)
        worksheet.write('L72', '3,71', cell_format)
        worksheet.write('M72', '5,45', cell_format)
        worksheet.write('N72', '3,77', cell_format)
        worksheet.write('O72', '1,27', cell_format)
        worksheet.write('P72', '2,5', cell_format)
        worksheet.write('Q72', '5,04', cell_format)

        # # third row
        worksheet.write('A73', 'Озабоченность питанием', cell_format)
        worksheet.write('B73', '2,44', cell_format)
        worksheet.write('C73', '1,37', cell_format)
        worksheet.write('D73', '1,07', cell_format)
        worksheet.write('E73', '3,81', cell_format)
        worksheet.write('F73', '4,66', cell_format)
        worksheet.write('G73', '0,91', cell_format)
        worksheet.write('H73', '3,75', cell_format)
        worksheet.write('I73', '5,57', cell_format)
        worksheet.write('J73', '4,33', cell_format)
        worksheet.write('K73', '1,1', cell_format)
        worksheet.write('L73', '3,23', cell_format)
        worksheet.write('M73', '5,43', cell_format)
        worksheet.write('N73', '3,84', cell_format)
        worksheet.write('O73', '0,86', cell_format)
        worksheet.write('P73', '2,98', cell_format)
        worksheet.write('Q73', '4,7', cell_format)

        # # fourth row
        worksheet.write('A74', 'Общий балл', cell_format)
        worksheet.write('B74', '2,05', cell_format)
        worksheet.write('C74', '1,33', cell_format)
        worksheet.write('D74', '0,72', cell_format)
        worksheet.write('E74', '3,38', cell_format)
        worksheet.write('F74', '4,22', cell_format)
        worksheet.write('G74', '1,14', cell_format)
        worksheet.write('H74', '3,08', cell_format)
        worksheet.write('I74', '5,36', cell_format)
        worksheet.write('J74', '4,48', cell_format)
        worksheet.write('K74', '0,9', cell_format)
        worksheet.write('L74', '3,58', cell_format)
        worksheet.write('M74', '5,38', cell_format)
        worksheet.write('N74', '3,8', cell_format)
        worksheet.write('O74', '0,89', cell_format)
        worksheet.write('P74', '2,91', cell_format)
        worksheet.write('Q74', '4,69', cell_format)

    def add_additional_sheet(self, workbook):
        # additional sheet
        summary_cols = ['Ограничение питания', 'Избегание питания', 'Избегание пищи', 'Правила питания', 'Пустой желудок', 
        'Озабоченность пищей, питанием или калориями', 'Страх потери контроля над питанием', 'Питание втайне от других', 
        'Питание в социальном контексте', 'Чувство вины в связи с питанием', 'Плоский живот', 'Озабоченность формой тела или весом', 
        'Значение формы тела', 'Страх набора веса', 'Неудовлетворённость формой тела', 'Дискомфорт при виде своего тела', 
        'Избегание демонстрации тела', 'Ощущение полноты', 'Важность веса', 'Реакция на просьбу взвешиваться', 'Озабоченность формой тела или весом',
        'Неудовлетворённость весом', 'Желание сбросить вес']

        capital_codes = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 
        'EDEQ_4', 'EDEQ_5', 'EDEQ_7', 'EDEQ_9', 'EDEQ_19', 'EDEQ_21', 'EDEQ_20', 'EDEQ_6', 'EDEQ_8', 'EDEQ_23', 'EDEQ_10', 
        'EDEQ_26', 'EDEQ_27', 'EDEQ_28', 'EDEQ_11', 'EDEQ_22', 'EDEQ_24', 'EDEQ_8', 'EDEQ_25', 'EDEQ_12']

        codes = [code.lower() for code in capital_codes]

        questions = [self.codes_to_questions[code] for code in codes]

        additional_data_frame = self.original_data[questions]
        names = self.original_data[self.name_col].apply(self.upper_first_letters)
        additional_data_frame.insert(0, 'фио', names)
        additional_data_frame = utils.replace_questions(additional_data_frame, self.questions_to_codes)
        additional_data_frame = utils.replace_answers(additional_data_frame, self.replace_answers_dict_edeq)

        additional_data = additional_data_frame.values

        data = np.array([
            ['ФИО'] + summary_cols
        ])
        additional_data = np.concatenate([data, additional_data], axis=0)

        additional_data_frame = pd.DataFrame(data=additional_data)
        additional_data_frame.to_excel(self.writer, index=False, sheet_name='additional')

        worksheet = self.writer.sheets['additional']
        # Create a format to use in the merged range.
        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#d9d2e9'})
        merge_format.set_font_size(10)
        merge_format.set_font_name('Arial')


        # Format cells.
        worksheet.merge_range('B1:F1', 'Ограничения', merge_format)
        worksheet.merge_range('G1:K1', 'Беспокойство о питании', merge_format)
        worksheet.merge_range('L1:S1', 'Беспокойство о форме тела', merge_format)
        worksheet.merge_range('T1:X1', 'Беспокойство о весе', merge_format)

        cell_format = workbook.add_format({'fg_color': '#ead1dc', 'text_wrap': True})
        cell_format.set_font_size(10)
        cell_format.set_font_name('Arial')
        worksheet.write('F2', 'Пустой желудок', cell_format)
        worksheet.write('K2', 'Чувство вины в связи с питанием', cell_format)
        worksheet.write('S2', 'Ощущение полноты', cell_format)
        worksheet.write('X2', 'Желание сбросить вес', cell_format)

        row_format = workbook.add_format({'text_wrap': True})
        row_format.set_font_size(10)
        row_format.set_font_name('Arial')
        worksheet.set_row(1, 80, row_format)

        col_format = workbook.add_format()
        col_format.set_font_size(10)
        col_format.set_font_name('Arial')
        worksheet.set_column(0, 0, 30, col_format)
        worksheet.set_column(1, len(summary_cols), 10, col_format)

    def process(self, input_filename, output_filename) -> None:
        # generate data frame for quiz evaluation
        self.input_filename = input_filename
        self.original_data = utils.prepare_data_frame(self.input_filename, sheet_name=0)
        self.original_data = utils.drop_columns(self.original_data, contains='дата заполнения')
        self.original_data = utils.drop_columns(self.original_data, contains='этап')
        self.original_data = utils.drop_columns(self.original_data, contains='город проживания')
        columns = self.original_data.columns.values

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        self.writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = self.writer.book

        self.quizes = {}
        # EDEQ
        self.quizes['edeq'] = Edeq(3, 33, columns)

        # DASS
        self.quizes['dass'] = Dass(self.quizes['edeq'].ec, 21, columns)

        # IES
        self.quizes['ies'] = Ies(self.quizes['dass'].ec, 23, columns)

        # DEBQ
        self.quizes['debq'] = Debq(self.quizes['ies'].ec, 33, columns)

        # NVM
        self.quizes['nvm'] = NVM(self.quizes['debq'].ec, 83, columns)

        # DERS
        self.quizes['ders'] = Ders(self.quizes['nvm'].ec, 18, columns)

        # ED-15
        self.quizes['ed15'] = Ed(self.quizes['ders'].ec, 15, columns)

        # preprocess *.xlsx-file
        client_data = self.process_data_frame()

        # calc the statistics
        for q in self.quizes.values():
            q.eval(self.data)

        cols = ['edeq_13', 'edeq_14', 'edeq_15', 'edeq_16', 'edeq_17', 'edeq_18',
        'edeq_29', 'edeq_30', 'edeq_31', 'edeq_32', 'edeq_33']
        for c in cols:
            question = self.codes_to_questions[c]
            question = question[0].upper() + question[1:]
            self.codes_to_questions[c] = question
            self.quizes['edeq'].data_frame[self.codes_to_questions[c]] = self.data[c].apply(str)

        self.general_res = pd.concat([client_data] + [val.format(val.data_frame, True) for val in self.quizes.values()], axis=1)
        self.general_res_transposed = pd.concat([client_data] + [val.format(val.data_frame, False).loc[:, val.data_frame.columns[1:]] for val in self.quizes.values()], axis=1)
        self.general_res_transposed_with_info = pd.concat([client_data] + [val.format(val.data_frame, True).loc[:, val.data_frame.columns[1:]] for val in self.quizes.values()], axis=1)

        self.post_process_data()

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        sheets = []
        self.data.to_excel(self.writer, index=False, sheet_name='replaced')
        
        self.general_res_transposed.reset_index(inplace=True)
        transposed_sheet = TransposedGeneralInfo(self.general_res_transposed, self.writer, 'transposed')
        sheets.append(transposed_sheet)

        self.general_res_transposed_with_info.reset_index(inplace=True)
        transposed_sheet_2 = TransposedGeneralInfo(self.general_res_transposed_with_info, self.writer, 'transposed_with_text')
        sheets.append(transposed_sheet_2)

        self.general_res = self.general_res.transpose()
        self.general_res.reset_index(inplace=True)
        general_sheet = GeneralInfo(self.general_res, self.writer, 'general')
        sheets.append(general_sheet)

        # format data
        for s in sheets:
            s.format(workbook)

        self.add_info_for_ed15(workbook, general_sheet.worksheet)

        self.add_additional_sheet(workbook)

        # Close the Pandas Excel writer and output the Excel file.
        self.writer.save()
