/**
 * Git Workflow Lab - 主脚本
 * @description 提供学习进度管理、主题切换、页面动画等功能
 * @version 2.0.0
 * @author Git Workflow Lab Team
 */

(function () {
    'use strict';

    // ============================================
    // 工具函数模块
    // ============================================

    /**
     * 防抖函数 - 限制函数在指定时间内的执行频率
     * @template {Function} F
     * @param {F} func - 要防抖的函数
     * @param {number} wait - 等待时间（毫秒）
     * @returns {F} 防抖后的函数
     */
    function debounce(func, wait = 300) {
        let timeoutId = null;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), wait);
        };
    }

    /**
     * 节流函数 - 确保函数在指定时间间隔内最多执行一次
     * @template {Function} F
     * @param {F} func - 要节流的函数
     * @param {number} limit - 时间间隔（毫秒）
     * @returns {F} 节流后的函数
     */
    function throttle(func, limit = 300) {
        let inThrottle = false;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * 安全执行函数，捕获异常并提供降级处理
     * @template T
     * @param {Function} fn - 要执行的函数
     * @param {T} fallback - 降级返回值
     * @param {string} [errorMsg] - 错误信息
     * @returns {T}
     */
    function safeExecute(fn, fallback, errorMsg = '') {
        try {
            const result = fn();
            return result !== undefined ? result : fallback;
        } catch (error) {
            console.warn(`[SafeExecute] Error${errorMsg ? `: ${errorMsg}` : ''}:`, error);
            return fallback;
        }
    }

    /**
     * 检查浏览器功能支持
     * @param {string} feature - 功能名称
     * @returns {boolean}
     */
    function supportsFeature(feature) {
        const features = {
            localStorage: (() => {
                try {
                    const test = '__storage_test__';
                    localStorage.setItem(test, test);
                    localStorage.removeItem(test);
                    return true;
                } catch (e) {
                    return false;
                }
            })(),
            IntersectionObserver: 'IntersectionObserver' in window,
            clipboard: 'clipboard' in navigator,
            fullscreen: 'fullscreenEnabled' in document || 'webkitFullscreenEnabled' in document
        };
        return features[feature] ?? false;
    }

    // ============================================
    // 学习进度管理模块
    // ============================================

    /**
     * 学习进度管理
     * @namespace LearningProgress
     */
    const LearningProgress = {
        /** @type {string} */
        STORAGE_KEY: 'git-workflow-lab-progress',

        /**
         * 获取存储的学习进度
         * @returns {Object} 进度数据对象
         */
        getProgress() {
            if (!supportsFeature('localStorage')) {
                return {};
            }
            return safeExecute(() => {
                const data = localStorage.getItem(this.STORAGE_KEY);
                return data ? JSON.parse(data) : {};
            }, {});
        },

        /**
         * 保存学习进度
         * @param {string} lessonId - 课程ID
         * @param {boolean} completed - 是否完成
         */
        saveProgress(lessonId, completed) {
            if (!supportsFeature('localStorage')) {
                return;
            }
            try {
                const progress = this.getProgress();
                progress[lessonId] = {
                    completed,
                    timestamp: Date.now()
                };
                localStorage.setItem(this.STORAGE_KEY, JSON.stringify(progress));
            } catch (error) {
                console.warn('[LearningProgress] Failed to save progress:', error);
            }
        },

        /**
         * 检查课程是否完成
         * @param {string} lessonId - 课程ID
         * @returns {boolean}
         */
        isCompleted(lessonId) {
            const progress = this.getProgress();
            return progress[lessonId]?.completed || false;
        },

        /**
         * 获取已完成的课程数量
         * @returns {number}
         */
        getCompletedCount() {
            const progress = this.getProgress();
            return Object.values(progress).filter(p => p.completed).length;
        },

        /**
         * 初始化学习进度显示
         */
        init() {
            safeExecute(() => {
                document.querySelectorAll('.lesson-card').forEach(card => {
                    const lessonId = card.dataset.lessonId ||
                        card.href?.split('/').pop()?.replace('.html', '');
                    if (lessonId && this.isCompleted(lessonId)) {
                        card.classList.add('completed');
                    }
                });
            }, undefined, 'LearningProgress.init');
        }
    };

    // ============================================
    // 主题管理模块
    // ============================================

    /**
     * 主题管理
     * @namespace ThemeManager
     */
    const ThemeManager = {
        /** @type {string} */
        STORAGE_KEY: 'theme',

        /**
         * 更新主题图标
         * @param {string} theme - 当前主题
         */
        updateIcon(theme) {
            const themeToggle = document.querySelector('.theme-toggle');
            if (!themeToggle) return;

            const icon = theme === 'dark'
                ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
                : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

            themeToggle.innerHTML = icon;
        },

        /**
         * 初始化主题功能
         */
        init() {
            try {
                const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
                const savedTheme = localStorage.getItem(this.STORAGE_KEY);

                if (savedTheme) {
                    document.documentElement.setAttribute('data-theme', savedTheme);
                    this.updateIcon(savedTheme);
                } else if (prefersDark.matches) {
                    document.documentElement.setAttribute('data-theme', 'dark');
                    this.updateIcon('dark');
                }

                // 监听系统主题变化
                prefersDark.addEventListener('change', (e) => {
                    if (!localStorage.getItem(this.STORAGE_KEY)) {
                        document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
                        this.updateIcon(e.matches ? 'dark' : 'light');
                    }
                });

                // 使用事件委托绑定主题切换
                document.addEventListener('click', (e) => {
                    const toggle = e.target.closest('.theme-toggle');
                    if (!toggle) return;

                    const currentTheme = document.documentElement.getAttribute('data-theme');
                    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
                    document.documentElement.setAttribute('data-theme', nextTheme);
                    localStorage.setItem(this.STORAGE_KEY, nextTheme);
                    this.updateIcon(nextTheme);
                });
            } catch (error) {
                console.warn('[ThemeManager] Initialization failed:', error);
            }
        }
    };

    // ============================================
    // 平滑滚动模块
    // ============================================

    /**
     * 平滑滚动管理
     * @namespace SmoothScroll
     */
    const SmoothScroll = {
        /**
         * 初始化平滑滚动
         */
        init() {
            // 使用事件委托处理所有锚点链接
            document.addEventListener('click', (e) => {
                const anchor = e.target.closest('a[href^="#"]');
                if (!anchor) return;

                const targetSelector = anchor.getAttribute('href');
                if (!targetSelector || targetSelector === '#') return;

                const target = document.querySelector(targetSelector);
                if (!target) return;

                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });

                // 更新URL但不触发滚动
                history.pushState(null, '', targetSelector);
            });
        }
    };

    // ============================================
    // 滚动动画模块
    // ============================================

    /**
     * 滚动动画管理
     * @namespace ScrollAnimation
     */
    const ScrollAnimation = {
        /** @type {IntersectionObserver|null} */
        observer: null,

        /**
         * 初始化滚动动画
         */
        init() {
            if (!supportsFeature('IntersectionObserver')) {
                // 降级处理：直接显示所有元素
                document.querySelectorAll('.info-card, .stat-item').forEach(el => {
                    el.style.opacity = '1';
                    el.style.transform = 'none';
                });
                return;
            }

            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                        this.observer?.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            document.querySelectorAll('.info-card, .stat-item').forEach((el, index) => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = `opacity 0.5s ease ${index * 0.1}s, transform 0.5s ease ${index * 0.1}s`;
                this.observer.observe(el);
            });
        },

        /**
         * 销毁观察者
         */
        destroy() {
            this.observer?.disconnect();
        }
    };

    // ============================================
    // 侧边栏激活状态模块
    // ============================================

    /**
     * 侧边栏激活状态管理
     * @namespace SidebarActive
     */
    const SidebarActive = {
        /** @type {Function|null} */
        handleScroll: null,

        /**
         * 初始化侧边栏激活状态
         */
        init() {
            const sections = document.querySelectorAll('h2[id]');
            const navLinks = document.querySelectorAll('.lesson-nav-list a');

            if (sections.length === 0 || navLinks.length === 0) {
                return;
            }

            // 使用节流处理滚动事件
            this.handleScroll = throttle(() => {
                let currentSectionId = '';

                sections.forEach((section) => {
                    const rect = section.getBoundingClientRect();
                    if (rect.top <= 150) {
                        currentSectionId = section.getAttribute('id');
                    }
                });

                navLinks.forEach((link) => {
                    const isActive = link.getAttribute('href') === `#${currentSectionId}`;
                    link.classList.toggle('active', isActive);
                });
            }, 100);

            window.addEventListener('scroll', this.handleScroll, { passive: true });
            // 初始检查
            this.handleScroll();
        },

        /**
         * 销毁侧边栏激活状态
         */
        destroy() {
            if (this.handleScroll) {
                window.removeEventListener('scroll', this.handleScroll);
            }
        }
    };

    // ============================================
    // 代码复制模块
    // ============================================

    /**
     * 代码复制功能
     * @namespace CodeCopy
     */
    const CodeCopy = {
        /** @type {HTMLElement[]} */
        buttons: [],

        /**
         * 初始化代码复制功能
         */
        init() {
            if (!supportsFeature('clipboard')) {
                // 降级处理：不显示复制按钮
                return;
            }

            // 使用事件委托处理点击
            document.addEventListener('click', async (e) => {
                const button = e.target.closest('.copy-button');
                if (!button) return;

                const pre = button.closest('pre');
                const codeElement = pre?.querySelector('code');
                if (!codeElement) return;

                try {
                    await navigator.clipboard.writeText(codeElement.textContent);
                    button.textContent = '已复制!';
                    setTimeout(() => {
                        button.textContent = '复制';
                    }, 2000);
                } catch (error) {
                    console.warn('[CodeCopy] Failed to copy:', error);
                    button.textContent = '复制失败';
                }
            });

            // 为所有 pre 元素添加复制按钮
            this.createButtons();
        },

        /**
         * 创建复制按钮
         */
        createButtons() {
            document.querySelectorAll('pre').forEach(pre => {
                if (pre.querySelector('.copy-button')) return;

                const button = document.createElement('button');
                button.className = 'copy-button';
                button.textContent = '复制';
                pre.style.position = 'relative';
                pre.appendChild(button);
                this.buttons.push(button);
            });
        }
    };

    // ============================================
    // 移动端导航模块
    // ============================================

    /**
     * 移动端导航管理
     * @namespace MobileNav
     */
    const MobileNav = {
        /** @type {HTMLElement|null} */
        hamburger: null,

        /**
         * 初始化移动端导航
         */
        init() {
            const nav = document.querySelector('.nav');
            const navLinks = document.querySelector('.nav-links');

            if (!nav || !navLinks) {
                return;
            }

            this.hamburger = document.createElement('button');
            this.hamburger.className = 'hamburger';
            this.hamburger.innerHTML = '☰';
            this.hamburger.setAttribute('aria-label', '菜单');
            this.hamburger.style.cssText = `
                display: none;
                background: none;
                border: none;
                font-size: 24px;
                cursor: pointer;
                padding: 8px;
                color: inherit;
            `;

            const mediaQuery = window.matchMedia('(max-width: 768px)');
            const handleMediaChange = (query) => {
                if (query.matches) {
                    this.hamburger.style.display = 'block';
                    navLinks.style.display = 'none';
                } else {
                    this.hamburger.style.display = 'none';
                    navLinks.style.display = 'flex';
                    this.resetNavStyles(navLinks);
                }
            };

            if (typeof mediaQuery.addEventListener === 'function') {
                mediaQuery.addEventListener('change', handleMediaChange);
            } else if (typeof mediaQuery.addListener === 'function') {
                mediaQuery.addListener(handleMediaChange);
            }

            handleMediaChange(mediaQuery);

            this.hamburger.addEventListener('click', () => {
                const isVisible = navLinks.style.display === 'flex';
                navLinks.style.display = isVisible ? 'none' : 'flex';

                if (!isVisible) {
                    navLinks.style.position = 'absolute';
                    navLinks.style.top = '64px';
                    navLinks.style.left = '0';
                    navLinks.style.right = '0';
                    navLinks.style.background = 'var(--bg-primary)';
                    navLinks.style.flexDirection = 'column';
                    navLinks.style.padding = '16px';
                    navLinks.style.borderBottom = '1px solid var(--border-color)';
                } else {
                    this.resetNavStyles(navLinks);
                }
            });

            nav.insertBefore(this.hamburger, nav.querySelector('.theme-toggle'));
        },

        /**
         * 重置导航样式
         * @param {HTMLElement} navLinks
         */
        resetNavStyles(navLinks) {
            navLinks.style.position = '';
            navLinks.style.top = '';
            navLinks.style.left = '';
            navLinks.style.right = '';
            navLinks.style.background = '';
            navLinks.style.flexDirection = '';
            navLinks.style.padding = '';
            navLinks.style.borderBottom = '';
        }
    };

    // ============================================
    // 页面切换过渡模块
    // ============================================

    /**
     * 页面切换过渡动画
     * @namespace PageTransition
     */
    const PageTransition = {
        /** @type {HTMLElement|null} */
        overlay: null,

        /**
         * 初始化页面过渡
         */
        init() {
            // 创建过渡遮罩
            this.overlay = document.createElement('div');
            this.overlay.className = 'page-transition-overlay';
            this.overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: var(--bg-primary, #f5f5f5);
                z-index: 9999;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease, visibility 0.3s ease;
                pointer-events: none;
            `;
            document.body.appendChild(this.overlay);

            // 拦截链接点击实现过渡效果
            document.addEventListener('click', (e) => {
                const link = e.target.closest('a:not([href^="#"]):not([target="_blank"])');
                if (!link || link.hostname !== window.location.hostname) return;

                // 排除外部链接和特殊链接
                if (link.href.includes('#') || link.href.endsWith('.pdf')) return;

                e.preventDefault();
                this.transitionTo(link.href);
            });
        },

        /**
         * 执行页面过渡
         * @param {string} url - 目标URL
         */
        transitionTo(url) {
            if (!this.overlay) return;

            this.overlay.style.visibility = 'visible';
            this.overlay.style.opacity = '1';

            setTimeout(() => {
                window.location.href = url;
            }, 300);
        }
    };

    // ============================================
    // 滚动进度指示器模块
    // ============================================

    /**
     * 滚动进度指示器
     * @namespace ScrollProgress
     */
    const ScrollProgress = {
        /** @type {HTMLElement|null} */
        indicator: null,

        /**
         * 初始化滚动进度指示器
         */
        init() {
            // 仅在文章页面显示
            if (!document.querySelector('article, .content, .lesson-content')) {
                return;
            }

            this.indicator = document.createElement('div');
            this.indicator.className = 'scroll-progress-indicator';
            this.indicator.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 0%;
                height: 3px;
                background: linear-gradient(90deg, var(--primary, #4a90d9), var(--secondary, #7b68ee));
                z-index: 10000;
                transition: width 0.1s ease-out;
            `;
            document.body.appendChild(this.indicator);

            // 使用节流处理滚动事件
            const handleScroll = throttle(() => {
                const scrollTop = window.scrollY;
                const docHeight = document.documentElement.scrollHeight - window.innerHeight;
                const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
                this.indicator.style.width = `${progress}%`;
            }, 50);

            window.addEventListener('scroll', handleScroll, { passive: true });
        }
    };

    // ============================================
    // 回到顶部模块
    // ============================================

    /**
     * 回到顶部按钮
     * @namespace BackToTop
     */
    const BackToTop = {
        /** @type {HTMLElement|null} */
        button: null,

        /**
         * 初始化回到顶部按钮
         */
        init() {
            this.button = document.createElement('button');
            this.button.className = 'back-to-top';
            this.button.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M18 15l-6-6-6 6"/>
                </svg>
            `;
            this.button.setAttribute('aria-label', '回到顶部');
            this.button.style.cssText = `
                position: fixed;
                bottom: 30px;
                right: 30px;
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background: var(--primary, #4a90d9);
                color: white;
                border: none;
                cursor: pointer;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s ease, visibility 0.3s ease, transform 0.3s ease;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
            `;

            // 悬停效果
            this.button.addEventListener('mouseenter', () => {
                this.button.style.transform = 'scale(1.1)';
            });
            this.button.addEventListener('mouseleave', () => {
                this.button.style.transform = 'scale(1)';
            });

            // 点击事件
            this.button.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });

            document.body.appendChild(this.button);

            // 使用节流处理滚动事件
            const handleScroll = throttle(() => {
                const scrollTop = window.scrollY;
                const showButton = scrollTop > 300;

                this.button.style.opacity = showButton ? '1' : '0';
                this.button.style.visibility = showButton ? 'visible' : 'hidden';
            }, 100);

            window.addEventListener('scroll', handleScroll, { passive: true });
        }
    };

    // ============================================
    // 全屏阅读模式模块
    // ============================================

    /**
     * 全屏阅读模式
     * @namespace FullscreenReader
     */
    const FullscreenReader = {
        /** @type {HTMLElement|null} */
        button: null,
        /** @type {boolean} */
        isActive: false,

        /**
         * 初始化全屏阅读模式
         */
        init() {
            // 检查是否支持全屏
            if (!supportsFeature('fullscreen')) {
                return;
            }

            // 仅在文章页面显示
            if (!document.querySelector('article, .content, .lesson-content')) {
                return;
            }

            this.button = document.createElement('button');
            this.button.className = 'fullscreen-reader-toggle';
            this.button.innerHTML = `
                <svg class="icon-expand" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>
                </svg>
                <svg class="icon-collapse" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display: none;">
                    <path d="M4 14h6m0 0v6m0-6L3 21M20 10h-6m0 0V4m0 6l7-7"/>
                </svg>
            `;
            this.button.setAttribute('aria-label', '全屏阅读模式');
            this.button.style.cssText = `
                position: fixed;
                bottom: 30px;
                right: 90px;
                width: 40px;
                height: 40px;
                border-radius: 8px;
                background: var(--bg-secondary, #fff);
                color: var(--text-primary, #333);
                border: 1px solid var(--border-color, #ddd);
                cursor: pointer;
                opacity: 0.8;
                transition: opacity 0.3s ease, transform 0.3s ease;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                z-index: 9999;
                display: flex;
                align-items: center;
                justify-content: center;
            `;

            this.button.addEventListener('mouseenter', () => {
                this.button.style.opacity = '1';
                this.button.style.transform = 'scale(1.05)';
            });
            this.button.addEventListener('mouseleave', () => {
                this.button.style.opacity = '0.8';
                this.button.style.transform = 'scale(1)';
            });

            this.button.addEventListener('click', () => this.toggle());
            document.body.appendChild(this.button);

            // 监听ESC键退出全屏
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isActive) {
                    this.exit();
                }
            });

            // 监听全屏变化事件
            document.addEventListener('fullscreenchange', () => this.handleFullscreenChange());
            document.addEventListener('webkitfullscreenchange', () => this.handleFullscreenChange());
        },

        /**
         * 切换全屏模式
         */
        toggle() {
            if (this.isActive) {
                this.exit();
            } else {
                this.enter();
            }
        },

        /**
         * 进入全屏模式
         */
        enter() {
            try {
                const elem = document.documentElement;
                if (elem.requestFullscreen) {
                    elem.requestFullscreen();
                } else if (elem.webkitRequestFullscreen) {
                    elem.webkitRequestFullscreen();
                }
                this.isActive = true;
                this.updateButtonIcon();
            } catch (error) {
                console.warn('[FullscreenReader] Failed to enter fullscreen:', error);
            }
        },

        /**
         * 退出全屏模式
         */
        exit() {
            try {
                if (document.exitFullscreen) {
                    document.exitFullscreen();
                } else if (document.webkitExitFullscreen) {
                    document.webkitExitFullscreen();
                }
                this.isActive = false;
                this.updateButtonIcon();
            } catch (error) {
                console.warn('[FullscreenReader] Failed to exit fullscreen:', error);
            }
        },

        /**
         * 处理全屏变化
         */
        handleFullscreenChange() {
            this.isActive = !!(
                document.fullscreenElement ||
                document.webkitFullscreenElement
            );
            this.updateButtonIcon();
        },

        /**
         * 更新按钮图标
         */
        updateButtonIcon() {
            if (!this.button) return;

            const expandIcon = this.button.querySelector('.icon-expand');
            const collapseIcon = this.button.querySelector('.icon-collapse');

            if (expandIcon && collapseIcon) {
                expandIcon.style.display = this.isActive ? 'none' : 'block';
                collapseIcon.style.display = this.isActive ? 'block' : 'none';
            }

            this.button.setAttribute('aria-label', this.isActive ? '退出全屏' : '全屏阅读模式');
        }
    };

    // ============================================
    // 懒加载检测模块
    // ============================================

    /**
     * 懒加载检测
     * @namespace LazyLoadDetector
     */
    const LazyLoadDetector = {
        /** @type {IntersectionObserver|null} */
        observer: null,

        /**
         * 初始化懒加载检测
         */
        init() {
            if (!supportsFeature('IntersectionObserver')) {
                // 降级处理：立即加载所有图片
                document.querySelectorAll('img[data-src]').forEach(img => {
                    img.src = img.dataset.src;
                });
                return;
            }

            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        if (img.dataset.srcset) {
                            img.srcset = img.dataset.srcset;
                            img.removeAttribute('data-srcset');
                        }
                        this.observer?.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px'
            });

            document.querySelectorAll('img[data-src], img[data-srcset]').forEach(img => {
                this.observer.observe(img);
            });
        },

        /**
         * 销毁观察者
         */
        destroy() {
            this.observer?.disconnect();
        }
    };

    // ============================================
    // 动态样式模块
    // ============================================

    /**
     * 动态样式管理
     * @namespace StyleManager
     */
    const StyleManager = {
        /** @type {HTMLStyleElement|null} */
        styleElement: null,

        /**
         * 初始化动态样式
         */
        init() {
            this.styleElement = document.createElement('style');
            this.styleElement.textContent = `
                /* 动画类 */
                .animate-in {
                    opacity: 1 !important;
                    transform: translateY(0) !important;
                }

                /* 课程完成标记 */
                .lesson-card.completed {
                    position: relative;
                }
                .lesson-card.completed::after {
                    content: '\\2713';
                    position: absolute;
                    top: 12px;
                    right: 12px;
                    width: 24px;
                    height: 24px;
                    background: var(--success, #4caf50);
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                }

                /* 复制按钮 */
                .copy-button {
                    position: absolute;
                    top: 8px;
                    right: 8px;
                    padding: 4px 12px;
                    font-size: 12px;
                    background: var(--bg-secondary, #fff);
                    color: var(--text-secondary, #666);
                    border: 1px solid var(--border-color, #ddd);
                    border-radius: 4px;
                    cursor: pointer;
                    opacity: 0;
                    transition: opacity 0.2s ease, background 0.2s ease;
                }
                pre:hover .copy-button {
                    opacity: 1;
                }
                .copy-button:hover {
                    background: var(--primary, #4a90d9);
                    color: white;
                }

                /* 汉堡菜单按钮悬停效果 */
                .hamburger:hover {
                    opacity: 0.7;
                }

                /* 导航链接过渡效果 */
                .nav-links a {
                    transition: color 0.2s ease, background 0.2s ease;
                }

                /* 激活的侧边栏链接 */
                .lesson-nav-list a.active {
                    color: var(--primary, #4a90d9);
                    font-weight: 600;
                }

                /* 暗色主题适配 */
                @media (prefers-color-scheme: dark) {
                    .scroll-progress-indicator {
                        background: linear-gradient(90deg, #5ba3ec, #9b8aff);
                    }
                    .back-to-top, .fullscreen-reader-toggle {
                        background: var(--bg-secondary, #2d2d2d);
                    }
                }
            `;
            document.head.appendChild(this.styleElement);
        }
    };

    // ============================================
    // 初始化入口
    // ============================================

    /**
     * 初始化所有模块
     */
    function initialize() {
        // 初始化样式
        StyleManager.init();

        // 初始化各个模块
        ThemeManager.init();
        SmoothScroll.init();
        ScrollAnimation.init();
        SidebarActive.init();
        CodeCopy.init();
        MobileNav.init();
        PageTransition.init();
        ScrollProgress.init();
        BackToTop.init();
        FullscreenReader.init();
        LazyLoadDetector.init();

        // 初始化学习进度
        LearningProgress.init();
    }

    // 监听DOM加载完成
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initialize);
    } else {
        // DOM已经加载，直接初始化
        initialize();
    }

    // 暴露API到全局（保持向后兼容）
    window.GitWorkflowLab = {
        LearningProgress,
        ThemeManager,
        SmoothScroll,
        ScrollAnimation,
        SidebarActive,
        CodeCopy,
        MobileNav,
        PageTransition,
        ScrollProgress,
        BackToTop,
        FullscreenReader,
        LazyLoadDetector,
        // 工具函数
        debounce,
        throttle,
        safeExecute,
        supportsFeature,
        // 重新初始化
        reinit: initialize
    };

})();
