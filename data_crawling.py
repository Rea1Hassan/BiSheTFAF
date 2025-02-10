import requests
import pandas as pd
import time
from datetime import datetime

# 参数设置
RequestURL = 'https://opendata.sz.gov.cn/api/29200_00403590/1/service.xhtml'   # 输入项目地址
appKey = '88a6e8a1c4164d64a7b2bbf91c09408d'  # API密钥
header = {'User-Agent': 'Custom'}  # 设置请求头
FileName = 'dataset2.csv'  # 输出文件名

# 用户输入页码和每页记录数
try:
    start_page = int(input("请输入开始的页码（例如1）："))
    end_page = int(input("请输入结束的页码："))
    rows_per_page = int(input("请输入每页返回的记录数（例如5000）："))
except ValueError:
    print("输入无效，请输入整数。")
    exit()

# 检查页码范围是否合理
if start_page > end_page:
    print("开始页码不能大于结束页码。")
    exit()

# 测试API请求，检查返回状态码是否为200
test_url = f"{RequestURL}?appKey={appKey}&page={start_page}&rows=1"
response = requests.get(test_url, headers=header)
if response.status_code != 200:
    print('API请求失败，状态码：', response.status_code)
    exit()

# 初始化数据列表
pd_data = []
total_records = 0  # 用于记录已获取的总记录数

for page_num in range(start_page, end_page + 1):
    # 计算当前页码对应的URL参数
    page_params = f'?appKey={appKey}&page={page_num}&rows={rows_per_page}'
    try:
        # 发送请求并获取响应内容
        response = requests.get(RequestURL + page_params, headers=header)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        # 检查是否有数据返回
        if 'data' not in data or not data['data']:
            print(f"第{page_num}页没有数据，可能是最后一页。")
            break

        # 获取当前页的数据
        records = data['data']
        total_records += len(records)

        # 将每条数据转换为DataFrame，并添加到pd_data列表中
        for row in records:
            # 转换TIME字段为日期时间格式
            row['TIME'] = datetime.fromtimestamp(row['TIME'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            pd_data.append(pd.DataFrame.from_dict(row, orient='index').T)

        print(f'获取第{page_num}页数据，共{len(records)}条记录。累计获取：{total_records}条记录。')
        time.sleep(0.5)  # 防止请求过快被限制

    except requests.exceptions.HTTPError as http_err:
        print(f'请求第{page_num}页数据失败，HTTP错误：{http_err}')
        break
    except Exception as e:
        print(f'请求第{page_num}页数据失败，原因：{e}')
        break

# 将所有DataFrame合并为一个DataFrame并保存为CSV文件
if pd_data:
    pd.concat(pd_data, ignore_index=True).to_csv(FileName, index=False)
    print(f'数据已成功保存为 {FileName}')
else:
    print('未获取到任何数据，请检查接口或参数。')