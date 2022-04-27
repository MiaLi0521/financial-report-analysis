import os

import pandas as pd
import matplotlib.pyplot as plt

from .utils import read_config, format_percentage, format_thousandth, plot_show, read_company_code


class FinancialAnalysis:
    def __init__(self, config_file, data_file=None):
        if data_file is None:
            data_file = os.path.join('dist', f'{read_company_code()}.csv')
        self.config_file = config_file
        self.table_index, self.images, self.titles, self.fields = read_config(self.config_file)
        self.df = pd.read_csv(data_file, index_col=0)
        self.tables = {}
        self.format_tables = {}

    def init_table(self, table_index):
        """从总数据集中提取需要的字段初始化为 DataFrame
            table_index: tables_fields 中定义的 key
        """
        t = pd.DataFrame(
            index=self.df.index,
            columns=self.fields[table_index]['columns']
        )
        t[self.fields[table_index]['auto']] = self.df[self.fields[table_index]['auto']]
        self.tables[table_index] = t
        return t

    def format_show_table(self, table_index, ignore=None):
        table = self.tables[table_index].copy()
        for column in table.columns:
            if ignore and column in ignore:
                continue
            if column.endswith('率') or column.endswith('比例'):
                table[column] = format_percentage(table[column])
            else:
                table[column] = format_thousandth(table[column])
        self.format_tables[table_index] = table.T
        return table.T

    @staticmethod
    def _save_plot_show(filename):
        if not os.path.isdir('images'):
            os.makedirs('images')
        plt.savefig(os.path.join('images', f'{filename}.png'), dpi=600, bbox_inches='tight')

    def show_plot(self, table_index, image_index=0):
        config = self.fields[table_index]['plot'][image_index]

        params = {k: v for k, v in config.items() if k != 'columns'}
        params['t'] = self.tables[table_index][config['columns']]
        params['image_title'] = self.images[table_index][image_index]
        plot_show(**params)
        self._save_plot_show(params['image_title'])

