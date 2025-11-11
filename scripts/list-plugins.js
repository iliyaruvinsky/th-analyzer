#!/usr/bin/env node

/**
 * Skywind Plugin Marketplace - Plugin Browser
 * Lists all available plugins with their metadata
 * Usage: node list-plugins.js [--category <category>] [--tool <tool>]
 */

const fs = require('fs');
const path = require('path');

// Parse command line arguments
const args = process.argv.slice(2);
let filterCategory = null;
let filterTool = null;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '--category' && i + 1 < args.length) {
        filterCategory = args[i + 1];
        i++;
    } else if (args[i] === '--tool' && i + 1 < args.length) {
        filterTool = args[i + 1];
        i++;
    } else if (args[i] === '--help') {
        console.log('Skywind Plugin Marketplace - Plugin Browser');
        console.log('');
        console.log('Usage: node list-plugins.js [options]');
        console.log('');
        console.log('Options:');
        console.log('  --category <name>    Filter by category');
        console.log('  --tool <name>        Filter by compatible tool (claude-code, cursor, windsurf)');
        console.log('  --help               Show this help message');
        console.log('');
        console.log('Examples:');
        console.log('  node list-plugins.js');
        console.log('  node list-plugins.js --category anti-hallucination');
        console.log('  node list-plugins.js --tool cursor');
        process.exit(0);
    }
}

// Colors for terminal output
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    dim: '\x1b[2m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m',
};

// Marketplace root directory
const marketplaceRoot = path.join(__dirname, '..');
const pluginsDir = path.join(marketplaceRoot, 'plugins');

// Find all plugin.json files
function findPlugins() {
    const plugins = [];

    function scanDirectory(dir, relativePath = '') {
        const entries = fs.readdirSync(dir, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            const relPath = path.join(relativePath, entry.name);

            if (entry.isDirectory()) {
                scanDirectory(fullPath, relPath);
            } else if (entry.name === 'plugin.json') {
                try {
                    const data = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
                    plugins.push({
                        ...data,
                        path: path.dirname(relPath),
                    });
                } catch (error) {
                    console.error(`${colors.red}Error reading ${fullPath}: ${error.message}${colors.reset}`);
                }
            }
        }
    }

    if (fs.existsSync(pluginsDir)) {
        scanDirectory(pluginsDir);
    }

    return plugins;
}

// Filter plugins based on criteria
function filterPlugins(plugins) {
    return plugins.filter(plugin => {
        if (filterCategory && plugin.category !== filterCategory) {
            return false;
        }

        if (filterTool) {
            const toolKey = filterTool === 'claude-code' ? 'claudeCode' : filterTool;
            if (!plugin.compatibility || !plugin.compatibility[toolKey]) {
                return false;
            }
        }

        return true;
    });
}

// Display plugins
function displayPlugins(plugins) {
    if (plugins.length === 0) {
        console.log(`${colors.yellow}No plugins found matching the criteria.${colors.reset}`);
        return;
    }

    // Group by category
    const byCategory = {};
    plugins.forEach(plugin => {
        if (!byCategory[plugin.category]) {
            byCategory[plugin.category] = [];
        }
        byCategory[plugin.category].push(plugin);
    });

    console.log(`${colors.blue}${colors.bright}╔═══════════════════════════════════════════════╗${colors.reset}`);
    console.log(`${colors.blue}${colors.bright}║   Skywind Plugin Marketplace - Catalog       ║${colors.reset}`);
    console.log(`${colors.blue}${colors.bright}╚═══════════════════════════════════════════════╝${colors.reset}`);
    console.log('');
    console.log(`${colors.green}Total plugins: ${plugins.length}${colors.reset}`);
    console.log('');

    // Display each category
    Object.keys(byCategory).sort().forEach(category => {
        console.log(`${colors.cyan}${colors.bright}📁 ${category.toUpperCase()}${colors.reset}`);
        console.log(`${colors.dim}${'─'.repeat(50)}${colors.reset}`);

        byCategory[category].forEach(plugin => {
            console.log(`${colors.bright}${plugin.name}${colors.reset} ${colors.dim}v${plugin.version}${colors.reset}`);
            console.log(`  ${colors.dim}ID:${colors.reset} ${plugin.id}`);
            console.log(`  ${colors.dim}Description:${colors.reset} ${plugin.description}`);

            // Compatibility
            const compat = [];
            if (plugin.compatibility.claudeCode) compat.push('Claude Code');
            if (plugin.compatibility.cursor) compat.push('Cursor');
            if (plugin.compatibility.windsurf) compat.push('Windsurf');
            if (plugin.compatibility.copilot) compat.push('Copilot');
            console.log(`  ${colors.dim}Compatible:${colors.reset} ${compat.join(', ')}`);

            // Tags
            if (plugin.tags && plugin.tags.length > 0) {
                console.log(`  ${colors.dim}Tags:${colors.reset} ${plugin.tags.join(', ')}`);
            }

            // Installation command
            console.log(`  ${colors.green}Install:${colors.reset} ${colors.dim}./scripts/install.sh ${plugin.id}${colors.reset}`);
            console.log('');
        });

        console.log('');
    });

    console.log(`${colors.blue}For more details on a plugin, see its README.md file${colors.reset}`);
    console.log(`${colors.blue}Installation: ./scripts/install.sh <plugin-id>${colors.reset}`);
}

// Main execution
try {
    const allPlugins = findPlugins();
    const filteredPlugins = filterPlugins(allPlugins);
    displayPlugins(filteredPlugins);
} catch (error) {
    console.error(`${colors.red}Error: ${error.message}${colors.reset}`);
    process.exit(1);
}
