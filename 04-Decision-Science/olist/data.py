import os
import pandas as pd


class Olist:
    def get_data(self):
        """
        This function returns a Python dict.
        Its keys should be 'sellers', 'orders', 'order_items' etc...
        Its values should be pandas.DataFrames loaded from csv files
        """
        # getting the path for the csvs
        root = os.path.dirname(os.path.dirname(__file__))
        csv_path = os.path.join(root, 'data', 'csv')

        # creating a list with the filenames
        file_names = [f for f in os.listdir(csv_path) if f.endswith('.csv')]

        # creating a list with my key names for the dictionary
        key_names = [key_name
            .replace('olist_','')
            .replace('_dataset','')
            .replace('.csv','')
            for key_name in file_names]

        # creating my data dictionary that contains all dataframes
        data = {}

        for (k, f) in zip(key_names, file_names):
            data[k] = pd.read_csv(os.path.join(csv_path, f))

        return data

    def ping(self):
        """
        You call ping I print pong.
        """
        print("pong")
