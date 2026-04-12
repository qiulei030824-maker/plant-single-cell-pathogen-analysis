#!/usr/bin/env python3
"""
GSE222584数据完整优化分析脚本（修复版 + 最佳参数）
基于五个理想脚本（01_check_gene_ids.py, 02_convert_gene_ids.py, 03_umap_diagnosis.py, 
04_fix_umap_clustering.py, 05_marker_gene_analysis.py）复用其逻辑
修复了以下问题：
1. 并行计算pickle错误（改为串行计算）
2. 标记基因文件解析错误
3. 条件标签不匹配问题
4. 直接使用最佳参数：resolution=0.4, n_neighbors=15
"""

import scanpy as sc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import warnings
import re
import json
import logging
from pathlib import Path
from scipy import stats
from sklearn.metrics import silhouette_score
import gseapy as gp
from statsmodels.stats.multitest import multipletests
import multiprocessing

# 设置随机种子
np.random.seed(42)
sc.settings.verbosity = 1
sc.settings.set_figure_params(dpi=300, facecolor='white')
warnings.filterwarnings('ignore')

# 设置日志
output_dir = '/data5/qiulei/onepiece/results/gse222584_optimized_bestparams'
os.makedirs(output_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'{output_dir}/analysis.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 设置绘图样式
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# ============================================================================
# 第一部分：数据加载和预处理
# ============================================================================

def load_and_preprocess_data():
    """加载数据并进行预处理"""
    logger.info("=" * 80)
    logger.info("步骤1: 加载数据")
    logger.info("=" * 80)
    
    # 加载数据
    data_path = '/data5/qiulei/onepiece/data/processed/gse222584/processed_data_optimized.h5ad'
    logger.info(f"加载数据: {data_path}")
    adata = sc.read_h5ad(data_path)
    logger.info(f"加载数据: {adata.n_obs} 个细胞, {adata.n_vars} 个基因")
    
    # 检查基因名格式
    gene_names = adata.var_names.tolist()
    ensembl_pattern = re.compile(r'^LOC_Os\d+g\d+')
    if any(ensembl_pattern.match(g) for g in gene_names[:10]):
        logger.info("基因名格式推测: Ensembl ID")
        # 转换基因ID为基因符号
        logger.info("转换基因ID为基因符号...")
        gene_mapping = load_gene_mapping()
        
        # 创建基因符号列
        gene_symbols = []
        for gene in adata.var_names:
            if gene in gene_mapping:
                gene_symbols.append(gene_mapping[gene])
            else:
                gene_symbols.append(gene)
        
        adata.var['gene_symbol'] = gene_symbols
        logger.info(f"基因ID转换统计: 总基因数: {adata.n_vars}, 成功转换: {len([g for g in gene_symbols if g != adata.var_names[0]])}")
    else:
        logger.info("基因名格式: 基因符号")
        adata.var['gene_symbol'] = adata.var_names
    
    # 修复条件标签：基于sample列创建正确的condition列
    logger.info("修复条件标签...")
    if 'sample' in adata.obs.columns:
        # 从sample列提取条件
        def extract_condition(sample):
            if sample.startswith('CK'):
                return 'Control'
            elif sample.startswith('RGSV'):
                return 'RGSV'
            elif sample.startswith('RRSV'):
                return 'RRSV'
            else:
                return 'Unknown'
        
        adata.obs['condition'] = adata.obs['sample'].apply(extract_condition)
        logger.info(f"修复后的条件: {adata.obs['condition'].unique().tolist()}")
    else:
        logger.warning("未找到sample列，使用原始condition列")
        if 'condition' not in adata.obs.columns:
            adata.obs['condition'] = 'Unknown'
    
    return adata

def load_gene_mapping():
    """加载基因ID映射表"""
    gene_mapping = {}
    mapping_files = [
        '/data5/qiulei/onepiece/memory-bank/rice_gene_id_mapping.txt',
        '/data5/qiulei/onepiece/memory-bank/rice_gene_symbols.txt'
    ]
    
    for mapping_file in mapping_files:
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    for line in f:
                        parts = line.strip().split('\t')
                        if len(parts) >= 2:
                            gene_id = parts[0].strip()
                            gene_symbol = parts[1].strip()
                            gene_mapping[gene_id] = gene_symbol
                logger.info(f"从 {mapping_file} 加载了 {len(gene_mapping)} 个基因映射")
                break
            except Exception as e:
                logger.warning(f"加载基因映射文件失败 {mapping_file}: {e}")
    
    return gene_mapping

# ============================================================================
# 第二部分：使用最佳参数进行聚类
# ============================================================================

def apply_best_parameters(adata):
    """直接使用最佳参数进行聚类"""
    logger.info("=" * 80)
    logger.info("步骤2: 使用最佳参数进行聚类")
    logger.info("=" * 80)
    
    # 最佳参数：resolution=0.4, n_neighbors=15
    best_resolution = 0.4
    best_n_neighbors = 15
    
    logger.info(f"使用最佳参数: resolution={best_resolution}, n_neighbors={best_n_neighbors}")
    
    # 计算邻居图
    sc.pp.neighbors(adata, n_neighbors=best_n_neighbors, n_pcs=30)
    
    # Leiden聚类
    sc.tl.leiden(adata, resolution=best_resolution, key_added='leiden_optimized')
    
    # 计算轮廓系数
    if adata.obsm.get('X_pca') is not None:
        n_clusters = len(adata.obs['leiden_optimized'].unique())
        if n_clusters > 1:
            silhouette_avg = silhouette_score(
                adata.obsm['X_pca'][:, :30],
                adata.obs['leiden_optimized'].astype('category').cat.codes
            )
        else:
            silhouette_avg = -1
    else:
        silhouette_avg = -1
    
    logger.info(f"聚类结果: {n_clusters} 个聚类, 轮廓系数: {silhouette_avg:.3f}")
    
    return adata, (best_resolution, best_n_neighbors), silhouette_avg

# ============================================================================
# 第三部分：细胞类型注释（修复版）
# ============================================================================

def load_marker_genes():
    """加载标记基因字典 - 改进版，处理粗体格式"""
    marker_files = [
        '/data5/qiulei/onepiece/memory-bank/rice_cell_type_marker_genes_dictionary.md',
        '/data5/qiulei/onepiece/memory-bank/rice_marker_genes_final.md'
    ]
    
    cell_type_markers = {}
    disease_markers = {}
    
    for marker_file in marker_files:
        if not os.path.exists(marker_file):
            logger.warning(f"标记基因文件不存在: {marker_file}")
            continue
        
        try:
            with open(marker_file, 'r') as f:
                content = f.read()
            
            # 处理细胞类型标记基因字典
            if marker_file.endswith('dictionary.md'):
                current_cell_type = None
                for line in content.split('\n'):
                    # 查找细胞类型标题
                    if line.startswith('## '):
                        # 匹配格式：## 1. 伴胞 (Companion Cells)
                        cell_type_match = re.search(r'## \d+\.\s+([^(]+)', line)
                        if cell_type_match:
                            current_cell_type = cell_type_match.group(1).strip()
                            if current_cell_type not in cell_type_markers:
                                cell_type_markers[current_cell_type] = []
                        else:
                            # 尝试匹配其他格式
                            cell_type_match = re.search(r'## ([^(]+)', line)
                            if cell_type_match:
                                current_cell_type = cell_type_match.group(1).strip()
                                if current_cell_type not in cell_type_markers:
                                    cell_type_markers[current_cell_type] = []
                    
                    # 查找基因符号（表格格式，处理粗体**gene**格式）
                    elif line.startswith('|') and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            gene_cell = parts[2].strip()
                            # 提取基因符号，去除粗体标记** **
                            gene_symbol = re.sub(r'\*\*(.+?)\*\*', r'\1', gene_cell)
                            if gene_symbol and gene_symbol != 'Gene Symbol' and gene_symbol != '---' and not gene_symbol.startswith('**'):
                                if current_cell_type:
                                    cell_type_markers[current_cell_type].append(gene_symbol)
            
            # 处理病虫害标记基因
            elif marker_file.endswith('final.md'):
                current_disease = None
                for line in content.split('\n'):
                    # 查找病虫害标题
                    if line.startswith('## '):
                        disease_match = re.search(r'## \d+\.\s+([^(]+)', line)
                        if disease_match:
                            current_disease = disease_match.group(1).strip()
                            if current_disease not in disease_markers:
                                disease_markers[current_disease] = []
                        else:
                            disease_match = re.search(r'## ([^(]+)', line)
                            if disease_match:
                                current_disease = disease_match.group(1).strip()
                                if current_disease not in disease_markers:
                                    disease_markers[current_disease] = []
                    
                    # 查找基因符号（表格格式）
                    elif line.startswith('|') and '|' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            gene_cell = parts[2].strip()
                            # 提取基因符号，去除粗体标记
                            gene_symbol = re.sub(r'\*\*(.+?)\*\*', r'\1', gene_cell)
                            if gene_symbol and gene_symbol != 'Gene Symbol' and gene_symbol != '---' and not gene_symbol.startswith('**'):
                                if current_disease:
                                    disease_markers[current_disease].append(gene_symbol)
        
        except Exception as e:
            logger.error(f"解析标记基因文件失败 {marker_file}: {e}")
    
    logger.info(f"加载了 {len(cell_type_markers)} 个细胞类型的标记基因")
    for cell_type, markers in cell_type_markers.items():
        logger.info(f"  {cell_type}: {len(markers)} 个标记基因")
    
    logger.info(f"加载了 {len(disease_markers)} 个病虫害的标记基因")
    
    return cell_type_markers, disease_markers

def annotate_by_literature(cluster_markers):
    """基于文献知识进行细胞类型注释"""
    # 基于已知的top markers进行注释
    literature_annotations = {
        # 防御响应细胞：包含PR蛋白、R基因等
        'defense_response': {
            'keywords': ['PR10', 'PR1', 'PR5', 'RPR', 'NBS-LRR', 'RLK', 'RLP'],
            'markers': ['OsPR10a', 'OsPR10b', 'RPR10b', 'RPR10a']
        },
        # 表皮细胞：包含脂质转移蛋白、角质合成相关基因
        'epidermal': {
            'keywords': ['LTP', 'CER', 'CUT', 'WAX', 'BDG', 'GPAT'],
            'markers': ['LTP1', 'LTP2', 'LTP3', 'OsLTP1.14', 'LRT2']
        },
        # 水分运输细胞：包含水通道蛋白
        'water_transport': {
            'keywords': ['PIP', 'TIP', 'NIP', 'SIP', 'AQP'],
            'markers': ['OsPIP2-2', 'OsPIP1a', 'OsTIP1-1', 'OsTIP2-1']
        },
        # 应激响应细胞：包含热激蛋白、氧化应激相关基因
        'stress_response': {
            'keywords': ['HSP', 'HSP70', 'HSP90', 'HSP100', 'LEA', 'DREB'],
            'markers': ['OsHSP82A', 'OsHsp17.3', 'OsHsp24.1', 'OsHSP18.0-CI']
        },
        # 解毒细胞：包含谷胱甘肽S-转移酶、细胞色素P450等
        'detoxification': {
            'keywords': ['GST', 'CYP', 'P450', 'UGT', 'ABC'],
            'markers': ['OsGSTF14', 'OsGSTF15', 'OsABCG1', 'OsCYP']
        },
        # 代谢细胞：包含糖代谢、能量代谢相关基因
        'metabolic': {
            'keywords': ['ADH', 'PDC', 'ALD', 'GAPDH', 'PGK', 'ENO'],
            'markers': ['ADH1', 'pdc1', 'AldC-1', 'OsADH']
        },
        # 转运细胞：包含转运蛋白、载体蛋白
        'transport': {
            'keywords': ['SUC', 'SWEET', 'MST', 'NRT', 'AMT', 'POT'],
            'markers': ['OsMST3', 'OsSUC2', 'OsSWEET']
        },
        # 细胞壁代谢细胞：包含细胞壁合成、修饰相关基因
        'cell_wall': {
            'keywords': ['XTH', 'XET', 'EXP', 'EXT', 'AGP', 'CESA'],
            'markers': ['riceXIP', 'OsAGP4', 'OsAGP14', 'OsXTH']
        },
        # 信号传导细胞：包含激酶、磷酸酶、受体等
        'signaling': {
            'keywords': ['RLK', 'CDPK', 'MAPK', 'PP2C', 'PTP', 'RLCK'],
            'markers': ['OsRLK', 'OsCDPK', 'OsMAPK']
        },
        # 转录调控细胞：包含转录因子
        'transcriptional_regulation': {
            'keywords': ['MYB', 'NAC', 'WRKY', 'bZIP', 'ERF', 'ARF'],
            'markers': ['OsERF#068', 'OsMYB', 'OsWRKY', 'OsNAC']
        }
    }
    
    cluster_annotations = {}
    
    for cluster, markers in cluster_markers.items():
        best_cell_type = 'Unknown'
        best_score = 0
        
        for cell_type, info in literature_annotations.items():
            score = 0
            
            # 检查关键词匹配
            for marker in markers[:10]:  # 只检查前10个标记基因
                marker_lower = marker.lower()
                for keyword in info['keywords']:
                    if keyword.lower() in marker_lower:
                        score += 2
                
                # 检查具体标记基因匹配
                if marker in info['markers']:
                    score += 3
            
            if score > best_score:
                best_score = score
                best_cell_type = cell_type
        
        # 如果分数太低，保持为Unknown
        if best_score < 2:
            best_cell_type = 'Unknown'
        
        cluster_annotations[cluster] = best_cell_type
    
    return cluster_annotations

def annotate_celltypes(adata):
    """细胞类型注释 - 改进版，结合标记基因和文献知识"""
    logger.info("=" * 80)
    logger.info("步骤3: 细胞类型注释")
    logger.info("=" * 80)
    
    # 加载标记基因
    cell_type_markers, disease_markers = load_marker_genes()
    
    # 计算每个聚类的标记基因
    sc.tl.rank_genes_groups(adata, 'leiden_optimized', method='wilcoxon')
    
    # 获取每个聚类的top标记基因
    n_genes = 50
    cluster_markers = {}
    
    for cluster in adata.obs['leiden_optimized'].unique():
        try:
            # 获取该聚类的top标记