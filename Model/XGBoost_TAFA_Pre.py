import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import tkinter as tk
from tkinter import messagebox


def preprocess_data(road_id):
    # 加载数据并指定完整路径
    df = pd.read_csv(r'D:\BiShe-HZX\BiSheTFAF\merged_with_road_info.csv')

    # 过滤出指定道路的数据
    df = df[df['ROADSECT_ID'] == road_id]

    # 特征工程
    df['avg_len'] = df['GOLEN'] / df['GOCOUNT']
    df['avg_time'] = df['GOTIME'] / df['GOCOUNT']
    df['v1'] = df['avg_len'] / df['avg_time']
    df['v2'] = df['v1'] * 3.6
    df['is_congested'] = (df['v2'] < df['JAM_SPEED']).astype(int)

    # 保存预处理后的数据到本地
    processed_file_path = f"D:\\BiShe-HZX\\BiSheTFAF\\processed_data_{road_id}.csv"
    df.to_csv(processed_file_path, index=False)

    features = ['PERIOD', 'GOCOUNT', 'avg_len', 'avg_time', 'v2', 'ROADLENGTH']
    X = df[features]
    y = df['is_congested']

    return X, y, processed_file_path


def train_and_evaluate(X, y, test_size):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report


def on_submit():
    try:
        road_id = int(entry_road_id.get())
        test_size = float(entry_test_size.get())

        if not 0 < test_size < 1:
            raise ValueError("测试集比例应在0和1之间")

        X, y, processed_file_path = preprocess_data(road_id)
        accuracy, report = train_and_evaluate(X, y, test_size)

        messagebox.showinfo("结果",
                            f"准确率: {accuracy:.4f}\n\n分类报告:\n{report}\n\n预处理后的数据已保存至: {processed_file_path}")
    except Exception as e:
        messagebox.showerror("错误", str(e))


# 创建主窗口
root = tk.Tk()
root.title("交通拥堵预测")

# 添加输入框和标签
tk.Label(root, text="道路ID:").grid(row=0, column=0)
entry_road_id = tk.Entry(root)
entry_road_id.grid(row=0, column=1)

tk.Label(root, text="测试集比例（例如，0.2表示20%）:").grid(row=1, column=0)
entry_test_size = tk.Entry(root)
entry_test_size.grid(row=1, column=1)

# 添加提交按钮
submit_button = tk.Button(root, text="提交", command=on_submit)
submit_button.grid(row=2, columnspan=2)

# 运行主循环
root.mainloop()