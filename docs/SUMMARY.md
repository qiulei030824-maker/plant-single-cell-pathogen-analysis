# 水稻叶片单细胞数据分析产出索引

## 概述

本目录包含水稻叶片单细胞数据（GSE222584）分析的全部关键产出。分析解决了两个核心问题：
1. **基因ID转换**：将Ensembl ID转换为基因符号
2. **过度聚类优化**：从272个聚类减少到12个合理聚类

## 目录结构

```
memory-bank/
├── README.md                    # 总体说明
├── SUMMARY.md                   # 本文件，详细索引
├── scripts/                     # 分析脚本
│   ├── 01_check_gene_ids.py     # 基因ID检查脚本
│   ├── 02_convert_gene_ids.py   # 基因ID转换脚本
│   ├── 03_umap_diagnosis.py     # UMAP诊断框架
│   ├── 04_fix_umap_simple.py    # UMAP修正脚本（简化版）
│   ├── 05_marker_gene_analysis.py # 标记基因分析脚本
│   └── optimize_plant_scRNA.py  # 植物单细胞优化脚本
├── reports/                     # 分析报告
│   ├── optimization_report.md   # 完整优化报告
│   ├── FINAL_SUMMARY.md         # 最终分析总结
│   ├── DIAGNOSIS_REPORT.md      # 诊断框架报告
│   ├── conversion_summary.md    # 基因转换统计
│   └── optimization_summary.md  # 优化过程总结
├── results/                     # 关键结果数据
│   ├── top_markers_per_cluster.csv      # 各聚类前5标记基因
│   ├── celltype_annotation_suggestions.csv # 细胞类型注释建议
│   └── gene_mapping_table.csv   # 基因ID映射表
└── figures/                     # 可视化图片
    ├── umap_optimized.png       # 优化后UMAP图（12个聚类）
    ├── dotplot_top_markers.png  # 标记基因点图
    ├── marker_genes_umap.png    # 标记基因UMAP表达图
    ├── hvg_sensitivity_test.png # HVG敏感性测试图
    └── pca_elbow_plot.png       # PCA肘部图
```

## 文件详细说明

### 脚本文件 (scripts/)

#### 1. `01_check_gene_ids.py`
- **功能**: 检查h5ad文件中的基因ID格式
- **输入**: 单细胞数据文件（h5ad格式）
- **输出**: 基因ID格式统计报告
- **关键函数**:
  - `check_gene_id_formats()`: 识别Ensembl ID、RAP-DB ID、占位符等格式
  - `summarize_gene_ids()`: 生成格式统计摘要

#### 2. `02_convert_gene_ids.py`
- **功能**: 将Ensembl ID转换为基因符号
- **输入**: 原始h5ad文件、基因映射文件
- **输出**: 更新后的h5ad文件（包含gene_symbol列）
- **关键函数**:
  - `load_gene_mapping()`: 加载基因映射关系
  - `convert_gene_ids()`: 执行ID转换
  - **转换统计**: 314/1199个Ensembl ID成功转换（26.2%）

#### 3. `03_umap_diagnosis.py`
- **功能**: 6步UMAP诊断框架
- **输入**: 单细胞数据
- **输出**: 诊断报告和可视化
- **诊断步骤**:
  1. 数据质量检查
  2. HVG敏感性测试
  3. PCA肘部图分析
  4. 原生质体效应评估
  5. UMAP参数网格搜索
  6. 批次效应整合评估

#### 4. `04_fix_umap_simple.py`
- **功能**: 简化版UMAP修正脚本
- **输入**: 诊断后的数据
- **输出**: 优化后的聚类结果
- **关键优化**:
  - HVG数量: 1000 → 2000
  - 聚类数: 272 → 12（减少95.6%）
  - 分辨率参数优化

#### 5. `05_marker_gene_analysis.py`
- **功能**: 标记基因分析和生物学解释
- **输入**: 优化后的单细胞数据
- **输出**: 标记基因表、可视化、细胞类型注释
- **分析方法**:
  - Wilcoxon检验识别标记基因
  - 每个聚类提取前10个标记基因
  - 基于已知标记基因推测细胞类型

