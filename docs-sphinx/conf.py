# ============================================
# Git Workflow Lab - Sphinx 文档配置
# ============================================

import os
import sys
from datetime import datetime

# 项目信息
project = 'Git Workflow Lab'
author = 'Git Workflow Lab Contributors'
copyright = f'{datetime.now().year}, {author}'
release = '1.2.1'

# 扩展配置
extensions = [
    'myst_parser',           # Markdown 支持
    'sphinx_copybutton',     # 代码复制按钮
    'sphinxcontrib.mermaid', # Mermaid 流程图
    'sphinx.ext.autodoc',    # 自动文档
    'sphinx.ext.viewcode',   # 源码链接
    'sphinx.ext.napoleon',   # Google/NumPy 风格 docstring
]

# 源文件配置
source_suffix = {
    '.md': 'markdown',
    '.rst': 'restructuredtext',
}
master_doc = 'index'

# 主题配置
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'style_nav_header_background': '#4a90d9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# 模板路径
templates_path = ['_templates']

# 静态文件
html_static_path = ['_static']

# 忽略模式
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '*.tmp',
    'site',
    '.venv',
]

# Markdown 配置
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'dollarmath',
    'fieldlist',
    'html_admonition',
    'html_image',
    'linkify',
    'replacements',
    'smartquotes',
    'strikethrough',
    'substitution',
    'tasklist',
]

myst_fence_as_directive = [
    'mermaid',
    'note',
    'warning',
]

# 代码高亮
pygments_style = 'sphinx'
highlight_language = 'none'

# 国际化
locale_dirs = ['locale/']
gettext_compact = False

# HTML 输出配置
html_logo = '_static/img/logo.png'
html_favicon = '_static/img/favicon.ico'
html_last_updated_fmt = '%Y-%m-%d %H:%M'
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True

# 自定义 CSS/JS
def setup(app):
    app.add_css_file('css/custom.css')
    app.add_js_file('js/custom.js')

# Mermaid 配置
mermaid_version = '10.6.1'
mermaid_init_js = "mermaid.initialize({startOnLoad:true,theme:'neutral'});"
