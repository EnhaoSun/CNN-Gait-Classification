import pandas as pd
import numpy as np
import os
import sys
import re
from IPython.display import clear_output

class WindowStepDataLoader:

    def __init__(self, window_size, datadir, usecols):
        self.datadir = datadir
        self.usecols = usecols
        self.window_size = window_size

    def save_dataset(self, filename):
        np.save('../processed_data/data/%s' % filename, self.data)
        np.save('../processed_data/targets/%s' % filename, self.targets)
   

    def load_dataset(self, sensor_position=None):
        data = []
        targets = []
        total_length = len(os.listdir(self.datadir))
        for file_index, file in enumerate(os.listdir(self.datadir)):
            clear_output(wait=True)
            print("%d / %d files loaded currently at: %s" % (file_index + 1, total_length, file))
            if file.endswith('.csv'):
                file_path = self.datadir + file
                target  = [
                    self.__get_target(file_path, 4),
                    self.__get_target(file_path, 5),
                    self.__get_target(file_path, 6),
                    self.__get_target(file_path, 7)
                ]
                if sensor_position != None and target[1] != sensor_position:
                    continue
                print(target)
                
                df = pd.read_csv(file_path, header=11, usecols=self.usecols)
                nr_rows = len(df.index)
                sys.stdout.write('.')
                for index, row in df.iterrows():
                    if (index % (nr_rows // 75) == 0):
                        sys.stdout.write('.')
                    window = df.iloc[index:index+self.window_size].values.flatten().tolist()
                    if len(window) != len(self.usecols) * self.window_size:
                        break
                    targets.append(target)
                    data.append(window)

        self.data = np.array(data)
        
        if np.size(self.data) == 0:
            print("Empty data set")
            return 0
        
        mean = self.data.mean(axis=1)
        std  = self.data.std(axis=1)
        self.data = (self.data - mean[:, np.newaxis]) / std[:, np.newaxis]
        self.targets = np.array(targets)

    def __get_target(self, filename, line_number):
        return re.sub(
            '[^a-zA-Z ]+',
            '',
            self.__get_line(filename, line_number).split(":")[1].strip()
        )

    def __get_line(self, filename, line_number):
        with open(filename) as f:
            file_header = [next(f).rstrip().split('# ')[1] for x in range(10)]
            return file_header[line_number]
