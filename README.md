# financial-report-analysis
本项目旨在通过分析 A 股上市公司发布的财务数据，了解公司的资产质量，行业地位，利润的形成过程、现金流情况，有没有粉饰报表等等。



## 关于数据集的下载

在分析前，需要从同花顺个股网 http://stockpage.10jqka.com.cn/ 下载 A 股上市公司的财报数据：



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-1.png)



下拉找【财务指标】，分别点击其中的【资产负债表】【利润表】【现金流量表】，然后【按年度】显示，点击【导出数据】即可导出对应的财务报表数据。



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-2.png)



下载好的财报数据类似于代码仓库中内置的数据集：



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-3.png)



至此，数据准备工作就完成了，可以开始我们的公司工作啦~

## 数据分析步骤

### 1. 数据预处理

在开始分析前，必须进行数据预处理工作，也就是执行 `generate_data.ipynb` 文件。在运行 `generate_data.ipynb` 前，须要对第三个 `cell` 中的科目进行手动赋值。



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-4.png)



依次填入近 6 年的数据即可，比如你下载的报告截止时间是 2020 年，那就依次填入 `2015` `2016` `2017` `2018` `2019` `2020` 六年的数据即可。



这些数据为什么需要手动填入呢？



由于会计科目的调整，往年的一些科目会出现无法导出的情况，比如 `其他流动资产里的理财产品` 和 `其他流动资产里的结构性存款` 科目。一些新增的科目，暂时还不支持导出，比如 `合同资产`  `合同负债` `应收款项融资`科目。对于 `长期应付款` 科目需要在财务报表附注中查看是否有息，如果是无息的长期应付款不计算在内。



上述科目填写完成后，运行 `generate_data.ipynb` 会在 `dist` 目录下生成一个 `data.csv` 的文件，其包含了资产负债表、利润表和现金流量表的汇总数据。



### 2. 资产质量分析

运行 `asset_quality_analysis.ipynb` 可完成资产质量分析，并在 `dist`目录下生成 `xxxxxx ASSET_QUALITY_ANALYSIS 2016~2020.docx` 格式的 Word 分析报告。



### 3. 通过资产负债表看一家企业牛不牛

运行 `asset_indepth_analysis.ipynb` 将从公司实力、偿债风险、公司竞争力、产品竞争力、主业专注度和暴雷几个方面展开资产负债表的进一步分析，并在 `dist` 目录下生成 `xxxxxx ASSET_INDEPTH_ANALYSIS 2016~2020.docx` 格式的分析报告。



### 4. 财务造假分析

运行 `asset_fraud_analysis.ipynb` 将对常见的粉饰报表的财务造假科目进行分析，帮助投资者识别雷区。运行完成后，会在 `dist` 目录下生成 `xxxxxx ASSET_FRAUD_ANALYSIS 2016~2020.docx` 格式的分析报告。



### 5. 企业是如何创造利润的？

运行 `profit_analysis.ipynb` 可以对利润表进行分析，从营业收入、营业成本、四费、税金及附加、营业利润、利润总额、净利润、归母净利润一步步了解企业利润的形成过程。运行结束后，会在 `dist` 目录下生成 `xxxxxx PROFIT_ANALYSIS 2016~2020.docx` 格式的分析报告。



### 6. 现金流水情况

运行 `cash_flow_analysis.ipynb` 将根据现金流量表分析企业造血能力、增长潜力、分红慷慨程度、现金增长情况以及可用现金等多个方面。



**！！！** 在运行 `cash_flow_analysis.ipynb` 时需要注意和分红相关的两个地方需要手动录入：



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-5.png)



如上图，需要填写每个年度计划分红的金额，也就是年报中披露的数字，比如 2019 年披露的分红除以 2019 年经营活动产生的现金流量净额，一般这个比例大于 20% ，分红都是比较慷慨的。对应的数据也可以在同花顺个股查看。



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-6.png)



**！！！！** 下面一个需要手动填写数据的位置为：



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-7.png)



有的公司分红太慷慨，不仅分了今年的利润，把上一年攒的利润也分出去了。因此，在分析现金增长情况的时候，需要我们把分红加回来。



**！！！** 这里需要注意，不能简单复制 `t4` 中的分红，因为今年实际分的钱其实是上一年年报中披露的分红。比如 2019 年年报披露的分红，这笔钱会在 2020 年分掉。因此，`t6` 中对应年份需要看除权除息的日期：



![](https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-8.png)



### 7. 综合分析

除了通过上述六个步骤拆开分析资产负债表、利润表和现金流量表之外，也可以选择更加简洁的方式。运行 `all_analysis.ipynb` 将从十九个步骤综合分析一家企业的财务报告，并在 `dist`目录下产生 `xxxxxx ALL_ANALYSIS 2016~2020.docx` 格式的分析报告。



更多精彩解读，扫描二维码，在小鱼的博客中获取吧~



<img src="https://raw.githubusercontent.com/MiaLi0521/financial-report-analysis/main/.readme/image-9.jpg" style="zoom:25%;" />