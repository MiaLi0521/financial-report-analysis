import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_company_code():
    with open('.company', 'r', encoding='utf-8') as f:
        code = f.read()
    return code


def read_process_config():
    """读取数据预处理配置文件"""
    with open(os.path.join(BASE_DIR, 'ini_files', 'pre_process.json'), encoding='utf-8') as f:
        config = json.load(f)
    return config


def read_config(file_name):
    with open(os.path.join(BASE_DIR, 'ini_files', file_name), encoding='utf-8') as f:
        config = json.load(f)
    return config['table_index'], config['images'], config['titles'], config['tables_fields']


def format_thousandth(arr):
    """将 arr 或 Series 中的数字使用千分位表示"""
    return arr.apply(lambda x: format(x, ',.0f'))


def format_percentage(arr):
    """将 arr 或 Series 中的数字使用百分制表示，小数点后保留 2 位"""
    return arr.apply(lambda x: format(x, '.2%'))


def plot_show(t, image_title='', y_label='单位：亿', kind='bar', y_format='hundred million',
              pct_change=False, save_image=False):
    if image_title.endswith('率') or image_title.endswith('比例'):
        y_label = ''
        y_format = ''

    ax1 = plt.subplot(111)
    xticks = np.array(t.index)
    ax1.set_ylabel(y_label)

    if type(t) == pd.Series and kind == 'bar':
        ax1.bar(xticks, t.values, width=0.5)
    else:
        t.plot(kind=kind, ax=ax1, rot=0)

    y1_max = t.max()
    y1_min = t.min()
    while type(y1_max) == pd.Series:
        y1_max = y1_max.max()
        y1_min = y1_min.min()

    if y1_min > 0:
        y1_min = 0

    y1_yticks = np.linspace(y1_min, y1_max, 8)
    if y_format == 'hundred million':
        plt.yticks(y1_yticks, map(lambda x: int(round(x / 100000000)), y1_yticks))
    else:
        plt.yticks(y1_yticks, map(lambda x: format(x, '.1%'), y1_yticks))

    # 总资产规模、营业收入、净利润需要分析环比增长率
    if type(t) == pd.Series and pct_change:
        ax2 = ax1.twinx()
        ax2.set_ylabel('环比增长率')
        y2 = t.pct_change().values
        ax2.plot(xticks, y2, linewidth=2.5, color='xkcd:light blue')

        y2_min = 0 if t.pct_change().min() > 0 else t.pct_change().min()
        y2_max = t.pct_change().max() + 0.1
        y2_yticks = np.linspace(y2_min, y2_max, 8)
        plt.yticks(y2_yticks, map(lambda x: format(x, '.1%'), y2_yticks))

    plt.title(image_title)
    if save_image:
        plt.savefig(os.path.join('images', f'{image_title}.png'), dpi=600, bbox_inches='tight')
