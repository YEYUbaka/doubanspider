# -*- coding: utf-8 -*-
"""
配置文件
包含项目的所有配置信息
"""

# Python 解释器路径
PYTHON_INTERPRETER = r"D:\Program Files\python3.9\python.exe"

# 城市配置
CITY = "wuhan"  # 武汉

# 豆瓣电影URL
DOUBAN_MOVIE_BASE_URL = "https://movie.douban.com"
DOUBAN_MOVIE_NOWPLAYING_URL = f"https://movie.douban.com/cinema/nowplaying/{CITY}/"
DOUBAN_MOVIE_COMMENTS_URL = "https://movie.douban.com/subject/{movie_id}/comments"

# 请求头配置 (桌面端, 用于爬取电影列表页面)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Rexxar API 请求头 (移动端, 用于爬取电影评论)
# 豆瓣 Rexxar API 是移动端内部接口, 返回 JSON 数据
# 相比桌面端 HTML 页面, 反爬虫策略更宽松, 无需 Selenium
REXXAR_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.165 Mobile Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
}

# Rexxar API 基础 URL
REXXAR_API_BASE_URL = "https://m.douban.com/rexxar/api/v2"
# 请求配置
REQUEST_DELAY = 5  # 请求延迟（秒，用于页面爬取）
REXXAR_API_DELAY = 2  # Rexxar API 请求间隔（秒，JSON API 比 HTML 页面轻量）
REQUEST_TIMEOUT = 15  # 请求超时（秒）
MAX_RETRIES = 3  # 最大重试次数

# 评论爬取配置
COMMENTS_PER_MOVIE = 30  # 每部电影爬取的评论数量
COMMENTS_PAGE_SIZE = 20  # 每页评论数量

# 文件路径配置
DATA_DIR = "data"
IMAGES_DIR = "images"
FONTS_DIR = "fonts"

# 输出文件配置
MOVIES_CSV_FILE = f"{DATA_DIR}/movies.csv"
MOVIES_JSON_FILE = f"{DATA_DIR}/movies.json"
TOP5_IMAGE_FILE = f"{IMAGES_DIR}/top5_movies.png"
WORDCLOUD_IMAGE_FILE = f"{IMAGES_DIR}/wordcloud.png"
WORD_STATISTICS_FILE = f"{DATA_DIR}/word_statistics.txt"

# 词云配置
WORDCLOUD_WIDTH = 800
WORDCLOUD_HEIGHT = 400
WORDCLOUD_FONT_PATH = "simhei.ttf"  # 中文字体路径，如果系统没有，需要下载
WORDCLOUD_BACKGROUND_COLOR = "white"

# 可视化配置
TOP_N_MOVIES = 5  # 显示前N部电影
CHART_TITLE = "想看人数Top 5电影"
CHART_XLABEL = "电影名称"
CHART_YLABEL = "想看人数"

# 词频统计配置
TOP_WORDS_COUNT = 20  # 统计高频词汇数量

