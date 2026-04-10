#!/bin/bash

# 水稻叶片单细胞数据分析产出整理脚本
# 将关键文件整理到 memory-bank 目录

set -e

# 基础目录
PROJECT_DIR="/data5/qiulei/onepiece"
MEMORY_BANK="$PROJECT_DIR/memory-bank"
SCRIPTS_DIR="$MEMORY_BANK/scripts"
REPORTS_DIR="$MEMORY_BANK/reports"
RESULTS_DIR="$MEMORY_BANK/results"
FIGURES_DIR="$MEMORY_BANK/figures"

echo "创建目录结构..."
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$REPORTS_DIR"
mkdir -p "$RESULTS_DIR"
mkdir -p "$FIGURES_DIR"

echo "复制脚本文件..."

# 1. 基因ID检查脚本
if [ -f "$PROJECT_DIR/scripts/01_check_gene_ids.py" ]; then
    cp "$PROJECT_DIR/scripts/01_check_gene_ids.py" "$SCRIPTS_DIR/"
    echo "  复制: 01_check_gene_ids.py"
fi

# 2. 基因ID转换脚本
if [ -f "$PROJECT_DIR/scripts/02_convert_gene_ids.py" ]; then
    cp "$PROJECT_DIR/scripts/02_convert_gene_ids.py" "$SCRIPTS_DIR/"
    echo "  复制: 02_convert_gene_ids.py"
fi

# 3. UMAP诊断脚本
if [ -f "$PROJECT_DIR/scripts/03_umap_diagnosis.py" ]; then
    cp "$PROJECT_DIR/scripts/03_umap_diagnosis.py" "$SCRIPTS_DIR/"
    echo "  复制: 03_umap_diagnosis.py"
fi

# 4. UMAP修正脚本（简化版）
if [ -f "$PROJECT_DIR/scripts/04_fix_umap_simple.py" ]; then
    cp "$PROJECT_DIR/scripts/04_fix_umap_simple.py" "$SCRIPTS_DIR/"
    echo "  复制: 04_fix_umap_simple.py"
fi

# 5. 标记基因分析脚本
if [ -f "$PROJECT_DIR/scripts/05_marker_gene_analysis.py" ]; then
    cp "$PROJECT_DIR/scripts/05_marker_gene_analysis.py" "$SCRIPTS_DIR/"
    echo "  复制: 05_marker_gene_analysis.py"
fi

# 6. 优化脚本（如果有R脚本）
if [ -f "$PROJECT_DIR/scripts/optimize_plant_scRNA.py" ]; then
    cp "$PROJECT_DIR/scripts/optimize_plant_scRNA.py" "$SCRIPTS_DIR/"
    echo "  复制: optimize_plant_scRNA.py"
fi

echo "复制报告文件..."

