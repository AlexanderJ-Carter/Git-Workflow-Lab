/**
 * Git Workflow Lab - Sphinx Custom JavaScript
 * Enhanced interactivity and UX improvements
 */

(function() {
  'use strict';

  // ============================================
  // Theme Management
  // ============================================
  const ThemeManager = {
    init() {
      this.theme = localStorage.getItem('theme') || 'light';
      this.applyTheme();
      this.createToggle();
    },

    applyTheme() {
      document.documentElement.setAttribute('data-theme', this.theme);
    },

    toggle() {
      this.theme = this.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', this.theme);
      this.applyTheme();
    },

    createToggle() {
      // Add theme toggle button to footer
      const footer = document.querySelector('footer');
      if (footer) {
        const toggleBtn = document.createElement('button');
        toggleBtn.className = 'theme-toggle btn';
        toggleBtn.innerHTML = this.theme === 'light' ? '🌙 Dark' : '☀️ Light';
        toggleBtn.style.cssText = `
          margin-top: 1rem;
          padding: 0.5rem 1rem;
          background: var(--bg-secondary);
          border: 1px solid var(--border-color);
          border-radius: 4px;
          cursor: pointer;
          transition: all 0.2s;
        `;
        toggleBtn.addEventListener('click', () => {
          this.toggle();
          toggleBtn.innerHTML = this.theme === 'light' ? '🌙 Dark' : '☀️ Light';
        });
        footer.appendChild(toggleBtn);
      }
    }
  };

  // ============================================
  // Code Block Enhancements
  // ============================================
  const CodeBlockEnhancer = {
    init() {
      this.addLanguageLabels();
      this.enhanceCopyButtons();
    },

    addLanguageLabels() {
      document.querySelectorAll('pre code').forEach(block => {
        const pre = block.parentElement;
        const classes = block.className.split(' ');

        // Find language class
        const langClass = classes.find(c => c.startsWith('language-'));
        if (langClass) {
          const lang = langClass.replace('language-', '');
          pre.setAttribute('data-language', lang);
        } else {
          pre.setAttribute('data-language', 'code');
        }
      });
    },

    enhanceCopyButtons() {
      // sphinx-copybutton already handles this
      // Add custom styling on success
      document.querySelectorAll('.copybutton').forEach(btn => {
        btn.addEventListener('click', () => {
          const originalText = btn.textContent;
          btn.textContent = '✓ Copied!';
          setTimeout(() => {
            btn.textContent = originalText;
          }, 2000);
        });
      });
    }
  };

  // ============================================
  // Smooth Scrolling
  // ============================================
  const SmoothScroller = {
    init() {
      document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
          const target = document.querySelector(this.getAttribute('href'));
          if (target) {
            e.preventDefault();
            target.scrollIntoView({
              behavior: 'smooth',
              block: 'start'
            });
          }
        });
      });
    }
  };

  // ============================================
  // Table Enhancements
  // ============================================
  const TableEnhancer = {
    init() {
      this.makeResponsive();
    },

    makeResponsive() {
      document.querySelectorAll('table').forEach(table => {
        const wrapper = document.createElement('div');
        wrapper.className = 'table-wrapper';
        wrapper.style.cssText = `
          overflow-x: auto;
          -webkit-overflow-scrolling: touch;
          margin: 1.5em 0;
        `;
        table.parentNode.insertBefore(wrapper, table);
        wrapper.appendChild(table);
      });
    }
  };

  // ============================================
  // External Links
  // ============================================
  const ExternalLinks = {
    init() {
      document.querySelectorAll('a[href^="http"]').forEach(link => {
        // Add external link icon
        if (!link.hostname.includes(window.location.hostname)) {
          link.setAttribute('target', '_blank');
          link.setAttribute('rel', 'noopener noreferrer');
          link.innerHTML += ' <small style="opacity: 0.6">↗</small>';
        }
      });
    }
  };

  // ============================================
  // Progress Indicator
  // ============================================
  const ProgressIndicator = {
    init() {
      this.createBar();
      window.addEventListener('scroll', () => this.update());
    },

    createBar() {
      const bar = document.createElement('div');
      bar.id = 'reading-progress';
      bar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        width: 0%;
        z-index: 9999;
        transition: width 0.1s;
      `;
      document.body.appendChild(bar);
      this.bar = bar;
    },

    update() {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (scrollTop / docHeight) * 100;
      this.bar.style.width = progress + '%';
    }
  };

  // ============================================
  // Initialize Everything
  // ============================================
  document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    CodeBlockEnhancer.init();
    SmoothScroller.init();
    TableEnhancer.init();
    ExternalLinks.init();
    ProgressIndicator.init();

    console.log('✨ Sphinx documentation enhanced!');
  });

})();
