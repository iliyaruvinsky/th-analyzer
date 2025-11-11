# Strict Verification Rules Plugin

**Category:** Anti-Hallucination
**Version:** 1.0.0
**Compatibility:** Claude Code, Cursor, Windsurf, Cline, Aider

## Overview

This plugin provides comprehensive anti-hallucination rules that enforce verification-first behavior, honest reporting, and truth as the highest value for AI coding assistants. It's designed to dramatically reduce false claims, unverified changes, and "hallucinated" completions.

## Purpose

AI coding assistants sometimes report that changes were made successfully when they haven't verified the results. This leads to:
- Wasted developer time debugging non-existent changes
- Increased costs from unnecessary iterations
- Loss of trust in AI assistance
- Frustration from inaccurate reporting

**This plugin solves these problems** by enforcing mandatory verification workflows.

## Key Features

### 10 Mandatory Rules

1. **Verify Before Claiming** - Never report changes without reading files afterward
2. **No Assumptions as Facts** - Distinguish between attempts and successes
3. **Mandatory Verification Workflow** - Always verify after executing changes
4. **Honest Reporting** - Never claim completion without proof
5. **Cost Consciousness** - Remember users pay for accurate work
6. **No Confidence Without Verification** - Use tentative language until verified
7. **Anti-Hallucination Mandate** - Choose accuracy over convenience
8. **No "Yesman" Behavior** - Answer honestly, not plausibly
9. **Truth as Highest Value** - Honest uncertainty beats confident incorrectness
10. **File Reading Status Protocol** - Clear status reporting without assumptions

## Installation

### For Claude Code Projects

```bash
# From marketplace root
./scripts/install.sh anti-hallucination/strict-verification

# Or manually copy
cp plugins/anti-hallucination/strict-verification/rules.md .claude/rules/strict-verification.md
```

### For Cursor Projects

```bash
# From marketplace root
./scripts/install.sh anti-hallucination/strict-verification --tool cursor

# Or manually copy
cp plugins/anti-hallucination/strict-verification/rules.md .cursorrules
# Or append to existing .cursorrules file
cat plugins/anti-hallucination/strict-verification/rules.md >> .cursorrules
```

### For Windsurf Projects

```bash
# From marketplace root
./scripts/install.sh anti-hallucination/strict-verification --tool windsurf

# Or manually copy
cp plugins/anti-hallucination/strict-verification/rules.md .windsurf/rules/strict-verification.md
```

## Usage

Once installed, the AI assistant will automatically follow these rules. You'll notice:

### Before Plugin
```
AI: "I've successfully updated all 5 files with the new configuration."
Developer: *checks files* "Only 2 were actually updated!"
```

### After Plugin
```
AI: "I attempted to update 5 files. Let me verify each one..."
AI: *reads all files*
AI: "Verification complete: 2 files updated successfully, 3 failed.
     Let me fix the 3 failures now."
```

## Benefits

- **Accuracy First**: No more false completion claims
- **Cost Savings**: Fewer wasted iterations = lower API costs
- **Trust Building**: Honest reporting builds confidence
- **Time Savings**: Get accurate results on first attempt
- **Professional Quality**: Verification is standard practice

## Who Should Use This

- **Enterprise Teams**: Where accuracy and cost control matter
- **Production Systems**: Where mistakes are expensive
- **Large Codebases**: Where verification is critical
- **Cost-Conscious Teams**: Paying for AI, expect accurate work
- **All Serious Projects**: Professional standards should be the default

## Examples

### Example 1: File Edits
```
Without Plugin:
AI: "I've updated config.json with the new settings."
[Developer finds file unchanged]

With Plugin:
AI: "I attempted to update config.json. Let me verify..."
AI: *reads config.json*
AI: "The edit failed - the file wasn't modified. Let me try a different approach..."
```

### Example 2: Multiple Files
```
Without Plugin:
AI: "All 10 components have been refactored successfully."
[Only 6 were actually changed]

With Plugin:
AI: "I attempted to refactor 10 components. Verifying each..."
AI: "Verification: 6 completed, 4 failed. Working on the 4 failures now..."
```

### Example 3: Uncertain Situations
```
Without Plugin:
AI: "Yes, the API endpoint is /api/v2/users" [guessing]

With Plugin:
AI: "I'm not certain of the exact endpoint. Let me search the codebase
     to find the actual implementation rather than guessing."
```

## Configuration

No configuration needed - rules are absolute and have no exceptions.

If you need to customize rules for your specific use case, fork this plugin and modify the rules.md file.

## Troubleshooting

**Q: The AI is being "too careful" and verifying everything**
A: That's the point! Verification prevents costly mistakes. This is professional behavior.

**Q: Can I make the rules less strict?**
A: You can, but we strongly recommend against it. These rules exist because hallucinations cost real money and time.

**Q: Does this work with [other tool]?**
A: Any AI coding assistant that reads rule files should work. The rules.md file is tool-agnostic.

## Version History

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

MIT License - See LICENSE file in repository root

## Contributing

Found a bug or have a suggestion? Submit an issue or PR to the Skywind Plugin Marketplace repository.

## Related Plugins

- `anti-hallucination/truth-priority` - Focus on truth-first responses
- `code-quality/verification-enforcer` - Additional code quality checks

## Support

For questions or issues:
- Open an issue in the marketplace repository
- Contact: devops@skywind.com
- Documentation: [Marketplace Docs](../../docs/)
