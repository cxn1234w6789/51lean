import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def wind_radar(data):
    """风向雷达图"""
    wind = list(data['风力方向'])
    wind_speed = list(data['风级'])

    # 将风向转换为角度值
    for i in range(0, 24):
        if wind[i] == "北风":
            wind[i] = 90
        elif wind[i] == "南风":
            wind[i] = 270
        elif wind[i] == "西风":
            wind[i] = 180
        elif wind[i] == "东风":
            wind[i] = 360
        elif wind[i] == "东北风":
            wind[i] = 45
        elif wind[i] == "西北风":
            wind[i] = 135
        elif wind[i] == "西南风":
            wind[i] = 225
        elif wind[i] == "东南风":
            wind[i] = 315

    degs = np.arange(45, 361, 45)
    temp = []
    for deg in degs:
        speed = []
        # 获取指定角度范围内的风速平均值
        for i in range(0, 24):
            if wind[i] == deg:
                speed.append(wind_speed[i])
        if len(speed) == 0:
            temp.append(0)
        else:
            temp.append(sum(speed) / len(speed))
    print(temp)

    N = 8
    theta = np.arange(0. + np.pi / 8, 2 * np.pi + np.pi / 8, 2 * np.pi / 8)
    # 数据极径
    radii = np.array(temp)
    # 绘制极区图坐标系
    plt.axes(polar=True)
    # 定义每个扇区的颜色（R,G,B），值越大颜色越接近蓝色
    colors = [(1 - x / max(temp), 1 - x / max(temp), 0.6) for x in radii]
    plt.bar(theta, radii, width=(2 * np.pi / N), bottom=0.0, color=colors)
    plt.title('一天风级图', x=0.2, fontsize=20)
    plt.show()


def calc_corr(a, b):
    """计算相关系数"""
    a_avg = sum(a) / len(a)
    b_avg = sum(b) / len(b)
    cov_ab = sum([(x - a_avg) * (y - b_avg) for x, y in zip(a, b)])
    sq = math.sqrt(sum([(x - a_avg) ** 2 for x in a]) * sum([(x - b_avg) ** 2 for x in b]))
    corr_factor = cov_ab / sq
    return corr_factor


def corr_tem_hum(data):
    """温湿度相关性分析"""
    tem = data['温度']
    hum = data['相对湿度']
    plt.scatter(tem, hum, color='blue')
    plt.title("温湿度相关性分析图")
    plt.xlabel("温度/°C")
    plt.ylabel("相对湿度/%")
    # 在图中添加相关系数文本
    plt.text(20, 40, "相关系数为:" + str(calc_corr(tem, hum)), fontdict={'size': '10', 'color': 'red'})
    plt.show()
    print("相关系数为:" + str(calc_corr(tem, hum)))


def main():
    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['simHei']  # 解决中文显示问题
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

    # 读取CSV文件（注意：原代码中文件名为'weather1.csv'和'weather14.csv'，需统一）
    data1 = pd.read_csv('weather1.csv', encoding='gb2312')
    print(data1)

    # 调用其他图表函数（原代码中存在未定义的函数，需根据实际需求补充）
    # tem_curve(data1)
    # hum_curve(data1)
    # air_curve(data1)

    wind_radar(data1)
    corr_tem_hum(data1)


if __name__ == '__main__':
    main()