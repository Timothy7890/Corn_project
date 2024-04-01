from Corn_model.Midline_extraction import extract_midline

"""
此代码为一键执行代码，可以直接生成中轴线；
在运行代码前需要确保原点云已经经过旋转对齐了Box;
输入输出的点云格式均为x y z R G B Nx Ny Nz.
"""


if __name__ == "__main__":
    # 输入点云文件的路径
    input_txt = "/home/timo/音乐/DELETE/预处理/01/Corn_01.txt"

    # 生成直线点云的点数
    num_points = 20000

    # 直线延伸的比例
    extend_ratio = 0.05

    extract_midline(input_txt, num_points, extend_ratio)