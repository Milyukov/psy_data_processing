from tests.utils.tables import *

if __name__ == '__main__':

    data_path = 'data/'

    input_filenames = [
        "EDEQ_final3.xlsx",
        "Анамнестические данные 1.xlsx",
        "Данные по возрасту.xlsx",
        "Данные по соматизации.xlsx"
    ]

    output_filenames = [
        "concatenated.xlsx",
        "Анамнестические данные 2.xlsx", 
        "Данные по возрасту 2.xlsx", 
        "Данные по соматизации 2.xlsx"
        ]

    sheetnames = [1, 1, 0, 0]

    drop_dublicates(data_path, input_filenames, './', output_filenames, sheetnames)

    concatenate_tables('./', output_filenames[1:], "concatenated.xlsx")
