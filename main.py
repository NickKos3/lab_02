__author__ = "Roman Gorilyi"
__version__ = "1.0.0"
__maintainer__ = "Roman Gorilyi"
__email__ = "rom4ik-007@yandex.ua"

from spyre import server

import pandas as pd
import urllib2
import json
from numpy import *
import matplotlib.pyplot as plt


region = ["Cherkasy", "Chernihiv", "Chernivci", "Crimea", "Dnipropetrovs'k", "Donets'k", "Ivano-Frankivs'k", "Kharkiv",
          "Kherson", "Khmel'nyts'kyy", "Kiev", "Kiev City", "Kirovohrad", "Luhans'k", "L'viv", "Mykolayiv", "Odessa",
          "Poltava", "Rivne", "Sevastopol'", "Sumy", "Ternopil'", "Transcarpathia", "Vinnytsya", "Volyn",
          "Zaporizhzhya", "Zhytomyr"]

region_index = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23', '24', '25', '26', '27']

Index = ['VCI', 'TCI', 'VHI']


class DataAnalyze(server.App):
    title = "Geo Ukraine vegitation data analysis"

    inputs = [{"input_type": 'dropdown',
               "label": 'Region',
               "options": [{"label": region[0], "value": region_index[0]},
                           {"label": region[1], "value": region_index[1]},
                           {"label": region[2], "value": region_index[2]},
                           {"label": region[3], "value": region_index[3]},
                           {"label": region[4], "value": region_index[4]},
                           {"label": region[5], "value": region_index[5]},
                           {"label": region[6], "value": region_index[6]},
                           {"label": region[7], "value": region_index[7]},
                           {"label": region[8], "value": region_index[8]},
                           {"label": region[9], "value": region_index[9]},
                           {"label": region[10], "value": region_index[10]},
                           {"label": region[11], "value": region_index[11]},
                           {"label": region[12], "value": region_index[12]},
                           {"label": region[13], "value": region_index[13]},
                           {"label": region[14], "value": region_index[14]},
                           {"label": region[15], "value": region_index[15]},
                           {"label": region[16], "value": region_index[16]},
                           {"label": region[17], "value": region_index[17]},
                           {"label": region[18], "value": region_index[18]},
                           {"label": region[19], "value": region_index[19]},
                           {"label": region[20], "value": region_index[20]},
                           {"label": region[21], "value": region_index[21]},
                           {"label": region[22], "value": region_index[22]},
                           {"label": region[23], "value": region_index[23]},
                           {"label": region[24], "value": region_index[24]},
                           {"label": region[25], "value": region_index[25]},
                           {"label": region[26], "value": region_index[26]}
                           ],
               "variable_name": 'region',
               "action_id": "update_data"},

              {"input_type": "text",
               "variable_name": "year",
               "label": "Year",
               "value": 1981,
               "action_id": "update_data"},

              {"input_type": "text",
               "variable_name": "min_week",
               "label": "From week",
               "value": 3,
               "action_id": "update_data"},

              {"input_type": "text",
               "variable_name": "max_week",
               "label": "To week",
               "value": 10,
               "action_id": "update_data"},

              {"input_type": 'dropdown',
               "label": 'Index',
               "options": [{"label": "vci", "value": Index[0]},
                           {"label": "tci", "value": Index[1]},
                           {"label": "vhi", "value": Index[2]}],
               "variable_name": 'index',
               "action_id": "update_data"}]

    controls = [{"control_type": "hidden",
                 "label": "get historical value of VCI/TCI/VHI",
                 "control_id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"output_type": "plot",
                "output_id": "plot",
                "control_id": "update_data",
                "tab": "Plot",  # must specify which tab each output should live in
                "on_page_load": True},

                {"output_type": "table",
                 "output_id": "table_id",
                 "control_id": "update_data",
                 "tab": "Table",
                 "on_page_load": True}]

    def getData(self, params):
        index = params['index']
        region_name = params['region']
        try:
            year = int(params['year'])
        except ValueError:
            year = 2008
        try:
            min_week = int(params['min_week'])
        except ValueError:
            min_week = 5
        try:
            max_week = int(params['max_week'])
        except ValueError:
            max_week = 20

        if min_week < 1 or min_week > max_week or min_week > 52:
            min_week = 1
        if max_week > 52 or max_week < 1:
            max_week = 52
        if year > 2015 and max_week > 5 or year < 1982:
            year = 2008

        df = pd.read_csv('Downloads/%s.csv' % region_name, index_col=False, header=1)
        df = df[df['year'] == int(year)]
        df = df[df['week'] >= int(min_week)]
        df = df[df['week'] <= int(max_week)]
        df = df[['week', index]]

        return df

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.set_index('week').plot()
        plt_obj.set_ylabel(list(df[:0])[1])
        plt_obj.set_title('week')
        fig = plt_obj.get_figure()
        return fig


app = DataAnalyze()
app.launch(port=49315)