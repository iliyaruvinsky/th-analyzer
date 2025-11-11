# Skywind Plugin Marketplace Installer (PowerShell)
# Universal installation script for AI coding assistant plugins
# Usage: .\install.ps1 -PluginId <plugin-id> [-Tool <tool-name>] [-TargetDir <target-dir>]

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$PluginId,

    [Parameter(Mandatory=$false)]
    [ValidateSet("claude-code", "cursor", "windsurf")]
    [string]$Tool = "claude-code",

    [Parameter(Mandatory=$false)]
    [string]$TargetDir = ".",

    [Parameter(Mandatory=$false)]
    [switch]$Help
)

# Show help
if ($Help) {
    Write-Host "Skywind Plugin Marketplace Installer" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Usage: .\install.ps1 -PluginId <plugin-id> [options]"
    Write-Host ""
    Write-Host "Parameters:"
    Write-Host "  -PluginId <id>      Plugin to install (e.g., anti-hallucination/strict-verification)"
    Write-Host "  -Tool <name>        Target tool: claude-code, cursor, windsurf (default: claude-code)"
    Write-Host "  -TargetDir <dir>    Target directory (default: current directory)"
    Write-Host "  -Help               Show this help message"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\install.ps1 -PluginId anti-hallucination/strict-verification"
    Write-Host "  .\install.ps1 -PluginId anti-hallucination/strict-verification -Tool cursor"
    Write-Host "  .\install.ps1 -PluginId code-quality/clean-code-enforcer -TargetDir C:\Projects\MyApp"
    exit 0
}

# Determine marketplace root
$MarketplaceRoot = Split-Path -Parent $PSScriptRoot

# Paths
$PluginPath = Join-Path $MarketplaceRoot "plugins\$PluginId"
$PluginJson = Join-Path $PluginPath "plugin.json"
$RulesFile = Join-Path $PluginPath "rules.md"

Write-Host "╔═══════════════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║   Skywind Plugin Marketplace Installer       ║" -ForegroundColor Blue
Write-Host "╚═══════════════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Validate plugin exists
if (-not (Test-Path $PluginPath)) {
    Write-Host "Error: Plugin '$PluginId' not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available plugins:" -ForegroundColor Yellow
    Get-ChildItem -Path (Join-Path $MarketplaceRoot "plugins") -Recurse -Filter "plugin.json" |
        ForEach-Object {
            $_.DirectoryName.Replace("$MarketplaceRoot\plugins\", "")
        } | Sort-Object
    exit 1
}

if (-not (Test-Path $PluginJson)) {
    Write-Host "Error: Plugin metadata (plugin.json) not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $RulesFile)) {
    Write-Host "Error: Plugin rules (rules.md) not found" -ForegroundColor Red
    exit 1
}

# Read plugin metadata
$PluginData = Get-Content $PluginJson -Raw | ConvertFrom-Json
$PluginName = $PluginData.name
$PluginVersion = $PluginData.version
$PluginCategory = $PluginData.category

Write-Host "Plugin: " -NoNewline -ForegroundColor Green
Write-Host $PluginName
Write-Host "Version: " -NoNewline -ForegroundColor Green
Write-Host $PluginVersion
Write-Host "Category: " -NoNewline -ForegroundColor Green
Write-Host $PluginCategory
Write-Host "Target Tool: " -NoNewline -ForegroundColor Green
Write-Host $Tool
Write-Host "Target Directory: " -NoNewline -ForegroundColor Green
Write-Host $TargetDir
Write-Host ""

# Determine installation path based on tool
switch ($Tool) {
    "claude-code" {
        $InstallPath = Join-Path $TargetDir ".claude\rules"
        $PluginFileName = (Split-Path $PluginId -Leaf) + ".md"
        $InstallFile = Join-Path $InstallPath $PluginFileName
    }
    "cursor" {
        $InstallPath = $TargetDir
        $InstallFile = Join-Path $InstallPath ".cursorrules"
    }
    "windsurf" {
        $InstallPath = Join-Path $TargetDir ".windsurf\rules"
        $PluginFileName = (Split-Path $PluginId -Leaf) + ".md"
        $InstallFile = Join-Path $InstallPath $PluginFileName
    }
    default {
        Write-Host "Error: Unsupported tool '$Tool'" -ForegroundColor Red
        Write-Host "Supported tools: claude-code, cursor, windsurf"
        exit 1
    }
}

# Create installation directory if it doesn't exist
if (-not (Test-Path $InstallPath)) {
    Write-Host "Creating directory: $InstallPath" -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
}

# Check if file exists and ask for confirmation
if ((Test-Path $InstallFile) -and ($Tool -ne "cursor")) {
    Write-Host "Warning: File already exists at $InstallFile" -ForegroundColor Yellow
    $response = Read-Host "Do you want to overwrite it? (y/N)"
    if ($response -notmatch '^[Yy]$') {
        Write-Host "Installation cancelled" -ForegroundColor Red
        exit 1
    }
}

# Special handling for Cursor (append mode)
if ($Tool -eq "cursor") {
    if (Test-Path $InstallFile) {
        Write-Host "Appending to existing .cursorrules file" -ForegroundColor Yellow
        Add-Content -Path $InstallFile -Value ""
        Add-Content -Path $InstallFile -Value "# ================================================"
        Add-Content -Path $InstallFile -Value "# Plugin: $PluginName ($PluginVersion)"
        Add-Content -Path $InstallFile -Value "# Category: $PluginCategory"
        Add-Content -Path $InstallFile -Value "# ================================================"
        Add-Content -Path $InstallFile -Value ""
        Get-Content $RulesFile | Add-Content -Path $InstallFile
    } else {
        Copy-Item $RulesFile -Destination $InstallFile
    }
} else {
    # Direct copy for other tools
    Copy-Item $RulesFile -Destination $InstallFile -Force
}

Write-Host "✓ Plugin installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Installation Details:" -ForegroundColor Blue
Write-Host "  Location: $InstallFile"
Write-Host "  Plugin: $PluginName v$PluginVersion"
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "  1. Restart your AI coding assistant"
Write-Host "  2. The rules will be automatically applied"
Write-Host "  3. Check the plugin README for usage examples: $PluginPath\README.md"
Write-Host ""
Write-Host "Happy coding with verified accuracy! 🎯" -ForegroundColor Blue
