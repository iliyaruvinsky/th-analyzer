# Contributing to Skywind Plugin Marketplace

Thank you for considering contributing to the Skywind Plugin Marketplace! This document provides guidelines for contributing plugins, improvements, and fixes.

## How to Contribute

### Types of Contributions

1. **New Plugins** - Share your AI assistant rules with the community
2. **Plugin Improvements** - Enhance existing plugins
3. **Bug Fixes** - Fix issues in scripts or plugins
4. **Documentation** - Improve docs, examples, or guides
5. **Tools** - Enhance installation or validation scripts

## Contributing a New Plugin

### Step 1: Prepare Your Plugin

1. **Test Your Rules** - Use your rules in real projects for at least 2 weeks
2. **Validate Effectiveness** - Ensure rules achieve their stated purpose
3. **Check Compatibility** - Test with Claude Code, Cursor, and/or Windsurf
4. **Document Benefits** - Have clear before/after examples

### Step 2: Choose a Category

Select an existing category or propose a new one:

- `anti-hallucination` - Accuracy and verification rules
- `code-quality` - Clean code, maintainability, standards
- `security` - Secure coding practices
- `workflow` - Git, CI/CD, PR workflows
- `performance` - Optimization guidelines
- `testing` - TDD, test coverage, QA
- `documentation` - Documentation standards

**Proposing a new category?** Open an issue first to discuss it.

### Step 3: Use the Plugin Template

```bash
# Copy the template
cp -r templates/plugin-template/ plugins/<category>/<your-plugin-name>/

# Required files:
# - plugin.json (metadata)
# - rules.md (the actual rules)
# - README.md (documentation)
# - CHANGELOG.md (version history)
```

### Step 4: Fill Out plugin.json

```json
{
  "id": "category/plugin-name",
  "name": "Human Readable Name",
  "version": "1.0.0",
  "description": "Brief description (10-200 chars)",
  "category": "your-category",
  "compatibility": {
    "claudeCode": true,
    "cursor": true,
    "windsurf": false,
    "copilot": false
  },
  "author": {
    "name": "Your Name or Organization",
    "email": "email@example.com",
    "url": "https://yourwebsite.com"
  },
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "license": "MIT",
  "tags": ["stable", "recommended"],
  "createdAt": "2025-10-14T00:00:00Z",
  "updatedAt": "2025-10-14T00:00:00Z"
}
```

