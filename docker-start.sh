#!/bin/bash

echo "🐳 启动 NeuraFlow Docker 容器..."

# 检查 Docker 是否运行
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker 未启动，请先启动 Docker 服务"
    exit 1
fi

# 检查 docker-compose 是否安装
if ! command -v docker-compose >/dev/null 2>&1; then
    echo "❌ docker-compose 未安装，正在尝试使用 docker compose..."
    if ! docker compose version >/dev/null 2>&1; then
        echo "❌ docker compose 也不可用，请安装 Docker Compose"
        exit 1
    fi
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# 构建并启动容器
echo "📦 构建并启动容器..."
$DOCKER_COMPOSE up --build -d

# 检查启动状态
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ NeuraFlow 启动成功！"
    echo "🌐 前端访问地址: http://localhost:3000"
    echo "🔧 后端API地址: http://localhost:8000"
    echo "📋 查看容器状态: $DOCKER_COMPOSE ps"
    echo "📜 查看日志: $DOCKER_COMPOSE logs -f"
    echo "🛑 停止服务: $DOCKER_COMPOSE down"
else
    echo "❌ 启动失败，请检查错误信息"
    exit 1
fi