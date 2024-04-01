# Corn_project



## 代码架构如下：

```
.
├── Corn_model
│   ├── __init__.py
│   ├── Midline_extraction
│   │   ├── __init__.py
│   │   ├── Middleline.py
│   └── Spatial_clustering
│       ├── cluster.py
│       ├── __init__.py
│       ├── process_to_12.py
│       ├── process_to_13.py
│       └── Sc_pipeline.py
├── Data_demo
│   ├── Corn_01.txt
│   ├── Corn_02.txt
│   ├── Corn_03.txt
│   └── Corn_04.txt
├── History
│   ├── Cal12to13_One.py
│   ├── DBSCAN_visual.py
│   └── Save12_One.py
├── README.md
└── Run
    ├── Generate_cluster.py
    └── Generate_midline.py

```



## 代码说明

代码可以一键实现两个功能：一是保存提取的中轴线点云； 二是保存空间聚类的可视化结果。

分别对应Run目录下的两个代码

```
└── Run
    ├── Generate_cluster.py
    └── Generate_midline.py
```







