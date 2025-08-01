# Music Web - 音乐网站

一个基于 FastAPI + Vue3 的现代化音乐网站，参考 [feedmusic.com](http://www.feedmusic.com/) 进行设计和开发。

## 项目结构

```
music_web/
├── backend/          # FastAPI 后端
│   ├── app/         # 应用核心代码
│   ├── database/    # 数据库相关
│   ├── models/      # 数据模型
│   ├── routes/      # API 路由
│   └── requirements.txt
├── frontend/        # Vue3 前端
│   ├── src/        # 源代码
│   ├── public/     # 静态资源
│   └── package.json
└── README.md
```

## 核心功能

### 前端功能
1. **第一屏 (Introduction)**
   - 动态背景效果
   - 文字滚动动画
   - 顶部导航栏（带进度条和快捷键）
   - 用户登录/注册界面

2. **第二屏 (News)**
   - 响应式网格布局（PC: 3列，移动端: 1列）
   - 新闻卡片展示（图片、标题、描述、创作者）
   - "更多"按钮分页加载

3. **交互体验**
   - 平滑屏幕切换效果
   - 响应式设计适配多设备

### 后端功能
1. **用户系统**
   - 用户注册/登录/登出
   - 密码加密存储
   - JWT 身份验证

2. **新闻管理**
   - 新闻 CRUD 操作
   - 图片上传功能
   - 分页查询接口
   - 创作者关联

## 技术栈

- **后端**: FastAPI + SQLite3 + SQLAlchemy
- **前端**: Vue3 + Vite + TypeScript
- **数据库**: SQLite3
- **身份验证**: JWT
- **版本控制**: Git

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
# 本地访问
uvicorn app.main:app --reload
# 或局域网访问
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 前端启动
```bash
cd frontend
npm install
# 复制环境配置文件
cp .env.example .env
# 编辑 .env 文件，设置正确的 API 地址
npm run dev
```

### 局域网访问配置
1. **后端配置**: 使用 `--host 0.0.0.0` 启动后端服务
2. **前端配置**: 
   - 编辑 `frontend/.env` 文件
   - 将 `VITE_API_BASE_URL` 设置为服务器的IP地址，如: `VITE_API_BASE_URL=http://192.168.1.100:8000`
3. **访问地址**: 
   - 前端: `http://your-server-ip:3000`
   - 后端API: `http://your-server-ip:8000`

## 数据库表结构

### 用户表 (users)
- id: 主键
- username: 用户名
- email: 邮箱
- password_hash: 加密密码
- created_at: 创建时间

### 新闻表 (news)
- id: 主键
- title: 标题
- description: 描述
- image_url: 图片地址
- creator: 创作者（关联用户名）
- created_at: 创建时间
- updated_at: 更新时间

## 开发进度

### ✅ 已完成功能
- [x] 项目结构搭建和环境配置
- [x] FastAPI 后端 API 开发完成
- [x] Vue3 前端页面开发完成
- [x] SQLite3 数据库设计和实现
- [x] JWT 用户认证系统
- [x] 新闻管理 CRUD 功能
- [x] 响应式界面设计
- [x] 管理后台完整功能
- [x] 跨域和网络访问配置
- [x] 调试工具和测试脚本

### 🎯 核心特性
- **动态介绍页面** - 背景动画、文字滚动效果
- **新闻展示系统** - 响应式网格布局、卡片设计
- **用户认证** - 注册、登录、JWT验证
- **管理后台** - 新闻创建、编辑、删除、图片选择
- **权限控制** - 用户只能管理自己的内容
- **网络部署** - 支持局域网和远程访问

### 📱 技术亮点
- **前端**: Vue3 + TypeScript + Pinia + Vite
- **后端**: FastAPI + SQLAlchemy + JWT + bcrypt
- **数据库**: SQLite3 (可轻松迁移到 PostgreSQL/MySQL)
- **部署**: Docker-ready，支持一键启动脚本
- **安全**: 密码加密、Token验证、CORS配置