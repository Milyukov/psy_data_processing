from cmath import isnan
import tests.utils.tables as utils
import pandas as pd
import numpy as np
import sys
import re

# EDEQ
edeq_start_col = 7
edeq_count = 33

# DASS
dass_start_col = edeq_start_col + edeq_count
dass_count = 21

# IES
ies_start_col = dass_start_col + dass_count
ies_count = 23

# DEBQ
debq_start_col = ies_start_col + ies_count
debq_count = 33

# NVM
nvm_start_col = debq_start_col + debq_count
nvm_count = 83

# DERS
ders_start_col = nvm_start_col + nvm_count
ders_count = 18

def calc_edeq(data, edeq_res):
    cols = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 'EDEQ_4', 'EDEQ_5']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Ограничения питания'] = data[cols].mean(axis=1, skipna=False)

    cols = ['EDEQ_7', 'EDEQ_9', 'EDEQ_19', 'EDEQ_20', 'EDEQ_21']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Беспокойство о питании'] = data[cols].mean(axis=1, skipna=False)

    cols = ['EDEQ_6', 'EDEQ_8', 'EDEQ_10', 'EDEQ_11', 'EDEQ_23', 'EDEQ_26', 'EDEQ_27', 'EDEQ_28']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Беспокойство о фигуре'] = data[cols].mean(axis=1, skipna=False)

    cols = ['EDEQ_8', 'EDEQ_12', 'EDEQ_22', 'EDEQ_24', 'EDEQ_25']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Беспокойство о весе'] = data[cols].mean(axis=1, skipna=False)

    cols = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 'EDEQ_4', 'EDEQ_5', 'EDEQ_6', 'EDEQ_7', 'EDEQ_8', 
    'EDEQ_9', 'EDEQ_10', 'EDEQ_11', 'EDEQ_12', 'EDEQ_19', 'EDEQ_20', 'EDEQ_21', 'EDEQ_22', 
    'EDEQ_23', 'EDEQ_24', 'EDEQ_25', 'EDEQ_26', 'EDEQ_27', 'EDEQ_28']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['EDEQ_Общий балл'] = data[cols].mean(axis=1, skipna=False)

def calc_dass(data, dass_res):

    def format_answer(x, suffix):
        if np.isnan(x):
            return ''
        return "{:.0f} ({})".format(x, suffix)

    dass_res['Шкала депрессии, тревоги и стресса (DASS-21)'] = ''

    cols = ['DASS_3', 'DASS_5', 'DASS_10', 'DASS_13', 'DASS_16', 'DASS_17', 'DASS_21']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    dass_res['Депрессия'] = 2 * data[cols].sum(axis=1, skipna=False)
    min_vals = [0, 10, 14, 21, 28]
    max_vals = [9, 13, 20, 27, 10000]
    suffixes = ['Нормативно', 'Неявно выражено', 'Средне выражено', 'Явно выражено', 'Крайне тяжело']
    locs = []
    for min_val, max_val, suffix in zip(min_vals, max_vals, suffixes):
        locs.append(dass_res['Депрессия'].between(min_val, max_val).values)
    for index, loc in enumerate(locs):
        dass_res.loc[loc, 'Депрессия'] = dass_res.loc[loc, 'Депрессия'].apply(lambda x: format_answer(x, suffixes[index]))

    cols = ['DASS_2', 'DASS_4', 'DASS_7', 'DASS_9', 'DASS_15', 'DASS_19', 'DASS_20']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    dass_res['Тревога'] = 2 * data[cols].sum(axis=1, skipna=False)
    min_vals = [0, 8, 10, 15, 20]
    max_vals = [7, 9, 14, 19, 10000]
    suffixes = ['Нормативно', 'Неявно выражено', 'Средне выражено', 'Явно выражено', 'Крайне тяжело']
    locs = []
    for min_val, max_val, suffix in zip(min_vals, max_vals, suffixes):
        locs.append(dass_res['Тревога'].between(min_val, max_val).values)
    for index, loc in enumerate(locs):
        dass_res.loc[loc, 'Тревога'] = dass_res.loc[loc, 'Тревога'].apply(lambda x: format_answer(x, suffixes[index]))

    cols = ['DASS_1', 'DASS_6', 'DASS_8', 'DASS_11', 'DASS_12', 'DASS_14', 'DASS_18']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    dass_res['Стресс'] = 2 * data[cols].sum(axis=1, skipna=False)

    min_vals = [0, 15, 19, 26, 34]
    max_vals = [14, 18, 25, 33, 10000]
    suffixes = ['Нормативно', 'Неявно выражено', 'Средне выражено', 'Явно выражено', 'Крайне тяжело']
    locs = []
    for min_val, max_val, suffix in zip(min_vals, max_vals, suffixes):
        locs.append(dass_res['Стресс'].between(min_val, max_val).values)
    for index, loc in enumerate(locs):
        dass_res.loc[loc, 'Стресс'] = dass_res.loc[loc, 'Стресс'].apply(lambda x: format_answer(x, suffixes[index]))

