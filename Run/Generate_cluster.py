from Corn_model.Spatial_clustering.Sc_pipeline import run_pipeline

if __name__ == "__main__":

    input_txt = "/home/timo/音乐/DELETE/预处理/01/Corn_01.txt"

    eps = 0.4

    threshold = 0.8

    run_pipeline(input_txt, eps, threshold)