#### 6. `optimize_plant_scRNA.py`
- **功能**: 植物单细胞数据优化管道
- **输入**: 原始单细胞数据
- **输出**: 优化后的分析结果
- **特点**: 针对植物数据的特殊处理（原生质体效应、应激基因等）

### 报告文件 (reports/)

#### 1. `optimization_report.md`
- **内容**: 完整分析总结，包含四步流程的详细结果
- **页数**: 约5页
- **关键部分**:
  - 项目背景和问题定义
  - 四步分析流程完成情况
  - 技术成果汇总
  - 关键发现和局限性
  - 下一步建议

#### 2. `FINAL_SUMMARY.md`
- **内容**: 最终分析报告，面向读者
- **页数**: 约3页
- **关键部分**:
  - 数据基本信息
  - 标记基因分析结果（每个聚类前3个标记基因）
  - 细胞类型推测
  - 生成文件列表
  - 结论与建议

#### 3. `DIAGNOSIS_REPORT.md`
- **内容**: UMAP诊断框架详细说明
- **来源**: `memory-bank/rice_leaf_umap_diagnosis.md`
- **关键内容**:
  - 6步诊断框架原理
  - 植物单细胞特殊挑战
  - R代码示例和参数建议

#### 4. `conversion_summary.md`
- **内容**: 基因ID转换统计报告
- **关键数据**:
  - 总Ensembl ID数: 1199
  - 成功转换数: 314
  - 转换成功率: 26.2%
  - 未转换原因分析

#### 5. `optimization_summary.md`
- **内容**: 优化过程总结
- **关键优化**:
  - 过度聚类问题识别和解决
  - 参数优化过程记录
  - 最终参数设置

### 结果数据文件 (results/)

#### 1. `top_markers_per_cluster.csv`
- **格式**: CSV
- **内容**: 每个聚类的前5个标记基因
- **列说明**:
  - `cluster`: 聚类编号（0-11）
  - `gene`: 基因ID
  - `gene_symbol`: 基因符号（如已转换）
  - `score`: Wilcoxon检验得分
  - `pval_adj`: 调整后p值
- **行数**: 60行（12个聚类 × 5个基因）

#### 2. `celltype_annotation_suggestions.csv`
- **格式**: CSV
- **内容**: 细胞类型注释建议
- **列说明**:
  - `cluster`: 聚类编号
  - `cell_type`: 推测的细胞类型（大部分为unknown，需要进一步注释）
- **备注**: 由于水稻特异性标记基因知识有限，大部分聚类未能准确注释

#### 3. `gene_mapping_table.csv`
- **格式**: CSV
- **内容**: 基因ID映射关系
- **列说明**:
  - `original_id`: 原始基因ID
  - `gene_symbol`: 对应的基因符号
  - `source`: 数据来源
- **行数**: 314行（成功映射的基因）

### 可视化图片 (figures/)

#### 1. `umap_optimized.png`
- **尺寸**: 3191 KB
- **内容**: 优化后的UMAP可视化（12个聚类）
- **特点**: 清晰的聚类分离，无过度聚类现象
- **颜色**: 12种不同颜色代表不同聚类

#### 2. `dotplot_top_markers.png`
- **尺寸**: 616 KB
- **内容**: 标记基因点图
- **特点**: 显示每个聚类前3个标记基因的表达情况
- **可视化**: 点的大小表示表达比例，颜色表示平均表达量

#### 3. `marker_genes_umap.png`
- **尺寸**: 5754 KB
- **内容**: 标记基因在UMAP上的表达图
- **布局**: 2×2子图，显示4个关键标记基因的表达模式
- **基因示例**: 包括核糖体基因、代谢相关基因等

#### 4. `hvg_sensitivity_test.png`
- **尺寸**: 110 KB
- **内容**: HVG数量敏感性测试
- **关键发现**: HVG数量从1000增加到2000时，聚类数从384减少到12
- **结论**: HVG选择对聚类结果有显著影响

