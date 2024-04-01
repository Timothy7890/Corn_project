from Midline_extraction import extract_midline

if __name__ == "__main__":
    # 输入点云文件的路径
    input_txt = "/home/timo/音乐/DELETE/预处理/01/Corn_01.txt"

    # 生成直线点云的点数
    num_points = 20000

    # 直线延伸的比例
    extend_ratio = 0.05

    extract_midline(input_txt, num_points, extend_ratio)