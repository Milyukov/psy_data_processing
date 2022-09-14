from model.sheet.sheet import Sheet

class TransposedGeneralInfo(Sheet):

    def __init__(self, data_frame, writer, sheet_name) -> None:
        super().__init__(data_frame)
        data_frame.to_excel(writer, index=False, sheet_name=sheet_name)
        self.worksheet = writer.sheets[sheet_name]

    def format(self, workbook):
        # Add some cell formats.
        format_index = workbook.add_format({'text_wrap': True})
        format_index.set_bold(True)
        format_index.set_align('left')
        assert self.worksheet.set_row(0, 50, format_index) == 0

        # format EDEQ, IES and DEBQ
        format_values = workbook.add_format({'num_format': '0.00'})
        format_values.set_bold(False)
        format_values.set_align('left')
        for row_index in range(1, len(self.data_frame.columns)):
            assert self.worksheet.set_row(row_index, 30, format_values) == 0

        # EDEQ
        outlier_format = workbook.add_format({'bg_color': '#FAA9A5', 'align': 'left'})
        blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
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

        col_index = 3
        options['minimum'] = -0.07
        options['maximum'] = 2.57
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = -0.24
        options['maximum'] = 1.48
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 0.55
        options['maximum'] = 3.75
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 0.22
        options['maximum'] = 2.96
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 0.34
        options['maximum'] = 2.77
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        # DASS
        outlier_format = workbook.add_format({'align': 'left'})
        blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
        blank = {
            'type': 'blanks', 
            'stop_if_true': True, 
            'format': blank_format
            }

        initial_col_index = 20 - 1
        for col_index in range(initial_col_index, initial_col_index + 3):
            self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
            self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, {'format': outlier_format})
        
        # IES
        outlier_format = workbook.add_format({'bg_color': '#FAA9A5', 'align': 'left'})
        blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
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

        col_index = 24 - 2            
        options['minimum'] = 2.8
        options['maximum'] = 4.2
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 2.33
        options['maximum'] = 4.03
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 2.91
        options['maximum'] = 4.23
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 2.49
        options['maximum'] = 4.09
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        options['minimum'] = 2.9
        options['maximum'] = 3.86
        col_index += 1
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, blank)
        self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        # DEBQ
        outlier_format = workbook.add_format({'align': 'left'})
        options = {
            'format': outlier_format
            }

        initial_col_index = 30 - 3
        for col_index in range(initial_col_index, initial_col_index + 3):
            self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        # NVM
        outlier_format = workbook.add_format({'align': 'left'})

        options = {
            'format': outlier_format
            }
        initial_col_index = 34 - 4
        for col_index in range(initial_col_index, initial_col_index + 5):
            self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)

        # DERS
        outlier_format = workbook.add_format({'align': 'left'})
        options = {
            'format': outlier_format
            }
        blank_format = workbook.add_format({'align': 'left', 'num_format': '0'})
        blank = {
            'type': 'blanks', 
            'stop_if_true': True, 
            'format': blank_format,
            }
        
        initial_row_index = 40 - 5
        for row_index in range(initial_row_index, initial_row_index + 7):
            self.worksheet.conditional_format(row_index, 1, row_index, self.data_frame.shape[0] - 1, blank)

        # ED-15
        outlier_format = workbook.add_format({'bg_color': '#FAA9A5', 'align': 'left'})
        options = {
            'format': outlier_format
            }
        
        initial_col_index = 48 - 6
        for col_index in range(initial_col_index, initial_col_index + 3):
            self.worksheet.conditional_format(1, col_index, self.data_frame.shape[0] - 1, col_index, options)
