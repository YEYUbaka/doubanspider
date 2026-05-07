# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

豆瓣电影爬虫系统，爬取指定城市（默认武汉）正在上映的电影信息（名称、想看人数等），并通过豆瓣 Rexxar API v2（移动端内部接口）获取电影短评，最后进行数据可视化和词云分析。

## 虚拟环境

```powershell
# Windows PowerShell 创建并激活
python -m venv venv
.\venv\Scripts\Activate.ps1

# 如遇执行策略错误:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Windows CMD
venv\Scripts\activate.bat

# 安装依赖
pip install -r requirements.txt

# 若遇到网络问题, 使用国内镜像:
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 运行命令

```bash
python main.py
```

## 项目架构

```
doubanspider/
├── main.py                  # 主程序入口, 编排 6 个步骤
├── spider.py                # 爬虫核心: 电影列表(HTML) + 评论(Rexxar API)
├── data_processor.py        # 数据处理: CSV/JSON 读写, 排序
├── visualizer.py            # 可视化: Top N 柱状图
├── wordcloud_generator.py   # 词云: jieba 分词 + wordcloud 生成
├── utils.py                 # 工具函数: 日志, 文本清洗, 数字提取
├── config.py                # 全局配置: URL, 请求头, 文件路径
├── requirements.txt         # 依赖列表
├── data/                    # 输出: movies.csv, movies.json, word_statistics.txt
└── images/                  # 输出: top5_movies.png, wordcloud.png
```

### 模块职责

| 模块 | 技术 | 职责 |
|------|------|------|
| `spider.py` | requests + BeautifulSoup + Rexxar API | 爬取电影列表和评论 |
| `data_processor.py` | pandas | CSV/JSON 读写, 按想看人数排序 |
| `visualizer.py` | matplotlib | 生成想看人数 Top N 柱状图 |
| `wordcloud_generator.py` | jieba, wordcloud | 中文分词, 词频统计, 生成词云 |
| `utils.py` | - | 日志配置, 文本清理, 数字/ID 提取 |

## 关键数据流

1. **电影列表**: GET `https://movie.douban.com/cinema/nowplaying/{city}/` -> BeautifulSoup HTML 解析
2. **电影评论**: GET `https://m.douban.com/rexxar/api/v2/movie/{movie_id}/interests?start=0&count=20&status=done` -> requests JSON 解析
3. **数据持久化**: CSV + JSON 双格式存储
4. **可视化**: Top N 柱状图 + 词云图

## 豆瓣 Rexxar API 说明

评论接口使用豆瓣移动端内部 API（Rexxar v2），关键信息:

- **端点**: `GET https://m.douban.com/rexxar/api/v2/movie/{movie_id}/interests`
- **评论端点说明**: 豆瓣 Rexxar API 不存在 `/comments` 端点 (返回 404), 实际使用 `/interests` 端点, 返回已看用户的评分短评
- **参数**: `start`(偏移), `count`(每页数), `status=done`(已看, 含短评)
- **其他可用端点**:
  - `GET /api/v2/subject/{movie_id}` — 电影详情 (含 comment_count)
  - `GET /api/v2/subject/{movie_id}/rating` — 评分统计
  - `GET /api/v2/subject_collection/movie_showing/items` — 正在上映列表
- **请求头**:
  - `User-Agent`: 必须使用 Android 移动端 UA
  - `Accept: application/json`
  - `Referer: https://m.douban.com/movie/subject/{movie_id}/`
- **JSON 返回格式**: `{"interests": [{"comment": "短评内容", "rating": {...}, "user": {...}}, ...], "total": N}`
- **限制**: 建议请求间隔 >= 2 秒, 无需 Cookie/登录态即可获取
- **优势**: 返回纯 JSON, 无需 Selenium/浏览器渲染, 反爬策略比桌面端宽松很多

## 重要配置项 (config.py)

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `CITY` | `"wuhan"` | 目标城市 |
| `REQUEST_DELAY` | `5` | API 请求间隔(秒) |
| `COMMENTS_PER_MOVIE` | `30` | 每部电影最大评论数 |
| `COMMENTS_PAGE_SIZE` | `20` | 每页评论数 |
| `TOP_N_MOVIES` | `5` | 图表显示前 N 部电影 |

## 常见开发任务

### 修改目标城市

编辑 `config.py` 中的 `CITY` 变量:
```python
CITY = "beijing"   # 北京
CITY = "shanghai"  # 上海
```

### 调整爬取数量

```python
COMMENTS_PER_MOVIE = 50  # 每部电影 50 条评论
TOP_N_MOVIES = 10        # Top 10 图表
```

### 增加请求延迟（遭遇反爬时）

```python
REQUEST_DELAY = 10  # 增加到 10 秒
```

### Rexxar API 不可用时的降级策略

如果 `m.douban.com/rexxar/api/v2/movie/{id}/comments` 返回空数据或 403:
1. 检查请求头中的 `User-Agent` 是否为最新移动端 UA
2. 尝试添加 `Cookie`（从浏览器复制登录后的 Cookie）
3. 可降级到桌面端 HTML 解析: `https://movie.douban.com/subject/{id}/comments?start=0&limit=20`

## 已知限制

- 电影列表仅爬取"正在上映"页面，不包含"即将上映"
- Rexxar API 为豆瓣内部接口，无官方文档，端点/参数可能随豆瓣更新而变化
- 评论仅爬取短评（comments），不包含长评（reviews）
- 词云需要系统安装中文字体（Windows 通常自带 SimHei）
- 输出文件（CSV/JSON/PNG）会覆盖写入，没有增量备份

## 依赖清单

```
requests, beautifulsoup4, lxml   # 网络爬虫
pandas                            # 数据处理
matplotlib                        # 可视化
jieba, wordcloud                  # 中文分词 + 词云
```

（无 Selenium/webdriver-manager 依赖——评论爬取已改用 Rexxar API）
