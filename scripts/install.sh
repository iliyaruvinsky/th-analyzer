#!/bin/bash

# Skywind Plugin Marketplace Installer
# Universal installation script for AI coding assistant plugins
# Usage: ./install.sh <plugin-id> [--tool <tool-name>] [--target <target-dir>]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
MARKETPLACE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="claude-code"
TARGET_DIR="."
PLUGIN_ID=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --tool)
            TOOL="$2"
            shift 2
            ;;
        --target)
            TARGET_DIR="$2"
            shift 2
            ;;
        --help)
            echo "Skywind Plugin Marketplace Installer"
            echo ""
            echo "Usage: ./install.sh <plugin-id> [options]"
            echo ""
            echo "Arguments:"
            echo "  plugin-id           Plugin to install (e.g., anti-hallucination/strict-verification)"
            echo ""
            echo "Options:"
            echo "  --tool <name>       Target tool: claude-code, cursor, windsurf (default: claude-code)"
            echo "  --target <dir>      Target directory (default: current directory)"
            echo "  --help              Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./install.sh anti-hallucination/strict-verification"
            echo "  ./install.sh anti-hallucination/strict-verification --tool cursor"
            echo "  ./install.sh code-quality/clean-code-enforcer --target /path/to/project"
            exit 0
            ;;
        *)
            if [ -z "$PLUGIN_ID" ]; then
                PLUGIN_ID="$1"
            else
                echo -e "${RED}Error: Unknown argument '$1'${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# Validate plugin ID
if [ -z "$PLUGIN_ID" ]; then
    echo -e "${RED}Error: Plugin ID is required${NC}"
    echo "Usage: ./install.sh <plugin-id> [--tool <tool-name>]"
    exit 1
fi

# Paths
PLUGIN_PATH="$MARKETPLACE_ROOT/plugins/$PLUGIN_ID"
PLUGIN_JSON="$PLUGIN_PATH/plugin.json"
RULES_FILE="$PLUGIN_PATH/rules.md"

# Validate plugin exists
if [ ! -d "$PLUGIN_PATH" ]; then
    echo -e "${RED}Error: Plugin '$PLUGIN_ID' not found${NC}"
    echo "Available plugins:"
    find "$MARKETPLACE_ROOT/plugins" -name "plugin.json" -exec dirname {} \; | sed "s|$MARKETPLACE_ROOT/plugins/||" | sort
    exit 1
fi

if [ ! -f "$PLUGIN_JSON" ]; then
    echo -e "${RED}Error: Plugin metadata (plugin.json) not found${NC}"
    exit 1
fi

if [ ! -f "$RULES_FILE" ]; then
    echo -e "${RED}Error: Plugin rules (rules.md) not found${NC}"
    exit 1
fi

# Read plugin metadata
PLUGIN_NAME=$(jq -r '.name' "$PLUGIN_JSON")
PLUGIN_VERSION=$(jq -r '.version' "$PLUGIN_JSON")
PLUGIN_CATEGORY=$(jq -r '.category' "$PLUGIN_JSON")

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Skywind Plugin Marketplace Installer       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Plugin:${NC} $PLUGIN_NAME"
echo -e "${GREEN}Version:${NC} $PLUGIN_VERSION"
echo -e "${GREEN}Category:${NC} $PLUGIN_CATEGORY"
echo -e "${GREEN}Target Tool:${NC} $TOOL"
echo -e "${GREEN}Target Directory:${NC} $TARGET_DIR"
echo ""

# Determine installation path based on tool
case $TOOL in
    claude-code)
        INSTALL_PATH="$TARGET_DIR/.claude/rules"
        INSTALL_FILE="$INSTALL_PATH/$(basename $PLUGIN_ID).md"
        ;;
    cursor)
        INSTALL_PATH="$TARGET_DIR"
        INSTALL_FILE="$INSTALL_PATH/.cursorrules"
        ;;
    windsurf)
        INSTALL_PATH="$TARGET_DIR/.windsurf/rules"
        INSTALL_FILE="$INSTALL_PATH/$(basename $PLUGIN_ID).md"
        ;;
    *)
        echo -e "${RED}Error: Unsupported tool '$TOOL'${NC}"
        echo "Supported tools: claude-code, cursor, windsurf"
        exit 1
        ;;
esac

# Create installation directory if it doesn't exist
if [ ! -d "$INSTALL_PATH" ]; then
    echo -e "${YELLOW}Creating directory: $INSTALL_PATH${NC}"
    mkdir -p "$INSTALL_PATH"
fi

# Check if file exists and ask for confirmation
if [ -f "$INSTALL_FILE" ] && [ "$TOOL" != "cursor" ]; then
    echo -e "${YELLOW}Warning: File already exists at $INSTALL_FILE${NC}"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation cancelled${NC}"
        exit 1
    fi
fi

# Special handling for Cursor (append mode)
if [ "$TOOL" == "cursor" ]; then
    if [ -f "$INSTALL_FILE" ]; then
        echo -e "${YELLOW}Appending to existing .cursorrules file${NC}"
        echo "" >> "$INSTALL_FILE"
        echo "# ================================================" >> "$INSTALL_FILE"
        echo "# Plugin: $PLUGIN_NAME ($PLUGIN_VERSION)" >> "$INSTALL_FILE"
        echo "# Category: $PLUGIN_CATEGORY" >> "$INSTALL_FILE"
        echo "# ================================================" >> "$INSTALL_FILE"
        echo "" >> "$INSTALL_FILE"
        cat "$RULES_FILE" >> "$INSTALL_FILE"
    else
        cp "$RULES_FILE" "$INSTALL_FILE"
    fi
else
    # Direct copy for other tools
    cp "$RULES_FILE" "$INSTALL_FILE"
fi

echo -e "${GREEN}✓ Plugin installed successfully!${NC}"
echo ""
echo -e "${BLUE}Installation Details:${NC}"
echo -e "  Location: $INSTALL_FILE"
echo -e "  Plugin: $PLUGIN_NAME v$PLUGIN_VERSION"
echo ""
echo -e "${GREEN}Next Steps:${NC}"
echo -e "  1. Restart your AI coding assistant"
echo -e "  2. The rules will be automatically applied"
echo -e "  3. Check the plugin README for usage examples: $PLUGIN_PATH/README.md"
echo ""
echo -e "${BLUE}Happy coding with verified accuracy! 🎯${NC}"
