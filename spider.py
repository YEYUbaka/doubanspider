# -*- coding: utf-8 -*-
"""
爬虫模块
负责爬取豆瓣电影信息和评论
"""

import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from utils import safe_request, clean_text, extract_number, get_movie_id_from_url
import config


class DoubanMovieSpider:
    """豆瓣电影爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)
        self.movies = []
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        获取网页内容并解析
        
        Args:
            url: 目标URL
            
        Returns:
            BeautifulSoup对象，失败返回None
        """
        try:
            logging.info(f"正在请求: {url}")
            
            # 修改请求头，移除br压缩，使用gzip
            headers = config.HEADERS.copy()
            headers['Accept-Encoding'] = 'gzip, deflate'
            
            response = self.session.get(
                url, 
                headers=headers,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            # 自动检测编码
            if response.encoding is None or response.encoding == 'ISO-8859-1':
                response.encoding = response.apparent_encoding or 'utf-8'
            
            # 调试：临时保存HTML内容用于分析
            try:
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logging.info(f"页面内容已保存到 debug_page.html，长度: {len(response.text)} 字符")
                # 检查是否包含常见的关键词
                if '豆瓣' in response.text or 'movie' in response.text.lower():
                    logging.info("页面内容看起来正常")
                else:
                    logging.warning("页面内容可能异常，可能遇到反爬虫")
            except Exception as e:
                logging.warning(f"保存调试文件失败: {str(e)}")
            
            # 检查是否被重定向或返回错误页面
            if len(response.text) < 1000:
                logging.warning(f"响应内容过短，可能被重定向或遇到反爬虫: {len(response.text)} 字符")
                logging.warning(f"响应状态码: {response.status_code}")
                logging.warning(f"响应URL: {response.url}")
                logging.warning(f"响应内容预览: {response.text[:500]}")
            
            soup = BeautifulSoup(response.text, 'lxml')
            time.sleep(config.REQUEST_DELAY)
            return soup
        except Exception as e:
            logging.error(f"请求失败 {url}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())
            return None
    
    def parse_movie_list(self, soup: BeautifulSoup) -> List[Dict]:
        """
        解析电影列表页面
        
        Args:
            soup: BeautifulSoup对象
            
        Returns:
            电影信息列表
        """
        movies = []
        try:
            # 尝试多种选择器来查找电影项
            movie_items = []
            
            # 方法1: 查找 li.list-item
            movie_items = soup.find_all('li', class_='list-item')
            
            # 方法2: 查找 ul#showing-soon 下的 li
            if not movie_items:
                ul = soup.find('ul', id='showing-soon') or soup.find('ul', class_='lists')
                if ul:
                    movie_items = ul.find_all('li')
            
            # 方法3: 查找所有包含电影链接的 li
            if not movie_items:
                all_li = soup.find_all('li')
                for li in all_li:
                    if li.find('a', href=lambda x: x and '/subject/' in str(x)):
                        movie_items.append(li)
            
            # 方法4: 查找 div.item
            if not movie_items:
                movie_items = soup.find_all('div', class_='item')
            
            # 方法5: 直接查找包含 /subject/ 的链接
            if not movie_items:
                links = soup.find_all('a', href=lambda x: x and '/subject/' in str(x))
                for link in links:
                    # 创建一个包装元素
                    parent = link.find_parent(['li', 'div'])
                    if parent and parent not in movie_items:
                        movie_items.append(parent)
            
            logging.info(f"找到 {len(movie_items)} 个可能的电影项")
            
            for item in movie_items:
                try:
                    movie = self._parse_movie_item(item)
                    if movie and movie.get('movie_name'):
                        movies.append(movie)
                        logging.info(f"解析电影: {movie['movie_name']}")
                except Exception as e:
                    logging.warning(f"解析电影项失败: {str(e)}")
                    continue
                    
        except Exception as e:
            logging.error(f"解析电影列表失败: {str(e)}")
            import traceback
            logging.debug(traceback.format_exc())
            
        return movies
    
    def _parse_movie_item(self, item) -> Optional[Dict]:
        """
        解析单个电影项
        
        Args:
            item: BeautifulSoup元素
            
        Returns:
            电影信息字典，失败返回None
        """
        try:
            movie = {}
            
            # 方法1: 优先从data-title属性获取电影名称
            movie['movie_name'] = clean_text(item.get('data-title', ''))
            
            # 方法2: 查找包含 /subject/ 的链接获取URL和名称
            title_elem = None
            links = item.find_all('a', href=lambda x: x and '/subject/' in str(x))
            if links:
                title_elem = links[0]
                # 如果data-title为空，从链接文本获取
                if not movie['movie_name']:
                    movie['movie_name'] = clean_text(title_elem.get_text())
            else:
                # 方法3: 查找 ticket-btn 类
                title_elem = item.find('a', class_='ticket-btn')
                if title_elem and not movie['movie_name']:
                    movie['movie_name'] = clean_text(title_elem.get_text())
            
            # 获取电影URL
            if title_elem:
                href = title_elem.get('href', '')
                if href:
                    if href.startswith('http'):
                        movie['movie_url'] = href
                    else:
                        movie['movie_url'] = config.DOUBAN_MOVIE_BASE_URL + href
                else:
                    movie['movie_url'] = ''
            else:
                # 尝试从data属性获取URL
                href = item.get('data-href', '') or item.get('data-url', '')
                if href:
                    if href.startswith('http'):
                        movie['movie_url'] = href
                    else:
                        movie['movie_url'] = config.DOUBAN_MOVIE_BASE_URL + href
                else:
                    movie['movie_url'] = ''
            
            # 如果还是没有电影名，尝试从标题标签获取
            if not movie.get('movie_name'):
                title_tag = item.find('h3') or item.find('h2') or item.find('span', class_='title') or item.find('li', class_='stitle')
                if title_tag:
                    link_in_tag = title_tag.find('a')
                    if link_in_tag:
                        movie['movie_name'] = clean_text(link_in_tag.get_text())
                    else:
                        movie['movie_name'] = clean_text(title_tag.get_text())
            
            if not movie.get('movie_name'):
                logging.debug(f"无法提取电影名称，item: {item.get('class')}")
                return None
            
            # 上映时间 - 尝试多种方法
            release_elem = (item.find('li', class_='release-date') or 
                          item.find('span', class_='release-date') or
                          item.find('div', class_='release-date'))
            if release_elem:
                movie['release_date'] = clean_text(release_elem.get_text())
            else:
                movie['release_date'] = item.get('data-release', '')
            
            # 国家/地区 - 尝试多种方法
            country_elem = (item.find('li', class_='country') or 
                         item.find('span', class_='country') or
                         item.find('div', class_='country'))
            if country_elem:
                movie['country'] = clean_text(country_elem.get_text())
            else:
                movie['country'] = item.get('data-region', '')
            
            # 想看人数 - 尝试多种方法
            wish_elem = (item.find('span', class_='wish') or 
                        item.find('li', class_='wish') or
                        item.find('span', class_='wish-count') or
                        item.find('div', class_='wish'))
            if wish_elem:
                wish_text = clean_text(wish_elem.get_text())
                movie['wish_count'] = extract_number(wish_text)
            else:
                wish_count = item.get('data-wish', '0')
                movie['wish_count'] = extract_number(str(wish_count))
            
            # 如果还是没有获取到想看人数，设为0
            if 'wish_count' not in movie or movie['wish_count'] is None:
                movie['wish_count'] = 0
            
            # 初始化评论列表
            movie['comments'] = []
            
            return movie
            
        except Exception as e:
            logging.error(f"解析电影项出错: {str(e)}")
            return None
    
    def fetch_movie_comments(self, movie: Dict) -> List[str]:
        """
        爬取电影评论
        
        Args:
            movie: 电影信息字典
            
        Returns:
            评论列表
        """
        comments = []
        movie_id = get_movie_id_from_url(movie.get('movie_url', ''))
        
        if not movie_id:
            logging.warning(f"无法获取电影ID: {movie.get('movie_name')}")
            return comments
        
        try:
            # 计算需要爬取的页数
            total_pages = (config.COMMENTS_PER_MOVIE + config.COMMENTS_PAGE_SIZE - 1) // config.COMMENTS_PAGE_SIZE
            
            for page in range(total_pages):
                start = page * config.COMMENTS_PAGE_SIZE
                comments_url = f"https://movie.douban.com/subject/{movie_id}/comments?start={start}&limit={config.COMMENTS_PAGE_SIZE}&status=P&sort=new_score"
                
                soup = self.fetch_page(comments_url)
                if not soup:
                    break
                
                # 解析评论
                comment_items = soup.find_all('span', class_='short')
                if not comment_items:
                    # 尝试其他可能的类名
                    comment_items = soup.find_all('div', class_='comment')
                
                page_comments = []
                for item in comment_items:
                    comment_text = clean_text(item.get_text())
                    if comment_text and len(comment_text) > 5:  # 过滤太短的评论
                        page_comments.append(comment_text)
                
                comments.extend(page_comments)
                logging.info(f"电影 {movie.get('movie_name')} 第 {page + 1} 页，获取 {len(page_comments)} 条评论")
                
                # 如果本页评论数少于预期，可能已到最后一页
                if len(page_comments) < config.COMMENTS_PAGE_SIZE:
                    break
                
                # 如果已获取足够评论，停止
                if len(comments) >= config.COMMENTS_PER_MOVIE:
                    break
            
            # 限制评论数量
            comments = comments[:config.COMMENTS_PER_MOVIE]
            logging.info(f"电影 {movie.get('movie_name')} 共获取 {len(comments)} 条评论")
            
        except Exception as e:
            logging.error(f"爬取评论失败 {movie.get('movie_name')}: {str(e)}")
        
        return comments
    
    def crawl_movies(self) -> List[Dict]:
        """
        爬取电影列表
        
        Returns:
            电影信息列表
        """
        logging.info("开始爬取电影列表...")
        soup = self.fetch_page(config.DOUBAN_MOVIE_NOWPLAYING_URL)
        
        if not soup:
            logging.error("无法获取电影列表页面")
            return []
        
        movies = self.parse_movie_list(soup)
        logging.info(f"共爬取 {len(movies)} 部电影")
        return movies
    
    def crawl_all_comments(self, movies: List[Dict]) -> List[Dict]:
        """
        为所有电影爬取评论
        
        Args:
            movies: 电影列表
            
        Returns:
            包含评论的电影列表
        """
        logging.info("开始爬取电影评论...")
        for i, movie in enumerate(movies, 1):
            logging.info(f"正在爬取第 {i}/{len(movies)} 部电影的评论: {movie.get('movie_name')}")
            comments = self.fetch_movie_comments(movie)
            movie['comments'] = comments
            time.sleep(config.REQUEST_DELAY)
        
        return movies

