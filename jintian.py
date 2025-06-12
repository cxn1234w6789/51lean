import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import re


def get_tem_hum_data():
    """从天气网站提取当天温湿度数据"""
    url = "http://www.weather.com.cn/weather/101280701.shtml"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        # 发送请求并处理编码
        response = requests.get(url, headers=headers)
        response.encoding = "utf-8"  # 尝试UTF-8编码，可根据实际情况调整
        soup = BeautifulSoup(response.text, "html.parser")

        # 定位当天天气数据块（通常是第一个li标签）
        today_data = soup.select("ul.t.clearfix li")[0]

        # 提取温度数据（格式如"28℃~25℃"）
        temp_text = today_data.select_one(".tem").text
        # 用正则表达式提取数字
        temps = re.findall(r"\d+", temp_text)
        if len(temps) == 2:
            min_temp, max_temp = int(temps[1]), int(temps[0])
        else:
            # 处理单温度值情况
            min_temp = max_temp = int(temps[0])

        # 提取湿度数据（在shidu标签中，格式如"湿度：60%"）
        humidity_text = today_data.select_one(".shidu").text
        humidity = int(re.findall(r"\d+", humidity_text)[0])

        # 假设当天有多个时段数据（实际可能需调整）
        # 这里模拟生成多个温度-湿度对（实际应根据网页结构提取）
        hours = 24
        temp_list = np.linspace(min_temp, max_temp, hours)
        hum_list = [humidity] * hours  # 假设湿度全天不变

        return temp_list, hum_list

    except Exception as e:
        print(f"数据提取失败: {e}")
        # 模拟数据（仅用于测试）
        return np.linspace(25, 30, 24), np.random.randint(60, 90, 24)


def visualize_tem_hum(temp, hum):
    """绘制温湿度散点图并计算相关系数"""

    # 计算相关系数
    def calc_corr(a, b):
        a_avg, b_avg = np.mean(a), np.mean(b)
        cov = np.sum((a - a_avg) * (b - b_avg))
        std = np.sqrt(np.sum((a - a_avg) ** 2) * np.sum((b - b_avg) ** 2))
        return cov / std if std != 0 else 0

    corr = calc_corr(temp, hum)

    # 可视化
    plt.figure(figsize=(10, 6))
    plt.scatter(temp, hum, color='blue', alpha=0.7, s=30)
    plt.title("三亚当天温湿度相关性分析", fontsize=16)
    plt.xlabel("温度 (°C)", fontsize=12)
    plt.ylabel("湿度 (%)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # 添加相关系数文本
    plt.text(min(temp) + (max(temp) - min(temp)) * 0.1,
             max(hum) * 0.9,
             f"相关系数: {corr:.2f}",
             fontsize=12, color='red', bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.show()
    print(f"温湿度相关系数: {corr:.2f}")


if __name__ == "__main__":
    # 设置中文字体
    plt.rcParams["font.sans-serif"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC"]
    plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

    # 提取数据并可视化
    temp_data, hum_data = get_tem_hum_data()
    visualize_tem_hum(temp_data, hum_data)