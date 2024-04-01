from Corn_model.Spatial_clustering import run_Spatial_clustering_pipeline

"""
此代码为一键执行代码，可以直接生成空间聚类的可视化结果;
在运行代码前需要确保原点云已经经过旋转对齐了Box;
输入的点云格式均为x y z R G B Nx Ny Nz.
"""

if __name__ == "__main__":

    input_txt = "/home/timo/音乐/DELETE/预处理/02/Corn_02.txt"

    eps = 0.4

    threshold = 0.8

    run_Spatial_clustering_pipeline(input_txt, eps, threshold)