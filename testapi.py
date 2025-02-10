import requests
from shapely.geometry import LineString, box
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import warnings
import math

warnings.filterwarnings('ignore')

# 解决中文乱码问题,并设置字体
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = ['SimHei']
plt.rcParams['font.sans-serif'] = ['SimHei']

EARTH_RADIUS_KM = 6371


def calculate_rect_bounds(center, diagonal_km):
    """计算以中心点为中心、对角线长度为diagonal_km的矩形边界"""
    half_diagonal_km = diagonal_km / 2

    # 计算纬度方向上的变化
    lat_change = (half_diagonal_km / EARTH_RADIUS_KM) * (180 / math.pi)

    # 经度方向上的变化需要考虑当前纬度的位置，因为地球是一个椭球体
    lng_change = lat_change / math.cos(math.radians(center[1]))

    south_west = [center[0] - lng_change, center[1] - lat_change]
    north_east = [center[0] + lng_change, center[1] + lat_change]

    print(
        f"Generated Rectangle Bounds: {south_west[0]:.6f},{south_west[1]:.6f};{north_east[0]:.6f},{north_east[1]:.6f}")

    return f"{south_west[0]:.6f},{south_west[1]:.6f};{north_east[0]:.6f},{north_east[1]:.6f}"


def get_geocode(address):
    """通过地址获取经纬度"""
    BASE_URL = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'address': address,
        'key': 'eb132e1d7f0110a0ce0a210459251fce'
    }

    res = requests.get(BASE_URL, params=params).json()
    if res['status'] == '1' and len(res['geocodes']) > 0:
        location = res['geocodes'][0]['location'].split(',')
        return float(location[0]), float(location[1])
    else:
        error_info = res.get('info', 'Unknown error')
        infocode = res.get('infocode', 'No infocode')
        print(f"Geocode Error: {error_info}, infocode: {infocode}")
        return None


def get_status_data(sub_rectangle):
    """获取态势数据"""
    data = {'name': [], 'status': [], 'geometry': []}

    BASE_URL = ('https://restapi.amap.com/v3/traffic/status/rectangle?rectangle={}'
                '&output=json&extensions=all&key=eb132e1d7f0110a0ce0a210459251fce')

    res = requests.get(BASE_URL.format(sub_rectangle)).json()
    print("API Response:", res)  # 打印API响应以便调试

    if res['status'] == '1' and 'roads' in res['trafficinfo']:
        for road in res['trafficinfo']['roads']:
            polylines = [(float(y[0]), float(y[1])) for y in
                         [x.split(',') for x in road['polyline'].split(';')]]
            if len(polylines) > 1:  # 确保至少有两个点形成一条线
                data['geometry'].append(LineString(polylines))
                data['name'].append(road['name'])
                data['status'].append(road['status'])
    else:
        error_info = res.get('info', 'Unknown error')
        infocode = res.get('infocode', 'No infocode')
        print(f"Error: {error_info}, infocode: {infocode}")
    return gpd.GeoDataFrame(data, geometry='geometry', crs="EPSG:4326")


def plot_status(data, base_map=False):
    """绘制态势图"""
    fig, ax = plt.subplots(figsize=(10, 10), dpi=300)  # 设置宽高相同以确保正方形显示
    colors = {'3': 'red', '2': 'orange', '1': 'green', '0': 'grey'}
    linewidths = {'3': 2.0, '2': 1.3, '1': 0.7, '0': 0.2}

    if not data.empty:
        # 将GeoDataFrame转换到Web Mercator投影
        data_web_mercator = data.to_crs(epsg=3857)
        data_web_mercator.plot(column='status', figsize=(10, 10), ax=ax, color=data['status'].map(colors),
                               linewidth=data['status'].map(linewidths))

        # 添加矩形边界框
        minx, miny, maxx, maxy = data.total_bounds
        rect = box(minx, miny, maxx, maxy)
        gpd.GeoSeries([rect]).set_crs(data.crs).to_crs(epsg=3857).plot(ax=ax, facecolor="none", edgecolor="blue")
    else:
        print("没有可用的交通态势数据")

    if base_map:
        ctx.add_basemap(ax,
                        source="http://wprd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&style=7&x={x}&y={y}&z={z}",
                        reset_extent=False, crs='epsg:3857', alpha=1)

    ax.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 用户输入地址名称
    address = input("请输入地址名称（例如：北京市朝阳区阜通东大街6号）：")

    # 获取经纬度坐标
    center_point = get_geocode(address)
    if center_point is None:
        print("无法获取到有效的经纬度坐标，请检查输入的地址是否正确。")
    else:
        print(f"Center Point Coordinates: {center_point}")  # 打印中心点坐标以供验证

        # 根据中心点生成一个对角线长度为5公里的正方形区域
        rectangle_str = calculate_rect_bounds(center=center_point, diagonal_km=5)

        # 获取并绘制交通态势
        traffic_data = get_status_data(sub_rectangle=rectangle_str)
        plot_status(traffic_data, base_map=True)