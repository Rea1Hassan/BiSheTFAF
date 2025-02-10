import pandas as pd
import os

# 输入文件列表
input_files = ['dataset0.csv', 'dataset1.csv', 'dataset2.csv']

# 输出文件名
output_file = './merged_dataset.csv'

# 检查输出文件是否存在，存在则删除
if os.path.exists(output_file):
    os.remove(output_file)

# 遍历输入文件并合并内容
header_written = False  # 标记表头是否已写入

for file in input_files:
    # 逐行读取文件
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 如果是第一个文件，保留表头
    if not header_written:
        with open(output_file, 'a', encoding='utf-8') as f_out:
            f_out.writelines(lines)
        header_written = True
    else:
        # 跳过表头，合并数据
        with open(output_file, 'a', encoding='utf-8') as f_out:
            f_out.writelines(lines[1:])  # 跳过第一行表头

print(f"文件合并完成，结果保存在 {output_file}")