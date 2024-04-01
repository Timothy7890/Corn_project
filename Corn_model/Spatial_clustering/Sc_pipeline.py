from .process_12 import process_point_cloud_12
from .process_13 import process_point_cloud_13
from .cluster import cluster_point_cloud

def run_pipeline(input_txt, eps=0.4, threshold=0.8):
    output_12 = f"{input_txt.split('.')[0]}_12.txt"
    output_13 = f"{input_txt.split('.')[0]}_13.txt"
    output_clustered = f"{input_txt.split('.')[0]}_clustered.txt"

    process_point_cloud_12(input_txt, output_12)
    process_point_cloud_13(output_12, output_13)
    cluster_point_cloud(output_13, output_clustered, eps, threshold)