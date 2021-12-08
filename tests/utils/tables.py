import pandas as pd
import numpy as np

def drop_dublicates(input_path, input_filenames, output_path, output_filenames, sheetnumbers=None):
    assert len(input_filenames) == len(output_filenames)

    if sheetnumbers is None:
        sheetnumbers = [0] * len(input_filenames)
    else:
        assert len(sheetnumbers) == len(input_filenames)

    for in_filename, out_filename, sheetnumber in zip(input_filenames, output_filenames, sheetnumbers):
        # xl = pd.ExcelFile(data_path + "EDEQ_final3.xlsx")
        # assert len(xl.sheet_names) == 1

        data = pd.read_excel(input_path + in_filename, sheet_name=sheetnumber)
        data = data.drop_duplicates()
        data.to_excel(output_path + out_filename, index=False)

def concatenate_tables(data_path, filenames, concat_filename):
    for fname in filenames[1:]:
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
