def calculate_radial_vector(point, line_points):
    """
    计算单个点到中线的径向量
    """
    dists = np.linalg.norm(line_points - point, axis=1)
    closest_point_idx = np.argmin(dists)
    closest_point = line_points[closest_point_idx]
    radial_vector = point - closest_point
    radial_vector /= np.linalg.norm(radial_vector)
    return radial_vector


def calculate_radial_vectors(pcd_points, line_points):
    """
    使用多线程计算每个点到中线的径向量
    """
    with ThreadPoolExecutor() as executor:
        radial_vectors = list(executor.map(lambda point: calculate_radial_vector(point, line_points), pcd_points))
    return np.array(radial_vectors)


def save_point_cloud(pcd_points, output_path):
    """
    保存处理后的点云
    """
    header = 'x y z r g b nx ny nz rx ry rz'
    fmt = ['%.6f'] * 12
    np.savetxt(f"{output_path}_12.txt", pcd_points, fmt=fmt, header=header, comments='')


def main(input_txt):
    pcd = o3d.io.read_point_cloud(input_txt, format='xyzrgb')
    pcd_points = np.asarray(pcd.points)
    pcd_colors = np.asarray(pcd.colors)
    pcd_normals = np.asarray(pcd.normals)
    pcd_data = np.hstack((pcd_points, pcd_colors, pcd_normals))

    vertices, faces = get_bounding_box(pcd)
    min_area_faces = find_min_area_faces(vertices, faces)
    line_points = generate_line_points(vertices, min_area_faces)
    radial_vectors = calculate_radial_vectors(pcd_points, line_points)

    pcd_data = np.hstack((pcd_data, radial_vectors))
    save_point_cloud(pcd_data, input_txt.split(".")[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process point cloud data')
    parser.add_argument('--inputtxt', type=str, required=True, help='Path to the input point cloud txt file')
    args = parser.parse_args()
    main(args.inputtxt)