import pandas as pd
import matplotlib.pyplot as plt
import ast
import math
import numpy as np


'''
滑动平均滤波算法
'''
def filter(datas, per):
    size = len(datas)
    print("length:", size)

    weights = list(datas.values())
    print("weights type:", type(weights))
    preweights = weights[slice(0, per)]
    print("preweights:", preweights)

    newdatas = [] * size
    newdatas[0:per] = preweights
    print("newdatas pre:", newdatas)

    value_buff = [] * per
    value_buff = preweights
    for data in weights[per:]:
        value_buff.pop(0)
        value_buff.append(data)
        newdata = np.mean(list(map(float, value_buff)))
        # print("新数据：", newdata)
        newdatas.append(newdata)

    for i in range(len(newdatas)):
        #"{:.1f}".format(data)
        newdatas[i] = round(float(newdatas[i]),1)
        #print("data:",data)
    print("新数据：", newdatas)
    return dict(zip(datas.keys(),newdatas))

def deal_row_data(row_item):
    if row_item['hardware_code'] is None or math.isnan(row_item['hardware_code']):
        return
    delta_data_str = row_item['delta_data']
    if delta_data_str is None or delta_data_str.strip() == '':
        return

    time_weight_data = ast.literal_eval(delta_data_str)
    if row_item['file_time_3'] is None or math.isnan(row_item['file_time_3']):
        return
    if row_item['file_time_4'] is None or math.isnan(row_item['file_time_4']):
        return
    pull_out_time = str(int(row_item['file_time_3'] - row_item['start_time']))

    pull_out_weight = time_weight_data[pull_out_time]
    pull_out_data = {pull_out_time : pull_out_weight}

    pull_in_time = str(int(row_item['file_time_4'] - row_item['start_time']))
    pull_in_weight = time_weight_data[pull_in_time]
    pull_in_data = {pull_in_time : pull_in_weight}

    min_weight = min(time_weight_data.values())
    print("min weight:", min_weight)
    min_weight_data = {k : v for k, v in time_weight_data.items() if v == min_weight}

    plt.plot(time_weight_data.keys(), time_weight_data.values(), label='原始数据', linewidth=0, color='b', marker='o', markerfacecolor='blue', markersize=2 )
    plt.plot(pull_out_data.keys(), pull_out_data.values(), label='拖框照片点', linewidth=0, color='y', marker='o', markerfacecolor='yellow', markersize=5 )
    plt.plot(pull_in_data.keys(), pull_in_data.values(), label='放框照片点', linewidth=0, color='g', marker='o', markerfacecolor='green', markersize=5 )
    plt.plot(min_weight_data.keys(), min_weight_data.values(), label='重量最低点', linewidth=1, color='r', marker='o', markerfacecolor='red', markersize=2 )
    newdatas = filter(time_weight_data.copy(), 10)
    plt.plot(newdatas.keys(), newdatas.values(), label='过滤数据', linewidth=1, color='black', marker='o', markerfacecolor='black', markersize=2 )
    plt.xlabel("time")
    plt.ylabel("weight")
    plt.xticks(rotation=45)
    plt.title("时间重量曲线")
    # 支持中文
    plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  #用来正常显示负号
    plt.legend()
    plt.grid(True)
    plt.savefig(str(int(row_item['hardware_code'])) + '_' + str(int(row_item['start_time'])) + '.png')
    plt.close('all')
    #fit = plt.figure()
    #fit.savefig(str(row_item['hardware_code']) + '.png')
    #plt.show()


if __name__ == '__main__':
    excel_file_name = 'test.xlsx'
    sheet_name = '导出结果'
    df = pd.read_excel(excel_file_name, sheet_name = sheet_name)
    #print(df)
    row_size = len(df)
    print(row_size)
    for row_index in range(row_size):
        row_item = df.loc[row_index]
        print("row item:", row_item)
        deal_row_data(row_item)
    #first_data = ast.literal_eval(df['delta_data'][0])
    #print(type(first_data))
    #print(first_data)