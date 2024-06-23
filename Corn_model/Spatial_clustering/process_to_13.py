import argparse
import numpy as np
from tqdm import tqdm  # 需要安装 tqdm 库
import os

def calculate_cosine(normal, radial):
    dot_product = np.dot(normal, radial)
    cosine = dot_product / (np.linalg.norm(normal) * np.linalg.norm(radial))
    return cosine

def process_point(point):
    normal = point[6:9]
    radial = point[9:12]
    cosine = calculate_cosine(normal, radial)
    return np.append(point, cosine)

def process_point_cloud(pcd_data):
    processed_data = []
    for point in tqdm(pcd_data, unit='points'):
        processed_data.append(process_point(point))
    return np.array(processed_data)

def save_point_cloud(pcd_data, output_path):
    header = 'x y z r g b nx ny nz rx ry rz cosine'
    fmt = ['%.6f'] * 3 + ['%d'] * 3 + ['%.6f'] * 7
    np.savetxt(output_path, pcd_data, fmt=fmt, header=header, comments='')

def process_point_cloud_13(input_txt, output_txt):
    if os.path.exists(output_txt):
        print(f"{output_txt}已存在，无需重复执行计算径向量与法向量的夹角。")
        return
    print("任务二:正在计算径向量与法向量的夹角...")
    pcd_data = np.loadtxt(input_txt, skiprows=1)
    processed_data = process_point_cloud(pcd_data)
    save_point_cloud(processed_data, output_txt)