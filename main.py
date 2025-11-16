# -*- coding: utf-8 -*-
"""
豆瓣电影爬虫主程序
"""

import logging
from utils import setup_logging, ensure_dir
from spider import DoubanMovieSpider
from data_processor import DataProcessor
from visualizer import Visualizer
from wordcloud_generator import WordCloudGenerator
import config


def main():
    """主函数"""
    # 设置日志
    setup_logging(logging.INFO)
    logging.info("=" * 60)
    logging.info("豆瓣电影爬虫程序启动")
    logging.info("=" * 60)
    
    # 确保目录存在
    ensure_dir(config.DATA_DIR)
    ensure_dir(config.IMAGES_DIR)
    ensure_dir(config.FONTS_DIR)
    
    try:
        # 1. 初始化各模块
        logging.info("\n[步骤 1/6] 初始化模块...")
        spider = DoubanMovieSpider()
        processor = DataProcessor()
        visualizer = Visualizer()
        wordcloud_gen = WordCloudGenerator()
        
        # 2. 爬取电影列表
        logging.info("\n[步骤 2/6] 爬取电影列表...")
        movies = spider.crawl_movies()
        
        if not movies:
            logging.error("未爬取到任何电影数据，程序退出")
            return
        
        logging.info(f"成功爬取 {len(movies)} 部电影的基本信息")
        
        # 3. 爬取电影评论
        logging.info("\n[步骤 3/6] 爬取电影评论...")
        movies = spider.crawl_all_comments(movies)
        
        # 统计评论数量
        total_comments = sum(len(movie.get('comments', [])) for movie in movies)
        logging.info(f"共爬取 {total_comments} 条评论")
        
        # 4. 保存原始数据
        logging.info("\n[步骤 4/6] 保存原始数据...")
        processor.save_to_csv(movies)
        processor.save_to_json(movies)
        
        # 5. 数据处理和可视化
        logging.info("\n[步骤 5/6] 数据处理和可视化...")
        sorted_movies = processor.sort_by_wish_count(movies)
        top_movies = processor.get_top_movies(sorted_movies)
        
        # 显示Top 5电影信息
        logging.info("\n想看人数Top 5电影:")
        for i, movie in enumerate(top_movies, 1):
            logging.info(f"  {i}. {movie.get('movie_name')}: {movie.get('wish_count')} 人想看")
        
        # 生成可视化图表
        visualizer.plot_top_movies(sorted_movies)
        
        # 6. 评论分析和词云生成
        logging.info("\n[步骤 6/6] 评论分析和词云生成...")
        wordcloud_gen.process_comments(movies)
        
        # 输出统计信息
        logging.info("\n" + "=" * 60)
        logging.info("程序执行完成！")
        logging.info("=" * 60)
        logging.info(f"输出文件:")
        logging.info(f"  - 数据文件: {config.MOVIES_CSV_FILE}, {config.MOVIES_JSON_FILE}")
        logging.info(f"  - 可视化图表: {config.TOP5_IMAGE_FILE}")
        logging.info(f"  - 词云图: {config.WORDCLOUD_IMAGE_FILE}")
        logging.info(f"  - 词频统计: {config.WORD_STATISTICS_FILE}")
        logging.info("=" * 60)
        
    except KeyboardInterrupt:
        logging.warning("\n用户中断程序")
    except Exception as e:
        logging.error(f"\n程序执行出错: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

