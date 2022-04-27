import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('mode.chained_assignment', None)

# 解决绘图中显示中文的问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

ANALYSIS_CONFIGS = ['all_analysis.json', 'asset_quality_analysis.json',
                    'asset_indepth_analysis.json', 'asset_fraud_analysis.json',
                    'profit_analysis.json', 'cash_flow_analysis.json']