**Important Fields:**
- `id` must match the directory path (category/plugin-name)
- `version` must follow [semantic versioning](https://semver.org/)
- `compatibility` must accurately reflect tested tools
- `keywords` help users discover your plugin

### Step 5: Write rules.md

**Best Practices for Rules:**

1. **Be Specific** - Vague rules get ignored
   - ❌ Bad: "Write good code"
   - ✅ Good: "ALWAYS verify file changes by reading the file after editing"

2. **Use Strong Language** - AI assistants need clear directives
   - Use: MUST, ALWAYS, NEVER, REQUIRED, MANDATORY
   - Avoid: "try to", "maybe", "if possible"

3. **Explain Why** - Rules with reasoning are followed better
   ```markdown
   ### Rule: Verify Before Claiming
   - NEVER report success without verification
   - WHY: Unverified claims waste user time and money
   ```

4. **Provide Examples** - Show what to do and what not to do
   ```markdown
   ❌ Bad: "I've updated the file"
   ✅ Good: "Let me verify the update... Confirmed: file updated"
   ```

5. **Make Rules Measurable** - AI should know if it's complying
   - ❌ Bad: "Be accurate"
   - ✅ Good: "Read file after every edit to verify changes"

### Step 6: Write README.md

Your plugin README should include:

1. **Overview** - What does this plugin do?
2. **Purpose** - What problem does it solve?
3. **Key Features** - List main rules/guidelines
4. **Installation** - How to install (copy from template)
5. **Usage** - What users will notice after installation
6. **Benefits** - Why use this plugin?
7. **Examples** - Before/after comparisons
8. **Who Should Use This** - Target audience

See [plugins/anti-hallucination/strict-verification/README.md](plugins/anti-hallucination/strict-verification/README.md) for a complete example.

### Step 7: Create CHANGELOG.md

Start with version 1.0.0:

```markdown
# Changelog

## [1.0.0] - 2025-10-14

### Added
- Initial release
- Rule 1: [description]
- Rule 2: [description]

### Compatibility
- Claude Code: ✅
- Cursor: ✅
```

Follow [Keep a Changelog](https://keepachangelog.com/) format.

### Step 8: Test Your Plugin

Before submitting:

```bash
# Test installation (Unix/Mac)
./scripts/install.sh your-category/your-plugin

# Test installation (Windows)
.\scripts\install.ps1 -PluginId your-category/your-plugin

# Verify it appears in listing
node scripts/list-plugins.js --category your-category
```

**Manual Testing:**
1. Install plugin in a test project
2. Use AI assistant with the plugin rules
3. Verify rules are being followed
4. Test with different tools (Claude Code, Cursor, etc.)

### Step 9: Submit Pull Request

1. Fork the repository
2. Create a branch: `git checkout -b plugin/category/plugin-name`
3. Commit your changes: `git commit -m "Add [plugin-name] plugin"`
4. Push to your fork: `git push origin plugin/category/plugin-name`
5. Open a Pull Request

**PR Description Should Include:**
- Plugin name and category
- Brief description
- What problem it solves
- Tools tested with
- Example of rules in action (optional but recommended)

## Plugin Quality Standards

### Required

- ✅ Follows plugin template structure
- ✅ Valid plugin.json matching schema
- ✅ Rules are clear and specific
- ✅ README with installation instructions
- ✅ CHANGELOG with version history
- ✅ Tested with at least one AI coding tool
- ✅ No malicious or harmful content

### Recommended

- ⭐ Tested with multiple tools (Claude Code, Cursor, Windsurf)
- ⭐ Real-world usage examples
- ⭐ Before/after comparisons
- ⭐ Clear benefits articulated
- ⭐ Proper versioning from the start

### Bonus Points

- 🌟 Screenshots or recordings showing plugin in action
- 🌟 Compatibility with 3+ tools
- 🌟 Detailed examples directory
- 🌟 Community feedback incorporated

## Code of Conduct

### Plugin Content Guidelines

**Allowed:**
- Professional development standards
- Best practices and patterns
- Security guidelines (defensive)
- Performance optimizations
- Quality assurance rules

**Not Allowed:**
- Malicious code or instructions
- Security exploits (offensive)
- Discriminatory content
- Spam or advertisements
- Copyrighted material without permission

### Community Guidelines

- Be respectful and professional
- Provide constructive feedback
- Help others learn
- Credit original authors
- Report issues responsibly

## Review Process

1. **Automated Checks** - CI validates plugin structure
2. **Manual Review** - Maintainers review content and quality
3. **Testing** - Optionally tested by reviewers
4. **Feedback** - Comments or change requests
5. **Approval** - Merged when ready

**Timeline:** Most PRs reviewed within 3-5 business days

## Updating Existing Plugins

### Version Increments

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (2.0.0) - Breaking changes to rules
- **MINOR** (1.1.0) - New rules added (backwards compatible)
- **PATCH** (1.0.1) - Bug fixes, typos, clarifications

### Update Process

1. Update plugin files
2. Increment version in plugin.json
3. Update CHANGELOG.md
4. Update `updatedAt` timestamp in plugin.json
5. Submit PR with version bump

## Questions?

- **General Questions** - Open a GitHub Discussion
- **Bug Reports** - Open an Issue
- **Plugin Ideas** - Open an Issue with "Plugin Proposal" label
- **Security Issues** - Email devops@skywind.com privately

## Recognition

Contributors are recognized in:
- Plugin README (author field)
- Repository contributors list
- Special thanks in releases

Thank you for making the Skywind Plugin Marketplace better!
