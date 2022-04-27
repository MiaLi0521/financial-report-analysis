import os
import re

import pandas as pd

from .utils import read_process_config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class DataProcess:
    def __init__(self, read_dir=os.path.join(BASE_DIR, 'dataset')):
        self.read_dir = read_dir
        self.config = read_process_config()
        self.dataset = {}
        self.company_code = set()

    def read_data(self, key):
        """从i问财下载的企业资产负债表、利润表以及现金流量表读取财报数据
           key: pre_process.json 中定义的键，包含 debt、benefit、cash
        """
        filename = None
        for file in os.listdir(self.read_dir):
            if not re.match(r'\d{6}_' + key + '_year.xls', file):
                continue
            filename = re.match(r'\d{6}_' + key + '_year.xls', file).group(0)
            self.company_code.add(re.match(r'(\d{6})_' + key + '_year.xls', file).group(1))

        if not filename:
            raise RuntimeError("数据读取路径下未发现相应的财务报表")
        if len(self.company_code) > 1:
            raise RuntimeError("数据读取路径下，请只放置一家公司的三张财务报表")

        df = pd.read_excel(os.path.join(self.read_dir, filename), sheet_name='Worksheet', header=1, index_col=0)
        df.dropna(inplace=True)  # 删除空行
        df.replace({'--': 0}, inplace=True)  # 将省略符号 '--' 替换为 0
        df = df.T[:6][::-1]  # 取最近 6 年的数据，正序排列
        df.columns.name = ''

        config = read_process_config()
        count = 0
        for field in config[key]['auto']:
            if field not in df:
                count += 1
                print(field, end=', ')
                df[field] = [0, 0, 0, 0, 0, 0]
        if count > 0:
            print('以上字段未找到，已自动赋值为0。')

        if config[key].get('hands'):
            print(f"\n！以下字段须手动赋值：{','.join(config[key].get('hands'))}")

        self.dataset[key] = df
        return df

    def save_data(self):
        # 水平方向拼接多个数据集
        name = self.company_code.pop()
        with open('.company', 'w', encoding='utf-8') as f:
            f.write(name)
        if not os.path.isdir('dist'):
            os.mkdir('dist')
        pd.concat(self.dataset.values(), axis=1).to_csv(os.path.join('dist', f'{name}.csv'))


