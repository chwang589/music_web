# Music Web 部署指南

## 🚀 一键启动 (推荐)

```bash
./start-lan.sh
```

## 📋 手动启动步骤

### 1. 安装依赖

**后端依赖:**
```bash
cd backend
pip install -r requirements.txt
```

**前端依赖:**
```bash
cd frontend
npm install
```

### 2. 配置环境

**获取本机IP地址:**
```bash
hostname -I | awk '{print $1}'
# 例如: 192.168.5.52
```

**配置前端环境:**
```bash
cd frontend
cp .env.example .env
# 编辑 .env 文件，设置 VITE_API_BASE_URL=http://你的IP:8000
```

### 3. 启动服务

**启动后端 (终端1):**
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**启动前端 (终端2):**
```bash
cd frontend
npm run dev
```

### 4. 访问地址

- **前端**: http://你的IP:3000
- **后端API**: http://你的IP:8000
- **API文档**: http://你的IP:8000/docs

## 🛠 故障排查

### 后端启动失败
```bash
# 检查Python环境
python --version
# 检查依赖
pip list | grep uvicorn
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 前端启动失败
```bash
# 检查Node.js版本
node --version
npm --version
# 清理并重新安装
rm -rf node_modules package-lock.json
npm install
```

### 端口被占用
```bash
# 检查端口占用
netstat -tuln | grep 8000  # 后端端口
netstat -tuln | grep 3000  # 前端端口
# 杀死占用进程
sudo lsof -t -i:8000 | xargs kill -9
sudo lsof -t -i:3000 | xargs kill -9
```

### 跨域问题
- 确保后端已启动且可访问
- 检查 `.env` 文件中的 API 地址是否正确
- 确认防火墙没有阻止端口访问

## 🔧 生产环境部署

**后端 (使用 gunicorn):**
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**前端 (构建静态文件):**
```bash
npm run build
# 使用 nginx 或其他静态文件服务器托管 dist/ 目录
```

## 📱 移动端访问

确保移动设备与服务器在同一局域网内，然后通过浏览器访问:
- http://服务器IP:3000

## 🔐 安全注意事项

- 生产环境中请更改 `backend/app/core/security.py` 中的 `SECRET_KEY`
- 更新 CORS 配置，移除 `"*"` 通配符
- 考虑使用 HTTPS 和反向代理