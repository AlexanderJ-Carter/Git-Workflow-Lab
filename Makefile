# ============================================
# Git Workflow Lab - Makefile
# ============================================

.PHONY: help install build clean docs docs-clean docs-serve test lint docker-up docker-down docker-logs fix-quotes

# 默认目标
help:
	@echo "Git Workflow Lab - 可用命令:"
	@echo ""
	@echo "  安装与构建:"
	@echo "    install          安装 Python 依赖"
	@echo "    build            构建静态网站 (_site/)"
	@echo "    clean            清理构建输出"
	@echo ""
	@echo "  文档:"
	@echo "    docs             构建 Sphinx 文档"
	@echo "    docs-clean       清理文档构建"
	@echo "    docs-serve       本地预览文档 (http://localhost:8000)"
	@echo ""
	@echo "  Docker:"
	@echo "    docker-up        启动本地实验环境"
	@echo "    docker-down      停止本地实验环境"
	@echo "    docker-logs      查看服务日志"
	@echo ""
	@echo "  代码质量:"
	@echo "    test             运行测试"
	@echo "    lint             代码检查"
	@echo "    fix-quotes       修复中文引号"
	@echo ""

# ============================================
# 安装与构建
# ============================================

install:
	pip install -r requirements-build.txt
	pip install -r docs-requirements.txt

build:
	python scripts/build-site.py
	@echo "✅ 网站构建完成: _site/"

clean:
	rm -rf _site/
	rm -rf __pycache__/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "✅ 清理完成"

# ============================================
# Sphinx 文档
# ============================================

docs:
	cd docs-sphinx && make html
	@echo "✅ 文档构建完成: docs-sphinx/_build/html/"

docs-clean:
	cd docs-sphinx && make clean
	@echo "✅ 文档清理完成"

docs-serve:
	@echo "📚 启动文档服务器: http://localhost:8000"
	cd docs-sphinx/_build/html && python -m http.server 8000

# ============================================
# Docker 服务
# ============================================

docker-up:
	@if [ ! -f .env ]; then \
		echo "❌ 错误: .env 文件不存在"; \
		echo "请复制 .env.example 为 .env 并配置必要的环境变量"; \
		exit 1; \
	fi
	docker-compose up -d
	@echo ""
	@echo "✅ 服务已启动:"
	@echo "  - 教程网站: http://localhost:8081"
	@echo "  - Web 终端: http://localhost:8080"
	@echo "  - Gitea:    http://localhost:3000"

docker-down:
	docker-compose down
	@echo "✅ 服务已停止"

docker-logs:
	docker-compose logs -f

docker-restart: docker-down docker-up

# ============================================
# 代码质量
# ============================================

test:
	@echo "运行测试..."
	python -m pytest tests/ -v --cov=. --cov-report=html

lint:
	@echo "代码检查..."
	python -m flake8 scripts/ --max-line-length=100
	python -m black --check scripts/
	python -m mypy scripts/

fix-quotes:
	python scripts/fix-quotes.py

# ============================================
# 发布
# ============================================

release-patch:
	@echo "创建 patch 版本发布..."
	bump2version patch
	git push --tags

release-minor:
	@echo "创建 minor 版本发布..."
	bump2version minor
	git push --tags

release-major:
	@echo "创建 major 版本发布..."
	bump2version major
	git push --tags

# ============================================
# 开发工具
# ============================================

watch:
	@echo "👀 监听文件变化并自动构建..."
	@pip install watchdog 2>/dev/null
	watchmedo shell-command -p "*.md;*.html;*.css;*.js" -R -c "make build" docs/ site/

format:
	@echo "格式化代码..."
	python -m black scripts/
	python -m isort scripts/
	@echo "✅ 代码格式化完成"

security-check:
	@echo "🔒 安全检查..."
	pip install bandit safety
	bandit -r scripts/
	safety check
