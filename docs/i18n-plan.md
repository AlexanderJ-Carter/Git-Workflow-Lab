# 🌍 Multilingual Support Plan

## Current Status

### ✅ Implemented

1. **README Translation**
   - ✅ Chinese: `README.md`
   - ✅ English: `README_EN.md`

2. **Documentation System**
   - ✅ Sphinx configured for i18n (`docs-sphinx/conf.py`)
   - ✅ Locale directory structure created
   - ✅ MyST Parser with internationalization support

3. **Source Files**
   - ✅ All course content in Chinese (`docs/lesson-*.md`)
   - ✅ Getting started guides in English (`docs-sphinx/getting-started/`)

### 🔄 In Progress

1. **Course Translation**
   - Priority lessons for English translation:
     - [ ] lesson-00-install-and-config.md
     - [ ] lesson-01-init-push.md
     - [ ] lesson-02-workspace-staging-history.md
     - [ ] lesson-04-branches-and-pr.md

2. **Website Localization**
   - [ ] Create i18n framework for `site/` pages
   - [ ] Language switcher component
   - [ ] Translated UI strings

### 📋 Planned

1. **Additional Languages**
   - [ ] Japanese
   - [ ] Spanish
   - [ ] French
   - [ ] German

2. **Automation**
   - [ ] CI/CD pipeline for translation validation
   - [ ] Translation memory integration
   - [ ] Community translation platform

## Implementation Guide

### Phase 1: English Documentation (Priority)

```bash
# 1. Create English documentation structure
mkdir -p docs-sphinx/locale/en/LC_MESSAGES

# 2. Extract translatable strings
cd docs-sphinx
make gettext

# 3. Generate English PO files
sphinx-intl update -p _build/gettext -l en

# 4. Build English documentation
make html BUILDDIR=_build/en -e SPHINXOPTS="-D language='en'"
```

### Phase 2: Website Localization

**Architecture**:
```javascript
// site/assets/js/i18n.js
const i18n = {
  currentLang: 'zh-CN',
  translations: {
    'en': {
      nav: { home: 'Home', courses: 'Courses', ... },
      ui: { start: 'Start Learning', ... }
    },
    'zh-CN': {
      nav: { home: '首页', courses: '课程', ... },
      ui: { start: '开始学习', ... }
    }
  }
};
```

### Phase 3: Community Translation

**Tools**:
- Crowdin / Transifex for collaborative translation
- GitHub Actions for automated deployment
- Translation memory for consistency

## Translation Priorities

### High Priority

1. Getting Started Guide
2. Basic Git Lessons (0-2)
3. Main README
4. Website UI elements

### Medium Priority

1. Advanced Git Lessons (3-5)
2. Best Practices
3. FAQ
4. Troubleshooting guides

### Low Priority

1. Blog posts
2. Case studies
3. Supplementary materials

## Quality Assurance

### Translation Review Process

1. **Initial Translation**
   - Translator completes translation
   - Uses translation memory for consistency

2. **Review**
   - Native speaker review
   - Technical accuracy check
   - Style guide compliance

3. **Approval**
   - Maintainer approval
   - Integration testing
   - Deployment

### Quality Metrics

- Completeness: % of strings translated
- Accuracy: Technical correctness
- Consistency: Terminology consistency
- Readability: Natural language flow

## Community Contributions

### How to Contribute Translations

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YOUR-USERNAME/Git-Workflow-Lab.git
   cd Git-Workflow-Lab
   ```

2. **Create Translation Branch**
   ```bash
   git checkout -b translation/en-lesson-00
   ```

3. **Translate**
   - Edit `.po` files or markdown files
   - Maintain formatting and structure
   - Keep code examples unchanged

4. **Test**
   ```bash
   make docs
   make docs-serve
   # Verify translation looks correct
   ```

5. **Submit PR**
   - Clear description of changes
   - Screenshots if applicable
   - Reference any related issues

### Translation Style Guide

**General Principles**:
- Clear and simple language
- Consistent terminology
- Cultural appropriateness
- Technical accuracy

**Git Terminology**:
- commit → 提交 (zh-CN) / commit (en)
- repository → 仓库 (zh-CN) / repository (en)
- branch → 分支 (zh-CN) / branch (en)
- merge → 合并 (zh-CN) / merge (en)

**Formatting**:
- Keep Markdown syntax intact
- Preserve code block language tags
- Maintain link structure
- Use appropriate quotation marks

## Resources

### Tools

- [Sphinx Internationalization](https://www.sphinx-doc.org/en/master/usage/advanced/intl.html)
- [gettext Manual](https://www.gnu.org/software/gettext/manual/)
- [sphinx-intl](https://github.com/sphinx-doc/sphinx-intl)

### Guides

- [Translation Best Practices](https://mozilla-l10n.github.io/documentation/localization/localization_best_practices.html)
- [Git Documentation Translation Guide](https://github.com/jnavila/git-manpages-l10n)

## Contact

For translation questions or collaboration:
- Open a GitHub issue with `translation` label
- Join GitHub Discussions
- Email maintainers (see CODEOWNERS)

---

**Status**: 🟡 Active Development
**Last Updated**: 2026-04-04
**Maintainers**: See CODEOWNERS file
