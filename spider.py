# -*- coding: utf-8 -*-
"""
爬虫模块
负责爬取豆瓣电影信息和评论

技术方案:
- 电影列表: requests + BeautifulSoup 解析"正在上映"页面
- 电影评论: 豆瓣 Rexxar API v2 (移动端内部接口, 返回 JSON)
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
        # 桌面端会话 (用于爬取电影列表页面)
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

        # 移动端会话 (用于 Rexxar API 爬取评论)
        self.mobile_session = requests.Session()
        self.mobile_session.headers.update(config.REXXAR_HEADERS)

        self.movies = []

    # ----------------------------------------------------------------
    # 通用请求方法
    # ----------------------------------------------------------------

    def _request_json(self, url: str, headers: dict = None, params: dict = None,
                      max_retries: int = None) -> Optional[dict]:
        """
        请求 JSON API，带重试机制

        Args:
            url: API URL
            headers: 请求头
            params: 查询参数
            max_retries: 最大重试次数

        Returns:
            JSON 响应字典，失败返回 None
        """
        if max_retries is None:
            max_retries = config.MAX_RETRIES

        for attempt in range(max_retries):
            try:
                logging.info(f"正在请求 API: {url}")
                session = self.mobile_session
                response = session.get(
                    url,
                    headers=headers or {},
                    params=params,
                    timeout=config.REQUEST_TIMEOUT
                )
                response.raise_for_status()

                # 检查是否真的是 JSON
                content_type = response.headers.get('Content-Type', '')
                if 'application/json' not in content_type and 'text/json' not in content_type:
                    # 可能被反爬，检查响应内容
                    if len(response.text) < 100 or '爬虫' in response.text:
                        logging.warning(f"API 响应异常 (尝试 {attempt + 1}/{max_retries}): "
                                        f"status={response.status_code}, "
                                        f"content_type={content_type}, "
                                        f"body={response.text[:200]}")
                        if attempt < max_retries - 1:
                            wait = 2 ** attempt
                            logging.info(f"等待 {wait}s 后重试...")
                            time.sleep(wait)
                            continue
                        return None

                return response.json()

            except requests.exceptions.JSONDecodeError as e:
                logging.warning(f"JSON 解析失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return None
            except Exception as e:
                logging.warning(f"API 请求失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    return None

        return None

    # ----------------------------------------------------------------
    # 电影列表爬取 (桌面端 HTML 解析)
    # ----------------------------------------------------------------

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

            headers = config.HEADERS.copy()
            headers['Accept-Encoding'] = 'gzip, deflate'

            response = self.session.get(
                url,
                headers=headers,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()

            if response.encoding is None or response.encoding == 'ISO-8859-1':
                response.encoding = response.apparent_encoding or 'utf-8'

            # 调试：临时保存HTML内容用于分析
            try:
                with open('debug_page.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                logging.info(f"页面内容已保存到 debug_page.html，长度: {len(response.text)} 字符")
                if '豆瓣' in response.text or 'movie' in response.text.lower():
                    logging.info("页面内容看起来正常")
                else:
                    logging.warning("页面内容可能异常，可能遇到反爬虫")
            except Exception as e:
                logging.warning(f"保存调试文件失败: {str(e)}")

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

            movie['movie_name'] = clean_text(item.get('data-title', ''))

            title_elem = None
            links = item.find_all('a', href=lambda x: x and '/subject/' in str(x))
            if links:
                title_elem = links[0]
                if not movie['movie_name']:
                    movie['movie_name'] = clean_text(title_elem.get_text())
            else:
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
                href = item.get('data-href', '') or item.get('data-url', '')
                if href:
                    if href.startswith('http'):
                        movie['movie_url'] = href
                    else:
                        movie['movie_url'] = config.DOUBAN_MOVIE_BASE_URL + href
                else:
                    movie['movie_url'] = ''

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

            # 上映时间
            release_elem = (item.find('li', class_='release-date') or
                          item.find('span', class_='release-date') or
                          item.find('div', class_='release-date'))
            if release_elem:
                movie['release_date'] = clean_text(release_elem.get_text())
            else:
                movie['release_date'] = item.get('data-release', '')

            # 国家/地区
            country_elem = (item.find('li', class_='country') or
                         item.find('span', class_='country') or
                         item.find('div', class_='country'))
            if country_elem:
                movie['country'] = clean_text(country_elem.get_text())
            else:
                movie['country'] = item.get('data-region', '')

            # 想看人数
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

            if 'wish_count' not in movie or movie['wish_count'] is None:
                movie['wish_count'] = 0

            movie['comments'] = []
            return movie

        except Exception as e:
            logging.error(f"解析电影项出错: {str(e)}")
            return None

    # ----------------------------------------------------------------
    # 评论爬取 (Rexxar API v2 移动端接口)
    # ----------------------------------------------------------------

    def fetch_movie_comments(self, movie: Dict) -> List[str]:
        """
        爬取电影评论 (使用豆瓣 Rexxar API v2)

        Rexxar API 是豆瓣移动端的内部接口，返回 JSON 数据，
        相比桌面端 HTML 页面，反爬虫策略更宽松。

        实际使用的端点:
            GET https://m.douban.com/rexxar/api/v2/movie/{movie_id}/interests
            参数: start, count, status=done
            返回: {"interests": [{"comment": "评论文本", ...}, ...], "total": N}

        注意: /comments 端点不存在 (返回 404), /interests 端点
        返回的是已看用户的评分和短评。

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
            total_pages = (config.COMMENTS_PER_MOVIE + config.COMMENTS_PAGE_SIZE - 1) // config.COMMENTS_PAGE_SIZE

            for page in range(total_pages):
                start = page * config.COMMENTS_PAGE_SIZE
                api_url = f"{config.REXXAR_API_BASE_URL}/movie/{movie_id}/interests"

                params = {
                    'start': start,
                    'count': config.COMMENTS_PAGE_SIZE,
                    'status': 'done',  # done=已看(有评分和短评), wish=想看
                }

                mobile_headers = {
                    'Referer': f'https://m.douban.com/movie/subject/{movie_id}/',
                }

                logging.info(f"正在请求评论 API (第 {page + 1} 页): "
                             f"{api_url}?start={start}&count={config.COMMENTS_PAGE_SIZE}")

                data = self._request_json(api_url, headers=mobile_headers, params=params)

                if not data:
                    logging.warning(f"获取第 {page + 1} 页评论失败，停止翻页")
                    break

                # 解析评论列表
                # 结构: {"interests": [{"comment": "...", "rating": {...}, ...}, ...]}
                raw_interests = data.get('interests', [])
                page_comments = []
                for item in raw_interests:
                    text = item.get('comment', '')
                    if text:
                        # 清理文本: 去掉评分前缀 (如 "8.0 " 在文本开头)
                        cleaned = clean_text(text)
                        if len(cleaned) > 5:  # 过滤太短的评论
                            page_comments.append(cleaned)

                comments.extend(page_comments)
                logging.info(f"电影 {movie.get('movie_name')} 第 {page + 1} 页，"
                             f"获取 {len(page_comments)} 条评论 (API 返回 {len(raw_interests)} 条)")

                # 如果 API 返回的数据量少于请求量，说明已到最后一页
                if len(raw_interests) < config.COMMENTS_PAGE_SIZE:
                    logging.info(f"API 返回数据不足一页 "
                                 f"({len(raw_interests)} < {config.COMMENTS_PAGE_SIZE})，停止翻页")
                    break

                if len(comments) >= config.COMMENTS_PER_MOVIE:
                    break

                # 请求间隔 (API 请求比 HTML 页面轻量，使用更短的延迟)
                time.sleep(config.REXXAR_API_DELAY)

            comments = comments[:config.COMMENTS_PER_MOVIE]
            logging.info(f"电影 {movie.get('movie_name')} 共获取 {len(comments)} 条评论")

        except Exception as e:
            logging.error(f"爬取评论失败 {movie.get('movie_name')}: {str(e)}")
            import traceback
            logging.error(traceback.format_exc())

        return comments

    # ----------------------------------------------------------------
    # 主流程
    # ----------------------------------------------------------------

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
