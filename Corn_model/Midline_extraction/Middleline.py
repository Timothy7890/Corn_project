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


def find_min_area_faces(vertices, faces):
    """
    找到最小面积的两个面
    """
    face_areas = []
    for face in faces:
        face_vertices = [vertices[i] for i in face]
        face_vertices = np.array(face_vertices)
        v1 = face_vertices[1] - face_vertices[0]
        v2 = face_vertices[2] - face_vertices[0]
        area = np.linalg.norm(np.cross(v1, v2))
        face_areas.append(area)

    min_area_indices = np.argsort(face_areas)[:2]
    min_area_faces = [faces[i] for i in min_area_indices]

    return min_area_faces


def generate_line_points(vertices, min_area_faces, num_points=100, extend_ratio=0.1):
    """
    在最小面积的两个面的中心点之间生成一条直线点云
    """
    face1_center = np.mean([vertices[i] for i in min_area_faces[0]], axis=0)
    face2_center = np.mean([vertices[i] for i in min_area_faces[1]], axis=0)

    line_vector = face2_center - face1_center
    line_length = np.linalg.norm(line_vector)
    line_direction = line_vector / line_length

    extended_length = line_length * (1 + 2 * extend_ratio)
    start_point = face1_center - line_direction * line_length * extend_ratio
    end_point = face2_center + line_direction * line_length * extend_ratio

    line_points = np.linspace(start_point, end_point, num_points)

    return line_points


def save_line_points(line_points, output_path):
    """
    保存直线点云
    """
    line_data = np.zeros((len(line_points), 9))
    line_data[:, :3] = line_points
    line_data[:, 3:6] = [79, 195, 247]  # 蓝色 (RGB 范围: 0-255)

    # 将 RGB 分量保留为整数
    line_data[:, 3:6] = line_data[:, 3:6].astype(int)

    np.savetxt(f"{output_path}_midline.txt", line_data, fmt='%.6f %.6f %.6f %d %d %d %.6f %.6f %.6f')

def extract_midline(input_txt, num_points=100, extend_ratio=0.1):
    pcd = o3d.io.read_point_cloud(input_txt, format='xyzrgb')
    vertices, faces = get_bounding_box(pcd)
    min_area_faces = find_min_area_faces(vertices, faces)
    line_points = generate_line_points(vertices, min_area_faces, num_points, extend_ratio)
    save_line_points(line_points, input_txt.split(".")[0])

def main(input_txt):
    pcd = o3d.io.read_point_cloud(input_txt, format='xyzrgb')
    vertices, faces = get_bounding_box(pcd)
    min_area_faces = find_min_area_faces(vertices, faces)
    line_points = generate_line_points(vertices, min_area_faces)
    save_line_points(line_points, input_txt.split(".")[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process point cloud data')
    parser.add_argument('--inputtxt', type=str, required=True, help='Path to the input point cloud txt file')
    args = parser.parse_args()
    main(args.inputtxt)