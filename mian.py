from standardizing import Sim
import pandas as pd
import xlrd
"""主函数"""


def read_in(addr):
    """读取匹配的非标准数据data_nonstand和对应的标准数据data_stand
    为方便修改匹配的非标准数据和标准数据，特将读入函数放在主程序文件中"""
    datafile = xlrd.open_workbook(addr)
    table = datafile.sheets()[0]
    matrix_text = pd.DataFrame([])
    for i in range(table.ncols):
        matrix_text[i] = table.col_values(i)
    matrix_text.rename(columns=matrix_text.iloc[0, :], inplace=True)
    matrix_text.drop([0], axis=0, inplace=True)
    data_nonstand = matrix_text[['标配纸盒容量（原）']]    # 匹配的非标准数据
    data_stand = matrix_text[['标配纸盒容量_y']]           # 匹配阿标准数据
    return data_nonstand, data_stand


address = '0731复印机（原数据-标准值）.xlsx'
data_non, data_st = read_in(address)
data_goal = input('输入非标准的数据：', )                  # 需要进行识别的非标准值
sim = Sim(data_goal, data_non, data_st)
value = sim.run()
print('data_goal标准化为：', value)
