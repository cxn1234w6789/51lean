import requests
from bs4 import BeautifulSoup
import csv
import json
import re  # 添加正则表达式模块


def getHTMLtext(url):
    """请求获得网页内容"""
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        print("成功访问")
        return r.text
    except:
        print("访问错误")
        return ""


def get_content(html):
    """处理得到当天24小时数据及1-7天数据"""
    final_day = []  # 存放当天数据
    final_7d = []  # 存放1-7天数据
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body

    # 爬取当天24小时数据
    data2 = body.find_all('div', {'class': 'left-div'})
    if len(data2) > 2:
        text = data2[2].find('script').string
        text = text[text.index('=') + 1:-2]  # 转换为JSON数据
        jd = json.loads(text)
        dayone = jd['od']['od2']
        count = 0
        for i in dayone:
            if count <= 23:
                temp = []
                temp.append(i['od21'])  # 时间
                temp.append(i['od22'])  # 温度
                temp.append(i['od24'])  # 风力方向
                temp.append(i['od25'])  # 风级
                temp.append(i['od26'])  # 降水量
                temp.append(i['od27'])  # 相对湿度
                temp.append(i['od28'])  # 空气质量
                final_day.append(temp)
                count += 1

    # 爬取1-7天数据
    data = body.find('div', {'id': '7d'})
    if data:
        ul = data.find('ul')
        li = ul.find_all('li')
        i = 0
        for day in li:
            if 0 < i < 7:
                temp = []
                # 提取日期
                date = day.find('h1').string
                date = date[:date.index(' ')]
                temp.append(date)
                # 提取天气
                inf = day.find_all('p')
                temp.append(inf[0].string)
                # 提取温度
                tem_low = inf[1].find('i').string
                tem_high = inf[1].find('span').string if inf[1].find('span') else None
                temp.append(tem_low[:-1])
                if tem_high and tem_high[-1] == 'C':
                    temp.append(tem_high[:-1])
                else:
                    temp.append(tem_high)
                # 提取风向
                wind = inf[2].find_all('span')
                for j in wind:
                    temp.append(j['title'])
                # 提取风级
                wind_scale = inf[2].find('i').string
                index1 = wind_scale.index('级')
                temp.append(int(wind_scale[index1 - 1:index1]))
                final_7d.append(temp)
                i += 1
    return final_day, final_7d


def get_content2(html):
    """处理得到8-14天数据"""
    final = []
    bs = BeautifulSoup(html, "html.parser")
    body = bs.body
    data = body.find('div', {'id': '15d'})
    if data:
        ul = data.find('ul')
        li = ul.find_all('li')
        i = 0
        for day in li:
            if i < 8:
                temp = []
                # 提取日期（改进版本，使用正则表达式匹配数字和汉字）
                date_elem = day.find('span', {'class': 'time'})
                if date_elem and date_elem.string:
                    date_text = date_elem.string
                    # 使用正则表达式提取日期部分（如"6月12日"）
                    date_match = re.search(r'(\d+月\d+日)', date_text)
                    if date_match:
                        date = date_match.group(1)
                    else:
                        # 如果没有匹配到标准日期格式，尝试其他处理方式
                        try:
                            # 尝试按空格分割
                            date_parts = date_text.split()
                            if date_parts:
                                date = date_parts[0]
                            else:
                                date = "未知日期"
                        except:
                            date = "未知日期"
                else:
                    date = "未知日期"
                temp.append(date)

                # 提取天气
                weather_elem = day.find('span', {'class': 'wea'})
                if weather_elem and weather_elem.string:
                    temp.append(weather_elem.string)
                else:
                    temp.append("未知天气")

                # 提取温度
                tem_elem = day.find('span', {'class': 'tem'})
                if tem_elem and tem_elem.text:
                    tem = tem_elem.text
                    try:
                        temp.append(tem[tem.index('/') + 1:-1])  # 最低气温
                        temp.append(tem[:tem.index('/') - 1])  # 最高气温
                    except ValueError:
                        # 如果温度格式异常，尝试其他处理方式
                        temp.extend(["未知", "未知"])
                else:
                    temp.extend(["未知", "未知"])

                # 提取风向
                wind_elem = day.find('span', {'class': 'wind'})
                if wind_elem and wind_elem.string:
                    wind = wind_elem.string
                    if '转' in wind:
                        temp.append(wind[:wind.index('转')])
                        temp.append(wind[wind.index('转') + 1:])
                    else:
                        temp.append(wind)
                        temp.append(wind)
                else:
                    temp.extend(["未知", "未知"])

                # 提取风级
                wind_scale_elem = day.find('span', {'class': 'wind1'})
                if wind_scale_elem and wind_scale_elem.string:
                    wind_scale = wind_scale_elem.string
                    try:
                        index1 = wind_scale.index('级')
                        temp.append(int(wind_scale[index1 - 1:index1]))
                    except (ValueError, IndexError):
                        temp.append(0)
                else:
                    temp.append(0)

                final.append(temp)
                i += 1
    return final


def write_to_csv(file_name, data, day=14):
    """保存数据到CSV文件"""
    with open(file_name, 'w', errors='ignore', newline='') as f:
        if day == 14:
            header = ['日期', '天气', '最低气温', '最高气温', '风向1', '风向2', '风级']
        else:
            header = ['小时', '温度', '风力方向', '风级', '降水量', '相对湿度', '空气质量']
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(data)


def main():
    """主函数：获取并保存天气数据"""
    print("Weather test")
    # 珠海天气网址
    url1 = 'http://www.weather.com.cn/weather/101280701.shtml'  # 7天天气
    url2 = 'http://www.weather.com.cn/weather15d/101280701.shtml'  # 8-15天天气

    # 获取网页内容
    html1 = getHTMLtext(url1)
    html2 = getHTMLtext(url2)

    # 解析数据
    data1, data1_7 = get_content(html1)  # 当天数据和1-7天数据
    data8_14 = get_content2(html2)  # 8-14天数据

    # 合并14天数据
    data14 = data1_7 + data8_14

    # 保存为CSV文件
    write_to_csv('weather14.csv', data14, day=14)
    write_to_csv('weather1.csv', data1, day=1)
    print("数据保存完成！")


if __name__ == '__main__':
    main()