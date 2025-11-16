# 🎬 豆瓣电影爬虫项目

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9-blue.svg)
![License](https://img.shields.io/badge/License-Learning-purple.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

一个功能完整的豆瓣电影信息爬虫系统，支持数据爬取、分析和可视化

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用教程](#-使用教程) • [项目结构](#-项目结构)

</div>

---

## 📖 项目简介

本项目是一个**豆瓣电影信息爬虫系统**，用于爬取指定城市（默认武汉）的豆瓣电影信息，并进行数据分析和可视化。项目采用模块化设计，代码规范清晰，适合Python学习者参考和实践。

### ✨ 主要功能

- 🕷️ **智能爬虫**：自动爬取电影基本信息（名称、链接、上映时间、国家、想看人数等）
- 💬 **评论采集**：批量获取电影评论，支持分页处理
- 📊 **数据分析**：自动排序、统计词频、分析高频/低频词汇
- 📈 **数据可视化**：生成Top 5电影柱状图和评论词云图
- 💾 **多格式存储**：支持CSV和JSON两种数据格式

## 🎯 开发背景

本项目由**刚学完Python的计算机专业大学生**开发，是一个综合性的爬虫实践项目。项目旨在：

- ✅ 巩固Python基础语法和面向对象编程
- ✅ 学习网络爬虫技术（requests、BeautifulSoup）
- ✅ 掌握数据处理和分析（pandas）
- ✅ 实践数据可视化（matplotlib）
- ✅ 学习中文文本处理（jieba、wordcloud）
- ✅ 培养项目开发能力和代码规范意识

## 🚀 功能特性

### 1. 数据爬取模块
- 爬取电影基本信息（名称、链接、上映时间、国家、想看人数）
- 批量获取电影评论（可配置每部电影的评论数量）
- 智能处理分页逻辑
- 异常处理和重试机制

### 2. 数据处理模块
- 按想看人数自动排序
- 支持CSV和JSON格式导出
- 数据清洗和验证

### 3. 数据可视化模块
- 生成Top N电影柱状图（默认Top 5）
- 自动处理长电影名称显示
- 高质量PNG图片输出

### 4. 评论分析模块
- 中文分词处理（jieba）
- 停用词过滤
- 词频统计（高频/低频词汇）
- 生成词云图

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| **编程语言** | Python 3.9 |
| **网络请求** | requests |
| **HTML解析** | BeautifulSoup4, lxml |
| **数据处理** | pandas |
| **数据可视化** | matplotlib |
| **中文分词** | jieba |
| **词云生成** | wordcloud |

## 📁 项目结构

```
douban-movie-spider/
├── 📄 main.py                 # 主程序入口
├── 🕷️ spider.py               # 爬虫模块
├── 📊 data_processor.py       # 数据处理模块
├── 📈 visualizer.py           # 可视化模块
├── ☁️ wordcloud_generator.py   # 词云生成模块
├── 🔧 utils.py                # 工具函数
├── ⚙️ config.py               # 配置文件
├── 📋 requirements.txt        # 依赖包列表
├── 📖 README.md               # 项目说明文档
├── 📚 DEPLOYMENT.md           # 部署指南
├── 📂 data/                   # 数据存储目录
│   ├── movies.csv            # CSV格式电影数据
│   ├── movies.json           # JSON格式电影数据
│   └── word_statistics.txt   # 词频统计报告
└── 📂 images/                 # 图片输出目录
    ├── top5_movies.png       # Top 5电影柱状图
    └── wordcloud.png         # 评论词云图
```

## 🚀 快速开始

### 环境要求

- Python 3.9 或更高版本
- 网络连接（需要访问豆瓣网站）

### 安装步骤

#### 1. 克隆项目

```bash
# 使用 Git 克隆
git clone https://github.com/YEYUbaka/doubanspider.git

# 或直接下载 ZIP 文件并解压
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

如果遇到执行策略错误，运行：
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

激活成功后，命令行提示符前会显示 `(venv)`。

#### 5. 安装依赖

```bash
pip install -r requirements.txt
```

#### 6. 运行程序

```bash
python main.py
```

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

# 请求延迟（秒）- 避免频繁请求
REQUEST_DELAY = 2

# 每部电影爬取的评论数量
COMMENTS_PER_MOVIE = 30

# 显示前N部电影
TOP_N_MOVIES = 5
```

### 修改目标城市

1. 打开 `config.py` 文件
2. 修改 `CITY` 变量：
   ```python
   CITY = "beijing"  # 改为北京
   ```
3. 保存并重新运行程序

### 自定义爬取数量

在 `config.py` 中修改：
```python
# 每部电影爬取的评论数量
COMMENTS_PER_MOVIE = 50  # 改为50条

# 显示前N部电影
TOP_N_MOVIES = 10  # 改为Top 10
```

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
| `top5_movies.png` | 想看人数Top 5电影的柱状图 |
| `wordcloud.png` | 基于评论生成的词云图 |

## ⚙️ 高级配置

### 调整请求延迟

如果遇到反爬虫限制，可以增加延迟时间：

```python
# config.py
REQUEST_DELAY = 3  # 增加到3秒
```

### 自定义词云样式

修改 `wordcloud_generator.py` 中的词云配置：

```python
wordcloud_config = {
    'width': 1200,      # 宽度
    'height': 600,      # 高度
    'background_color': 'white',  # 背景色
    'colormap': 'viridis',  # 颜色方案
}
```

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
   - Windows系统通常自带中文字体
   - Linux系统可能需要安装中文字体包

4. **数据使用**
   - 爬取的数据仅供学习使用
   - 请勿用于商业目的
   - 尊重版权和隐私

## ❓ 常见问题

### Q1: 爬取失败怎么办？

**A:** 检查以下几点：
- ✅ 网络连接是否正常
- ✅ 能否正常访问豆瓣网站
- ✅ 如果遇到反爬虫限制，增加 `REQUEST_DELAY` 的值
- ✅ 检查请求头设置是否正确

### Q2: 词云图中文显示乱码？

**A:** 确保系统安装了中文字体：
- Windows: 通常自带 SimHei、SimSun 等字体
- Linux: 安装中文字体包 `sudo apt-get install fonts-wqy-microhei`
- Mac: 系统自带中文字体

程序会自动查找系统字体，如果找不到会显示警告。

### Q3: 如何修改目标城市？

**A:** 在 `config.py` 中修改 `CITY` 变量：
```python
CITY = "beijing"  # 北京
CITY = "shanghai"  # 上海
CITY = "guangzhou"  # 广州
```

### Q4: 虚拟环境激活失败？

**A:** Windows PowerShell 执行策略问题：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q5: 依赖安装失败？

**A:** 尝试以下方法：
- 使用国内镜像源：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
- 升级 pip：`python -m pip install --upgrade pip`
- 检查 Python 版本是否为 3.9 或更高

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 开发规范

- 代码遵循 PEP 8 规范
- 使用 UTF-8 编码
- 所有函数和类都有文档字符串
- 包含完整的异常处理
- 使用有意义的变量命名

## 📄 许可证

本项目仅用于**学习研究目的**，不进行商业用途。

## 🔗 相关链接

- [项目部署指南](DEPLOYMENT.md)
- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [pandas 文档](https://pandas.pydata.org/docs/)

## 👤 作者

**计算机专业大学生**

- GitHub: [@YEYUbaka](https://github.com/YEYUbaka)

---

<div align="center">

如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！

Made with ❤️ by a Python learner

</div>
