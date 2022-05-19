import pandas as pd
import numpy as np
import os

def prepare_data_frame(filename, sheet_name=None):
    df = pd.read_excel(filename, sheet_name=sheet_name)
    df.columns = df.columns.str.lower()
    df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
    return df

def replace_answers(table_df, answers_dict):
    df = table_df.astype(object).replace(answers_dict)
    return df

def replace_questions(table_df, questions_dict):
    df = table_df.rename(columns=questions_dict)
    return df

def drop_columns(table_df, contains=None):
    if contains is None:
        return table_df
    cols = [c for c in table_df.columns if not contains.lower() in c.lower()]

    df = table_df[cols]
    return df

def drop_dublicates(input_path, input_filenames, output_path, output_filenames, sheetnumbers=None):
    assert len(input_filenames) == len(output_filenames)

    if sheetnumbers is None:
        sheetnumbers = [0] * len(input_filenames)
    else:
        assert len(sheetnumbers) == len(input_filenames)

    for in_filename, out_filename, sheetnumber in zip(input_filenames, output_filenames, sheetnumbers):
        data = pd.read_excel(os.path.join(input_path, in_filename), sheet_name=sheetnumber)
        data = data.drop_duplicates()
        data.to_excel(os.path.join(output_path, out_filename), index=False)

def drop_dublicates_by_cols(cols, input_path, input_filenames, output_path, output_filenames, sheetnumbers=None):
    assert len(input_filenames) == len(output_filenames)

    if sheetnumbers is None:
        sheetnumbers = [0] * len(input_filenames)
    else:
        assert len(sheetnumbers) == len(input_filenames)

    for in_filename, out_filename, sheetnumber in zip(input_filenames, output_filenames, sheetnumbers):
        data = pd.read_excel(os.path.join(input_path, in_filename), sheet_name=sheetnumber)
        duplicated_data = data[data.duplicated(subset=cols, keep=False)]
        data = data.drop_duplicates(subset=cols)
        data.to_excel(os.path.join(output_path, out_filename), index=False)
        duplicated_path = '{}/{}_duplicates.{}'.format(output_path, *out_filename.split('.'))
        duplicated_data.to_excel(duplicated_path, index=False)

def concatenate_tables(data_path, filenames, concat_filename):
    for fname in filenames:
        concatenated_df = pd.read_excel(data_path + concat_filename)
        cur_df =  pd.read_excel(data_path + fname)

        columns_1 = concatenated_df.columns.tolist()
        columns_1_lowered = [col.lower() for col in columns_1]
        columns_2 = cur_df.columns.tolist()
        columns_2_filtered = []
        for col in columns_2:
            if col.lower() in columns_1_lowered:
                print("Dropped '{}' column".format(col))
                continue
            columns_2_filtered.append(col)
        concatenated_data = concatenated_df.values
        concatenated_data = np.concatenate((concatenated_data, np.empty((concatenated_df.shape[0], len(columns_2_filtered)))), axis=1)
        for index, row in concatenated_df.iterrows():
            row_found = cur_df.loc[(cur_df["Фамилия"] == row["Фамилия"]) & (cur_df["Имя"] == row["Имя"]) & (cur_df["Отчество"] == row["Отчество"])]
            if len(row_found) > 0:
                concatenated_data[index, len(columns_1):] = row_found[columns_2_filtered].values[0, :]
            else:
                concatenated_data[index, len(columns_1):] = np.nan

        concatenated_table = pd.DataFrame(data=concatenated_data, columns = columns_1 + columns_2_filtered)
        concatenated_table.to_excel(data_path + concat_filename, index=False)
