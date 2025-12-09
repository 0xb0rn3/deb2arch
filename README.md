<div align="center">

# 📄 deb2arch

<img src="https://img.shields.io/badge/Arch-Linux-1793D1?style=for-the-badge&logo=arch-linux&logoColor=white" alt="Arch Linux">
<img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white" alt="Bash">
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">

### 🚀 Smart .deb to Arch Package Converter

*Convert Debian packages to Arch Linux with intelligent dependency detection*

**Engineered by [oxbv1 | 0xb0rn3](https://github.com/0xb0rn3)**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples)

</div>

---

## 🎯 Overview

**deb2arch** converts Debian (.deb) packages into native Arch Linux packages (.pkg.tar.zst) with automatic binary analysis for dependency detection.

```
┌───────────────────────────────────────────────────┐
│  .deb Package  →  deb2arch  →  .pkg.tar.zst       │
│                     ↓                              │
│           [Binary ELF Analysis]                    │
│           [Debian→Arch Translation]                │
│           [Smart Dependency Detection]             │
└───────────────────────────────────────────────────┘
```

## ✨ Features

<table>
<tr>
<td width="50%">

### 🎨 **Interface**
- Direct path input or interactive menu
- Auto-detection of package metadata
- Progress indicators with feedback
- Quote-aware path parsing

### 📦 **Input**
- Local .deb files
- All compression formats (xz, gz, zst)
- Control file parsing

</td>
<td width="50%">

### 🔬 **Analysis**
- **ELF binary scanning** with readelf
- **70+ library mappings** (Qt, GTK, X11, etc.)
- Debian→Arch package translation
- Real-time verification with pacman
- Control file dependency parsing

### ⚡ **Production**
- Auto-installs missing dependencies
- **Auto-update from GitHub**
- Comprehensive error handling
- Optional auto-install after build
- Version management

</td>
</tr>
</table>

## 🔍 Dependency Detection

### How It Works

```
┌───────────────────────────────────────────────────┐
│ 1. Extract .deb → Find ELF binaries               │
│ 2. Run readelf -d → Extract NEEDED libraries      │
│ 3. Map libraries → Arch packages                  │
│    • libQt6Core.so.6 → qt6-base                   │
│    • libgtk-3.so.0 → gtk3                         │
│    • libxcb-cursor.so.0 → xcb-util-cursor         │
│ 4. Verify with pacman -Ss                         │
│ 5. Translate Debian control dependencies          │
│ 6. Deduplicate and generate depends=()            │
└───────────────────────────────────────────────────┘
```

## 📋 Requirements

```bash
# Auto-installed if missing:
- binutils      # ar, readelf
- libarchive    # bsdtar
- pacman        # makepkg
- python        # Core analyzer
```

## 🔧 Installation

### Quick Install

```bash
git clone https://github.com/0xb0rn3/deb2arch.git
cd deb2arch
chmod +x run deb2arch.py
./run
```

### Install Globally

```bash
sudo cp run /usr/local/bin/deb2arch
sudo cp deb2arch.py /usr/local/bin/
deb2arch
```

### 🔄 Auto-Update

```bash
./run
# 🔍 Checking for updates...
# ✅ Latest version

./run --update  # Force update check
./run --version # Show version
./run --help    # Show help
```

## 🚀 Usage

### Command Line

```bash
./run               # Run normally (auto-checks updates)
./run --update      # Check for updates
./run --version     # Show version
./run --help        # Show help
```

### Quick Start

**Direct Path Input**
```bash
./run
/home/user/downloads/package.deb
```

### Full Workflow

```
┌───────────────────────────────────────────┐
│ 1. Start Tool                             │
│    ./run                                  │
└───────────────────────────────────────────┘
           ↓
┌───────────────────────────────────────────┐
│ 2. Provide .deb Path                      │
│    /path/to/file.deb                      │
└───────────────────────────────────────────┘
           ↓
┌───────────────────────────────────────────┐
│ 3. Auto-Extract Metadata                  │
│    • Package name (from filename)         │
│    • Version (from control file)          │
│    • Description (from control)           │
│    • Press Enter to accept defaults       │
└───────────────────────────────────────────┘
           ↓
┌───────────────────────────────────────────┐
│ 4. Smart Dependency Detection             │
│    • Scans ELF binaries                   │
│    • Translates Debian packages           │
│    • Verifies with pacman                 │
│    • Shows detected dependencies          │
│    • Allows manual additions              │
└───────────────────────────────────────────┘
           ↓
┌───────────────────────────────────────────┐
│ 5. Build & Install                        │
│    • Generates PKGBUILD                   │
│    • Builds with makepkg                  │
│    • Optional: auto-install with pacman   │
└───────────────────────────────────────────┘
```

## 💡 Examples

### Example 1: FDM (Free Download Manager)

```bash
$ ./run

╔═══════════════════════════════════════════════╗
║      deb2arch - .deb to Arch Converter        ║
║      Engineered by: oxbv1 | 0xb0rn3           ║
║      Version: 0.0.1                           ║
╚═══════════════════════════════════════════════╝

🔍 Checking for updates...
✅ Latest version

📦 Package Source
Enter path to .deb file: /home/user/freedownloadmanager.deb

🔍 Extracting package info...

📋 Package Information
👤 Maintainer [Your Name <email@example.com>]: oxbv1 <q4n0@proton.me>
Package name [freedownloadmanager]: ↵
Version [6.31.0.6549]: ↵
Release [1]: ↵
Architecture [x86_64]: ↵
Description [FDM is a powerful download accelerator]: ↵
URL: freedownloadmanager.org
License [MIT]: ↵

🔬 Analyzing dependencies...
Scanning for ELF binaries...
Found 47 ELF files
Detected 89 unique libraries
Verifying packages...
  ✓ qt6-base (from libQt6Core.so.6)
  ✓ openssl (from libssl.so.3)
  ✓ ffmpeg (from libavcodec.so.60)
  ✓ xcb-util-cursor (from libxcb-cursor.so.0)

Dependencies [qt6-base,openssl,ffmpeg,xcb-util-cursor]: ↵

📁 Build directory [/tmp/deb2arch-build]: ~/builds/fdm
🚀 Install after build? [y/N]: y

✏️  Generating PKGBUILD...
✅ PKGBUILD created: /home/user/builds/fdm/PKGBUILD

🔨 Build now? [Y/n]: y

Building package (this may take a while)...
==> Making package: freedownloadmanager 6.31.0.6549-1
✅ Build successful!
📦 Package: /home/user/builds/fdm/freedownloadmanager-6.31.0.6549-1-x86_64.pkg.tar.zst

Installing package...
✅ Installed!

✨ Done!
```

### Example 2: Quick Conversion

```bash
$ ./run
/home/user/app.deb
↵↵↵↵↵↵↵↵
y
y
```

## 📊 Dependency Translation

deb2arch includes **70+ pre-configured mappings**:

| Debian Package | Arch Package | Category |
|---------------|--------------|----------|
| `libxcb-cursor0` | `xcb-util-cursor` | X11 |
| `libgtk-3-0` | `gtk3` | GUI |
| `libqt5core5a` | `qt5-base` | Qt5 |
| `libqt6core6` | `qt6-base` | Qt6 |
| `libssl-dev` | `openssl` | Security |
| `libcurl4` | `curl` | Network |
| `libavcodec58` | `ffmpeg` | Media |
| `build-essential` | `base-devel` | Build |

### Library Detection

```python
# Qt Framework
libQt5*.so → qt5-base
libQt6*.so → qt6-base

# GTK/GNOME
libgtk-*.so → gtk3/gtk4
libglib-*.so → glib2

# X11/Wayland
libxcb*.so → libxcb, xcb-util-*
libwayland*.so → wayland

# Media
libav*.so → ffmpeg
libpulse*.so → libpulse

# And 50+ more mappings...
```

## 🎯 Use Cases

- 🔒 **Security Tools**: Convert Kali/Parrot packages
- 💼 **Proprietary Software**: Package commercial apps
- 🧪 **Testing**: Try Debian/Ubuntu packages on Arch
- 📦 **Package Maintenance**: Create Arch packages from upstream
- 🎮 **Gaming**: Convert game installers
- 🏢 **Enterprise**: Deploy .deb packages on Arch

## 🛠️ Advanced Usage

### Customize Dependencies

```bash
Dependencies [qt6-base,openssl]: qt6-base,openssl,custom-lib
```

### Custom Build Directory

```bash
Build directory [/tmp/deb2arch-build]: ~/projects/packaging/myapp
```

### Architecture Override

```bash
Architecture [x86_64]: aarch64  # ARM packages
Architecture [x86_64]: any      # arch-independent
```

## 🐛 Troubleshooting

### Update Check Fails

```
⚠️  Could not check for updates
```

**Solution**:
```bash
cd /path/to/deb2arch
git pull origin main
```

### Missing Dependencies

```bash
sudo pacman -S binutils libarchive python
```

### Build Fails

```bash
cat ~/builds/myapp/PKGBUILD
```

## 📈 Performance

### Benchmark (Typical .deb ~50MB)

| Task | Time |
|------|------|
| Extract .deb info | <1s |
| Binary analysis | 2-5s |
| Dependency translation | <1s |
| Build package | 10-60s |
| **Total** | **15-70s** |

### Tested With

- ✅ FDM (Free Download Manager) - 50MB
- ✅ Chrome/Chromium - 200MB
- ✅ VS Code - 100MB
- ✅ Small CLI tools - <5MB
- ✅ Game engines

## 🤝 Contributing

```bash
git clone https://github.com/yourusername/deb2arch.git
git checkout -b feature/improve-detection
# Make changes
git commit -am "Add more mappings"
git push origin feature/improve-detection
```

### Code Style

- **Bash**: 4-space indent
- **Python**: PEP 8
- **Testing**: Test with 3+ different .deb files

## 📜 License

MIT License - Copyright (c) 2024 oxbv1 | 0xb0rn3

## 🙏 Acknowledgments

- Built for the **Arch Linux community**
- Inspired by `debtap` and `alien`
- ELF analysis powered by GNU `binutils`

## 📞 Contact

**oxbv1 | 0xb0rn3**

- 🐙 GitHub: [@0xb0rn3](https://github.com/0xb0rn3)
- 📧 Email: q4n0@proton.me
- 💬 Issues: [GitHub Issues](https://github.com/0xb0rn3/deb2arch/issues)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!

**Made with ❤️ for the Arch Linux community**

```
 ▓▓▓▓▓▓╗ ▓▓╗  ▓▓╗▓▓▓▓▓▓╗  ▓▓▓▓▓▓╗ ▓▓▓▓▓▓╗ ▓▓▓╗   ▓▓╗▓▓▓▓▓▓▓╗
▓▓╔═▓▓▓▓╗╚▓▓╗▓▓╔╝▓▓╔══▓▓╗▓▓╔═▓▓▓▓╗▓▓╔══▓▓╗▓▓▓▓╗  ▓▓║▓▓╔════╝
▓▓║▓▓╔▓▓║ ╚▓▓▓╔╝ ▓▓▓▓▓▓╔╝▓▓║▓▓╔▓▓║▓▓▓▓▓╔╝▓▓╔▓▓▓╗ ▓▓║▓▓▓▓▓╗  
▓▓▓▓╔╝▓▓║ ▓▓╔▓▓╗ ▓▓╔══▓▓╗▓▓▓▓╔╝▓▓║▓▓╔══▓▓╗▓▓║╚▓▓╗▓▓║▓▓╔══╝  
╚▓▓▓▓▓▓╔╝▓▓╔╝ ▓▓╗▓▓▓▓▓▓╔╝╚▓▓▓▓▓▓╔╝▓▓║  ▓▓║▓▓║ ╚▓▓▓▓║▓▓▓▓▓▓▓╗
 ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝
```

**Current Version**: 0.0.1 (Stable Release)

[⬆ Back to Top](#-deb2arch)

</div>
