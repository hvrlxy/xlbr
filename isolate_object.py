import regex as re
import sys
import os
import pandas as pd

class SearchPattern:
    def __init__(self, df):
        self.df = df
        self.num_columns = len(self.df.columns)
        new_columns = list(range(self.num_columns - 2)) + ["contextRef", "#text"]
        self.df.columns = new_columns

    def search_code(self, code):
        num_columns = len(self.df.columns)
        code_column = -1
        for i in range(num_columns):
            cvalues = list(self.df.iloc[:, i])
            if code in cvalues:
                code_column = i
                break
        if code_column == -1:
            raise Exception("Code not found")
        code_df = self.df[self.df[code_column] == code]
        for i in range(code_column):
            code_df = code_df.drop(i, axis=1)
        return code_df, code_column

    def flatten_code_df(self, code_df, code_column):
        code_df = code_df.drop(code_column, axis=1)
        code_df = code_df.drop("contextRef", axis=1)
        
        final_data = {}
        max_entry = 0

        benchmark = ''

        for i in range(len(code_df)):
            column_name = ''
            for j in range(code_column+1, self.num_columns - 2):
                column_name += list(code_df[j])[i] + '.'
            if i == 0 and benchmark == '':
                benchmark = column_name
            if column_name == benchmark:
                if column_name not in final_data:
                    final_data[column_name] = []
                max_entry += 1
                final_data[column_name] += [''] * (max_entry - len(final_data[column_name]))
                final_data[column_name].append(list(code_df['#text'])[i])
            else:
                if column_name not in final_data:
                    final_data[column_name] = []
                while len(final_data[column_name]) < len(final_data[benchmark]) - 1:
                    final_data[column_name].append('')
                final_data[column_name].append(list(code_df['#text'])[i])

        for key in final_data:
            while len(final_data[key]) < len(final_data[benchmark]):
                final_data[key].append('')
        return pd.DataFrame.from_dict(final_data)

    def generate_pandas(self, code):
        code_df, code_column = self.search_code(code)
        return self.flatten_code_df(code_df, code_column)

    def to_excel(self, code, file_name):
        result_df = self.generate_pandas(code)
        result_df.to_excel(file_name)

    def to_csv(self, code, file_name):
        result_df = self.generate_pandas(code)
        result_df.to_csv(file_name)
    



