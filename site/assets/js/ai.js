/**
 * Git Workflow Lab - 共享 AI 客户端
 * @description 全站可复用的 AI 调用层：设置存储、项目知识上下文、按 provider 切换请求（ask 非流式 / askStream SSE 流式）。
 *   - 复用 main.js 的 GitWorkflowLab.supportsFeature / safeExecute / LessonCatalog；
 *   - 传输层从 ai-assistant.html 提取并修正两个 bug（Anthropic system 字段丢失、设置读取无 try/catch）；
 *   - 系统提示 = 静态项目自述 + 动态课程地图（来自 lessons.json）+ 调用方提供的 perPageContext；
 *   - 用户自备 API Key（存于 localStorage 'git-ai-settings'），无后端、无共享密钥。
 *   仅在需要的页面加载（main.js 之后，defer 保证顺序）。
 */
(function () {
    'use strict';

    const GWL = window.GitWorkflowLab || (window.GitWorkflowLab = {});

    // 本地兜底工具（main.js 已有则复用，没有也能独立工作）
    const safeExecute = GWL.safeExecute || function (fn, fallback) {
        try {
            const r = fn();
            return r === undefined ? fallback : r;
        } catch (e) {
            return fallback;
        }
    };
    const hasLocalStorage = (() => {
        try {
            localStorage.setItem('__ai_probe', '1');
            localStorage.removeItem('__ai_probe');
            return true;
        } catch (e) {
            return false;
        }
    })();

    // ============================================
    // 静态项目自述（约 1.2KB，常量）
    // ============================================
    const PREAMBLE = `你是「Git Workflow Lab」的 AI 学习助手——一个开源 Git 与 CI/CD 教学项目（48 课时、11 个阶段 A–K）的专属助教，而非通用聊天机器人。

## 项目背景（必须基于这些事实作答）
- 课程结构：48 课时，按阶段 A–K 编排：
  · 阶段 A-B 环境与基础（安装配置、终端、commit/push/pull）
  · 阶段 C 分支与协作（分支、PR、冲突、rebase、SSH）
  · 阶段 D 救火与恢复（cherry-pick、revert、reflog、stash）
  · 阶段 E 工程化实践（hooks、大仓库、签名、bisect、worktree、submodule 等）
  · 阶段 F CI/CD（GitHub Actions、多阶段流水线、Secrets）
  · 阶段 G 安全（密钥与凭据管理）
  · 阶段 H 进阶实用（conventional commits、代码审查、fork/upstream、hotfix）
  · 阶段 I 计算机基础（shell、docker、http、yaml、进程与网络）
  · 阶段 J 编程与跨平台 CLI（Python、PowerShell、Bash 对照）
  · 阶段 K 配置与文本处理（正则、git 配置进阶、.gitattributes）
- 本地实验环境（Docker Compose）：Nginx 教程站点 :8081、ttyd Web 终端 :8080、Gitea :3000（内置 SSH :2222）、PostgreSQL。演示仓库：playground/playground-hello、playground/playground-ci。
- 双模式：GitHub Pages 可在线阅读课程与自测；本地 Docker 环境解锁终端、Gitea 与完整实验。
- 学习闭环：读课 → 动手 → 测验，辅以闪卡 / 场景挑战 / 成就徽章。

## 回答要求
1. 用简体中文回答。
2. 结合本项目的课程体系作答；相关时把问题指回具体课时（如「对应 lesson-05 合并冲突」）。
3. 给命令时用代码块，并给出可执行的具体示例。
4. 优先给出「下一步该做什么」的可操作建议；遇到报错先解释原因再给修复步骤。
5. 若问题明显超出 Git/CI-CD/计算机基础课程范围，友好地提醒聚焦本课程。`;

    // ============================================
    // AIClient 模块
    // ============================================
    const AIClient = {
        STORAGE_KEY: 'git-ai-settings',
        MESSAGES_KEY: 'git-ai-messages',

        DEFAULTS: {
            apiProvider: 'openai',
            apiKey: '',
            apiEndpoint: 'https://api.openai.com/v1',
            model: 'gpt-4o-mini'
        },

        /**
         * 各服务商默认模型：切换服务商时空值/旧默认自动替换，
         * 避免拿着 OpenAI 的模型名去请求 Anthropic（必然 400）。
         */
        DEFAULT_MODELS: {
            openai: 'gpt-4o-mini',
            anthropic: 'claude-sonnet-5-5',
            custom: 'llama3'
        },

        /** 课程地图缓存（来自 lessons.json，经 LessonCatalog 加载）。 */
        _courseMap: null,

        // ---------------- 设置存储 ----------------

        /** 读取设置，损坏或缺失时安全回落到默认值（修复原 ai-assistant 无 try/catch 的崩溃问题）。 */
        getSettings() {
            if (!hasLocalStorage) return { ...this.DEFAULTS };
            return safeExecute(() => {
                const raw = localStorage.getItem(this.STORAGE_KEY);
                if (!raw) return { ...this.DEFAULTS };
                const p = JSON.parse(raw);
                const provider = p.apiProvider || this.DEFAULTS.apiProvider;
                return {
                    apiProvider: provider,
                    apiKey: p.apiKey || '',
                    apiEndpoint: p.apiEndpoint || this.DEFAULTS.apiEndpoint,
                    // 缺省模型跟随服务商（避免 Anthropic 用户拿到 OpenAI 默认模型名）
                    model: p.model || this.DEFAULT_MODELS[provider] || this.DEFAULTS.model
                };
            }, { ...this.DEFAULTS });
        },

        /** 合并写入设置（caller 可只传部分字段）。 */
        saveSettings(partial) {
            if (!hasLocalStorage) return this.getSettings();
            const merged = Object.assign({}, this.DEFAULTS, this.getSettings(), partial || {});
            const persist = {
                apiProvider: merged.apiProvider,
                apiKey: merged.apiKey,
                apiEndpoint: merged.apiEndpoint,
                model: merged.model
            };
            // 明文存储用户自备 API Key（by-design：静态无后端站，存的是用户自己的 key 在自己的浏览器，
            // 项目从不代理或经手密钥）。CodeQL js/clear-text-storage-of-sensitive-data 已按 false-positive dismiss。
            safeExecute(() => localStorage.setItem(this.STORAGE_KEY, JSON.stringify(persist)));
            return persist;
        },

        /** 是否已配置可用：有 Key 即可；或本地/兼容端点（如 Ollama）可无 Key。 */
        isConfigured() {
            const s = this.getSettings();
            if (s.apiKey) return true;
            // 非 Anthropic 的 OpenAI 兼容端点（含本地 LLM）可不带 Key
            return s.apiProvider !== 'anthropic' && !!this.sanitizeEndpoint(s.apiEndpoint);
        },

        // ---------------- 对话历史 ----------------

        loadMessages() {
            if (!hasLocalStorage) return [];
            return safeExecute(() => {
                const raw = localStorage.getItem(this.MESSAGES_KEY);
                if (!raw) return [];
                const p = JSON.parse(raw);
                return Array.isArray(p)
                    ? p.filter((m) => m && (m.role === 'user' || m.role === 'assistant'))
                        .map((m) => ({ role: m.role, content: String(m.content) }))
                    : [];
            }, []);
        },

        saveMessages(messages) {
            if (!hasLocalStorage) return;
            safeExecute(() => localStorage.setItem(this.MESSAGES_KEY, JSON.stringify(messages || [])));
        },

        clearMessages() {
            if (!hasLocalStorage) return;
            safeExecute(() => localStorage.removeItem(this.MESSAGES_KEY));
        },

        // ---------------- 上下文构建 ----------------

        /** 渲染紧凑课程地图（id → 标题 → 简介），按 lessons.json 顺序。 */
        async _loadCourseMap() {
            if (this._courseMap !== null) return this._courseMap;
            this._courseMap = '';
            try {
                const LC = GWL.LessonCatalog;
                const lessons = LC && LC.load ? await LC.load() : [];
                if (Array.isArray(lessons) && lessons.length) {
                    this._courseMap = '\n\n## 课程地图（48 课 / 11 阶段 A–K，[阶段] id 标题 — 简介）\n'
                        + lessons.map((l) => `[${l.stage}] ${l.id} ${l.title} — ${l.desc || ''}`.trim()).join('\n');
                }
            } catch (err) {
                console.warn('[AIClient] 课程地图加载失败', err);
                this._courseMap = '';
            }
            return this._courseMap;
        },

        /**
         * 组装系统提示：静态自述 + 动态课程地图 + 调用方 perPageContext。
         * @param {Object} [opts]
         * @param {string} [opts.perPageContext] 页面级上下文（当前课程正文 / 报错规则 / 题目 / 用户问题上下文）
         * @returns {Promise<string>}
         */
        async buildSystemPrompt(opts = {}) {
            const courseMap = await this._loadCourseMap();
            const perPage = opts.perPageContext ? `\n\n## 当前页面上下文\n${opts.perPageContext}` : '';
            return `${PREAMBLE}${courseMap}${perPage}`;
        },

        // ---------------- 请求发送 ----------------

        /**
         * 校验并规范化 endpoint：仅允许 http(s)，剥离 query/hash 与多余斜杠。
         * 防止 javascript:/data: 等协议直接进入 fetch（原 ai-assistant 直接拼接 raw，存在注入风险）。
         */
        sanitizeEndpoint(raw) {
            try {
                const s = String(raw || '').trim();
                if (!s) return '';
                if (!/^https?:\/\//i.test(s)) return '';
                const u = new URL(s);
                const path = u.pathname.replace(/\/+$/, '');
                return `${u.protocol}//${u.host}${path}`;
            } catch (e) {
                return '';
            }
        },

        /**
         * 组装单次请求的 url/headers/body（ask 与 askStream 共用）。
         * @private
         * @param {Object} settings
         * @param {string} systemPrompt
         * @param {Array<{role:string,content:string}>} convo
         * @param {boolean} stream 是否请求 SSE 流式响应
         * @returns {{url:string, headers:Object, body:string}}
         */
        _buildRequest(settings, systemPrompt, convo, stream) {
            if (settings.apiProvider === 'anthropic') {
                // 修复：原版丢弃了首条 system 消息又未放入 system 字段，导致 Claude 从未收到
                // 项目知识。这里用顶层 system 字段正确传递（而非删掉首条消息）。
                return {
                    url: 'https://api.anthropic.com/v1/messages',
                    headers: {
                        'Content-Type': 'application/json',
                        'x-api-key': settings.apiKey,
                        'anthropic-version': '2023-06-01'
                    },
                    body: JSON.stringify({
                        model: settings.model,
                        max_tokens: 2048,
                        stream: stream || undefined,
                        system: systemPrompt,
                        messages: convo
                    })
                };
            }
            // OpenAI / OpenAI 兼容端点（含 'custom'：Ollama、vLLM、LM Studio、Azure 等）
            const endpoint = this.sanitizeEndpoint(settings.apiEndpoint) || this.DEFAULTS.apiEndpoint;
            const headers = { 'Content-Type': 'application/json' };
            // 有 Key 才带 Authorization（本地无鉴权端点可留空）
            if (settings.apiKey) {
                headers['Authorization'] = `Bearer ${settings.apiKey}`;
            }
            const payload = {
                model: settings.model,
                temperature: 0.7,
                messages: [{ role: 'system', content: systemPrompt }, ...convo]
            };
            if (stream) payload.stream = true;
            return { url: `${endpoint}/chat/completions`, headers, body: JSON.stringify(payload) };
        },

        /**
         * 带默认超时的 POST；统一超时/取消的错误形态（取消保留 AbortError 名称供调用方识别）。
         * @private
         * @param {string} url
         * @param {Object} headers
         * @param {string} body
         * @param {AbortSignal} [signal]
         * @returns {Promise<Response>}
         */
        async _post(url, headers, body, signal) {
            // 默认 120s 超时：端点无响应时避免请求无限挂起（调用方传 signal 时以其为准）
            const timeoutSignal = (typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function')
                ? AbortSignal.timeout(120000)
                : undefined;
            try {
                return await fetch(url, {
                    method: 'POST',
                    headers,
                    body,
                    signal: signal || timeoutSignal
                });
            } catch (err) {
                if (err && err.name === 'TimeoutError') {
                    throw new Error('请求超时（120 秒无响应），请确认端点可用后重试。');
                }
                if (err && err.name === 'AbortError') {
                    const cancelled = new Error('请求已取消。');
                    cancelled.name = 'AbortError';
                    throw cancelled;
                }
                throw err;
            }
        },

        /** 非 2xx 时读取错误体并抛出可读错误。 */
        async _httpError(response) {
            const err = await response.json().catch(() => ({}));
            throw new Error((err && err.error && err.error.message) || `API 请求失败 (${response.status})`);
        },

        /** 从完整 JSON 响应中提取文本（ask 的非流式路径）。 */
        _extractText(data, provider) {
            const text = provider === 'anthropic'
                ? (data && data.content && data.content[0] && data.content[0].text)
                : (data && data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content);
            return text || '';
        },

        /** 校验设置并构建 convo（含本次用户输入），ask / askStream 共用。 */
        async _prepare(opts) {
            let settings = opts.settings || this.getSettings();
            // 旧版保存可能把 OpenAI 默认模型名留给 Anthropic（必然 400），此处纠正
            if (settings.apiProvider === 'anthropic' && settings.model === this.DEFAULT_MODELS.openai) {
                settings = { ...settings, model: this.DEFAULT_MODELS.anthropic };
            }
            // Anthropic 必须带 Key；OpenAI 兼容端点（含本地 LLM，如 Ollama/vLLM）可不带 Key
            if (settings.apiProvider === 'anthropic' && !settings.apiKey) {
                throw new Error('Anthropic 需要 API Key，请在 AI 设置中填写。');
            }
            const systemPrompt = await this.buildSystemPrompt({ perPageContext: opts.perPageContext || '' });
            const convo = (Array.isArray(opts.history) ? opts.history : [])
                .filter((m) => m && (m.role === 'user' || m.role === 'assistant'))
                .map((m) => ({ role: m.role, content: String(m.content) }));
            convo.push({ role: 'user', content: String(opts.userMessage || '') });
            return { settings, systemPrompt, convo };
        },

        /**
         * 单一入口：组装系统提示 + 按 provider 切换请求。
         * @param {Object} opts
         * @param {string} opts.userMessage 本次用户输入
         * @param {string} [opts.perPageContext] 页面级上下文
         * @param {Array<{role:string,content:string}>} [opts.history] 历史（仅 user/assistant 被采用）
         * @param {Object} [opts.settings] 显式覆盖设置
         * @param {AbortSignal} [opts.signal] 可取消
         * @returns {Promise<{text:string}>}
         */
        async ask(opts = {}) {
            const { settings, systemPrompt, convo } = await this._prepare(opts);
            const { url, headers, body } = this._buildRequest(settings, systemPrompt, convo, false);

            const response = await this._post(url, headers, body, opts.signal);
            if (!response.ok) {
                await this._httpError(response);
            }
            const data = await response.json();
            return { text: this._extractText(data, settings.apiProvider) };
        },

        /**
         * 流式问答：SSE 增量返回，每收到一段文本回调 onDelta(delta, fullText)。
         * 首 token 即开始呈现，长回答不再需要盯着打字指示器干等。
         * 环境不支持响应流（file:// 等）时自动退化为一次性返回。
         * @param {Object} opts 同 ask()
         * @param {Function} [onDelta] (delta: string, fullText: string) => void
         * @returns {Promise<{text:string}>} 完整回答
         */
        async askStream(opts = {}, onDelta = () => {}) {
            const { settings, systemPrompt, convo } = await this._prepare(opts);
            const { url, headers, body } = this._buildRequest(settings, systemPrompt, convo, true);

            const response = await this._post(url, headers, body, opts.signal);
            if (!response.ok) {
                await this._httpError(response);
            }

            // 无 body 流（老浏览器 / file:// 协议）时退化为一次性解析
            if (!response.body || typeof response.body.getReader !== 'function') {
                const data = await response.json();
                const text = this._extractText(data, settings.apiProvider);
                if (text) onDelta(text, text);
                return { text };
            }

            const provider = settings.apiProvider;
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let full = '';
            const emit = (delta) => {
                if (!delta) return;
                full += delta;
                onDelta(delta, full);
            };

            // 逐行解析 SSE：OpenAI 兼容为 choices[0].delta.content + [DONE] 哨兵，
            // Anthropic 为 content_block_delta 事件的 delta.text。
            for (;;) {
                const { done, value } = await reader.read();
                if (done) break;
                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';
                for (const line of lines) {
                    const trimmed = line.trim();
                    if (!trimmed.startsWith('data:')) continue;
                    const payload = trimmed.slice(5).trim();
                    if (!payload || payload === '[DONE]') continue;
                    let json;
                    try { json = JSON.parse(payload); } catch (e) { continue; }
                    if (provider === 'anthropic') {
                        if (json.type === 'content_block_delta' && json.delta && typeof json.delta.text === 'string') {
                            emit(json.delta.text);
                        }
                    } else {
                        const delta = json.choices && json.choices[0] && json.choices[0].delta
                            && json.choices[0].delta.content;
                        if (typeof delta === 'string') emit(delta);
                    }
                }
            }
            return { text: full };
        },

        // ---------------- 渲染辅助（供各集成页复用，避免重复实现 XSS 转义） ----------------

        /** HTML 转义。 */
        escapeHtml(text) {
            return String(text == null ? '' : text).replace(/[&<>"']/g, (c) => (
                { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
            ));
        },

        /**
         * 把 AI 返回的文本渲染为安全 HTML：先转义，再用 marked（若页面已加载）解析 markdown；
         * marked 不可用时退化为 <br> 换行。先转义可防止 AI 输出中的原始 HTML 被注入。
         */
        renderToHtml(text) {
            const safe = this.escapeHtml(text);
            if (window.marked && typeof window.marked.parse === 'function') {
                try { return window.marked.parse(safe); } catch (e) { /* 落入回退 */ }
            }
            return safe.replace(/\n/g, '<br>');
        },

        // ---------------- 共享设置弹窗（约束 A：全站可用的配置入口） ----------------

        /** 当前已挂载的设置弹窗元素。 */
        _settingsEl: null,

        /**
         * 打开共享设置弹窗；保存后回调 onSaved。
         * @param {Object} [opts]
         * @param {Function} [opts.onSaved] 保存成功回调
         */
        openSettings(opts = {}) {
            const onSaved = typeof opts.onSaved === 'function' ? opts.onSaved : null;
            if (this._settingsEl) {
                this._settingsEl.remove();
                this._settingsEl = null;
                return;
            }
            const s = this.getSettings();
            const overlay = document.createElement('div');
            overlay.className = 'ai-settings';
            overlay.setAttribute('role', 'dialog');
            overlay.setAttribute('aria-modal', 'true');
            overlay.setAttribute('aria-label', 'AI 设置');
            overlay.innerHTML = `
                <div class="ai-settings__panel">
                    <h3>AI 助教设置</h3>
                    <p class="ai-settings__hint">兼容任何 OpenAI 兼容接口或 Anthropic。API Key 仅存于本机浏览器，调用直连你填的端点，本项目不经手密钥。本地端点（如 Ollama）可留空 Key。</p>
                    <label class="ai-settings__field"><span>服务商</span>
                        <select class="ai-settings__provider">
                            <option value="openai">OpenAI 及兼容 API（可改端点）</option>
                            <option value="anthropic">Anthropic (Claude)</option>
                            <option value="custom">本地 / 自定义兼容端点（Ollama、vLLM 等，可无 Key）</option>
                        </select>
                    </label>
                    <label class="ai-settings__field"><span>API Key（本地端点可留空）</span>
                        <input type="password" class="ai-settings__key" placeholder="sk-... / sk-ant-... / 留空用于本地" autocomplete="off" />
                    </label>
                    <label class="ai-settings__field ai-settings__field--endpoint"><span>端点 (Endpoint)</span>
                        <input type="text" class="ai-settings__endpoint" placeholder="https://api.openai.com/v1 或 http://localhost:11434/v1" autocomplete="off" />
                    </label>
                    <label class="ai-settings__field"><span>模型 (Model)</span>
                        <input type="text" class="ai-settings__model" placeholder="gpt-4o-mini / claude-sonnet-5-5 / llama3 ..." autocomplete="off" />
                    </label>
                    <div class="ai-settings__actions">
                        <button type="button" class="ai-settings__cancel">取消</button>
                        <button type="button" class="ai-settings__save">保存</button>
                    </div>
                </div>`;
            // 内联样式，避免依赖 style.css（与 KeyboardShortcuts 帮助弹窗一致的做法）
            Object.assign(overlay.style, {
                position: 'fixed', inset: '0', zIndex: '10001',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                background: 'rgba(15, 23, 42, 0.55)', backdropFilter: 'blur(2px)'
            });
            const panel = overlay.querySelector('.ai-settings__panel');
            Object.assign(panel.style, {
                width: 'min(440px, 92vw)', background: 'var(--bg-primary, #fff)',
                color: 'var(--text-primary, #1e293b)', padding: '28px',
                borderRadius: '20px', border: '1px solid var(--border-color, #e2e8f0)',
                boxShadow: '0 24px 70px rgba(15, 23, 42, 0.28)', fontFamily: 'inherit'
            });
            const provider = overlay.querySelector('.ai-settings__provider');
            const key = overlay.querySelector('.ai-settings__key');
            const endpoint = overlay.querySelector('.ai-settings__endpoint');
            const model = overlay.querySelector('.ai-settings__model');
            const endpointField = overlay.querySelector('.ai-settings__field--endpoint');
            provider.value = s.apiProvider;
            key.value = s.apiKey;
            endpoint.value = s.apiEndpoint;
            model.value = s.model;
            const syncProvider = () => {
                endpointField.style.display = (provider.value === 'anthropic') ? 'none' : '';
                model.placeholder = this.DEFAULT_MODELS[provider.value] || this.DEFAULTS.model;
                // 模型为空或仍是其他服务商的默认值时，自动切换到当前服务商的默认模型
                const current = model.value.trim().toLowerCase();
                const isOtherDefault = Object.keys(this.DEFAULT_MODELS).some((p) =>
                    p !== provider.value && this.DEFAULT_MODELS[p].toLowerCase() === current);
                if (!current || isOtherDefault) {
                    model.value = this.DEFAULT_MODELS[provider.value] || '';
                }
            };
            syncProvider();
            provider.addEventListener('change', syncProvider);

            const close = () => { overlay.remove(); this._settingsEl = null; };
            overlay.querySelector('.ai-settings__cancel').addEventListener('click', close);
            overlay.addEventListener('click', (e) => { if (e.target === overlay) close(); });
            overlay.querySelector('.ai-settings__save').addEventListener('click', () => {
                const cleaned = this.sanitizeEndpoint(endpoint.value);
                this.saveSettings({
                    apiProvider: provider.value,
                    apiKey: key.value.trim(),
                    apiEndpoint: (provider.value === 'anthropic') ? this.DEFAULTS.apiEndpoint : (cleaned || endpoint.value.trim()),
                    model: model.value.trim() || this.DEFAULT_MODELS[provider.value] || this.DEFAULTS.model
                });
                close();
                if (onSaved) { try { onSaved(); } catch (e) { /* 忽略回调错误 */ } }
            });

            document.body.appendChild(overlay);
            this._settingsEl = overlay;
            key.focus();
        }
    };

    // 挂载到全局命名空间（增强而非覆盖，避免抹掉 main.js 已设置的字段）
    GWL.AIClient = AIClient;
})();
