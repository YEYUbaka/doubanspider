# 🎬 豆瓣电影爬虫项目

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![License](https://img.shields.io/badge/License-Learning-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
[![zread](https://img.shields.io/badge/Ask_Zread-_.svg?style=plastic&color=00b0aa&labelColor=000000&logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTQuOTYxNTYgMS42MDAxSDIuMjQxNTZDMS44ODgxIDEuNjAwMSAxLjYwMTU2IDEuODg2NjQgMS42MDE1NiAyLjI0MDFWNC45NjAxQzEuNjAxNTYgNS4zMTM1NiAxLjg4ODEgNS42MDAxIDIuMjQxNTYgNS42MDAxSDQuOTYxNTZDNS4zMTUwMiA1LjYwMDEgNS42MDE1NiA1LjMxMzU2IDUuNjAxNTYgNC45NjAxVjIuMjQwMUM1LjYwMTU2IDEuODg2NjQgNS4zMTUwMiAxLjYwMDEgNC45NjE1NiAxLjYwMDFaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00Ljk2MTU2IDEwLjM5OTlIMi4yNDE1NkMxLjg4ODEgMTAuMzk5OSAxLjYwMTU2IDEwLjY4NjQgMS42MDE1NiAxMS4wMzk5VjEzLjc1OTlDMS42MDE1NiAxNC4xMTM0IDEuODg4MSAxNC4zOTk5IDIuMjQxNTYgMTQuMzk5OUg0Ljk2MTU2QzUuMzE1MDIgMTQuMzk5OSA1LjYwMTU2IDE0LjExMzQgNS42MDE1NiAxMy43NTk5VjExLjAzOTlDNS42MDE1NiAxMC42ODY0IDUuMzE1MDIgMTAuMzk5OSA0Ljk2MTU2IDEwLjM5OTlaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik0xMy43NTg0IDEuNjAwMUgxMS4wMzg0QzEwLjY4NSAxLjYwMDEgMTAuMzk4NCAxLjg4NjY0IDEwLjM5ODQgMi4yNDAxVjQuOTYwMUMxMC4zOTg0IDUuMzEzNTYgMTAuNjg1IDUuNjAwMSAxMS4wMzg0IDUuNjAwMUgxMy43NTg0QzE0LjExMTkgNS42MDAxIDE0LjM5ODQgNS4zMTM1NiAxNC4zOTg0IDQuOTYwMVYyLjI0MDFDMTQuMzk4NCAxLjg4NjY0IDE0LjExMTkgMS42MDAxIDEzLjc1ODQgMS42MDAxWiIgZmlsbD0iI2ZmZiIvPgo8cGF0aCBkPSJNNCAxMkwxMiA0TDQgMTJaIiBmaWxsPSIjZmZmIi8%2BCjxwYXRoIGQ9Ik00IDEyTDEyIDQiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4K&logoColor=ffffff)](https://zread.ai/YEYUbaka/doubanspider)

一个功能完整的豆瓣电影信息爬虫系统，支持数据爬取、分析和可视化

[项目简介](#-项目简介) • [快速开始](#-快速开始) • [使用教程](#-使用教程) • [项目结构](#-项目结构) • [更新日志](#-更新日志)

</div>

---

## 📖 项目简介

本项目是一个**豆瓣电影信息爬虫系统**，用于爬取指定城市（默认武汉）的豆瓣电影信息，并进行数据分析和可视化。项目采用模块化设计，代码规范清晰。

### ✨ 主要功能

- 🕷️ **智能爬虫**：自动爬取电影基本信息（名称、链接、上映时间、国家、想看人数等）
- 💬 **评论采集**：通过 [Rexxar API](https://github.com/x1ao4/douban-api) 批量获取电影短评（移动端内部接口，无需浏览器）
- 📊 **数据分析**：自动排序、统计词频、分析高频/低频词汇
- 📈 **数据可视化**：生成 Top 5 电影柱状图和评论词云图
- 💾 **多格式存储**：支持 CSV 和 JSON 两种数据格式

### 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| **编程语言** | Python 3.9 |
| **网络请求** | requests + Rexxar API |
| **HTML解析** | BeautifulSoup4, lxml |
| **数据处理** | pandas |
| **数据可视化** | matplotlib |
| **中文分词** | jieba |
| **词云生成** | wordcloud |

### 🔗 引用的 Rexxar API

评论数据通过豆瓣移动端内部接口 **Rexxar API v2** 获取：

- **项目**: [x1ao4/douban-api](https://github.com/x1ao4/douban-api) — 豆瓣移动端 API 服务
- **端点**: `GET https://m.douban.com/rexxar/api/v2/movie/{id}/interests`
- **说明**: 返回已看用户的评分短评 JSON 数据，无需 Cookie/登录态，反爬策略比桌面端宽松

---

## 🚀 快速开始

### 环境要求

- Python 3.9 或更高版本
- 网络连接（需要访问豆瓣网站）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/YEYUbaka/doubanspider.git
```

#### 2. 进入项目目录

```bash
cd doubanspider
```

#### 3. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

#### 4. 激活虚拟环境

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```
如果遇到执行策略错误：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows CMD:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### 5. 安装依赖

```bash
pip install -r requirements.txt
```

国内用户可使用镜像加速：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 6. 运行程序

```bash
python main.py
```

---

## 📖 使用教程

### 基本使用

1. **运行主程序**
   ```bash
   python main.py
   ```

2. **程序会自动执行以下步骤：**
   - ✅ 爬取电影列表
   - ✅ 获取每部电影的评论
   - ✅ 保存数据到本地文件
   - ✅ 生成可视化图表
   - ✅ 生成词云图

3. **查看结果**
   - 数据文件：`data/movies.csv` 和 `data/movies.json`
   - 可视化图表：`images/top5_movies.png`
   - 词云图：`images/wordcloud.png`
   - 词频统计：`data/word_statistics.txt`

### 配置说明

主要配置在 `config.py` 文件中，可以根据需要修改：

```python
# 目标城市（豆瓣城市代码）
CITY = "wuhan"  # 可改为 "beijing", "shanghai" 等

# 请求延迟（秒）
REQUEST_DELAY = 5        # 页面爬取延迟
REXXAR_API_DELAY = 2     # API 请求间隔

# 每部电影爬取的评论数量
COMMENTS_PER_MOVIE = 30

# 显示前N部电影
TOP_N_MOVIES = 5
```

### 修改目标城市

```python
CITY = "beijing"   # 北京
CITY = "shanghai"  # 上海
CITY = "guangzhou" # 广州
```

### 自定义爬取数量

```python
COMMENTS_PER_MOVIE = 50  # 每部电影 50 条评论
TOP_N_MOVIES = 10        # Top 10 图表
```

---

## 📁 项目结构

```
douban-movie-spider/
├── 📄 main.py                 # 主程序入口，编排 6 个步骤
├── 🕷️ spider.py               # 爬虫模块（电影列表 + Rexxar API 评论）
├── 📊 data_processor.py       # 数据处理模块
├── 📈 visualizer.py           # 可视化模块
├── ☁️ wordcloud_generator.py   # 词云生成模块
├── 🔧 utils.py                # 工具函数
├── ⚙️ config.py               # 配置文件
├── 📋 requirements.txt        # 依赖包列表
├── 📖 README.md               # 项目说明文档
├── 📝 CLAUDE.md               # AI 工作指引文档
├── 📂 data/                   # 数据存储目录
│   ├── movies.csv            # CSV格式电影数据
│   ├── movies.json           # JSON格式电影数据
│   └── word_statistics.txt   # 词频统计报告
└── 📂 images/                 # 图片输出目录
    ├── top5_movies.png       # Top 5电影柱状图
    └── wordcloud.png         # 评论词云图
```

### 模块职责

| 模块 | 技术 | 职责 |
|------|------|------|
| `main.py` | - | 编排 6 个步骤：初始化 → 爬取列表 → 爬取评论 → 保存 → 可视化 → 词云 |
| `spider.py` | requests + BeautifulSoup + Rexxar API | 爬取电影列表 HTML 和评论 JSON |
| `data_processor.py` | pandas | CSV/JSON 读写，按想看人数排序 |
| `visualizer.py` | matplotlib | 生成 Top N 柱状图 |
| `wordcloud_generator.py` | jieba, wordcloud | 中文分词，词频统计，生成词云 |
| `utils.py` | - | 日志配置，文本清洗，数字/ID 提取 |

---

## 📊 输出文件说明

### 数据文件

| 文件 | 格式 | 说明 |
|------|------|------|
| `movies.csv` | CSV | 电影信息表格，可用Excel打开 |
| `movies.json` | JSON | 电影信息JSON格式，便于程序处理 |
| `word_statistics.txt` | TXT | 词频统计报告，包含高频和低频词汇 |

### 图片文件

| 文件 | 说明 |
|------|------|
| `top5_movies.png` | 想看人数 Top 5 电影的柱状图 |
| `wordcloud.png` | 基于评论生成的词云图 |

---

## ⚙️ 高级配置

### 调整请求延迟

如果遇到反爬虫限制，可以增加延迟时间：

```python
# config.py
REQUEST_DELAY = 10       # 页面爬取间隔增加到 10 秒
REXXAR_API_DELAY = 5     # API 请求间隔增加到 5 秒
```

### 自定义词云样式

修改 `wordcloud_generator.py` 中的词云配置：

```python
wordcloud_config = {
    'width': 1200,           # 宽度
    'height': 600,           # 高度
    'background_color': 'white',  # 背景色
    'colormap': 'viridis',   # 颜色方案
}
```

---

## ⚠️ 注意事项

1. **遵守网站规则**
   - 本项目仅用于学习研究目的
   - 请遵守豆瓣网站的服务条款
   - 不要进行商业用途

2. **网络环境**
   - 确保能够正常访问豆瓣网站
   - 如果遇到访问限制，可能需要使用代理

3. **字体支持**
   - 词云图需要中文字体支持
   - Windows 系统通常自带 SimHei 字体
   - Linux 系统可能需要安装中文字体包

4. **数据使用**
   - 爬取的数据仅供学习使用
   - 请勿用于商业目的
   - 尊重版权和隐私

---

## ❓ 常见问题

### Q1: 爬取失败怎么办？

**A:** 检查以下几点：
- ✅ 网络连接是否正常
- ✅ 能否正常访问豆瓣网站
- ✅ 如果遇到反爬虫限制，增加 `REQUEST_DELAY` 的值
- ✅ 检查请求头设置是否正确

### Q2: 评论爬取数量为0？

**A:** 可能原因和解决方法：
- 该电影为新上映影片，暂无用户评分短评（Rexxar API 正常返回空数据）
- 检查网络是否能正常访问 `m.douban.com`
- 更新 `config.py` 中的 `REXXAR_HEADERS` 的 `User-Agent` 为最新移动端 UA
- 若持续失败，可尝试添加 Cookie（从浏览器复制登录后的 Cookie）

### Q3: Rexxar API 返回 403 或 404？

**A:** 豆瓣内部 API 可能已更新：
- 404 说明端点路径已变，需通过抓包分析最新的 Rexxar API 路径
- 403 说明请求头被拦截，更新 `REXXAR_HEADERS` 中的 `User-Agent` 为最新 Android UA
- 添加 `Referer: https://m.douban.com/movie/subject/{movie_id}/` 请求头

### Q4: 词云图中文显示乱码？

**A:** 确保系统安装了中文字体：
- Windows: 通常自带 SimHei、SimSun 等字体
- Linux: 安装中文字体包 `sudo apt-get install fonts-wqy-microhei`
- Mac: 系统自带中文字体

程序会自动查找系统字体，如果找不到会显示警告。

### Q5: 虚拟环境激活失败？

**A:** Windows PowerShell 执行策略问题：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q6: 依赖安装失败？

**A:** 尝试以下方法：
- 使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- 升级 pip：`python -m pip install --upgrade pip`
- 检查 Python 版本是否为 3.9 或更高

---

## 🔔 更新日志

### 2026-05-07 重大更新 - 改用 Rexxar API 爬取评论，移除 Selenium

#### 🐛 问题描述
在重新运行项目时发现，评论爬取功能完全失效，所有电影的评论数量都是 0 条。经排查，`webdriver-manager` 无法连接谷歌服务器下载 ChromeDriver，导致 **Selenium 初始化失败**。

#### 🔍 问题原因
原有方案的依赖链问题：
- 评论爬取依赖 Selenium + ChromeDriver
- ChromeDriver 通过 `webdriver-manager` 自动下载
- 在某些网络环境下无法访问谷歌 CDN，导致整个评论功能不可用

#### ✅ 解决方案
弃用 Selenium，改用豆瓣 **Rexxar API v2**（移动端内部接口），直接请求 JSON 数据：

**技术实现：**
1. 使用 `https://m.douban.com/rexxar/api/v2/movie/{id}/interests` 端点
2. 模拟 Android 移动端请求头（User-Agent、Referer）
3. 分页获取已看用户的评分短评（`status=done`）
4. JSON 纯数据解析，无需浏览器渲染

**修改文件：**
- `spider.py` - 移除 Selenium 代码，新增 `_request_json()` 方法和 Rexxar API 爬取逻辑
- `config.py` - 新增 `REXXAR_HEADERS`、`REXXAR_API_DELAY` 等配置项
- `requirements.txt` - 移除 selenium 和 webdriver-manager 依赖
- `CLAUDE.md` - **新建**，项目文档和工作指引

#### 📊 修复效果
- ❌ **修复前**: 评论爬取完全失效 = 0条
- ✅ **修复后**: 55 部电影成功爬取，**共 1,648 条评论**
- ✅ **每部电影**: 稳定获取 30 条（达到配置上限）
- ✅ **速度提升**: 无需启动浏览器，每部电影仅需 7 秒

#### 🚀 使用说明
**依赖已精简：**
```bash
pip install -r requirements.txt
```
无需安装 Chrome 浏览器和 ChromeDriver，纯 Python 依赖。

**注意事项：**
- Rexxar API 是豆瓣移动端内部接口，无官方文档，端点可能随豆瓣更新而变化
- 若 API 返回 403 或空数据，尝试更新 `config.py` 中的 `REXXAR_HEADERS` 的 `User-Agent`
- 建议保持 `REXXAR_API_DELAY = 2` 的请求间隔，避免触发限流

---

### 2025-01-24 重大更新 - 修复评论爬取功能（已废弃）

> ⚠️ **注意**: 此方案已被 2026-05-07 的 Rexxar API 方案取代。以下内容仅作历史记录保留。

#### 🐛 问题描述
在重新运行项目时发现，虽然热搜榜电影名称、链接、想看人数都能正常获取，但**评论爬取功能完全失效**，所有电影的评论数量都是0条。

#### 🔍 问题原因
经过调试分析发现，豆瓣网站对评论页面启用了 **JavaScript 反爬虫验证机制**：
- 访问评论页面时返回一个 JavaScript 挑战页面
- 需要执行 SHA-512 哈希计算（工作量证明 PoW）
- 传统的 requests 库无法执行 JavaScript，导致无法获取真实评论内容

#### ✅ 解决方案
采用 **Selenium + Chrome WebDriver** 技术方案，使用真实浏览器模拟访问：

**技术实现：**
1. 集成 Selenium WebDriver（无头模式运行）
2. 自动等待页面 JavaScript 执行完成
3. 解析渲染后的 HTML 获取评论内容
4. 保持合理的请求延迟避免被封

#### 📊 修复效果
- ❌ **修复前**: 所有电影评论数量 = 0条
- ✅ **修复后**: 每部电影成功获取 19-30条评论
- ✅ **测试结果**: 62部电影全部正常爬取评论

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 👤 作者

**卑微计算机专业大学生**

- GitHub: [@YEYUbaka](https://github.com/YEYUbaka)

### 🤖 AI 协助

- **Claude Code** (Anthropic) — 代码审查与优化建议

---

## 📄 许可证

本项目仅用于**学习研究目的**，不进行商业用途。

---

<div align="center">

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！

Made with ❤️ by a Python learner

</div>
