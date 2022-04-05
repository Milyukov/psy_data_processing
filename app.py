import tests.utils.tables as utils
import pandas as pd
import numpy as np

# EDEQ
edeq_start_col = 7
edeq_count = 33

# DASS
dass_start_col = edeq_start_col + edeq_count #41
dass_count = 21

# IES
ies_start_col = dass_start_col + dass_count #63
ies_count = 23

# DEBQ
debq_start_col = ies_start_col + ies_count #89
debq_count = 33

# NVM
nvm_start_col = debq_start_col + debq_count #123
nvm_count = 83

# DERS
ders_start_col = nvm_start_col + nvm_count #208
ders_count = 18

def calc_edeq(data, edeq_res):
    edeq_res['Опросник питания (EDEQ)'] = ''

    cols = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 'EDEQ_4', 'EDEQ_5']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Ограничения питания'] = data[cols].mean(axis=1)

    cols = ['EDEQ_7', 'EDEQ_9', 'EDEQ_19', 'EDEQ_20', 'EDEQ_21']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Беспокойство о питании'] = data[cols].mean(axis=1)

    cols = ['EDEQ_6', 'EDEQ_8', 'EDEQ_10', 'EDEQ_11', 'EDEQ_23', 'EDEQ_26', 'EDEQ_27', 'EDEQ_28']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Беспокойство о фигуре'] = data[cols].mean(axis=1)

    cols = ['EDEQ_8', 'EDEQ_12', 'EDEQ_22', 'EDEQ_24', 'EDEQ_25']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['Беспокойство о весе'] = data[cols].mean(axis=1)

    cols = ['EDEQ_1', 'EDEQ_2', 'EDEQ_3', 'EDEQ_4', 'EDEQ_5', 'EDEQ_6', 'EDEQ_7', 'EDEQ_8', 
    'EDEQ_9', 'EDEQ_10', 'EDEQ_11', 'EDEQ_12', 'EDEQ_19', 'EDEQ_20', 'EDEQ_21', 'EDEQ_22', 
    'EDEQ_23', 'EDEQ_24', 'EDEQ_25', 'EDEQ_26', 'EDEQ_27', 'EDEQ_28']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    edeq_res['EDEQ_Общий балл'] = data[cols].mean(axis=1)

def calc_dass(data, dass_res):
    dass_res['Шкала депрессии, тревоги и стресса (DASS-21)'] = ''

    cols = ['DASS_3', 'DASS_5', 'DASS_10', 'DASS_13', 'DASS_16', 'DASS_17', 'DASS_21']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    dass_res['Депрессия'] = 2 * data[cols].sum(axis=1)

    cols = ['DASS_2', 'DASS_4', 'DASS_7', 'DASS_9', 'DASS_15', 'DASS_19', 'DASS_20']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    dass_res['Тревога'] = 2 * data[cols].sum(axis=1)

    cols = ['DASS_1', 'DASS_6', 'DASS_8', 'DASS_11', 'DASS_12', 'DASS_14', 'DASS_18']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    dass_res['Стресс'] = 2 * data[cols].sum(axis=1)

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
    
    cols = ['DEBQ_1', 'DEBQ_2', 'DEBQ_3', 'DEBQ_4', 'DEBQ_5', 'DEBQ_6', 'DEBQ_7', 'DEBQ_8', 'DEBQ_9', 'DEBQ_10']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Ограничительный'] = data[cols].mean(axis=1)

    cols = ['DEBQ_11', 'DEBQ_12', 'DEBQ_13', 'DEBQ_14', 'DEBQ_15', 'DEBQ_16', 'DEBQ_17', 'DEBQ_18', 'DEBQ_19', 'DEBQ_20', 'DEBQ_21', 'DEBQ_22', 'DEBQ_23']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Эмоциональный'] = data[cols].mean(axis=1)

    cols = ['DEBQ_24', 'DEBQ_25', 'DEBQ_26', 'DEBQ_27', 'DEBQ_28', 'DEBQ_29', 'DEBQ_30', 'DEBQ_31', 'DEBQ_32', 'DEBQ_33']
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Экстернальный'] = data[cols].mean(axis=1)

