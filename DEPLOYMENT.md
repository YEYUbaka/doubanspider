# 项目部署与分发指南

本文档详细说明如何将豆瓣电影爬虫项目上传到 GitHub 或 Gitee，以及如何分发给其他用户使用。

## 目录

- [准备工作](#准备工作)
- [上传到 GitHub](#上传到-github)
- [上传到 Gitee](#上传到-gitee)
- [后续更新](#后续更新)
- [项目分发](#项目分发)
- [常见问题](#常见问题)

## 准备工作

### 1. 检查项目文件

确保项目包含以下必要文件：
- ✅ 所有 Python 源代码文件（.py）
- ✅ `requirements.txt` 依赖文件
- ✅ `README.md` 项目说明
- ✅ `.gitignore` Git 忽略文件
- ✅ `.cursorrules` 项目规则（可选）

### 2. 清理不需要的文件

项目已经配置了 `.gitignore`，会自动忽略：
- 虚拟环境目录（venv/）
- Python 缓存文件（__pycache__/）
- 运行时生成的数据文件（data/*.csv, data/*.json 等）
- 生成的图片文件（images/*.png 等）
- IDE 配置文件

### 3. 确保代码完整

运行一次项目，确保没有错误：
```bash
python main.py
```

## 上传到 GitHub

### 方法一：使用命令行（推荐）

#### 步骤 1：创建 GitHub 仓库

1. 访问 [GitHub](https://github.com) 并登录
2. 点击右上角 "+" → "New repository"
3. 填写仓库信息：
   - **Repository name**: `douban-movie-spider`（或你喜欢的名称）
   - **Description**: `豆瓣电影信息爬虫系统 - 爬取、分析和可视化武汉地区电影数据`
   - **Visibility**: 选择 Public（公开）或 Private（私有）
   - **不要勾选** "Add a README file"、"Add .gitignore"、"Choose a license"（因为我们已经有了）
4. 点击 "Create repository"

#### 步骤 2：初始化本地 Git 仓库

打开终端（PowerShell 或 CMD），进入项目目录：

```bash
# 切换到项目目录
cd "f:\Cursor projects\爬虫\豆瓣"

# 初始化 Git 仓库
git init

# 添加所有文件到暂存区
git add .

# 提交文件
git commit -m "Initial commit: 豆瓣电影爬虫项目"

# 重命名主分支为 main（GitHub 默认分支名）
git branch -M main
```

#### 步骤 3：连接远程仓库并推送

```bash
# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送到远程仓库
git push -u origin main
```

**注意**：如果遇到认证问题，需要：
- 使用 Personal Access Token（推荐）
- 或配置 SSH 密钥

#### 配置 GitHub 认证

**方法 A：使用 Personal Access Token**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 "Generate new token"
3. 选择权限：至少勾选 `repo`
4. 生成后复制 token
5. 推送时使用 token 作为密码

**方法 B：使用 SSH 密钥**

```bash
# 生成 SSH 密钥（如果还没有）
ssh-keygen -t ed25519 -C "your_email@example.com"

# 添加 SSH 密钥到 GitHub
# 1. 复制公钥内容：cat ~/.ssh/id_ed25519.pub
# 2. GitHub → Settings → SSH and GPG keys → New SSH key
# 3. 粘贴公钥并保存

# 使用 SSH 地址
git remote set-url origin git@github.com:你的用户名/仓库名.git
git push -u origin main
```

### 方法二：使用 GitHub Desktop

1. 下载并安装 [GitHub Desktop](https://desktop.github.com/)
2. 登录 GitHub 账号
3. File → Add Local Repository → 选择项目目录
4. 填写提交信息，点击 "Commit to main"
5. 点击 "Publish repository" 上传到 GitHub

## 上传到 Gitee

### 方法一：使用命令行

#### 步骤 1：创建 Gitee 仓库

1. 访问 [Gitee](https://gitee.com) 并登录
2. 点击右上角 "+" → "新建仓库"
3. 填写仓库信息：
   - **仓库名称**: `douban-movie-spider`
   - **仓库介绍**: `豆瓣电影信息爬虫系统`
   - **是否开源**: 选择公开或私有
   - **不要勾选** "使用Readme文件初始化这个仓库"
4. 点击 "创建"

#### 步骤 2：初始化并推送

```bash
# 如果还没有初始化 Git
git init
git add .
git commit -m "Initial commit: 豆瓣电影爬虫项目"
git branch -M main

# 添加 Gitee 远程仓库
git remote add origin https://gitee.com/你的用户名/仓库名.git

# 推送到 Gitee
git push -u origin main
```

**注意**：首次推送可能需要输入 Gitee 账号密码。

### 方法二：使用 Gitee 网页导入

1. 如果项目已经在 GitHub，可以在 Gitee 使用"导入仓库"功能
2. Gitee → 右上角 "+" → "导入仓库"
3. 输入 GitHub 仓库地址
4. 点击导入

## 后续更新

当代码有修改时，按以下步骤更新：

```bash
# 1. 查看修改状态
git status

# 2. 添加修改的文件
git add .

# 3. 提交更改（写清楚修改内容）
git commit -m "修复了爬虫解析问题"

# 4. 推送到远程仓库
git push
```

### 提交信息规范

建议使用清晰的提交信息：
- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `refactor: 代码重构`
- `style: 代码格式调整`

## 项目分发

### 方式一：直接分享仓库链接

将仓库链接分享给其他人：
- GitHub: `https://github.com/你的用户名/仓库名`
- Gitee: `https://gitee.com/你的用户名/仓库名`

### 方式二：创建 Release 版本

1. **GitHub**:
   - 仓库页面 → Releases → Create a new release
   - 填写版本号（如 v1.0.0）和描述
   - 上传源代码压缩包（可选）

2. **Gitee**:
   - 仓库页面 → 发行版 → 创建发行版
   - 填写版本信息和附件

### 方式三：导出为 ZIP

```bash
# 在项目根目录执行
# Windows PowerShell
Compress-Archive -Path * -DestinationPath ../douban-movie-spider.zip -Exclude venv,__pycache__

# 或手动压缩，排除 venv 和 __pycache__ 目录
```

## 其他人如何使用

### 1. 克隆项目

```bash
# 从 GitHub 克隆
git clone https://github.com/你的用户名/仓库名.git

# 从 Gitee 克隆
git clone https://gitee.com/你的用户名/仓库名.git

# 进入项目目录
cd 仓库名
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat

# 安装依赖
pip install -r requirements.txt
```

### 3. 运行项目

```bash
python main.py
```

## 常见问题

### Q1: 推送时提示 "remote: Support for password authentication was removed"

**解决方案**：使用 Personal Access Token 或 SSH 密钥

### Q2: 如何同时推送到 GitHub 和 Gitee？

```bash
# 添加两个远程仓库
git remote add github https://github.com/用户名/仓库名.git
git remote add gitee https://gitee.com/用户名/仓库名.git

# 分别推送
git push github main
git push gitee main

# 或使用脚本同时推送
git push github main && git push gitee main
```

### Q3: 如何更新远程仓库地址？

```bash
# 查看当前远程仓库
git remote -v

# 修改远程仓库地址
git remote set-url origin 新的仓库地址
```

### Q4: 忘记提交某些文件怎么办？

```bash
# 添加遗漏的文件
git add 文件名

# 提交
git commit -m "添加遗漏的文件"

# 推送
git push
```

### Q5: 如何回退到之前的版本？

```bash
# 查看提交历史
git log

# 回退到指定提交（保留修改）
git reset --soft 提交ID

# 回退到指定提交（丢弃修改）
git reset --hard 提交ID
```

## 最佳实践

1. **定期提交**：不要等到所有功能完成才提交，应该经常提交
2. **清晰的提交信息**：每次提交都要写清楚做了什么
3. **使用分支**：开发新功能时创建新分支，完成后合并到主分支
4. **更新 README**：项目有重大更新时，记得更新 README.md
5. **添加 LICENSE**：如果项目要开源，添加许可证文件

## 相关资源

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 帮助文档](https://docs.github.com/)
- [Gitee 帮助文档](https://gitee.com/help)
- [Git 常用命令速查](https://education.github.com/git-cheat-sheet-education.pdf)

---

**提示**：如果遇到问题，可以查看项目的 Issues 或联系项目维护者。

