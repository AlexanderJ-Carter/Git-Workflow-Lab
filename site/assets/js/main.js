// Git Workflow Lab - 主脚本

// 主题切换
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');

    // 设置初始主题
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else if (prefersDark.matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon('dark');
    }

    // 切换主题
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }
}

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

// 平滑滚动
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// 侧边栏活动项
function initSidebarActive() {
    const sections = document.querySelectorAll('h2[id]');
    const navLinks = document.querySelectorAll('.lesson-nav-list a');

    if (sections.length === 0 || navLinks.length === 0) return;

    window.addEventListener('scroll', () => {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (scrollY >= sectionTop - 100) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
}

// 代码复制
function initCodeCopy() {
    document.querySelectorAll('pre').forEach(pre => {
        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = '复制';

        pre.style.position = 'relative';
        pre.appendChild(button);

        button.addEventListener('click', async () => {
            const code = pre.querySelector('code').textContent;
            await navigator.clipboard.writeText(code);
            button.textContent = '已复制!';
            setTimeout(() => {
                button.textContent = '复制';
            }, 2000);
        });
    });
}

// 移动端导航
function initMobileNav() {
    const nav = document.querySelector('.nav');
    const navLinks = document.querySelector('.nav-links');

    // 创建汉堡菜单按钮
    const hamburger = document.createElement('button');
    hamburger.className = 'hamburger';
    hamburger.innerHTML = '☰';
    hamburger.style.cssText = `
        display: none;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        padding: 8px;
    `;

    // 响应式显示
    const mediaQuery = window.matchMedia('(max-width: 768px)');
    function handleMediaChange(e) {
        if (e.matches) {
            hamburger.style.display = 'block';
            navLinks.style.display = 'none';
        } else {
            hamburger.style.display = 'none';
            navLinks.style.display = 'flex';
        }
    }

    mediaQuery.addListener(handleMediaChange);
    handleMediaChange(mediaQuery);

    hamburger.addEventListener('click', () => {
        const isVisible = navLinks.style.display === 'flex';
        navLinks.style.display = isVisible ? 'none' : 'flex';
        navLinks.style.cssText = `
            display: ${isVisible ? 'none' : 'flex'};
            position: absolute;
            top: 64px;
            left: 0;
            right: 0;
            background: var(--bg-primary);
            flex-direction: column;
            padding: 16px;
            border-bottom: 1px solid var(--border-color);
        `;
    });

    nav.insertBefore(hamburger, nav.querySelector('.theme-toggle'));
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSmoothScroll();
    initSidebarActive();
    initCodeCopy();
    initMobileNav();
});