def calc_ies(data, res):
    res['Шкала интуитивного питания  (IES-23)'] = ''
    cols = ['IES_1', 'IES_2', 'IES_3', 'IES_4', 'IES_5', 'IES_6']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Безусловное разрешение есть'] = data[cols].mean(axis=1)

    cols = ['IES_7', 'IES_8', 'IES_9', 'IES_10', 'IES_11', 'IES_12', 'IES_13', 'IES_14']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Прием пищи по физическим, а не эмоциональным причинам'] = data[cols].mean(axis=1)

    cols = ['IES_15', 'IES_16', 'IES_17', 'IES_18', 'IES_19', 'IES_20']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Доверие внутренним ощущениям голода и сытости'] = data[cols].mean(axis=1)


    cols = ['IES_21', 'IES_22', 'IES_23']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Конгруэнтность "Тело/Выбор еды"'] = data[cols].mean(axis=1)

    cols = ['ies_{}'.format(i) for i in range(1, ies_count + 1)]
    res['IES_Общий балл'] = data[cols].mean(axis=1)

def calc_debq(data, res):
    res['Опросник стиля пищевого поведения / Голладский пищевой опросник (DEBQ)'] = ''

    scale_name = 'Ограничительный'
    cols = ['DEBQ_1', 'DEBQ_2', 'DEBQ_3', 'DEBQ_4', 'DEBQ_5', 'DEBQ_6', 'DEBQ_7', 'DEBQ_8', 'DEBQ_9', 'DEBQ_10']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].mean(axis=1)
    res[scale_name] = res[scale_name].apply(
        lambda x: '{:.2f}'.format(x) + " (норма: 2.4)" if not np.isnan(x) else '')

    scale_name = 'Эмоциональный'
    cols = ['DEBQ_11', 'DEBQ_12', 'DEBQ_13', 'DEBQ_14', 'DEBQ_15', 'DEBQ_16', 'DEBQ_17', 'DEBQ_18', 'DEBQ_19', 'DEBQ_20', 'DEBQ_21', 'DEBQ_22', 'DEBQ_23']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].mean(axis=1)
    res[scale_name] = res[scale_name].apply(
        lambda x: '{:.2f}'.format(x) + " (норма: 1.8)" if not np.isnan(x) else '')

    scale_name = 'Экстернальный'
    cols = ['DEBQ_24', 'DEBQ_25', 'DEBQ_26', 'DEBQ_27', 'DEBQ_28', 'DEBQ_29', 'DEBQ_30', 'DEBQ_31', 'DEBQ_32', 'DEBQ_33']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].mean(axis=1)
    res[scale_name] = res[scale_name].apply(
        lambda x: '{:.2f}'.format(x) + " (норма: 2.7)" if not np.isnan(x) else '')

