# Docker Troubleshooting Guide

## Issue: Docker Command Not Recognized

If you get `'docker' is not recognized`, try these steps:

### Step 1: Check Docker Desktop is Running

1. Look for Docker Desktop icon in system tray (bottom right)
2. If not running, start Docker Desktop from Start menu
3. Wait for it to fully start (whale icon should be steady, not animating)

### Step 2: Restart Your Terminal

**Important:** After installing Docker, you MUST:
1. Close ALL command prompt/PowerShell windows
2. Open a NEW command prompt/PowerShell
3. Try `docker --version` again

The PATH environment variable is updated when Docker Desktop starts, but existing terminals don't see it.

### Step 3: Verify Docker Desktop is Running

Open Docker Desktop application and check:
- Status shows "Docker Desktop is running"
- No error messages
- Settings → General → "Use the WSL 2 based engine" is checked (if available)

### Step 4: Manual PATH Check

If still not working, Docker might not be in PATH. Check:

**Typical Docker paths:**
- `C:\Program Files\Docker\Docker\resources\bin`
- `C:\Program Files\Docker\Docker\resources\wsl`

**To add manually:**
1. Open System Properties → Environment Variables
2. Edit PATH variable
3. Add Docker paths above
4. Restart terminal

### Step 5: Verify Installation

After restarting terminal, run:
```cmd
docker --version
```

Should show: `Docker version 24.x.x, build xxxxx`

## Quick Fix Checklist

- [ ] Docker Desktop is installed
- [ ] Docker Desktop is running (check system tray)
- [ ] Closed and reopened command prompt/PowerShell
- [ ] Tried `docker --version` in new terminal
- [ ] Restarted computer (if still not working)

## Alternative: Use Docker Desktop GUI

If command line doesn't work, you can:
1. Open Docker Desktop
2. Use the GUI to manage containers
3. Or use the terminal built into Docker Desktop

## Still Not Working?

1. **Reinstall Docker Desktop** - Sometimes installation doesn't complete properly
2. **Check Windows Features** - Ensure WSL 2 and Virtual Machine Platform are enabled
3. **Check BIOS** - Virtualization must be enabled in BIOS
4. **Check Windows Version** - Must be Windows 10/11 64-bit Pro/Enterprise/Education

## Test After Fix

Once Docker works, test with:
```cmd
docker --version
docker ps
```

Then proceed with:
```cmd
cd path\to\treasure-hunt-analyzer
docker-compose up -d
```

