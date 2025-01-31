# TFAFapp/traffic_status.py

import requests
from django.conf import settings


def get_traffic_status_from_api(road_name, adcode, level='', extensions='base', api_key=''):
    """
    获取指定道路的交通态势数据。

    参数:
        road_name (str): 道路名称。
        adcode (str): 城市编码。
        level (str, optional): 道路等级。默认为空字符串。
        extensions (str, optional): 返回信息详细程度 ('base' 或 'all')。默认为 'base'。
        api_key (str): 高德地图API密钥。

    返回:
        dict: 包含交通态势数据或错误信息的字典。
    """

    if not api_key:
        return {'error': '缺少API密钥'}

    url = "https://restapi.amap.com/v3/traffic/status/road"
    params = {
        'key': api_key,
        'name': road_name,
        'adcode': adcode,
        'extensions': extensions
    }
    # 如果提供了level参数，则添加到请求中
    if level:
        params['level'] = level

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get('status') == '1':
            return data  # 成功返回的数据
        else:
            return {'error': data.get('info', '未知错误')}
    except requests.RequestException as e:
        return {'error': f"请求失败: {e}"}