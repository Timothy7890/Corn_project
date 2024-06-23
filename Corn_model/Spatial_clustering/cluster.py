import argparse
import numpy as np
from sklearn.cluster import DBSCAN
import os

def cluster_and_color(pcd_data, eps=0.4, threshold=0.8):
    """
    对语义A进行DBSCAN空间聚类,并为不同聚类和语义使用原始颜色
    """
    # 根据阈值过滤语义A和语义B
    semantic_a = pcd_data[pcd_data[:, 12] > threshold]
    semantic_b = pcd_data[pcd_data[:, 12] <= threshold]

    # 创建coords_A和coords_B矩阵
    coords_A = np.hstack((semantic_a[:, :6], np.zeros((len(semantic_a), 1)), semantic_a[:, 6:9]))
    coords_B = np.hstack((semantic_b[:, :6], np.zeros((len(semantic_b), 1)), semantic_b[:, 6:9]))

    # 对语义A进行DBSCAN聚类
    db = DBSCAN(eps=eps, min_samples=10).fit(coords_A[:, :3])
    labels = db.labels_

    # 更新coords_A和coords_B的聚类标签和语义标签
    coords_A = np.hstack((coords_A[:, :6], np.ones((len(coords_A), 1)), labels[:, np.newaxis] + 1, coords_A[:, 7:]))
    coords_A[labels == -1, 6] = 0  # 将离散点和小聚类的语义标签设置为0
    coords_A[labels == -1, 7] = 0  # 将离散点和小聚类的实例标签设置为0
    coords_B = np.hstack((coords_B[:, :6], np.zeros((len(coords_B), 1)), np.full((len(coords_B), 1), -1), coords_B[:, 7:]))

    # 合并coords_A和coords_B
    colored_data = np.vstack((coords_A, coords_B))

    return colored_data

def save_colored_data(colored_data, output_path):
    """
    保存着色后的点云数据
    """
    header = 'x y z r g b se in Nx Ny NZ'
    fmt = '%.6f %.6f %.6f %d %d %d %d %d %.6f %.6f %.6f'
    np.savetxt(output_path, colored_data, fmt=fmt, header=header, comments='')

def cluster_point_cloud(input_txt, output_txt, eps=0.4, threshold=0.8):
    if os.path.exists(output_txt):
        print(f"{output_txt}已存在，无需重复执行计算夹角分类和空间聚类。")
        return
    print("任务三:正在利用夹角进行分类和空间聚类...")
    pcd_data = np.loadtxt(input_txt, skiprows=1)
    colored_data = cluster_and_color(pcd_data, eps, threshold)
    save_colored_data(colored_data, output_txt)
