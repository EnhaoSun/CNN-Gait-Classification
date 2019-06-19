import pandas as pd
import re

class StepRecordDataLoader:

    def __init__(self, filename, usecols):
        self.filename = filename
        self.usecols = usecols

    def get_data_frame(self):
        return pd.read_csv(self.filename, header=11, usecols=self.usecols)

    def get_number_of_steps(self):
        return int(re.findall(r'\d+', self.__get_line(8))[0])

    def __get_line(self, line_number):
        with open(self.filename) as f:
            file_header = [next(f).rstrip().split('# ')[1] for x in range(10)]
            return file_header[line_number]