def calc_nvm(data, res):
    res['NVM - Нидерландский личностный опросник'] = ''
    
    cols = 'NVM_4+NVM_6+NVM_9+NVM_10+NVM_16+NVM_21+NVM_22+NVM_24+NVM_31+NVM_32+NVM_33+NVM_38+NVM_43+NVM_48+NVM_49+NVM_51+NVM_58+NVM_59+NVM_69+NVM_70+NVM_80+NVM_82'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Негативизм'] = data[cols].sum(axis=1, skipna=False)

    cols = 'NVM_1+NVM_2+NVM_3+NVM_5+NVM_7+NVM_11+NVM_12+NVM_13+NVM_14+NVM_15+NVM_17+NVM_19+NVM_25+NVM_27+NVM_30+NVM_35+NVM_37+NVM_41+NVM_52+NVM_54'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Соматизация'] = data[cols].sum(axis=1, skipna=False)

    cols = 'NVM_20+NVM_36+NVM_39+NVM_42+NVM_45+NVM_55+NVM_60+NVM_63+NVM_64+NVM_65+NVM_68+NVM_71+NVM_73+NVM_79+NVM_81'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Застенчивость'] = data[cols].sum(axis=1, skipna=False)

    cols = 'NVM_8+NVM_18+NVM_26+NVM_28+NVM_29+NVM_34+NVM_44+NVM_57+NVM_61+NVM_66+NVM_67+NVM_74+NVM_75'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Психопатология'] = data[cols].sum(axis=1, skipna=False)

    cols = 'NVM_23+NVM_40+NVM_46+NVM_47+NVM_50+NVM_53+NVM_56+NVM_62+NVM_72+NVM_76+NVM_77+NVM_78+NVM_83'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Экстраверсия'] = data[cols].sum(axis=1, skipna=False)

def calc_ders(data, res):
    res['Шкала трудностей эмоциональной регуляции (DERS-18)'] = ''

    scale_name = 'Осозанность'
    cols = 'DERS_1+DERS_4+DERS_6'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].sum(axis=1, skipna=False)
    res[scale_name] = res[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

    scale_name = 'Ясность'
    cols = 'DERS_2+DERS_3+DERS_5'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].sum(axis=1, skipna=False)
    res[scale_name] = res[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

    scale_name = 'Целенаправленность'
    cols = 'DERS_8+DERS_12+DERS_15'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].sum(axis=1, skipna=False)
    res[scale_name] = res[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

    scale_name = 'Управление импульсами'
    cols = 'DERS_9+DERS_16+DERS_18'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].sum(axis=1, skipna=False)
    res[scale_name] = res[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

    scale_name = 'Непринятие эмоциональных реакций'
    cols = 'DERS_7+DERS_13+DERS_14'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].sum(axis=1, skipna=False)
    res[scale_name] = res[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

    scale_name = 'Стратегии'
    cols = 'DERS_10+DERS_11+DERS_17'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res[scale_name] = data[cols].sum(axis=1, skipna=False)
    res[scale_name] = res[scale_name].apply(lambda x: '{:.0f}'.format(x) + " из 15" if not np.isnan(x) else '')

    cols = ['ders_{}'.format(i) for i in range(1, ders_count + 1)]
    res['DERS_Общий балл'] = data[cols].sum(axis=1, skipna=False).apply(lambda x: '{:.0f}'.format(x) if not np.isnan(x) else '')

def format_edeq(worksheet, general_res, header_format, outlier_format, blank_format):
    row_index = 3
    worksheet.set_row(row_index, None, header_format)

    blank = {
        'type': 'blanks', 
        'stop_if_true': True, 
        'format': blank_format
        }

    options = {
        'type': 'cell',
        'criteria': 'not between',
        'minimum': -0.07,
        'maximum': 2.57,
        'format': outlier_format
    }

    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = -0.24
    options['maximum'] = 1.48
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 0.55
    options['maximum'] = 3.75
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 0.22
    options['maximum'] = 2.96
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 0.34
    options['maximum'] = 2.77
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

def format_dass(worksheet, general_res, header_format, outlier_format, blank_format):
    blank = {
        'type': 'blanks', 
        'stop_if_true': True, 
        'format': blank_format
        }

    initial_row_index = 20
    worksheet.set_row(initial_row_index, None, header_format)
    initial_row_index += 1
    for row_index in range(initial_row_index, initial_row_index + 3):
        worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
        worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, {'format': outlier_format})