def calc_nvm(data, res):
    res['NVM - Нидерландский личностный опросник'] = ''
    
    cols = 'NVM_4+NVM_6+NVM_9+NVM_10+NVM_16+NVM_21+NVM_22+NVM_24+NVM_31+NVM_32+NVM_33+NVM_38+NVM_43+NVM_48+NVM_49+NVM_51+NVM_58+NVM_59+NVM_69+NVM_70+NVM_80+NVM_82'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Негативизм'] = data[cols].sum(axis=1)

    cols = 'NVM_1+NVM_2+NVM_3+NVM_5+NVM_7+NVM_11+NVM_12+NVM_13+NVM_14+NVM_15+NVM_17+NVM_19+NVM_25+NVM_27+NVM_30+NVM_35+NVM_37+NVM_41+NVM_52+NVM_54'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Соматизация'] = data[cols].sum(axis=1)

    cols = 'NVM_20+NVM_36+NVM_39+NVM_42+NVM_45+NVM_55+NVM_60+NVM_63+NVM_64+NVM_65+NVM_68+NVM_71+NVM_73+NVM_79+NVM_81'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Застенчивость'] = data[cols].sum(axis=1)

    cols = 'NVM_8+NVM_18+NVM_26+NVM_28+NVM_29+NVM_34+NVM_44+NVM_57+NVM_61+NVM_66+NVM_67+NVM_74+NVM_75'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Психопатология'] = data[cols].sum(axis=1)

    cols = 'NVM_23+NVM_40+NVM_46+NVM_47+NVM_50+NVM_53+NVM_56+NVM_62+NVM_72+NVM_76+NVM_77+NVM_78+NVM_83'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Экстраверсия'] = data[cols].sum(axis=1)

def calc_ders(data, res):
    res['Шкала трудностей эмоциональной регуляции (DERS-18)'] = ''
    
    cols = 'DERS_1+DERS_4+DERS_6'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Осозанность'] = data[cols].sum(axis=1)

    cols = 'DERS_2+DERS_3+DERS_5'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Ясность'] = data[cols].sum(axis=1)

    cols = 'DERS_8+DERS_12+DERS_15'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Целенаправленность'] = data[cols].sum(axis=1)

    cols = 'DERS_9+DERS_16+DERS_18'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Управление импульсами'] = data[cols].sum(axis=1)

    cols = 'DERS_7+DERS_13+DERS_14'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Непринятие эмоциональных реакций'] = data[cols].sum(axis=1)

    cols = 'DERS_10+DERS_11+DERS_17'
    cols = cols.split('+')
    for i, col in enumerate(cols):
        cols[i] = col.lower()
    res['Стратегии'] = data[cols].sum(axis=1)

    cols = ['ders_{}'.format(i) for i in range(1, ders_count + 1)]
    res['DERS_Общий балл'] = data[cols].sum(axis=1)

if __name__ == '__main__':
    filename = '/home/gleb/Projects/tables/data/интуит_проверка.xlsx'

    data = utils.prepare_data_frame(filename, sheet_name=0) #'сырые данные и правила'
    cols = data.columns.values

    # get questions names
    question_cols = ['фио']

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

    data = data[question_cols]

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
    edeq_res = pd.DataFrame()
    calc_edeq(data, edeq_res)

    cols = ['edeq_13', 'edeq_14', 'edeq_15', 'edeq_16', 'edeq_17', 'edeq_18',
    'edeq_29', 'edeq_30', 'edeq_31', 'edeq_32', 'edeq_33']
    for c in cols:
        question = codes_to_questions[c]
        question = question[0].upper() + question[1:]
        edeq_res[codes_to_questions[c]] = data[c].apply(str)

    general_res = edeq_res.copy()
    calc_dass(data, general_res)
    calc_ies(data, general_res)
    calc_debq(data, general_res)
    calc_nvm(data, general_res)
    calc_ders(data, general_res)

    edeq_res.set_axis(data['фио'], inplace=True)
    general_res.set_axis(data['фио'], inplace=True)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter('/tmp/exp.xlsx', engine='xlsxwriter')
    data.to_excel(writer, index=False, sheet_name='replaced')
    general_res = general_res.transpose()
    general_res.to_excel(writer, index=True, sheet_name='general')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['general']

    # Add some cell formats.
    format_index = workbook.add_format()
    format_index.set_bold(True)
    format_index.set_align('left')
    assert worksheet.set_column(0, 0, 50, format_index) == 0

    format_values = workbook.add_format({'num_format': '0.00'})
    format_values.set_bold(False)
    format_values.set_align('right')
    assert worksheet.set_column(1, len(general_res.columns), None, format_values) == 0

    # row = general_res.iloc[[2]]
    # numeric_values = row.values[:, 0]
    # indices = np.where(np.logical_or(numeric_values<-0.24, numeric_values>1.48))[0]
    # # Set the column width and format.
    # for col_num in indices:
    #     assert worksheet.set_column(col_num + 1, col_num + 1, None, format_index) == 0

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
