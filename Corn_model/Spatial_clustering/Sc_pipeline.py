from .process_to_12 import process_point_cloud_12
from .process_to_13 import process_point_cloud_13
from .cluster import cluster_point_cloud


def run_Spatial_clustering_pipeline(input_txt, eps=0.4, threshold=0.8):
    output_12 = f"{input_txt.split('.')[0]}_12.txt"
    output_13 = f"{input_txt.split('.')[0]}_13.txt"
    output_clustered = f"{input_txt.split('.')[0]}_DBSCAN_clustered.txt"

    # 执行计算径向量
    process_point_cloud_12(input_txt, output_12)
    # 计算径向量与法向量的夹角
    process_point_cloud_13(output_12, output_13)
    # 利用夹角进行分类和空间聚类
    cluster_point_cloud(output_13, output_clustered, eps, threshold)
    print(f"{input_txt}目录执行完成\n")