def format_ies(worksheet, general_res, header_format, outlier_format, blank_format):
    row_index = 24
    worksheet.set_row(row_index, None, header_format)

    blank = {
        'type': 'blanks', 
        'stop_if_true': True, 
        'format': blank_format
        }

    options = {
        'type': 'cell',
        'criteria': 'not between',
        'minimum': 2.8,
        'maximum': 4.2,
        'format': outlier_format
    }

    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 2.33
    options['maximum'] = 4.03
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 2.91
    options['maximum'] = 4.23
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 2.49
    options['maximum'] = 4.09
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

    options['minimum'] = 2.9
    options['maximum'] = 3.86
    row_index += 1
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)
    worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

def format_debq(worksheet, general_res, header_format, outlier_format, blank_format):
    options = {
        'format': outlier_format
        }
    initial_row_index = 30
    worksheet.set_row(initial_row_index, None, header_format)

    initial_row_index += 1
    for row_index in range(initial_row_index, initial_row_index + 3):
        worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

def format_nvm(worksheet, general_res, header_format, outlier_format, blank_format):
    options = {
        'format': outlier_format
        }

    initial_row_index = 34
    worksheet.set_row(initial_row_index, None, header_format)

    initial_row_index += 1
    for row_index in range(initial_row_index, initial_row_index + 5):
        worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, options)

def format_ders(worksheet, general_res, header_format, outlier_format, blank_format):
    blank = {
        'type': 'blanks', 
        'stop_if_true': True, 
        'format': blank_format,
        }

    initial_row_index = 40
    worksheet.set_row(initial_row_index, None, header_format)

    initial_row_index += 1
    for row_index in range(initial_row_index, initial_row_index + 7):
        worksheet.conditional_format(row_index, 1, row_index, len(general_res.columns) - 1, blank)

