import argparse
import numpy as np
from sklearn.cluster import DBSCAN

def cluster_and_color(pcd_data, eps=0.4, threshold=0.8):
    """
    对语义A进行DBSCAN空间聚类,并为不同聚类和语义使用不同颜色
    """
    # 根据阈值过滤语义A和语义B
    semantic_a = pcd_data[pcd_data[:, 12] > threshold]
    semantic_b = pcd_data[pcd_data[:, 12] <= threshold]

    # 创建coords_A和coords_B矩阵
    coords_A = np.hstack((semantic_a[:, :3], np.ones((len(semantic_a), 1))))
    coords_B = np.hstack((semantic_b[:, :3], np.zeros((len(semantic_b), 1))))

    # 对语义A进行DBSCAN聚类
    db = DBSCAN(eps=eps, min_samples=10).fit(coords_A[:, :3])
    labels = db.labels_

    # 更新coords_A和coords_B的聚类标签和语义标签
    coords_A = np.hstack((coords_A, labels[:, np.newaxis]))
    coords_A[labels == -1, 3] = 0  # 将离散点和小聚类的语义标签设置为0
    coords_B = np.hstack((coords_B, np.full((len(coords_B), 1), -1)))

    # 为每个聚类分配不同的颜色,并将离群点的颜色设置为白色
    num_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    colors = np.random.randint(0, 256, size=(num_clusters + 1, 3))
    colors[-1] = [255, 255, 255]  # 将离群点的颜色设置为白色

    # 为coords_A和coords_B着色
    coords_A = np.hstack((coords_A, colors[coords_A[:, 4].astype(int)]))
    coords_B = np.hstack((coords_B, np.full((len(coords_B), 3), 255)))  # 语义B使用白色

    # 合并coords_A和coords_B
    colored_data = np.vstack((coords_A, coords_B))

    return colored_data

def save_colored_data(colored_data, output_path):
    """
    保存着色后的点云数据
    """
    header = 'x y z semantic cluster_label r g b'
    fmt = '%.6f %.6f %.6f %d %d %d %d %d'
    np.savetxt(f"{output_path}_DBSCAN.txt", colored_data, fmt=fmt, header=header, comments='')

def cluster_point_cloud(input_txt, output_txt, eps=0.4, threshold=0.8):
    pcd_data = np.loadtxt(input_txt, skiprows=1)
    colored_data = cluster_and_color(pcd_data, eps, threshold)
    save_colored_data(colored_data, output_txt)