# 1. 完整分析总结
if [ -f "$PROJECT_DIR/results/optimized_analysis/complete_analysis_summary.md" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/complete_analysis_summary.md" "$REPORTS_DIR/optimization_report.md"
    echo "  复制: complete_analysis_summary.md -> optimization_report.md"
fi

# 2. 最终分析报告
if [ -f "$PROJECT_DIR/results/optimized_analysis/final_analysis_report.md" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/final_analysis_report.md" "$REPORTS_DIR/FINAL_SUMMARY.md"
    echo "  复制: final_analysis_report.md -> FINAL_SUMMARY.md"
fi

# 3. 诊断报告（从memory-bank中已有的）
if [ -f "$MEMORY_BANK/rice_leaf_umap_diagnosis.md" ]; then
    cp "$MEMORY_BANK/rice_leaf_umap_diagnosis.md" "$REPORTS_DIR/DIAGNOSIS_REPORT.md"
    echo "  复制: rice_leaf_umap_diagnosis.md -> DIAGNOSIS_REPORT.md"
fi

# 4. 基因转换统计
if [ -f "$PROJECT_DIR/results/optimized_analysis/step2_gene_id_conversion.md" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/step2_gene_id_conversion.md" "$REPORTS_DIR/conversion_summary.md"
    echo "  复制: step2_gene_id_conversion.md -> conversion_summary.md"
fi

# 5. 优化总结
if [ -f "$PROJECT_DIR/results/optimized_analysis/step3_optimization_summary.md" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/step3_optimization_summary.md" "$REPORTS_DIR/optimization_summary.md"
    echo "  复制: step3_optimization_summary.md -> optimization_summary.md"
fi

echo "复制结果数据文件..."

# 1. 标记基因表
if [ -f "$PROJECT_DIR/results/optimized_analysis/marker_genes_top5_summary.csv" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/marker_genes_top5_summary.csv" "$RESULTS_DIR/top_markers_per_cluster.csv"
    echo "  复制: marker_genes_top5_summary.csv -> top_markers_per_cluster.csv"
fi

# 2. 细胞类型注释
if [ -f "$PROJECT_DIR/results/optimized_analysis/cell_type_annotations.csv" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/cell_type_annotations.csv" "$RESULTS_DIR/celltype_annotation_suggestions.csv"
    echo "  复制: cell_type_annotations.csv -> celltype_annotation_suggestions.csv"
fi

# 3. 基因映射表
if [ -f "$PROJECT_DIR/results/optimized_analysis/gene_mapping_gse222584.csv" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/gene_mapping_gse222584.csv" "$RESULTS_DIR/gene_mapping_table.csv"
    echo "  复制: gene_mapping_gse222584.csv -> gene_mapping_table.csv"
fi

echo "复制可视化图片..."

# 1. UMAP对比图（优化后）
if [ -f "$PROJECT_DIR/results/optimized_analysis/optimized_umap_summary.png" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/optimized_umap_summary.png" "$FIGURES_DIR/umap_optimized.png"
    echo "  复制: optimized_umap_summary.png -> umap_optimized.png"
fi

# 2. 标记基因点图
if [ -f "$PROJECT_DIR/results/optimized_analysis/marker_genes_dotplot.png" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/marker_genes_dotplot.png" "$FIGURES_DIR/dotplot_top_markers.png"
    echo "  复制: marker_genes_dotplot.png -> dotplot_top_markers.png"
fi

# 3. 标记基因UMAP表达图
if [ -f "$PROJECT_DIR/results/optimized_analysis/marker_genes_umap.png" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/marker_genes_umap.png" "$FIGURES_DIR/marker_genes_umap.png"
    echo "  复制: marker_genes_umap.png -> marker_genes_umap.png"
fi

# 4. HVG敏感性测试图
if [ -f "$PROJECT_DIR/results/optimized_analysis/hvg_sensitivity_test.png" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/hvg_sensitivity_test.png" "$FIGURES_DIR/hvg_sensitivity_test.png"
    echo "  复制: hvg_sensitivity_test.png"
fi

# 5. PCA肘部图
if [ -f "$PROJECT_DIR/results/optimized_analysis/pca_elbow_plot.png" ]; then
    cp "$PROJECT_DIR/results/optimized_analysis/pca_elbow_plot.png" "$FIGURES_DIR/pca_elbow_plot.png"
    echo "  复制: pca_elbow_plot.png"
fi

echo "创建README文件..."
cat > "$MEMORY_BANK/README.md" << 'EOF'
# 水稻叶片单细胞数据分析 Memory Bank

本目录包含水稻叶片单细胞数据分析（GSE222584）的全部关键产出，包括脚本、报告、结果数据和可视化图片。

## 目录结构

- `scripts/` - 分析脚本（Python）
- `reports/` - 分析报告（Markdown格式）
- `results/` - 关键结果数据（CSV格式）
- `figures/` - 可视化图片（PNG格式）
- `SUMMARY.md` - 文件索引和说明

## 分析概述

本次分析解决了两个核心问题：
1. **基因ID转换**：将Ensembl ID转换为基因符号
2. **过度聚类优化**：从272个聚类减少到12个合理聚类

## 主要发现

1. **基因ID转换成功率**：26.2%（314/1199个Ensembl ID）
2. **聚类优化效果**：减少95.6%的过度聚类
3. **标记基因识别**：为12个聚类识别前10个标记基因
4. **数据质量**：54,237个细胞，2,000个高变基因

## 使用说明

1. 查看 `SUMMARY.md` 了解所有文件的详细说明
2. 运行脚本前确保安装所需依赖（scanpy, pandas, matplotlib等）
3. 数据文件路径可能需要根据实际环境调整

## 相关文件位置

- **原始数据**：`/data5/qiulei/onepiece/data/raw/gse222584/`
- **处理数据**：`/data5/qiulei/onepiece/data/processed/gse222584/processed_data_optimized.h5ad`
- **完整结果**：`/data5/qiulei/onepiece/results/optimized_analysis/`

## 联系信息

如有问题，请参考原始分析记录或联系项目负责人。
EOF

echo "整理完成！"
echo "文件已保存到: $MEMORY_BANK"
echo "请查看 $MEMORY_BANK/SUMMARY.md 获取详细文件说明"