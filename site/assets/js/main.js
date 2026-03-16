// Git Workflow Lab - 主脚本

function updateThemeIcon(theme) {
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    }
}

function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme');

    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);
    } else if (prefersDark.matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon('dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', nextTheme);
            localStorage.setItem('theme', nextTheme);
            updateThemeIcon(nextTheme);
        });
    }
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener('click', (event) => {
            const targetSelector = anchor.getAttribute('href');
            const target = targetSelector ? document.querySelector(targetSelector) : null;

            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        });
    });
}

function initSidebarActive() {
    const sections = document.querySelectorAll('h2[id]');
    const navLinks = document.querySelectorAll('.lesson-nav-list a');

    if (sections.length === 0 || navLinks.length === 0) {
        return;
    }

    window.addEventListener('scroll', () => {
        let currentSectionId = '';

        sections.forEach((section) => {
            if (window.scrollY >= section.offsetTop - 100) {
                currentSectionId = section.getAttribute('id');
            }
        });

        navLinks.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${currentSectionId}`);
        });
    });
}

function initCodeCopy() {
    document.querySelectorAll('pre').forEach((pre) => {
        const codeElement = pre.querySelector('code');
        if (!codeElement) {
            return;
        }

        const button = document.createElement('button');
        button.className = 'copy-button';
        button.textContent = '复制';
        pre.style.position = 'relative';
        pre.appendChild(button);

        button.addEventListener('click', async () => {
            await navigator.clipboard.writeText(codeElement.textContent);
            button.textContent = '已复制!';
            setTimeout(() => {
                button.textContent = '复制';
            }, 2000);
        });
    });
}

function initMobileNav() {
    const nav = document.querySelector('.nav');
    const navLinks = document.querySelector('.nav-links');

    if (!nav || !navLinks) {
        return;
    }

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

    const mediaQuery = window.matchMedia('(max-width: 768px)');
    function handleMediaChange(eventOrQuery) {
        if (eventOrQuery.matches) {
            hamburger.style.display = 'block';
            navLinks.style.display = 'none';
        } else {
            hamburger.style.display = 'none';
            navLinks.style.display = 'flex';
            navLinks.style.position = '';
            navLinks.style.top = '';
            navLinks.style.left = '';
            navLinks.style.right = '';
            navLinks.style.background = '';
            navLinks.style.flexDirection = '';
            navLinks.style.padding = '';
            navLinks.style.borderBottom = '';
        }
    }

    if (typeof mediaQuery.addEventListener === 'function') {
        mediaQuery.addEventListener('change', handleMediaChange);
    } else if (typeof mediaQuery.addListener === 'function') {
        mediaQuery.addListener(handleMediaChange);
    }

    handleMediaChange(mediaQuery);

    hamburger.addEventListener('click', () => {
        const isVisible = navLinks.style.display === 'flex';
        navLinks.style.display = isVisible ? 'none' : 'flex';
        navLinks.style.position = 'absolute';
        navLinks.style.top = '64px';
        navLinks.style.left = '0';
        navLinks.style.right = '0';
        navLinks.style.background = 'var(--bg-primary)';
        navLinks.style.flexDirection = 'column';
        navLinks.style.padding = '16px';
        navLinks.style.borderBottom = '1px solid var(--border-color)';
    });

    nav.insertBefore(hamburger, nav.querySelector('.theme-toggle'));
}

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSmoothScroll();
    initSidebarActive();
    initCodeCopy();
    initMobileNav();
});