#### 5. `pca_elbow_plot.png`
- **尺寸**: 213 KB
- **内容**: PCA肘部图
- **关键发现**: 50个PC仅解释24.1%的方差
- **意义**: 数据可能需要更多PC或不同降维方法

## 原始数据位置

### 大文件（未复制到memory-bank）
1. **原始数据文件**:
   - 位置: `/data5/qiulei/onepiece/data/raw/gse222584/`
   - 格式: 可能包含多个h5ad或RDS文件
   - 大小: 较大，建议不移动

2. **处理后的数据文件**:
   - 主文件: `/data5/qiulei/onepiece/data/processed/gse222584/processed_data_optimized.h5ad`
   - 内容: 优化后的单细胞数据（12个聚类）
   - 大小: 较大，包含完整表达矩阵

3. **完整结果目录**:
   - 位置: `/data5/qiulei/onepiece/results/optimized_analysis/`
   - 内容: 所有中间结果和完整输出
   - 建议: 参考此目录获取更完整的结果

## 分析流程总结

### 第一步：基因ID转换
1. 检查基因ID格式，识别Ensembl ID等
2. 加载基因映射文件，执行ID转换
3. 统计转换成功率，生成映射表

### 第二步：UMAP诊断
1. 应用6步诊断框架
2. 识别HVG选择不当为主要问题
3. 评估批次效应、PCA解释方差等

### 第三步：参数优化
1. 增加HVG数量至2000
2. 优化聚类分辨率参数
3. 从272个聚类减少到12个合理聚类

### 第四步：验证与报告
1. 识别每个聚类的标记基因
2. 创建可视化结果
3. 尝试细胞类型注释
4. 生成完整分析报告

## 关键参数设置

### 最终优化参数
- **HVG数量**: 2000
- **PCA组件数**: 50
- **聚类算法**: Leiden
- **聚类分辨率**: 0.5
- **UMAP参数**: 
  - n_neighbors: 15
  - min_dist: 0.3
  - metric: euclidean

### 数据统计
- **总细胞数**: 54,237
- **总基因数**: 2,000（HVG）
- **聚类数**: 12（优化后）
- **批次数**: 9
- **批次效应**: 不明显（标准化熵 > 0.9）

## 使用建议

### 1. 复现分析
```bash
# 1. 检查基因ID
python scripts/01_check_gene_ids.py --input /path/to/data.h5ad

# 2. 转换基因ID  
python scripts/02_convert_gene_ids.py --input /path/to/data.h5ad --mapping gene_mapping_table.csv

# 3. 运行诊断
python scripts/03_umap_diagnosis.py --input /path/to/processed_data.h5ad

# 4. 优化参数
python scripts/04_fix_umap_simple.py --input /path/to/diagnosed_data.h5ad

# 5. 分析标记基因
python scripts/05_marker_gene_analysis.py --input /path/to/optimized_data.h5ad
```

### 2. 扩展分析
1. **补充基因注释**: 使用更完整的水稻基因注释数据库
2. **功能富集分析**: 对标记基因进行GO和KEGG分析
3. **比较分析**: 与已发表的水稻单细胞数据比较
4. **实验验证**: 使用原位杂交验证标记基因表达

### 3. 注意事项
- 脚本中的文件路径可能需要根据实际环境调整
- 部分基因ID未能转换，需要额外注释工作
- 细胞类型注释需要更多水稻特异性标记基因知识
- 大文件（h5ad）未复制到memory-bank，使用时需引用原始位置

## 版本信息

- **分析完成时间**: 2026年4月10日
- **数据来源**: GEO accession GSE222584
- **分析工具**: Scanpy (Python单细胞分析库)
- **脚本语言**: Python 3.12
- **环境**: scanpy_env虚拟环境

## 联系与引用

如需使用本分析结果，请引用：
- 原始数据: GSE222584 (水稻叶片单细胞转录组)
- 分析方法: 基于Scanpy的单细胞分析流程
- 诊断框架: 生信菜鸟团UMAP诊断框架

如有问题或需要进一步分析，请联系项目负责人。