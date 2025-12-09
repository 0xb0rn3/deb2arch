<div align="center">

# 📄 deb2arch

<img src="https://img.shields.io/badge/Arch-Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white" alt="Arch Linux">
<img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Bash">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">

### 🚀 Smart .deb to Arch Package Converter

*Convert Debian packages to Arch Linux with intelligent dependency detection*

**Engineered by [oxbv1 | 0xb0rn3](https://github.com/0xb0rn3)**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## 🎯 Overview

**deb2arch** is a powerful, intelligent tool that converts Debian (.deb) packages into native Arch Linux packages (.pkg.tar.zst). It features **advanced binary analysis** to automatically detect and translate dependencies, making cross-distro package installation seamless.

```
┌───────────────────────────────────────────────────────┐
│  .deb Package  →  deb2arch  →  .pkg.tar.zst          │
│                     ↓                                 │
│           [Smart Dependency Detection]                │
│           [Debian→Arch Translation]                   │
│           [Binary ELF Analysis]                       │
└───────────────────────────────────────────────────────┘
```

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 **Smart Interface**
- Direct path input or interactive menu
- Auto-detection of package metadata
- Intelligent default suggestions
- Progress indicators with detailed feedback

### 📦 **Flexible Input**
- Local .deb files
- Remote URLs (downloads automatically)
- Handles all compression formats (xz, gz, zst)
- Quote-aware path parsing

</td>
<td width="50%">

### 🔬 **Advanced Analysis**
- **ELF binary scanning** with readelf
- **70+ library mappings** (Qt, GTK, X11, etc.)
- Automatic Debian→Arch package translation
- Real-time package verification with pacman
- Control file parsing

### ⚡ **Production Ready**
- Auto-installs missing dependencies
- **Auto-update from GitHub** (checks on startup)
- Comprehensive error handling
- Detailed build output
- Optional auto-install after build
- Version management (`--version`, `--update`)

</td>
</tr>
</table>

## 🔍 Dependency Detection

### How It Works

```
┌─────────────────────────────────────────────────────┐
│ 1. Extract .deb → Find ELF binaries                 │
│ 2. Run readelf -d → Extract NEEDED libraries        │
│ 3. Map libraries → Arch packages                    │
│    • libQt6Core.so.6 → qt6-base                     │
│    • libgtk-3.so.0 → gtk3                           │
│    • libxcb-cursor.so.0 → xcb-util-cursor           │
│ 4. Verify with pacman -Ss                           │
│ 5. Translate Debian control dependencies            │
│ 6. Deduplicate and generate depends=()              │
└─────────────────────────────────────────────────────┘
```

### Example Detection Output

```
🔬 Analyzing dependencies...
Extracting .deb for analysis...
Scanning for ELF binaries in /tmp/...
Found 47 ELF files
Detected 89 unique libraries
Verifying packages...
  ✓ qt6-base (from libQt6Core.so.6)
  ✓ gtk3 (from libgtk-3.so.0)
  ✓ openssl (from libssl.so.3)
  ✓ ffmpeg (from libavcodec.so.60)
  ✓ xcb-util-cursor (from libxcb-cursor.so.0)
  ✗ proprietary-lib (not in repos, check AUR)

Translating Debian dependencies...
  libxcb-cursor0 → xcb-util-cursor
  libgtk-3-0 → gtk3
```

## 📋 Requirements

```bash
# Auto-installed by deb2arch if missing:
- binutils      # ar, readelf for .deb extraction and ELF analysis
- libarchive    # bsdtar for archive handling
- pacman        # makepkg for building packages
- python        # Dependency analyzer (uses stdlib only)
```

These are standard on Arch Linux. If missing, deb2arch installs them automatically.

## 🔧 Installation

### Quick Install

```bash
# Clone the repository
git clone https://github.com/0xb0rn3/deb2arch.git

# Navigate to directory
cd deb2arch

# Make executable
chmod +x run

# Run the tool
./run
```

### Install Globally (Optional)

```bash
# Copy to /usr/local/bin
sudo cp run /usr/local/bin/deb2arch

# Now run from anywhere
deb2arch
```

### 🔄 Auto-Update Feature

deb2arch automatically checks for updates on startup when installed via git:

```bash
# On every run:
./run
# 🔍 Checking for updates...
# ✅ You're on the latest version

# If update available:
./run
# 📦 Update available!
# New version available on GitHub
# Update now? [Y/n]: y
# ✅ Updated successfully!
# Restarting with new version...
```

**Manual update commands:**

```bash
# Check for updates without running the tool
./run --update

# Show current version
./run --version
# deb2arch version 2.0.0
# Repository: https://github.com/0xb0rn3/deb2arch

# Show help
./run --help
```

**Note**: Auto-update only works when installed via `git clone`. If you copied the script manually, you'll need to update manually by re-cloning or pulling.

## 🚀 Usage

### Command Line Options

```bash
# Run normally (auto-checks for updates)
./run

# Check for updates only
./run --update
./run -u

# Show version
./run --version
./run -v

# Show help
./run --help
./run -h
```

### Quick Start

**Method 1: Direct Path Input** (Fastest)
```bash
./run
# At the prompt, paste:
/home/user/downloads/package.deb
```

**Method 2: Interactive Menu**
```bash
./run
# Enter: 1 (for local file)
# Then paste path
```

**Method 3: Remote URL**
```bash
./run
# Enter: 2 (for URL)
# Then paste URL
```

### Full Workflow

```
┌─────────────────────────────────────────────┐
│ 1. Start Tool                               │
│    ./run                                     │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│ 2. Provide .deb Source                      │
│    • Direct path: /path/to/file.deb        │
│    • Or menu: 1 → path                      │
│    • Or URL: 2 → http://...                 │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│ 3. Auto-Extract Metadata                    │
│    • Package name (from filename)           │
│    • Version (from control file)            │
│    • Description (from control)             │
│    • Press Enter to accept defaults         │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│ 4. Smart Dependency Detection               │
│    • Scans ELF binaries automatically       │
│    • Translates Debian packages             │
│    • Verifies with pacman                   │
│    • Shows detected dependencies            │
│    • Allows manual additions                │
└─────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────┐
│ 5. Build & Install                          │
│    • Generates PKGBUILD                     │
│    • Builds with makepkg                    │
│    • Optional: auto-install with pacman     │
└─────────────────────────────────────────────┘
```

## 💡 Examples

### Example 1: FDM (Free Download Manager)

```bash
$ ./run

╔════════════════════════════════════════════════╗
║      deb2arch - .deb to Arch Converter        ║
║      Engineered by: oxbv1 | 0xb0rn3           ║
║      Version: 2.0.0                           ║
╚════════════════════════════════════════════════╝

🔍 Checking for updates...
✅ You're on the latest version

📦 Package Source
Enter path to .deb file (or 1/2 for menu): /home/user/freedownloadmanager.deb

🔍 Extracting package info...

📝 Package Information
👤 Maintainer [Your Name <email@example.com>]: oxbv1 <q4n0@proton.me>
Package name [freedownloadmanager]: ↵
Version [6.31.0.6549]: ↵
Release [1]: ↵
Architecture [x86_64]: ↵
Description [FDM is a powerful modern download accelerator...]: ↵
URL: freedownloadmanager.org
License [MIT]: ↵

🔬 Analyzing dependencies...
Extracting .deb for analysis...
Scanning for ELF binaries...
Found 47 ELF files
Detected 89 unique libraries
Verifying packages...
  ✓ qt6-base (from libQt6Core.so.6)
  ✓ openssl (from libssl.so.3)
  ✓ ffmpeg (from libavcodec.so.60)
  ✓ xcb-util-cursor (from libxcb-cursor.so.0)
  ✓ zstd (from libzstd.so.1)

Translating Debian dependencies...
  libxcb-cursor0 → xcb-util-cursor
  bubblewrap → bubblewrap

Dependencies [qt6-base,openssl,ffmpeg,xcb-util-cursor,...]: ↵

📁 Build directory [/tmp/deb2arch-build]: ~/builds/fdm
🚀 Install after build? [y/N]: y

✍️  Generating PKGBUILD...
✅ PKGBUILD created: /home/user/builds/fdm/PKGBUILD

🔨 Build now? [Y/n]: y

Building package (this may take a while)...
==> Making package: freedownloadmanager 6.31.0.6549-1
==> Checking runtime dependencies...
==> Checking buildtime dependencies...
==> Retrieving sources...
==> Extracting sources...
==> Starting package()...
==> Tidying install...
==> Creating package "freedownloadmanager"...
==> Finished making: freedownloadmanager 6.31.0.6549-1

✅ Build successful!
📦 Package: /home/user/builds/fdm/freedownloadmanager-6.31.0.6549-1-x86_64.pkg.tar.zst

Installing package...
[sudo] password for user:
loading packages...
resolving dependencies...
✅ Installed!

✨ Done!
```

### Example 2: Quick Conversion

```bash
# Paste path directly, accept all defaults, auto-install
$ ./run
/home/user/app.deb  # Paste path
↵↵↵↵↵↵↵↵           # Accept all defaults
y                   # Install after build
y                   # Build now
# Done in ~30 seconds!
```

### Example 3: Custom Configuration

```bash
$ ./run
1                           # Menu mode
/path/to/package.deb        # Local file

# Custom metadata:
oxbv1 <q4n0@proton.me>     # Maintainer
myapp                       # Package name
2.5.1                       # Version
security-tool               # Different name
# ... etc

# Manual dependencies:
qt6-base,libxcb,custom-lib  # Add custom deps

~/builds/security           # Custom build dir
n                           # Don't auto-install
y                           # But do build now
```

## 📊 Dependency Translation Map

deb2arch includes **70+ pre-configured mappings**:

| Debian Package | Arch Package | Category |
|---------------|--------------|----------|
| `libxcb-cursor0` | `xcb-util-cursor` | X11 |
| `libgtk-3-0` | `gtk3` | GUI |
| `libgtk-3-dev` | `gtk3` | GUI |
| `libqt5core5a` | `qt5-base` | Qt5 |
| `libqt6core6` | `qt6-base` | Qt6 |
| `libnss3` | `nss` | Security |
| `libssl-dev` | `openssl` | Security |
| `libcurl4` | `curl` | Network |
| `libavcodec58` | `ffmpeg` | Media |
| `libpulse0` | `libpulse` | Audio |
| `libgbm1` | `mesa` | Graphics |
| `libpq5` | `postgresql-libs` | Database |
| `libmariadb3` | `mariadb-libs` | Database |
| `build-essential` | `base-devel` | Build |

### Library Detection

The ELF analyzer automatically detects:

```python
# Qt Framework
libQt5*.so → qt5-base
libQt6*.so → qt6-base

# GTK/GNOME
libgtk-*.so → gtk3/gtk4
libglib-*.so → glib2
libcairo*.so → cairo

# X11/Wayland
libxcb*.so → libxcb, xcb-util-*
libwayland*.so → wayland
libxkbcommon*.so → libxkbcommon

# Media
libav*.so → ffmpeg
libpulse*.so → libpulse
libasound*.so → alsa-lib

# And 50+ more mappings...
```

## 🎯 Use Cases

- 🔒 **Security Tools**: Convert Kali/Parrot packages to Arch
- 💼 **Proprietary Software**: Package commercial apps (Slack, Discord alternatives, etc.)
- 🧪 **Testing**: Try Debian/Ubuntu packages on Arch
- 📦 **Package Maintenance**: Create Arch packages from upstream .deb releases
- 🎮 **Gaming**: Convert game installers and dependencies
- 🏢 **Enterprise**: Deploy company .deb packages on Arch infrastructure

## 🛠️ Advanced Usage

### Customize Dependencies

```bash
# After auto-detection, you can modify:
Dependencies [qt6-base,openssl,ffmpeg]: qt6-base,openssl,ffmpeg,custom-lib,aur-package
```

### Custom Build Directory

```bash
Build directory [/tmp/deb2arch-build]: ~/projects/packaging/myapp
Save package to [~/projects/packaging/myapp]: ~/releases/
```

### Architecture Override

```bash
Architecture [x86_64]: aarch64  # For ARM packages
Architecture [x86_64]: any      # For arch-independent packages
```

### Manual PKGBUILD Editing

```bash
# After generation:
vim ~/builds/myapp/PKGBUILD

# Then build manually:
cd ~/builds/myapp
makepkg -sf
sudo pacman -U myapp-1.0.0-1-x86_64.pkg.tar.zst
```

## 🐛 Troubleshooting

### Issue: Update Check Fails

```
⚠️  Could not check for updates (no internet?)
```

**Causes**:
- No internet connection
- Not installed via git clone
- GitHub is unreachable

**Solution**:
```bash
# Manual update:
cd /path/to/deb2arch
git pull origin main

# Or re-clone:
git clone https://github.com/0xb0rn3/deb2arch.git
```

### Issue: Missing Dependencies Not Auto-Installing

```bash
# Manual install:
sudo pacman -S binutils libarchive python
```

### Issue: Dependency Detection Incomplete

```bash
# Run with more verbose output:
cd /tmp
# Check the analyzer output manually:
python3 /tmp/deb2arch_analyzer.py /path/to/extracted/deb
```

### Issue: Package Not in Official Repos

```
  ✗ proprietary-lib (not in repos, check AUR)
```

**Solution**: Manually install from AUR first:
```bash
yay -S proprietary-lib
# Then re-run deb2arch
```

### Issue: Build Fails

```bash
# Check the PKGBUILD:
cat ~/builds/myapp/PKGBUILD

# Common fixes:
# 1. Add missing dependencies manually
# 2. Check architecture (x86_64 vs any)
# 3. Verify source path is correct
```

### Issue: Permission Errors After Install

The PKGBUILD includes comprehensive permission fixes, but if issues persist:

```bash
# Manual fix for executables:
sudo find /opt/myapp -type f -name "*.sh" -exec chmod +x {} \;
sudo find /opt/myapp -type f -executable -exec chmod +x {} \;

# Manual fix for libraries:
sudo find /opt/myapp -type f -name "*.so*" -exec chmod 755 {} \;
```

## 📈 Performance

### Benchmark (Typical .deb ~50MB)

| Task | Time | Details |
|------|------|---------|
| Dependency check | <1s | Checks 5 core dependencies |
| Extract .deb info | <1s | Reads control file |
| Binary analysis | 2-5s | Scans all ELF files |
| Dependency translation | <1s | Maps and verifies packages |
| Build package | 10-60s | Depends on package size |
| **Total** | **15-70s** | Full end-to-end |

### Tested With

- ✅ FDM (Free Download Manager) - 50MB, Qt6 app
- ✅ Chrome/Chromium - 200MB, complex deps
- ✅ VS Code - 100MB, Electron app
- ✅ Small CLI tools - <5MB, minimal deps
- ✅ Game engines - Unity, Godot installers

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

### Priority Tasks

1. **Expand Library Mappings**
   - Add more obscure library → package mappings
   - Test with more .deb packages
   
2. **Improve Detection**
   - Better heuristics for proprietary libraries
   - Enhanced AUR package suggestions
   
3. **Testing**
   - Add test suite with various .deb files
   - Automated testing on common packages

### How to Contribute

```bash
# 1. Fork the repository
git clone https://github.com/yourusername/deb2arch.git

# 2. Create a feature branch
git checkout -b feature/improve-detection

# 3. Make your changes
vim run  # Edit the main script

# 4. Test thoroughly
./run /path/to/test.deb

# 5. Commit and push
git commit -am "Improve Qt6 detection"
git push origin feature/improve-detection

# 6. Open a Pull Request
```

### Code Style

- **Bash**: 4-space indent, use `[[ ]]` for tests
- **Python**: PEP 8, type hints encouraged
- **Comments**: Explain complex logic
- **Testing**: Test with at least 3 different .deb files

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 oxbv1 | 0xb0rn3

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

## 🙏 Acknowledgments

- Built for the **Arch Linux community**
- Inspired by `debtap` and `alien`, but modernized
- Special thanks to all contributors and testers
- ELF analysis powered by GNU `binutils`

## 📞 Contact & Support

**oxbv1 | 0xb0rn3**

- 🐙 GitHub: [@0xb0rn3](https://github.com/0xb0rn3)
- 📧 Email: q4n0@proton.me
- 💬 Issues: [GitHub Issues](https://github.com/0xb0rn3/deb2arch/issues)
- 📦 Project: [deb2arch](https://github.com/0xb0rn3/deb2arch)

### Getting Help

1. **Check this README** - Most questions answered here
2. **Search Issues** - Someone may have had the same problem
3. **Open an Issue** - Provide:
   - Your Arch Linux version
   - The .deb file you're trying to convert
   - Full error output
   - Steps to reproduce

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ for the Arch Linux community**

```
 ▓▓▓▓▓▓╗ ▓▓╗  ▓▓╗▓▓▓▓▓▓╗  ▓▓▓▓▓▓╗ ▓▓▓▓▓▓╗ ▓▓▓╗   ▓▓╗▓▓▓▓▓▓▓╗
▓▓╔═▓▓▓▓╗╚▓▓╗▓▓╔╝▓▓╔══▓▓╗▓▓╔═▓▓▓▓╗▓▓╔══▓▓╗▓▓▓▓╗  ▓▓║▓▓╔════╝
▓▓║▓▓╔▓▓║ ╚▓▓▓╔╝ ▓▓▓▓▓▓╔╝▓▓║▓▓╔▓▓║▓▓▓▓▓▓╔╝▓▓╔▓▓╗ ▓▓║▓▓▓▓▓╗  
▓▓▓▓╔╝▓▓║ ▓▓╔▓▓╗ ▓▓╔══▓▓╗▓▓▓▓╔╝▓▓║▓▓╔══▓▓╗▓▓║╚▓▓╗▓▓║▓▓╔══╝  
╚▓▓▓▓▓▓╔╝▓▓╔╝ ▓▓╗▓▓▓▓▓▓╔╝╚▓▓▓▓▓▓╔╝▓▓║  ▓▓║▓▓║ ╚▓▓▓▓║▓▓▓▓▓▓▓╗
 ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
```

**Current Version**: 2.0.0 (Smart Detection Release)

[⬆ Back to Top](#-deb2arch)

</div>
