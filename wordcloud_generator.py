# -*- coding: utf-8 -*-
"""
词云生成模块
负责评论分析、词频统计和词云图生成
"""

import os
import logging
import jieba
import jieba.analyse
from collections import Counter
from typing import List, Dict, Tuple
from wordcloud import WordCloud
import config
from utils import ensure_dir


class WordCloudGenerator:
    """词云生成器类"""
    
    def __init__(self, stopwords_file: str = None):
        """
        初始化词云生成器
        
        Args:
            stopwords_file: 停用词文件路径
        """
        self.stopwords = set()
        if stopwords_file and os.path.exists(stopwords_file):
            self.load_stopwords(stopwords_file)
        else:
            # 使用默认停用词
            self._init_default_stopwords()
    
    def _init_default_stopwords(self):
        """初始化默认停用词"""
        default_stopwords = {
            # 常用停用词
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
            '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
            '自己', '这', '这个', '这样', '那样', '那么',
            '非常', '特别', '真的', '还是', '可以', '应该', '觉得', '感觉', '但是',
            '不过', '虽然', '如果', '因为', '所以', '然后', '还有', '就是', '只是',
            '什么', '怎么', '为什么', '多少', '哪个', '哪些',
            '豆瓣', '评分', '评论', '用户', '网友', '大家', '我们', '你们', '他们',
            '啊', '呢', '吧', '吗', '呀', '哦', '嗯', '哈哈', '呵呵',
            # 电影相关停用词
            '电影', '影片', '片子', '这部', '剧情', '演员', '导演', '演技', '画面', '音乐', '特效',
            '好看', '不错', '一般', '还行', '不好', '难看', '垃圾', '烂片', '好片', '经典',
            '推荐', '值得', '值得看', '值得一看', '值得推荐', '不推荐', '不推荐看',
        }
        self.stopwords.update(default_stopwords)
    
    def load_stopwords(self, filepath: str):
        """
        从文件加载停用词
        
        Args:
            filepath: 停用词文件路径
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.stopwords.add(word)
            logging.info(f"从文件加载 {len(self.stopwords)} 个停用词")
        except Exception as e:
            logging.warning(f"加载停用词文件失败: {str(e)}")
    
    def extract_comments(self, movies: List[Dict]) -> str:
        """
        从电影列表中提取所有评论
        
        Args:
            movies: 电影列表
            
        Returns:
            合并后的评论文本
        """
        all_comments = []
        for movie in movies:
            comments = movie.get('comments', [])
            all_comments.extend(comments)
        
        text = ' '.join(all_comments)
        logging.info(f"提取了 {len(all_comments)} 条评论，总字符数: {len(text)}")
        return text
    
    def segment_text(self, text: str) -> List[str]:
        """
        对文本进行分词
        
        Args:
            text: 原始文本
            
        Returns:
            分词后的词列表
        """
        # 使用jieba分词
        words = jieba.cut(text, cut_all=False)
        
        # 过滤停用词和单字符
        filtered_words = []
        for word in words:
            word = word.strip()
            if (len(word) > 1 and 
                word not in self.stopwords and 
                not word.isspace() and
                not word.isdigit()):
                filtered_words.append(word)
        
        logging.info(f"分词完成，共 {len(filtered_words)} 个有效词汇")
        return filtered_words
    
    def count_word_frequency(self, words: List[str]) -> Counter:
        """
        统计词频
        
        Args:
            words: 词列表
            
        Returns:
            词频统计Counter对象
        """
        word_freq = Counter(words)
        logging.info(f"统计完成，共 {len(word_freq)} 个不同词汇")
        return word_freq
    
    def get_top_words(self, word_freq: Counter, top_n: int = None) -> List[Tuple[str, int]]:
        """
        获取高频词汇
        
        Args:
            word_freq: 词频统计Counter对象
            top_n: 前N个高频词，默认使用配置文件中的值
            
        Returns:
            (词汇, 频次)元组列表
        """
        if top_n is None:
            top_n = config.TOP_WORDS_COUNT
        
        top_words = word_freq.most_common(top_n)
        return top_words
    
    def get_low_frequency_words(self, word_freq: Counter) -> List[Tuple[str, int]]:
        """
        获取低频词汇（出现1次的词汇）
        
        Args:
            word_freq: 词频统计Counter对象
            
        Returns:
            (词汇, 频次)元组列表
        """
        low_freq_words = [(word, count) for word, count in word_freq.items() if count == 1]
        logging.info(f"找到 {len(low_freq_words)} 个低频词汇（出现1次）")
        return low_freq_words
    
    def save_word_statistics(self, word_freq: Counter, filepath: str = None):
        """
        保存词频统计结果
        
        Args:
            word_freq: 词频统计Counter对象
            filepath: 保存路径，默认使用配置文件中的路径
        """
        if filepath is None:
            filepath = config.WORD_STATISTICS_FILE
        
        ensure_dir(config.DATA_DIR)
        
        try:
            top_words = self.get_top_words(word_freq)
            low_freq_words = self.get_low_frequency_words(word_freq)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("词频统计报告\n")
                f.write("=" * 50 + "\n\n")
                
                f.write(f"总词汇数: {len(word_freq)}\n")
                f.write(f"总词频: {sum(word_freq.values())}\n\n")
                
                f.write("-" * 50 + "\n")
                f.write(f"高频词汇 Top {config.TOP_WORDS_COUNT}:\n")
                f.write("-" * 50 + "\n")
                for i, (word, count) in enumerate(top_words, 1):
                    f.write(f"{i:2d}. {word:15s} : {count:5d} 次\n")
                
                f.write("\n" + "-" * 50 + "\n")
                f.write(f"低频词汇（出现1次）: {len(low_freq_words)} 个\n")
                f.write("-" * 50 + "\n")
                # 只显示前100个低频词，避免文件过大
                for i, (word, count) in enumerate(low_freq_words[:100], 1):
                    f.write(f"{word:15s} : {count:5d} 次\n")
                if len(low_freq_words) > 100:
                    f.write(f"... 还有 {len(low_freq_words) - 100} 个低频词\n")
            
            logging.info(f"词频统计已保存到: {filepath}")
        except Exception as e:
            logging.error(f"保存词频统计失败: {str(e)}")
            raise
    
    def generate_wordcloud(self, word_freq: Counter, filepath: str = None):
        """
        生成词云图
        
        Args:
            word_freq: 词频统计Counter对象
            filepath: 保存路径，默认使用配置文件中的路径
        """
        if filepath is None:
            filepath = config.WORDCLOUD_IMAGE_FILE
        
        ensure_dir(config.IMAGES_DIR)
        
        try:
            # 准备词频字典
            word_dict = dict(word_freq)
            
            if not word_dict:
                logging.warning("没有词汇数据，无法生成词云")
                return
            
            # 配置词云参数
            wordcloud_config = {
                'width': config.WORDCLOUD_WIDTH,
                'height': config.WORDCLOUD_HEIGHT,
                'background_color': config.WORDCLOUD_BACKGROUND_COLOR,
                'max_words': 200,
                'relative_scaling': 0.5,
                'colormap': 'viridis',
            }
            
            # 尝试使用中文字体
            font_path = config.WORDCLOUD_FONT_PATH
            if os.path.exists(font_path):
                wordcloud_config['font_path'] = font_path
            else:
                # 尝试系统字体路径
                system_fonts = [
                    'C:/Windows/Fonts/simhei.ttf',
                    'C:/Windows/Fonts/simsun.ttc',
                    'C:/Windows/Fonts/msyh.ttc',
                ]
                for font in system_fonts:
                    if os.path.exists(font):
                        wordcloud_config['font_path'] = font
                        break
                else:
                    logging.warning("未找到中文字体，词云可能无法正确显示中文")
            
            # 生成词云
            wordcloud = WordCloud(**wordcloud_config)
            wordcloud.generate_from_frequencies(word_dict)
            
            # 保存图片
            wordcloud.to_file(filepath)
            logging.info(f"词云图已保存到: {filepath}")
            
        except Exception as e:
            logging.error(f"生成词云失败: {str(e)}")
            raise
    
    def process_comments(self, movies: List[Dict], stopwords_file: str = None):
        """
        处理评论，生成词频统计和词云
        
        Args:
            movies: 电影列表
            stopwords_file: 停用词文件路径
        """
        logging.info("开始处理评论数据...")
        
        # 提取评论
        text = self.extract_comments(movies)
        
        if not text or len(text.strip()) < 10:
            logging.warning("评论数据不足，无法进行分析")
            return
        
        # 分词
        words = self.segment_text(text)
        
        if not words:
            logging.warning("分词结果为空")
            return
        
        # 统计词频
        word_freq = self.count_word_frequency(words)
        
        # 保存统计结果
        self.save_word_statistics(word_freq)
        
        # 生成词云
        self.generate_wordcloud(word_freq)
        
        logging.info("评论处理完成")

