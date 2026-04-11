# GSE222584 水稻病毒感染单细胞RNA-seq分析项目

## 项目概述
本项目提供了对GSE222584数据集的完整单细胞RNA-seq分析流程。该数据集包含水稻叶片在两种病毒（RGSV和RRSV）感染条件下的单细胞转录组数据。

## 分析内容
1. **数据预处理**: 质量控制、标准化、特征选择
2. **降维和可视化**: PCA、UMAP
3. **细胞聚类**: Leiden算法，使用最佳参数（resolution=0.4, n_neighbors=15）
4. **细胞类型注释**: 基于水稻标记基因字典和文献知识
5. **差异表达分析**: 三个对比组（Control vs RGSV, Control vs RRSV, RGSV vs RRSV）
6. **通路富集分析**: 使用本地水稻GO注释文件
7. **保守性分析**: 与已知病虫害标记基因比较
8. **可视化**: 8种不同类型的图表

## 文件结构
```
plant-single-cell-pathogen-analysis/
├── README.md                          # 本文件
├── docs/
│   ├── gse222584_analysis_summary.md          # 原始分析总结
│   ├── gse222584_optimized_analysis_summary.md # 优化分析总结
│   └── gse222584_environment_config.yml       # 环境配置
├── scripts/
│   ├── run_gse222584_optimized_fixed_bestparams.py  # 主分析脚本
│   └── start_analysis.sh                          # 启动脚本
└── data/
    └── README_data.md                            # 数据下载说明
```

## 快速开始

### 1. 环境设置
```bash
# 创建conda环境
conda create -n rice_scRNA python=3.12
conda activate rice_scRNA

# 安装依赖包
pip install scanpy==1.10.0 anndata==0.10.0 pandas==2.2.0 numpy==1.26.0
pip install scipy==1.12.0 matplotlib==3.8.0 seaborn==0.13.0
pip install gseapy==1.0.6 statsmodels==0.14.0 scikit-learn==1.4.0
```

### 2. 数据准备
1. 从NCBI GEO下载GSE222584数据（accession: GSE222584）
2. 将数据预处理为h5ad格式
3. 下载水稻GO注释文件

### 3. 运行分析
```bash
# 运行主分析脚本
python scripts/run_gse222584_optimized_fixed_bestparams.py

# 或使用启动脚本
bash scripts/start_analysis.sh
```

## 分析结果

### 细胞类型注释结果
分析识别了10个聚类，注释为9种细胞类型：
1. **防御响应细胞** (defense_response): 包含PR蛋白、R基因等防御相关基因
2. **表皮细胞** (epidermal): 包含脂质转移蛋白、角质合成相关基因
3. **代谢细胞** (metabolic): 包含糖代谢、能量代谢相关基因
4. **细胞壁代谢细胞** (cell_wall): 包含细胞壁合成、修饰相关基因
5. **解毒细胞** (detoxification): 包含谷胱甘肽S-转移酶、细胞色素P450等
6. **转运细胞** (transport): 包含转运蛋白、载体蛋白
7. **水分运输细胞** (water_transport): 包含水通道蛋白
8. **应激响应细胞** (stress_response): 包含热激蛋白、氧化应激相关基因
9. **未知细胞类型** (Unknown)

### 差异表达分析结果
- **Control vs RGSV**: 1,973个显著差异基因（490上调，1,483下调）
- **Control vs RRSV**: 998个显著差异基因（420上调，578下调）
- **RGSV vs RRSV**: 1,410个显著差异基因（988上调，422下调）

### 通路富集分析结果
Control vs RGSV下调基因富集到150个Reactome通路。

## 技术细节

### 最佳参数
- **分辨率 (resolution)**: 0.4
- **邻居数 (n_neighbors)**: 15
- **轮廓系数**: 0.032
- **聚类数**: 10

### 分析方法
1. **数据预处理**: 对数标准化、高变基因选择
2. **降维**: PCA（30个主成分）
3. **聚类**: Leiden算法
4. **差异表达**: Wilcoxon秩和检验，FDR校正
5. **富集分析**: 超几何检验，使用本地水稻GO注释

## 输出文件
分析生成以下输出文件：
- `processed_data_with_celltype.h5ad`: 带细胞类型注释的数据
- `cell_type_annotations.csv`: 细胞类型注释详情
- `de_*_vs_*_*.csv`: 差异表达分析结果
- `*_enrichment.csv`: 通路富集分析结果
- 多种可视化图表（PNG格式）

## 引用
如果使用此分析流程，请引用：
- **Scanpy**: Wolf et al., Genome Biology, 2018
- **GSE222584数据集**: 原始研究论文
- **水稻GO注释**: Rice Genome Annotation Project Release 7

## 联系方式
如有问题或建议，请通过GitHub Issues提交。

## 许可证
本项目采用MIT许可证。详见LICENSE文件。

## 更新日志
- **2026-04-11**: 初始版本发布，包含完整分析流程
- **2026-04-10**: 参数优化和错误修复
- **2026-04-09**: 初始分析完成