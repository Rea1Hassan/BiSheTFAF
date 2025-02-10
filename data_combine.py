import pandas as pd

# 读取通行情况数据表
merged_dataset = pd.read_csv('merged_dataset.csv')

# 读取路段信息表
road_info = pd.read_csv('road_info.csv')

# 按 ROADSECT_ID 进行合并，以 merged_dataset.csv 为主表
merged_result = pd.merge(merged_dataset, road_info, on='ROADSECT_ID', how='left')

# 将合并结果保存到新的 CSV 文件
merged_result.to_csv('merged_with_road_info.csv', index=False)

print("文件合并完成，结果保存在 merged_with_road_info.csv")