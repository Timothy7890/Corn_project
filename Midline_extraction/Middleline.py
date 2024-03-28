import argparse
import numpy as np
import open3d as o3d


def get_bounding_box(pcd):
    """
    获取点云的外接矩形边界框
    """
    min_bound = pcd.get_min_bound()
    max_bound = pcd.get_max_bound()

    x_min, y_min, z_min = min_bound
    x_max, y_max, z_max = max_bound

    vertices = [
        [x_min, y_min, z_min],
        [x_max, y_min, z_min],
        [x_max, y_max, z_min],
        [x_min, y_max, z_min],
        [x_min, y_min, z_max],
        [x_max, y_min, z_max],
        [x_max, y_max, z_max],
        [x_min, y_max, z_max],
    ]

    faces = [
        [0, 1, 2, 3],  # 底面
        [4, 5, 6, 7],  # 顶面
        [0, 1, 5, 4],  # 前面
        [2, 3, 7, 6],  # 后面
        [0, 3, 7, 4],  # 左面
        [1, 2, 6, 5],  # 右面
    ]

    return vertices, faces


def save_faces(vertices, faces, output_path):
    """
    保存外接矩形的六个面的点云
    """
    face_data = np.zeros((24, 9))

    for i, face in enumerate(faces):
        for j, vertex_idx in enumerate(face):
            face_data[i * 4 + j, :3] = vertices[vertex_idx]
            face_data[i * 4 + j, 3:6] = [1, 0, 0]  # 红色

    np.savetxt(f"{output_path}_sixface.txt", face_data, fmt='%.6f')


def main(input_txt):
    pcd = o3d.io.read_point_cloud(input_txt, format='xyzrgb')
    vertices, faces = get_bounding_box(pcd)
    save_faces(vertices, faces, input_txt.split(".")[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process point cloud data')
    parser.add_argument('--inputtxt', type=str, required=True, help='Path to the input point cloud txt file')
    args = parser.parse_args()
    main(args.inputtxt)