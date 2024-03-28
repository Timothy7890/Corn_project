import argparse
import numpy as np
from concurrent.futures import ThreadPoolExecutor


def get_bounding_box(pcd_points):
    """
    从NumPy数组中计算点云的外接矩形边界框
    """
    x_min, y_min, z_min = np.min(pcd_points, axis=0)
    x_max, y_max, z_max = np.max(pcd_points, axis=0)

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


def generate_line_equation(vertices, min_area_faces):
    """
    生成中线的解析方程
    """
    face1_center = np.mean([vertices[i] for i in min_area_faces[0]], axis=0)
    face2_center = np.mean([vertices[i] for i in min_area_faces[1]], axis=0)

    line_direction = face2_center - face1_center
    line_direction /= np.linalg.norm(line_direction)

    point_on_line = face1_center

    return line_direction, point_on_line


def calculate_radial_vector(point, line_direction, point_on_line):
    """
    计算单个点到中线的径向量
    """
    line_vector = line_direction
    point_vector = point - point_on_line

    radial_vector = point_vector - np.dot(point_vector, line_vector) * line_vector
    radial_vector /= np.linalg.norm(radial_vector)

    return radial_vector


def calculate_radial_vectors(pcd_points, line_direction, point_on_line):
    """
    使用多线程计算每个点到中线的径向量
    """
    with ThreadPoolExecutor() as executor:
        radial_vectors = list(
            executor.map(lambda point: calculate_radial_vector(point, line_direction, point_on_line), pcd_points))
    return np.array(radial_vectors)


def save_point_cloud(pcd_data, output_path):
    """
    保存处理后的点云
    """
    header = 'x y z r g b nx ny nz rx ry rz'
    fmt = ['%.6f'] * 12
    np.savetxt(f"{output_path}_12.txt", pcd_data, fmt=fmt, header=header, comments='')


def main(input_txt):
    pcd_data = np.loadtxt(input_txt, skiprows=1)
    pcd_points = pcd_data[:, :3]

    vertices, faces = get_bounding_box(pcd_points)
    min_area_faces = find_min_area_faces(vertices, faces)
    line_direction, point_on_line = generate_line_equation(vertices, min_area_faces)
    radial_vectors = calculate_radial_vectors(pcd_points, line_direction, point_on_line)

    pcd_data = np.hstack((pcd_data, radial_vectors))
    save_point_cloud(pcd_data, input_txt.split(".")[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process point cloud data')
    parser.add_argument('--inputtxt', type=str, required=True, help='Path to the input point cloud txt file')
    args = parser.parse_args()
    main(args.inputtxt)