def run(filename):
    original_data = utils.prepare_data_frame(filename, sheet_name=0)
    original_data = utils.drop_columns(original_data, contains='дата заполнения')
    cols = original_data.columns.values

    # get questions names
    question_cols = []

    edeq_questions = cols[edeq_start_col:edeq_start_col + edeq_count]
    question_cols.extend(edeq_questions)

    dass_questions = cols[dass_start_col:dass_start_col + dass_count]
    question_cols.extend(dass_questions)

    ies_questions = cols[ies_start_col:ies_start_col + ies_count]
    question_cols.extend(ies_questions)

    debq_questions = cols[debq_start_col:debq_start_col + debq_count]
    question_cols.extend(debq_questions)

    nvm_questions = cols[nvm_start_col:nvm_start_col + nvm_count]
    question_cols.extend(nvm_questions)

    ders_questions = cols[ders_start_col:ders_start_col + ders_count]
    question_cols.extend(ders_questions)

    additional_info = ['возраст', 'рост', 'текущий вес']
    data = original_data[additional_info + question_cols]
    data['возраст'] = data['возраст'].fillna(0).astype(int)

    names = original_data[['фио', 'имя']].apply(lambda x: x[x.first_valid_index()], axis=1)
    data.insert(0, 'фио', names)

    # generate new question names
    questions_to_codes = {}
    codes_to_questions = {}

    for number, q in enumerate(edeq_questions):
        questions_to_codes[q] = 'edeq_{}'.format(number + 1)
        codes_to_questions['edeq_{}'.format(number + 1)] = q

    for number, q in enumerate(dass_questions):
        questions_to_codes[q] = 'dass_{}'.format(number + 1)

    for number, q in enumerate(ies_questions):
        questions_to_codes[q] = 'ies_{}'.format(number + 1)

    for number, q in enumerate(debq_questions):
        questions_to_codes[q] = 'debq_{}'.format(number + 1)

    for number, q in enumerate(nvm_questions):
        questions_to_codes[q] = 'nvm_{}'.format(number + 1)

    for number, q in enumerate(ders_questions):
        questions_to_codes[q] = 'ders_{}'.format(number + 1)

    data = utils.replace_questions(data, questions_to_codes)

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
    
    data = utils.replace_answers(data, replace_answers_dict)

    replace_inverted_answers_dict = {
        1: 5,
        2: 4,
        4: 2,
        5: 1
    }

    data[inverted_columns] = utils.replace_answers(data[inverted_columns], replace_inverted_answers_dict)

    ### calculate statistics
    general_res = pd.DataFrame([''] * len(data), columns=['Опросник питания (EDEQ)'])

    general_res.insert(0, 'Возраст', data['возраст'])

    def format_weight(val):
        val_str = '{}'.format(val)
        res = re.search('\d*.*,*\d', val_str)
        res = res.group()
        res = res.replace(',', '.')
        return float(res)

    weight = data['edeq_29'].fillna(0).apply(format_weight)

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

    height = data['edeq_30'].fillna(0).apply(format_height)
    general_res.insert(1, 'ИМТ', weight.div(height.apply(lambda x: x ** 2)))
    calc_edeq(data, general_res)

    cols = ['edeq_13', 'edeq_14', 'edeq_15', 'edeq_16', 'edeq_17', 'edeq_18',
    'edeq_29', 'edeq_30', 'edeq_31', 'edeq_32', 'edeq_33']
    for c in cols:
        question = codes_to_questions[c]
        question = question[0].upper() + question[1:]
        codes_to_questions[c] = question
        general_res[codes_to_questions[c]] = data[c].apply(str)

    general_res = general_res.replace(np.nan, '')
    general_res = general_res.replace('nan', '')

    calc_dass(data, general_res)
    calc_ies(data, general_res)
    calc_debq(data, general_res)
    calc_nvm(data, general_res)
    calc_ders(data, general_res)

    def upper_first_letters(s):
        words = s.split()
        new_words = []
        for word in words:
            new_words.append(word[0].upper() + word[1:])
        return ' '.join(new_words)

    data['фио'] = data['фио'].apply(upper_first_letters)
    general_res.set_axis(data['фио'], inplace=True)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')
    data.to_excel(writer, index=False, sheet_name='replaced')
    general_res = general_res.transpose()
    general_res.reset_index(inplace=True)
    general_res.to_excel(writer, index=False, sheet_name='general')

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
    assert worksheet.set_column(1, len(general_res.columns), 30, format_values) == 0

    # format DASS, NVM and DERS
    format_values = workbook.add_format({'num_format': '0', 'align': 'left'})
    assert worksheet.set_row(1, None, format_values) == 0

    # label outliers
    header_format = workbook.add_format({'bg_color': 'yellow'})
    outlier_format = workbook.add_format({'bg_color': '#FAA9A5', 'align': 'left'})
    blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
    format_edeq(worksheet, general_res, header_format, outlier_format, blank_format)
    format_ies(worksheet, general_res, header_format, outlier_format, blank_format)

    outlier_format = workbook.add_format({'align': 'left'})
    format_dass(worksheet, general_res, header_format, outlier_format, blank_format)
    format_nvm(worksheet, general_res, header_format, outlier_format, blank_format)
    format_debq(worksheet, general_res, header_format, outlier_format, blank_format)
    format_ders(worksheet, general_res, header_format, outlier_format, blank_format)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

if __name__ == '__main__':
    filename = sys.argv[1]
    run(filename)
