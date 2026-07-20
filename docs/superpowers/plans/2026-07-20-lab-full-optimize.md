# Lab Full Optimize Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix Docker/SSH/init defects, clean the repo, wire the lesson→quiz→practice loop, expand Linux/Git content, and polish UX micro-interactions.

**Architecture:** Single feature branch with layered commits: infra → catalog/teaching loop → content → UX. Shared `site/assets/data/lessons.json` is the lesson catalog source of truth for JS pages.

**Tech Stack:** Docker Compose, bash entrypoints, static HTML/CSS/JS, pytest, GitHub Actions.

## Global Constraints

- Preserve existing site visual language in `site/assets/css/style.css`; only additive motion tokens.
- Demo repos MUST be `playground-hello` and `playground-ci`.
- Site port is `8081`; never `8082`.
- Do not vendor full linux-command corpus; curated subset + external link only.
- Chinese UI copy; no backward-compat shims; no redundant try/except fallbacks.
- Commit frequently; push to `cursor/lab-full-optimize-2fe3`.

---

### Task 1: Docker compose + Gitea init unification

**Files:**
- Modify: `docker-compose.yml`
- Modify: `docker/gitea/entrypoint.sh`
- Modify: `docker/terminal/welcome.sh`
- Modify: `docker/terminal/Dockerfile`
- Modify: `scripts/init-gitea.sh`
- Modify: `scripts/init-gitea-manual.sh`
- Modify: `Dockerfile`
- Modify: `.dockerignore`
- Modify: `.env.example`
- Modify: `Makefile`

- [ ] Enable SSH (`START_SSH_SERVER=true`, port `2222:2222`)
- [ ] Fix healthchecks to `wget`; healthy depends_on for db→gitea
- [ ] Remove dead `init-gitea.sh` volume mount
- [ ] Create `playground-hello` + `playground-ci`; stop logging password
- [ ] Align welcome + manual scripts; run ttyd as `playground`
- [ ] Add `make docker-up` env validation for CHANGE_ME / empty secrets
- [ ] Commit: `fix(docker): enable SSH, unify init, harden healthchecks`

### Task 2: CI + lesson check + cleanup clutter

**Files:**
- Modify: `.github/workflows/check-lessons.yml`
- Modify: `.github/workflows/code-quality.yml`
- Modify: `.github/workflows/security-scan.yml`
- Modify: `.github/workflows/docker.yml`
- Create: `.github/workflows/test.yml`
- Delete or stop shipping: `site/test-iframe.html`
- Unify: keep `docs/viewer.html` as source; `site/docs/viewer.html` sync or symlink via build
- Fix README issue template links; remove duplicate `cspell.json` or merge
- Fix port 8082 → 8081 across site/docs

- [ ] Allow lesson prefixes `00`, `06a`, `06b` without false duplicate fail
- [ ] Add pytest workflow
- [ ] Path-filter docker builds; scan both Dockerfiles
- [ ] Commit: `chore: cleanup clutter and fix CI checks`

### Task 3: Shared lessons catalog + teaching loop wiring

**Files:**
- Create: `site/assets/data/lessons.json`
- Modify: `site/docs/viewer.html`
- Modify: `site/assets/js/main.js`
- Modify: `site/quiz.html`
- Modify: `site/learning-path.html`
- Modify: `site/search.html`
- Modify: `site/lessons/index.html`
- Modify: `site/flashcards.html`
- Modify: `site/index.html`
- Modify: `site/workspace.html`
- Modify: `tests/test_site_integrity.py`

- [ ] Export catalog JSON covering all 23+ lessons with id, file, stage, title, quizId
- [ ] Viewer footer: mark complete, quiz link, flashcards, next, open workspace
- [ ] Fix quiz return hrefs to `docs/viewer.html?file=...`
- [ ] Fix learning-path stages (include security 18–19); search 18–19
- [ ] Workspace reads `pendingCommand`; lesson picker
- [ ] Onboarding wizard on index (Pages vs Docker)
- [ ] Flashcards: lessonId filter + nextReviewAt SRS fields
- [ ] Commit: `feat(site): unify lesson catalog and learning loop`

### Task 4: Content expansion (Linux + new lessons)

**Files:**
- Modify: `docs/lesson-00-terminal-basics.md`
- Modify: `docs/lesson-06a-ssh-setup-and-clone.md` (align SSH port/repos)
- Create: `docs/lesson-20-bisect.md`
- Create: `docs/lesson-21-worktree.md`
- Modify: `site/command-sheet.html` or cheatsheet page — add Linux section
- Modify: `docs/lessons-overview.md`, `docs/learning-path.md`
- Update quiz banks for new lessons lightly
- Fill missing 如何确认 / 常见错误 in 06b, 10, 12

- [ ] Curate Linux commands with link to https://linux-command.alexander.xin/
- [ ] New lessons follow `_lesson_template.md` structure
- [ ] Commit: `feat(docs): expand Linux terminal and advanced Git lessons`

### Task 5: UX micro-interactions + workspace guidance

**Files:**
- Modify: `site/assets/css/style.css`
- Modify: `site/assets/js/main.js`
- Modify: `site/workspace.html`
- Modify: `site/quick-start.html`

- [ ] Motion tokens: fade-in, button press, progress transition, complete pulse
- [ ] Workspace: lesson selector, sticky guide bar, SSH help panel
- [ ] Mobile stack layout for workspace
- [ ] Commit: `feat(ux): micro-interactions and workspace guidance`

### Task 6: Verification

- [ ] `pytest -q`
- [ ] `python scripts/build-site.py`
- [ ] Grep for 8082, hello-git, playground2026 password log, curl healthcheck on nginx
- [ ] Push branch and open/update PR

---

## Spec coverage

| Spec section | Tasks |
|--------------|-------|
| A Infra | 1, 2 |
| B Teaching loop | 3 |
| C Content | 4 |
| D UX | 5 |
| Acceptance | 6 |
