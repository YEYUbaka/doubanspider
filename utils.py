# -*- coding: utf-8 -*-
"""
工具函数模块
提供通用的工具函数
"""

import os
import time
import logging
from typing import Optional


def setup_logging(log_level=logging.INFO):
    """
    配置日志系统
    
    Args:
        log_level: 日志级别，默认为INFO
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def ensure_dir(directory: str):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"创建目录: {directory}")


def safe_request(func):
    """
    请求装饰器，添加异常处理和重试机制
    
    Args:
        func: 请求函数
    """
    def wrapper(*args, **kwargs):
        from config import MAX_RETRIES
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.warning(f"请求失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    logging.error(f"请求最终失败: {str(e)}")
                    raise
                time.sleep(2 ** attempt)  # 指数退避
        return None
    return wrapper


def clean_text(text: str) -> str:
    """
    清理文本，去除多余空白字符
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
    return " ".join(text.split())


def extract_number(text: str) -> int:
    """
    从文本中提取数字
    
    Args:
        text: 包含数字的文本
        
    Returns:
        提取的数字，如果提取失败返回0
    """
    if not text:
        return 0
    import re
    numbers = re.findall(r'\d+', text.replace(',', ''))
    if numbers:
        return int(numbers[0])
    return 0


def get_movie_id_from_url(url: str) -> Optional[str]:
    """
    从豆瓣电影URL中提取电影ID
    
    Args:
        url: 豆瓣电影URL
        
    Returns:
        电影ID，如果提取失败返回None
    """
    if not url:
        return None
    import re
    match = re.search(r'/subject/(\d+)/', url)
    if match:
        return match.group(1)
    return None

