import argparse
import numpy as np
from tqdm import tqdm  # 需要安装 tqdm 库

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
    fmt = ['%.6f'] * 13
    np.savetxt(f"{output_path}_13.txt", pcd_data, fmt=fmt, header=header, comments='')

def main(input_txt):
    pcd_data = np.loadtxt(input_txt, skiprows=1)
    processed_data = process_point_cloud(pcd_data)
    save_point_cloud(processed_data, input_txt.split(".")[0])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process point cloud data')
    parser.add_argument('--input12', type=str, required=True, help='Path to the input 12-column point cloud txt file')
    args = parser.parse_args()
    main(args.input12)