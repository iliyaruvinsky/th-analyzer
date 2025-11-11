# Skywind Plugin Marketplace

**One unified marketplace for all AI coding assistant plugins**

## Marketplace Structure

```
skywind-plugin-marketplace/
├── README.md                           # Marketplace overview & catalog
├── CONTRIBUTING.md                     # How to submit plugins
├── plugin-schema.json                  # Plugin metadata schema
│
├── plugins/
│   ├── anti-hallucination/            # Category: Reduce AI hallucinations
│   │   ├── strict-verification/       # Plugin name
│   │   │   ├── plugin.json
│   │   │   ├── rules.md               # Universal rules file
│   │   │   ├── README.md
│   │   │   └── CHANGELOG.md
│   │   └── truth-priority/
│   │       ├── plugin.json
│   │       ├── rules.md
│   │       └── README.md
│   │
│   ├── code-quality/                  # Category: Code quality standards
│   │   ├── clean-code-enforcer/
│   │   └── solid-principles/
│   │
│   ├── security/                      # Category: Security guidelines
│   │   ├── secure-coding/
│   │   └── owasp-top-10/
│   │
│   ├── workflow/                      # Category: Development workflow
│   │   ├── git-commit-standards/
│   │   └── pr-best-practices/
│   │
│   └── performance/                   # Category: Performance optimization
│       └── optimization-rules/
│
├── scripts/
│   ├── install.sh                     # Universal installer (Unix/Mac)
│   ├── install.ps1                    # Universal installer (Windows)
│   ├── list-plugins.js                # Browse available plugins
│   └── validate.js                    # Validate plugin structure
│
├── templates/
│   ├── plugin-template/               # New plugin starter
│   │   ├── plugin.json
│   │   ├── rules.md
│   │   └── README.md
│   └── category-template/             # New category starter
│
└── docs/
    ├── getting-started.md
    ├── plugin-development.md
    ├── installation-guide.md
    └── best-practices.md
```

## Categories (Branches)

Each category organizes plugins by purpose:

1. **anti-hallucination** - Rules to improve AI accuracy and verification
2. **code-quality** - Clean code, SOLID principles, maintainability
3. **security** - Secure coding practices, vulnerability prevention
4. **workflow** - Git, CI/CD, PR standards, team collaboration
5. **performance** - Optimization guidelines, efficiency rules
6. **testing** - TDD, test coverage, quality assurance
7. **documentation** - Documentation standards, inline comments

## Plugin Structure

Each plugin contains:
- **plugin.json** - Metadata (name, version, author, compatibility)
- **rules.md** - Universal rules (works for Claude Code, Cursor, Windsurf, etc.)
- **README.md** - Description, installation, usage examples
- **CHANGELOG.md** - Version history (optional)

## Installation Flow

```bash
# Browse plugins
node scripts/list-plugins.js

# Install specific plugin
./scripts/install.sh anti-hallucination/strict-verification

# Install multiple plugins
./scripts/install.sh anti-hallucination/strict-verification code-quality/clean-code-enforcer

# Install entire category
./scripts/install.sh anti-hallucination/*
```

## Why One Marketplace?

- **Single source of truth** for all plugins
- **Easier discovery** - browse all plugins in one place
- **Consistent structure** - same format for all plugins
- **Simpler maintenance** - one repo to manage
- **Team collaboration** - everyone contributes to same marketplace
- **Version control** - track all plugin changes in one Git history
