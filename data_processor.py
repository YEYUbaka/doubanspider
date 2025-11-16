# -*- coding: utf-8 -*-
"""
数据处理模块
负责数据的处理、排序和统计
"""

import json
import logging
import pandas as pd
from typing import List, Dict
import config
from utils import ensure_dir


class DataProcessor:
    """数据处理器类"""
    
    def __init__(self):
        """初始化数据处理器"""
        pass
    
    def save_to_csv(self, movies: List[Dict], filepath: str = None):
        """
        保存数据到CSV文件
        
        Args:
            movies: 电影列表
            filepath: 文件路径，默认使用配置文件中的路径
        """
        if filepath is None:
            filepath = config.MOVIES_CSV_FILE
        
        ensure_dir(config.DATA_DIR)
        
        try:
            # 准备数据，将评论列表转换为字符串
            data = []
            for movie in movies:
                row = movie.copy()
                # 将评论列表转换为字符串
                if 'comments' in row:
                    row['comments'] = ' | '.join(row['comments'])
                data.append(row)
            
            df = pd.DataFrame(data)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            logging.info(f"数据已保存到CSV文件: {filepath}")
        except Exception as e:
            logging.error(f"保存CSV文件失败: {str(e)}")
            raise
    
    def save_to_json(self, movies: List[Dict], filepath: str = None):
        """
        保存数据到JSON文件
        
        Args:
            movies: 电影列表
            filepath: 文件路径，默认使用配置文件中的路径
        """
        if filepath is None:
            filepath = config.MOVIES_JSON_FILE
        
        ensure_dir(config.DATA_DIR)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(movies, f, ensure_ascii=False, indent=2)
            logging.info(f"数据已保存到JSON文件: {filepath}")
        except Exception as e:
            logging.error(f"保存JSON文件失败: {str(e)}")
            raise
    
    def sort_by_wish_count(self, movies: List[Dict], ascending: bool = False) -> List[Dict]:
        """
        根据想看人数对电影进行排序
        
        Args:
            movies: 电影列表
            ascending: 是否升序，默认False（降序）
            
        Returns:
            排序后的电影列表
        """
        try:
            sorted_movies = sorted(
                movies, 
                key=lambda x: x.get('wish_count', 0), 
                reverse=not ascending
            )
            logging.info(f"已按想看人数排序（{'降序' if not ascending else '升序'}）")
            return sorted_movies
        except Exception as e:
            logging.error(f"排序失败: {str(e)}")
            return movies
    
    def get_top_movies(self, movies: List[Dict], top_n: int = None) -> List[Dict]:
        """
        获取Top N电影
        
        Args:
            movies: 电影列表
            top_n: 前N部电影，默认使用配置文件中的值
            
        Returns:
            Top N电影列表
        """
        if top_n is None:
            top_n = config.TOP_N_MOVIES
        
        sorted_movies = self.sort_by_wish_count(movies)
        top_movies = sorted_movies[:top_n]
        logging.info(f"获取Top {top_n}电影")
        return top_movies
    
    def load_from_csv(self, filepath: str = None) -> List[Dict]:
        """
        从CSV文件加载数据
        
        Args:
            filepath: 文件路径，默认使用配置文件中的路径
            
        Returns:
            电影列表
        """
        if filepath is None:
            filepath = config.MOVIES_CSV_FILE
        
        try:
            df = pd.read_csv(filepath, encoding='utf-8-sig')
            movies = df.to_dict('records')
            
            # 将评论字符串转换回列表
            for movie in movies:
                if 'comments' in movie and isinstance(movie['comments'], str):
                    movie['comments'] = movie['comments'].split(' | ')
            
            logging.info(f"从CSV文件加载 {len(movies)} 部电影")
            return movies
        except Exception as e:
            logging.error(f"加载CSV文件失败: {str(e)}")
            return []
    
    def load_from_json(self, filepath: str = None) -> List[Dict]:
        """
        从JSON文件加载数据
        
        Args:
            filepath: 文件路径，默认使用配置文件中的路径
            
        Returns:
            电影列表
        """
        if filepath is None:
            filepath = config.MOVIES_JSON_FILE
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                movies = json.load(f)
            logging.info(f"从JSON文件加载 {len(movies)} 部电影")
            return movies
        except Exception as e:
            logging.error(f"加载JSON文件失败: {str(e)}")
            return []

