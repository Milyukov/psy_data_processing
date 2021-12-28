import unittest
from utils.tables import *
import math

class TestTableUtils(unittest.TestCase):

    def setUp(self):
        self.input_path = '/tmp/'
        self.output_path = '/tmp/'
        self.input_filenames = ['test_drop_dublicates_1.xlsx', 'test_drop_dublicates_2.xlsx']
        self.output_filenames = ['test_drop_dublicates_1_2.xlsx', 'test_drop_dublicates_2_2.xlsx']
        self.true_answers = [3, 1]

        self.line1 = ['Мков', 'Глб', 'Сргч', 1, 2, 3]
        self.line2 = ['Атджва', 'Юл', 'Фкмрдн', 1, 2, 3]
        self.line3 = ['Суслва', 'Елн', 'Брсвн', 1, 2, 3]

        data_arrays = []

        data_arrays.append(
            np.array(
                [
                    self.line1,
                    self.line3,
                    self.line1,
                    self.line2,
                    self.line2,
                    self.line3
                ]
            )
        )

        data_arrays.append(
            np.array(
                [
                    self.line1,
                    self.line1,
                    self.line1,
                    self.line1,
                    self.line1
                ]
            )
        )

        for index, fname in enumerate(self.input_filenames):
            data_frame = pd.DataFrame(data=data_arrays[index], 
            columns=['Фамилия', 'Имя', 'Отчество', 'col{}'.format(3 * index + 1), 'col{}'.format(3 * index + 2), 'col{}'.format(3 * index + 3)])
            data_frame.to_excel(self.input_path + fname, index=False)

    def test_drop_dublicates(self):

        drop_dublicates(self.input_path, self.input_filenames, self.output_path, self.output_filenames)

        for index, fname in enumerate(self.output_filenames):
            data_frame = pd.read_excel(self.output_path + fname)
            self.assertEqual(data_frame.shape[0], self.true_answers[index])

    def test_concatenate_tables(self):
        drop_dublicates(self.input_path, self.input_filenames, self.output_path, self.output_filenames)
        concatenate_tables(self.output_path, self.output_filenames[1:], self.output_filenames[0])
        data_frame = pd.read_excel(self.output_path + self.output_filenames[0])
        self.assertEqual(data_frame.shape[1], 9)

        data1 = [
                self.line1 + [1.0, 2.0, 3.0],
                self.line3 + [np.nan, np.nan, np.nan],
                self.line2 + [np.nan, np.nan, np.nan]
            ]

        data_frame_1 = pd.DataFrame(data=data1, columns=
        ['Фамилия', 'Имя', 'Отчество', 'col1', 'col2', 'col3', 'col4', 'col5', 'col6'])

        for row, row_ref in zip(data_frame.values, data_frame_1.values):
            for val, val_ref in zip(row, row_ref):
                print(val)
                print(val_ref)
                if pd.isna(val) and pd.isna(val_ref):
                    continue
                self.assertEqual(val, val_ref)

if __name__ == '__main__':
    unittest.main()
