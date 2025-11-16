# -*- coding: utf-8 -*-
"""
可视化模块
负责生成数据可视化图表
"""

import logging
import matplotlib.pyplot as plt
import matplotlib
from typing import List, Dict
import config
from utils import ensure_dir

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class Visualizer:
    """可视化类"""
    
    def __init__(self):
        """初始化可视化器"""
        pass
    
    def plot_top_movies(self, movies: List[Dict], top_n: int = None, filepath: str = None):
        """
        绘制Top N电影柱状图
        
        Args:
            movies: 电影列表（已排序）
            top_n: 显示前N部电影，默认使用配置文件中的值
            filepath: 保存路径，默认使用配置文件中的路径
        """
        if top_n is None:
            top_n = config.TOP_N_MOVIES
        
        if filepath is None:
            filepath = config.TOP5_IMAGE_FILE
        
        ensure_dir(config.IMAGES_DIR)
        
        try:
            # 获取Top N电影
            top_movies = movies[:top_n]
            
            if not top_movies:
                logging.warning("没有电影数据可绘制")
                return
            
            # 提取数据
            movie_names = [movie.get('movie_name', '未知') for movie in top_movies]
            wish_counts = [movie.get('wish_count', 0) for movie in top_movies]
            
            # 处理电影名称过长的情况
            max_name_length = 15
            movie_names_display = []
            for name in movie_names:
                if len(name) > max_name_length:
                    movie_names_display.append(name[:max_name_length] + '...')
                else:
                    movie_names_display.append(name)
            
            # 创建图表
            plt.figure(figsize=(12, 6))
            bars = plt.bar(range(len(movie_names_display)), wish_counts, 
                          color='steelblue', alpha=0.8, edgecolor='navy', linewidth=1.2)
            
            # 在柱状图上添加数值标签
            for i, (bar, count) in enumerate(zip(bars, wish_counts)):
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{count}',
                        ha='center', va='bottom', fontsize=10, fontweight='bold')
            
            # 设置标题和标签
            plt.title(config.CHART_TITLE, fontsize=16, fontweight='bold', pad=20)
            plt.xlabel(config.CHART_XLABEL, fontsize=12)
            plt.ylabel(config.CHART_YLABEL, fontsize=12)
            
            # 设置x轴刻度
            plt.xticks(range(len(movie_names_display)), movie_names_display, 
                      rotation=45, ha='right', fontsize=10)
            
            # 设置y轴从0开始
            plt.ylim(bottom=0)
            
            # 添加网格线
            plt.grid(axis='y', alpha=0.3, linestyle='--')
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图片
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            logging.info(f"图表已保存到: {filepath}")
            
            # 显示图表（可选）
            # plt.show()
            
            plt.close()
            
        except Exception as e:
            logging.error(f"生成图表失败: {str(e)}")
            raise

