# TFAFapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.conf import settings

# 保留原有的index视图
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def get_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            address = data.get('address')
            if not address:
                return JsonResponse({'error': '缺少地址参数'}, status=400)

            location = get_location_from_address(address, settings.AMAP_API_KEY)  # 使用API Key
            if location:
                return JsonResponse({'location': location})
            else:
                return JsonResponse({'error': '未找到对应位置'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON格式'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"处理请求时出错: {str(e)}"}, status=500)

    return JsonResponse({'error': '无效请求方法'}, status=405)

def get_location_from_address(address, api_key):
    geocode_url = 'https://restapi.amap.com/v3/geocode/geo'
    params = {
        'address': address,
        'key': api_key,
        'output': 'json',
    }

    try:
        response = requests.get(geocode_url, params=params)
        response.raise_for_status()

        data = response.json()
        print("完整响应数据:", data)  # 调试信息

        if data['status'] == '1' and data.get('infocode') == '10000':
            geo_codes = data.get('geocodes', [])
            if geo_codes:
                location = geo_codes[0].get('location')
                print(f"地址: {address} 对应的经纬度是: {location}")  # 调试信息
                return location
            else:
                print("未找到对应位置")  # 调试信息
        else:
            print(
                f"API响应异常，状态: {data.get('status')}, 错误信息: {data.get('info')}, infocode: {data.get('infocode')}")
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")  # 调试信息

    return None


# TFAFapp/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .traffic_status import get_traffic_status_from_api
from django.conf import settings
# TFAFapp/views.py

from .traffic_status import get_traffic_status_from_api
from django.conf import settings

@csrf_exempt
def query_traffic_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            road_name = data.get('road_name')
            adcode = data.get('adcode')
            level = data.get('level', '')
            extensions = data.get('extensions', 'base')

            if not road_name or not adcode:
                return JsonResponse({'error': '缺少必要的参数'}, status=400)

            traffic_data = get_traffic_status_from_api(
                road_name=road_name,
                adcode=adcode,
                level=level,
                extensions=extensions,
                api_key=settings.AMAP_API_KEY
            )

            if 'error' in traffic_data:
                return JsonResponse(traffic_data, status=500)
            else:
                return JsonResponse(traffic_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的JSON格式'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f"处理请求时出错: {str(e)}"}, status=500)

    return JsonResponse({'error': '无效请求方法'}, status=405)




