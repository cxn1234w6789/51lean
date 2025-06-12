import requests
from lxml import etree
import csv


# 定义方法
def getWeather(url):
    weather_info = []
    headers = {
        'Cookie': 'UserId=17496035600867617; Hm_lvt_5326a74bb3e3143580750a123a85e7a1=1749603561; Hm_lpvt_5326a74bb3e3143580750a123a85e7a1=1749603561; HMACCOUNT=F52D64889A80249F; Hm_lvt_7c50c7060f1f743bccf8c150a646e90a=1749603561; Hm_lpvt_7c50c7060f1f743bccf8c150a646e90a=1749603561; UserId=17496037381787088; Hm_lvt_ab6a683aa97a52202eab5b3a9042a8d2=1749603739; Hm_lpvt_ab6a683aa97a52202eab5b3a9042a8d2=1749603739; HMACCOUNT=91DB9E7447263287',
        'referer': 'https://lishi.tianqi.com/shanghai/201701.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0'
    }

    try:
        # 发起请求，接受响应数据
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 数据预处理
        resp_html = etree.HTML(response.text)

        # 修正xpath表达式
        resp_list = resp_html.xpath("//ul[@class='thrui']/li")

        for li in resp_list:
            day_weather_info = {}

            # 日期
            date_text = li.xpath("./div[1]/text()")
            day_weather_info['date_time'] = date_text[0].split(' ')[0] if date_text else ""

            # 最高气温(处理摄氏度符号)
            high_text = li.xpath("./div[2]/text()")
            high = high_text[0] if high_text else ""
            day_weather_info['high'] = high.replace("°C", "")

            # 最低气温
            low_text = li.xpath("./div[3]/text()")
            low = low_text[0] if low_text else ""
            day_weather_info['low'] = low.replace("°C", "")

            # 天气
            weather_text = li.xpath("./div[4]/text()")
            day_weather_info['weather'] = weather_text[0] if weather_text else ""

            weather_info.append(day_weather_info)

    except Exception as e:
        print(f"获取天气数据时出错: {e}")

    return weather_info


# 主程序
all_weather_data = []

# 获取1月份数据
january_url = "https://lishi.tianqi.com/shanghai/201701.html"
january_data = getWeather(january_url)
all_weather_data.extend(january_data)
print(f"已获取1月份数据，共{len(january_data)}条记录")

# 获取2-12月份数据
for month in range(2, 13):
    # 格式化月份为两位数
    month_str = str(month).zfill(2)
    url = f"https://lishi.tianqi.com/shanghai/2017{month_str}.html"

    # 更新referer

    monthly_data = getWeather(url)
    all_weather_data.extend(monthly_data)
    print(f"已获取{month}月份数据，共{len(monthly_data)}条记录")

# 数据写入CSV
try:
    with open('../weather_2017.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # 写入列名
        writer.writerow(['日期', '最高气温', '最低气温', '天气'])

        # 写入数据
        for day_data in all_weather_data:
            writer.writerow([
                day_data['date_time'],
                day_data['high'],
                day_data['low'],
                day_data['weather']
            ])

        print(f"数据已成功写入 weather_2017.csv，共{len(all_weather_data)}条记录")

except Exception as e:
    print(f"写入CSV文件时出错:{e}")
