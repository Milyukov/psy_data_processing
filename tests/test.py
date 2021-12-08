import unittest
from utils.tables import *

class TestTableUtils(unittest.TestCase):

    def setUp(self):
        self.input_path = '/tmp/'
        self.output_path = '/tmp/'
        self.input_filenames = ['test_drop_dublicates_1.xlsx', 'test_drop_dublicates_2.xlsx']
        self.output_filenames = ['test_drop_dublicates_1_2.xlsx', 'test_drop_dublicates_2_2.xlsx']
        self.true_answers = [3, 1]

        line1 = ['Мков', 'Глб', 'Сргч', 1, 2, 3]
        line2 = ['Атджва', 'Юл', 'Фкмрдн', 1, 2, 3]
        line3 = ['Суслва', 'Елн', 'Брсвн', 1, 2, 3]

        data_arrays = []

        data_arrays.append(
            np.array(
                [
                    line1,
                    line3,
                    line1,
                    line2,
                    line2,
                    line3
                ]
            )
        )

        data_arrays.append(
            np.array(
                [
                    line1,
                    line1,
                    line1,
                    line1,
                    line1,
                    line1
                ]
            )
        )

        for index, fname in enumerate(self.input_filenames):
            data_frame = pd.DataFrame(data=data_arrays[index], columns=['Фамилия', 'Имя', 'Отчество', 'col1', 'col2', 'col3'])
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
        self.assertTrue(data_frame.shape[1], 9)

if __name__ == '__main__':
    unittest.main()
