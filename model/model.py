import pandas as pd
import numpy as np
from model.edeq import Edeq
from model.dass import Dass
from model.ies import Ies
from model.debq import Debq
from model.nvm import NVM
from model.ders import Ders

import tests.utils.tables as utils
import re

class Model:

    def __init__(self) -> None:
        pass

    def process_data_frame(self):
        # read and preprocess *.xlsx-file
        self.original_data = utils.prepare_data_frame(self.input_filename, sheet_name=0)
        self.original_data = utils.drop_columns(self.original_data, contains='дата заполнения')
        columns = self.original_data.columns.values

        # get questions names
        question_cols = []
        questions = {}
        for q in self.quizes:
            cols = self.quizes[q].get_cols(columns)
            questions[q] = cols
            question_cols.extend(cols)

        additional_info = ['возраст', 'рост', 'текущий вес']
        self.data = self.original_data[additional_info + question_cols]
        self.data['возраст'] = self.data['возраст'].fillna(0).astype(int)

        names = self.original_data[['фио', 'имя']].apply(lambda x: x[x.first_valid_index()], axis=1)
        self.data.insert(0, 'фио', names)

        # generate new question names
        self.questions_to_codes = {}
        self.codes_to_questions = {}

        for key in questions:
            for number, q in enumerate(questions[key]):
                self.questions_to_codes[q] = '{}_{}'.format(key, number + 1)
                self.codes_to_questions['{}_{}'.format(key, number + 1)] = q

        self.data = utils.replace_questions(self.data, self.questions_to_codes)

        # generate new answers names
        replace_answers_dict = {
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
            # DASS
            'вообще не относится ко мне': 0,
            'относилось ко мне до некоторой степени или некоторое время': 1,
            'относилось ко мне в значительной мере или значительную часть времени': 2,
            'относилось ко мне полностью или большую часть времени': 3,
            # IES
            'полностью не согласен': 1,
            'не согласен': 2,
            'ни то, ни другое': 3,
            'согласен': 4,
            'полностью согласен': 5,
            # DEBQ
            'никогда': 1,
            'очень редко': 2,
            'иногда': 3,
            'часто': 4,
            'очень часто': 5,
            # NVM
            'неверно': 0,
            'затрудняюсь ответить': 1,
            'верно': 2,
            # DERS
            'почти никогда (0-10%)': 1,
            'иногда (11-35%)': 2,
            'примерно половину времени (36-65%)': 3,
            'большую часть времени (66-90%)': 4,
            'почти всегда (91-100%)': 5
        }

        inverted_columns = ['IES_1', 'IES_2', 'IES_3', 'IES_7', 'IES_8', 'IES_9', 'IES_10', 'DEBQ_31', 'DERS_1', 'DERS_4', 'DERS_6']
        for index, col in enumerate(inverted_columns):
            inverted_columns[index] = col.lower()
        
        self.data = utils.replace_answers(self.data, replace_answers_dict)

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
            res = re.search('\d*.*,*\d', val_str)
            res = res.group()
            res = res.replace(',', '.')
            return float(res)

        weight = self.data['edeq_29'].fillna(0).apply(format_weight)

        def format_height(val):
            val_str = '{}'.format(val)
            res = re.search('\d*.*,*\d', val_str)
            res = res.group()
            res = res.replace(',', '.')
            if '.' in res:
                integer_part, fraction = res.split('.')
                if float(integer_part) >= 100:
                    return float(res) / 100.0
                return float(res)
            else:
                return float(res) / 100.0

        height = self.data['edeq_30'].fillna(0).apply(format_height)
        client_data.insert(1, 'ИМТ', weight.div(height.apply(lambda x: x ** 2)))
        return client_data

    def post_process_data(self):
        self.general_res = self.general_res.replace(np.nan, '')
        self.general_res = self.general_res.replace('nan', '')

        def upper_first_letters(s):
            words = s.split()
            new_words = []
            for word in words:
                new_words.append(word[0].upper() + word[1:])
            return ' '.join(new_words)

        self.data['фио'] = self.data['фио'].apply(upper_first_letters)
        self.general_res.set_axis(self.data['фио'], inplace=True)

    def process(self, input_filename, output_filename, mode) -> None:
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        self.writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = self.writer.book

        self.quizes = {}
        # EDEQ
        self.quizes['edeq'] = Edeq(7, 33, workbook)

        # DASS
        self.quizes['dass'] = Dass(self.quizes['edeq'].ec, 21, workbook)

        # IES
        self.quizes['ies'] = Ies(self.quizes['dass'].ec, 23, workbook)

        # DEBQ
        self.quizes['debq'] = Debq(self.quizes['ies'].ec, 33, workbook)

        # NVM
        self.quizes['nvm'] = NVM(self.quizes['debq'].ec, 83, workbook)

        # DERS
        self.quizes['ders'] = Ders(self.quizes['nvm'].ec, 18, workbook)

        # generate data frame for quiz evaluation
        self.input_filename = input_filename
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
        writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
        self.data.to_excel(writer, index=False, sheet_name='replaced')
        self.general_res = self.general_res.transpose()
        self.general_res.reset_index(inplace=True)
        self.general_res.to_excel(writer, index=False, sheet_name='general')

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets['general']

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
            q.format(worksheet, self.general_res)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
