import pandas as pd
import numpy as np
import argparse
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Path to excel file")
parser.add_argument("-o", "--output", help="Path to excel file")
parser.add_argument("-c", "--config", help="Path to config")

class Model:

    def __init__(self) -> None:
        pass

    @staticmethod
    def ascii_to_int(c):
        if isinstance(c, str):
            return ord(c.lower()) - ord("a")
        return c

    @staticmethod
    def get_inverse_dict(answers_config):
        max_val = 0
        min_val = np.inf
        for key, val in answers_config.items():
            val = Model.ascii_to_int(val)
            if val > max_val:
                max_val = val
            if val < min_val:
                min_val = val
        
        invers_answers = {}
        for key, val in answers_config.items():
            val = Model.ascii_to_int(val)
            invers_answers[key] = -val + max_val + min_val
        return invers_answers

    @staticmethod
    def compute_scale(data_frame, scale):
        method = scale["method"]
        scale_range = scale["range"]
        if isinstance(scale_range, str):
            scale_range = scale_range.split(',')
        scale_range = [Model.ascii_to_int(i) for i in scale_range]
        if method.lower() == "avg":
            return data_frame.iloc[:, scale_range].mean(axis=1)
        elif method.lower() == "sum":
            return data_frame.iloc[:, scale_range].sum(axis=1)

    @staticmethod
    def process(input_path, output_path, config_path):
        results = {}
        config = None
        with open(config_path, "r", encoding="utf8") as stream:
            try:
                config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(output_path, engine="xlsxwriter")
    

        for quiz_config in config:
            # get quiz name
            quize_name = quiz_config["name"]
            # read corresponding sheet
            quiz_data_frame = pd.read_excel(input_path, sheet_name=quize_name)
            # convert all strings to lower case
            quiz_data_frame.columns = quiz_data_frame.columns.str.lower()
            results[quize_name] = quiz_data_frame.copy()
            # get inverse answers dictionary
            inverse_answers = Model.get_inverse_dict(quiz_config["answers"])
            # get relevant columns
            start_col = quiz_config["questions"]["start_index"]
            start_col = Model.ascii_to_int(start_col)
            questions_num = quiz_config["questions"]["number"]
            cols = quiz_data_frame.columns
            # columns with inverse answers
            inverse_cols_range = quiz_config["questions"]["inverse_range"]
            if isinstance(inverse_cols_range, str):
                inverse_cols_range = inverse_cols_range.split(',')
            inverse_cols_range = [Model.ascii_to_int(i) for i in inverse_cols_range]
            inverse_cols = cols[inverse_cols_range].values
            # columns with direct answers
            direct_cols_range = [i for i in range(len(cols)) if i not in inverse_cols_range and i >= start_col and i < start_col + questions_num]
            direct_cols = cols[direct_cols_range].values
            # replace string answers according to defined mappings
            for col in direct_cols:
                results[quize_name][col] = results[quize_name][col].str.lower()
                results[quize_name] = results[quize_name].replace({col: quiz_config["answers"]})
            for col in inverse_cols:
                results[quize_name][col] = results[quize_name][col].str.lower()
                results[quize_name] = results[quize_name].replace({col: inverse_answers}) 
            # compute scales
            scales = {}
            for scale in quiz_config["scales"]:
                scales[scale["name"]] = Model.compute_scale(results[quize_name], scale)
            for scale_name, scale_val in scales.items():
                results[quize_name][scale_name] = scale_val
            results[quize_name].to_excel(writer, sheet_name=quize_name)
        
        # Close the Pandas Excel writer and output the Excel file.
        writer.close()

if __name__ == '__main__':
    args = parser.parse_args()
    res = Model().process(args.input, args.output, args.config)
