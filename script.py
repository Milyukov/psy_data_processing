import pandas as pd
import numpy as np

def drop_dublicates(data_path):

    # xl = pd.ExcelFile(data_path + "EDEQ_final3.xlsx")
    # assert len(xl.sheet_names) == 1

    data = pd.read_excel(data_path + "EDEQ_final3.xlsx", sheet_name=1)
    data = data.drop_duplicates()
    data.to_excel("concatenated.xlsx", index=False)

    data = pd.read_excel(data_path + "Анамнестические данные 1.xlsx", sheet_name=1)
    data = data.drop_duplicates()
    data.to_excel("Анамнестические данные 2.xlsx", index=False)

    data = pd.read_excel(data_path + "Данные по возрасту.xlsx", sheet_name=0)
    data = data.drop_duplicates()
    data.to_excel("Данные по возрасту 2.xlsx", index=False)

    data = pd.read_excel(data_path + "Данные по соматизации.xlsx", sheet_name=0)
    data = data.drop_duplicates()
    data.to_excel("Данные по соматизации 2.xlsx", index=False)

if __name__ == '__main__':

    data_path = 'data/'

    drop_dublicates(data_path)

    names = [
        "Анамнестические данные 2.xlsx", 
        "Данные по возрасту 2.xlsx", 
        "Данные по соматизации 2.xlsx"
        ]
    for fname in names:
        concatenated_df = pd.read_excel("concatenated.xlsx")
        cur_df =  pd.read_excel(fname)

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
        concatenated_table.to_excel("concatenated.xlsx", index=False)
