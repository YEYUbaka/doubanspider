# 豆瓣电影爬虫项目

## 项目简介

本项目是一个豆瓣电影信息爬虫系统，用于爬取武汉地区豆瓣电影信息，进行数据分析和可视化。

## 开发背景

本项目由刚学完Python的计算机专业大学生开发，是一个综合性的爬虫实践项目。项目旨在：
- 巩固Python基础语法和面向对象编程
- 学习网络爬虫技术（requests、BeautifulSoup）
- 掌握数据处理和分析（pandas）
- 实践数据可视化（matplotlib）
- 学习中文文本处理（jieba、wordcloud）
- 培养项目开发能力和代码规范意识

## 功能特性

1. **数据爬取**：爬取武汉地区豆瓣电影信息（电影名、链接、上映时间、国家、想看人数、评论等）
2. **数据排序**：根据想看人数对电影进行排序
3. **数据可视化**：生成想看人数Top 5电影的柱状图
4. **评论分析**：分析电影评论，统计高频和低频词汇
5. **词云生成**：基于评论生成词云图

## 技术栈

- Python 3.9
- requests：HTTP请求
- BeautifulSoup4：HTML解析
- pandas：数据处理
- matplotlib：数据可视化
- jieba：中文分词
- wordcloud：词云生成
- lxml：HTML解析器

## 项目结构

```
豆瓣/
├── .cursorrules          # 项目规则文件
├── requirements.txt      # 依赖包列表
├── README.md            # 项目说明文档
├── main.py              # 主程序入口
├── spider.py            # 爬虫模块
├── data_processor.py    # 数据处理模块
├── visualizer.py        # 可视化模块
├── wordcloud_generator.py # 词云生成模块
├── utils.py             # 工具函数
├── config.py            # 配置文件
├── data/                # 数据存储目录
│   ├── movies.csv
│   ├── movies.json
│   └── word_statistics.txt
└── images/              # 图片输出目录
    ├── top5_movies.png
    └── wordcloud.png
```

## 安装步骤

### 1. 确保Python版本

本项目使用Python 3.9，解释器路径为：`D:\Program Files\python3.9\python.exe`

### 2. 创建虚拟环境（推荐）

虚拟环境可以隔离项目依赖，避免与系统Python环境冲突，**强烈推荐使用**。

**创建虚拟环境：**
```bash
"D:\Program Files\python3.9\python.exe" -m venv venv
```

**激活虚拟环境：**
- Windows PowerShell:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  如果遇到执行策略错误，可以运行：
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- Windows CMD:
  ```cmd
  venv\Scripts\activate.bat
  ```

激活成功后，命令行提示符前会显示 `(venv)`。

### 3. 安装依赖

**在虚拟环境中安装（推荐）：**
```bash
# 先激活虚拟环境，然后执行
pip install -r requirements.txt
```

**或直接安装（不推荐）：**
```bash
"D:\Program Files\python3.9\python.exe" -m pip install -r requirements.txt
```

### 4. 运行程序

**在虚拟环境中运行（推荐）：**
```bash
# 先激活虚拟环境，然后执行
python main.py
```

**或直接运行（不推荐）：**
```bash
"D:\Program Files\python3.9\python.exe" main.py
```

### 5. 退出虚拟环境

使用完毕后，可以退出虚拟环境：
```bash
deactivate
```

## 使用说明

1. **运行主程序**：直接运行 `main.py` 即可完成所有功能
2. **查看结果**：
   - 数据文件保存在 `data/` 目录
   - 可视化图表保存在 `images/` 目录
   - 词频统计保存在 `data/word_statistics.txt`

## 配置说明

主要配置在 `config.py` 文件中：

- `CITY`：目标城市（默认：wuhan）
- `REQUEST_DELAY`：请求延迟时间（秒）
- `COMMENTS_PER_MOVIE`：每部电影爬取的评论数量
- `TOP_N_MOVIES`：显示前N部电影

## 输出文件说明

- `movies.csv`：电影信息CSV格式
- `movies.json`：电影信息JSON格式
- `top5_movies.png`：想看人数Top 5电影柱状图
- `wordcloud.png`：评论词云图
- `word_statistics.txt`：词频统计报告

## 注意事项

1. **反爬虫应对**：程序已设置合理的请求延迟和请求头，请遵守网站服务条款
2. **数据使用**：本项目仅用于学习研究目的，不进行商业用途
3. **网络环境**：确保网络连接正常，能够访问豆瓣网站
4. **字体支持**：词云图需要中文字体支持，程序会自动查找系统字体

## 常见问题

### Q: 爬取失败怎么办？
A: 检查网络连接，确保能够访问豆瓣网站。如果遇到反爬虫限制，可以增加 `REQUEST_DELAY` 的值。

### Q: 词云图中文显示乱码？
A: 确保系统安装了中文字体（如：SimHei、SimSun等），程序会自动查找系统字体。

### Q: 如何修改目标城市？
A: 修改 `config.py` 中的 `CITY` 变量即可。

## 开发规范

- 代码遵循PEP 8规范
- 使用UTF-8编码
- 所有函数和类都有文档字符串
- 包含完整的异常处理

## 项目分发与上传

### 上传到 GitHub

1. **创建 GitHub 仓库**
   - 访问 [GitHub](https://github.com) 并登录
   - 点击右上角 "+" → "New repository"
   - 填写仓库名称（如：douban-movie-spider）
   - 选择 Public 或 Private
   - 不要勾选 "Initialize this repository with a README"（因为已有README）
   - 点击 "Create repository"

2. **初始化 Git 仓库并上传**
   ```bash
   # 在项目根目录执行
   git init
   git add .
   git commit -m "Initial commit: 豆瓣电影爬虫项目"
   git branch -M main
   git remote add origin https://github.com/你的用户名/仓库名.git
   git push -u origin main
   ```

3. **如果遇到认证问题**
   - 使用 Personal Access Token（推荐）
   - 或使用 SSH 密钥：`git remote set-url origin git@github.com:你的用户名/仓库名.git`

### 上传到 Gitee（码云）

1. **创建 Gitee 仓库**
   - 访问 [Gitee](https://gitee.com) 并登录
   - 点击右上角 "+" → "新建仓库"
   - 填写仓库名称和描述
   - 选择公开或私有
   - 不要勾选 "使用Readme文件初始化这个仓库"
   - 点击 "创建"

2. **初始化 Git 仓库并上传**
   ```bash
   # 在项目根目录执行
   git init
   git add .
   git commit -m "Initial commit: 豆瓣电影爬虫项目"
   git branch -M main
   git remote add origin https://gitee.com/你的用户名/仓库名.git
   git push -u origin main
   ```

### 后续更新代码

```bash
# 添加修改的文件
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到远程仓库
git push
```

### 其他人如何使用你的项目

1. **克隆项目**
   ```bash
   # GitHub
   git clone https://github.com/你的用户名/仓库名.git
   
   # Gitee
   git clone https://gitee.com/你的用户名/仓库名.git
   ```

2. **按照安装步骤操作**
   - 进入项目目录
   - 创建虚拟环境
   - 安装依赖
   - 运行程序

## 许可证

本项目仅用于学习研究目的。

