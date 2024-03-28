import argparse
import numpy as np
import open3d as o3d


def find_min_area_faces(pcd):
    """
    找到点云的最小外接矩形的最小面积的两个面
    """
    obb = pcd.get_oriented_bounding_box()
    obb_corners = np.asarray(obb.get_box_points())
    areas = []
    for i in range(0, len(obb_corners), 4):
        face = obb_corners[i:i + 4]
        area = np.linalg.norm(np.cross(face[1] - face[0], face[2] - face[0]))
        areas.append(area)
    min_area_indices = np.argsort(areas)[:2]
    min_area_faces = [obb_corners[i:i + 4] for i in [min_area_indices[0] * 4, min_area_indices[1] * 4]]
    return min_area_faces


def visualize_line(pcd, min_area_faces, output_path):
    """
    将两个最小面积面的中心点连线可视化为蓝色点云,并保存为txt文件
    """
    face1 = min_area_faces[0]
    face2 = min_area_faces[1]
    center1 = np.mean(face1, axis=0)
    center2 = np.mean(face2, axis=0)
    line_points = np.stack([center1, center2], axis=0)
    line_pcd = o3d.geometry.PointCloud()
    line_pcd.points = o3d.utility.Vector3dVector(line_points)
    line_pcd.paint_uniform_color([0, 0, 1])  # 蓝色
    o3d.visualization.draw_geometries([pcd, line_pcd])

    line_data = np.zeros((len(line_points), 9))
    line_data[:, :3] = line_points
    line_data[:, 3:6] = [0, 0, 1]  # RGB值为蓝色
    np.savetxt(f"{output_path}_middleline.txt", line_data, fmt='%.6f')


def main(input_txt):
    pcd = o3d.io.read_point_cloud(input_txt, format='xyz')
    min_area_faces = find_min_area_faces(pcd)
    visualize_line(pcd, min_area_faces, input_txt.split(".")[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process point cloud data')
    parser.add_argument('--inputtxt', type=str, required=True, help='Path to the input point cloud txt file')
    args = parser.parse_args()
    main(args.inputtxt)