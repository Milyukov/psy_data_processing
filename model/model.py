import pandas as pd
import numpy as np
from model.edeq import Edeq
from model.dass import Dass
from model.ies import Ies
from model.debq import Debq
from model.nvm import NVM
from model.ders import Ders
from model.ed15 import Ed

import tests.utils.tables as utils
import re

class Model:

    def __init__(self) -> None:
        pass

    def process_data_frame(self):
        # get questions names
        question_cols = []
        questions = {}
        for q in self.quizes:
            cols = self.quizes[q].get_cols()
            questions[q] = cols
            question_cols.extend(cols)

        additional_info = ['фио', 'возраст']
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
        replace_answers_dict_edeq = {
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
        
        replace_answers_dict_dass = {
            # DASS
            'вообще не относится ко мне': 0,
            'относилось ко мне до некоторой степени или некоторое время': 1,
            'относилось ко мне в значительной мере или значительную часть времени': 2,
            'относилось ко мне полностью или большую часть времени': 3,
            np.nan: '',
            'nan': '',
            'NaN': ''
        }
        replace_answers_dict_ies = {
            # IES
            'полностью не согласен': 1,
            'не согласен': 2,
            'ни то, ни другое': 3,
            'согласен': 4,
            'полностью согласен': 5
        }
        replace_answers_dict_debq = {
            # DEBQ
            'никогда': 1,
            'очень редко': 2,
            'иногда': 3,
            'часто': 4,
            'очень часто': 5
        }
        replace_answers_dict_nvm = {
            # NVM
            'неверно': 0,
            'затрудняюсь ответить': 1,
            'верно': 2,
            np.nan: '',
            'nan': '',
            'NaN': ''
        }

        replace_answers_dict_ders = {
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

        replace_answers_dict_ed15 = {
            'никогда': 0,
            'редко': 1,
            'изредка': 2,
            'иногда': 3,
            'часто': 4,
            'очень часто': 5,
            'всегда': 6
        }

        replace_answers_dict_ed15_back = {val: key for (key, val) in replace_answers_dict_ed15.items()}

        inverted_columns = ['IES_1', 'IES_2', 'IES_3', 'IES_7', 'IES_8', 'IES_9', 'IES_10', 'DEBQ_31', 'DERS_1', 'DERS_4', 'DERS_6']
        for index, col in enumerate(inverted_columns):
            inverted_columns[index] = col.lower()



        edeq_data = utils.replace_answers(data[['edeq_{}'.format(i) for i in range(1, self.quizes['edeq'].count + 1)]], replace_answers_dict_edeq)
        dass_data = utils.replace_answers(data[['dass_{}'.format(i) for i in range(1, self.quizes['dass'].count + 1)]], replace_answers_dict_dass)
        ies_data = utils.replace_answers(data[['ies_{}'.format(i) for i in range(1, self.quizes['ies'].count + 1)]], replace_answers_dict_ies)
        debq_data = utils.replace_answers(data[['debq_{}'.format(i) for i in range(1, self.quizes['debq'].count + 1)]], replace_answers_dict_debq)
        nvm_data = utils.replace_answers(data[['nvm_{}'.format(i) for i in range(1, self.quizes['nvm'].count + 1)]], replace_answers_dict_nvm)
        ders_data = utils.replace_answers(data[['ders_{}'.format(i) for i in range(1, self.quizes['ders'].count + 1)]], replace_answers_dict_ders)
        ed15_data = utils.replace_answers(data[['ed15_{}'.format(i) for i in range(1, self.quizes['ed15'].count + 1)]], replace_answers_dict_ed15)

        self.data = pd.concat([edeq_data, dass_data, ies_data, debq_data, nvm_data, ders_data, ed15_data], axis=1)
        self.data['возраст'] = self.original_data['возраст'].fillna(0).astype(int)

        names = self.original_data['фио']#.apply(lambda x: x[x.first_valid_index()], axis=1)
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

        def format_weight(val):
            val_str = '{}'.format(val)
            res = re.findall('\d*\.?,?\d+',val_str)
            if len(res) > 0:
                res = res[0].replace(',', '.')
                return float(res)
            return 0.0

        weight = self.data['edeq_29'].fillna(0).apply(format_weight)

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

        height = self.data['edeq_30'].fillna(0).apply(format_height)
        client_data.insert(1, 'ИМТ', weight.div(height.apply(lambda x: x ** 2)))
        return client_data

    def post_process_data(self):
        self.general_res = self.general_res.replace(np.nan, '')
        self.general_res = self.general_res.replace('nan', '')

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

        self.data['фио'] = self.data['фио'].apply(upper_first_letters)
        self.general_res.set_axis(self.data['фио'], inplace=True)

    def add_infor_for_ed15(self, workbook, worksheet):
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

    def process(self, input_filename, output_filename, mode) -> None:
        # generate data frame for quiz evaluation
        self.input_filename = input_filename
        self.original_data = utils.prepare_data_frame(self.input_filename, sheet_name=0)
        self.original_data = utils.drop_columns(self.original_data, contains='дата заполнения')
        self.original_data = utils.drop_columns(self.original_data, contains='этап')
        self.original_data = utils.drop_columns(self.original_data, contains='название клиента')
        self.original_data = utils.drop_columns(self.original_data, contains='город проживания')
        columns = self.original_data.columns.values

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        self.writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = self.writer.book
        empty_frame = pd.DataFrame()
        empty_frame.to_excel(self.writer, index=False, sheet_name='general')
        worksheet = self.writer.sheets['general']

        self.quizes = {}
        # EDEQ
        self.quizes['edeq'] = Edeq(2, 33, columns, workbook, worksheet)

        # DASS
        self.quizes['dass'] = Dass(self.quizes['edeq'].ec, 21, columns, workbook, worksheet)

        # IES
        self.quizes['ies'] = Ies(self.quizes['dass'].ec, 23, columns, workbook, worksheet)

        # DEBQ
        self.quizes['debq'] = Debq(self.quizes['ies'].ec, 33, columns, workbook, worksheet)

        # NVM
        self.quizes['nvm'] = NVM(self.quizes['debq'].ec, 83, columns, workbook, worksheet)

        # DERS
        self.quizes['ders'] = Ders(self.quizes['nvm'].ec, 18, columns, workbook, worksheet)

        # ED-15
        self.quizes['ed15'] = Ed(self.quizes['ders'].ec, 15, columns, workbook, worksheet)

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

        self.general_res = pd.concat([client_data] + [val.data_frame for val in self.quizes.values()], axis=1)

        self.post_process_data()

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        self.data.to_excel(self.writer, index=False, sheet_name='replaced')
        self.general_res = self.general_res.transpose()
        self.general_res.reset_index(inplace=True)
        self.general_res.to_excel(self.writer, index=False, sheet_name='general')

        # Add some cell formats.
        format_index = workbook.add_format({'text_wrap': True})
        format_index.set_bold(True)
        format_index.set_align('left')
        assert worksheet.set_column(0, 0, 50, format_index) == 0

        # format EDEQ, IES and DEBQ
        format_values = workbook.add_format({'num_format': '0.00'})
        format_values.set_bold(False)
        format_values.set_align('left')
        assert worksheet.set_column(1, len(self.general_res.columns), 30, format_values) == 0

        # format DASS, NVM and DERS
        format_values = workbook.add_format({'num_format': '0', 'align': 'left'})
        assert worksheet.set_row(1, None, format_values) == 0

        # format data
        for q in self.quizes.values():
            q.format()

        self.add_infor_for_ed15(workbook, worksheet)

        # Close the Pandas Excel writer and output the Excel file.
        self.writer.save()