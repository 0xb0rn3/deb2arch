#!/usr/bin/env python3

import os
import sys
import json
import subprocess
import tempfile
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional, Set

VERSION = "0.0.1"

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'

MAPPINGS = {
    'build-essential': 'base-devel',
    'gcc': 'gcc', 'g++': 'gcc', 'make': 'make', 'cmake': 'cmake',
    'libssl-dev': 'openssl', 'libssl3': 'openssl', 'libssl1.1': 'openssl',
    'libcrypto++': 'crypto++',
    'zlib1g': 'zlib', 'zlib1g-dev': 'zlib',
    'libbz2-1.0': 'bzip2', 'libbz2-dev': 'bzip2',
    'liblzma5': 'xz', 'liblzma-dev': 'xz',
    'libzstd1': 'zstd', 'libzstd-dev': 'zstd',
    'libxml2': 'libxml2', 'libxml2-dev': 'libxml2',
    'libxslt1.1': 'libxslt', 'libxslt1-dev': 'libxslt',
    'libsqlite3-0': 'sqlite', 'libsqlite3-dev': 'sqlite',
    'libpq5': 'postgresql-libs', 'libpq-dev': 'postgresql-libs',
    'libmariadb3': 'mariadb-libs', 'libmariadb-dev': 'mariadb-libs',
    'libcurl4': 'curl', 'libcurl4-openssl-dev': 'curl', 'libcurl4-gnutls-dev': 'curl',
    'libgtk-3-0': 'gtk3', 'libgtk-3-dev': 'gtk3',
    'libgtk-4-1': 'gtk4', 'libgtk-4-dev': 'gtk4',
    'libqt5core5a': 'qt5-base', 'libqt5gui5': 'qt5-base', 'libqt5widgets5': 'qt5-base',
    'qtbase5-dev': 'qt5-base', 'libqt6core6': 'qt6-base',
    'libx11-6': 'libx11', 'libx11-dev': 'libx11',
    'libxext6': 'libxext', 'libxrender1': 'libxrender',
    'libxcb1': 'libxcb', 'libxcb-cursor0': 'xcb-util-cursor',
    'libwayland-client0': 'wayland', 'libwayland-server0': 'wayland',
    'libc6': 'glibc', 'libc6-dev': 'glibc',
    'libstdc++6': 'gcc-libs', 'libgcc-s1': 'gcc-libs',
    'python3': 'python', 'python3-dev': 'python', 'python3-pip': 'python-pip',
    'perl': 'perl', 'perl-base': 'perl',
    'coreutils': 'coreutils', 'findutils': 'findutils',
    'grep': 'grep', 'sed': 'sed', 'gawk': 'gawk',
    'libnss3': 'nss', 'libnotify4': 'libnotify',
    'libxtst6': 'libxtst', 'libgbm1': 'mesa'
}

LIB_MAPPINGS = {
    'libQt5Core': 'qt5-base', 'libQt5Gui': 'qt5-base', 'libQt5Widgets': 'qt5-base',
    'libQt5Network': 'qt5-base', 'libQt5DBus': 'qt5-base',
    'libQt6Core': 'qt6-base', 'libQt6Gui': 'qt6-base', 'libQt6Widgets': 'qt6-base',
    'libgtk-3': 'gtk3', 'libgtk-4': 'gtk4', 'libgdk-3': 'gtk3',
    'libglib-2': 'glib2', 'libgio-2': 'glib2', 'libgobject-2': 'glib2',
    'libcairo': 'cairo', 'libpango': 'pango', 'libatk': 'atk',
    'libgdk_pixbuf': 'gdk-pixbuf2',
    'libX11': 'libx11', 'libXext': 'libxext', 'libXrender': 'libxrender',
    'libxcb': 'libxcb', 'libxcb-cursor': 'xcb-util-cursor',
    'libxcb-icccm': 'xcb-util-wm', 'libxcb-image': 'xcb-util-image',
    'libxcb-keysyms': 'xcb-util-keysyms', 'libxcb-render-util': 'xcb-util-renderutil',
    'libxcb-util': 'xcb-util', 'libxkbcommon': 'libxkbcommon',
    'libxkbcommon-x11': 'libxkbcommon-x11',
    'libwayland-client': 'wayland', 'libwayland-cursor': 'wayland',
    'libwayland-egl': 'wayland',
    'libssl': 'openssl', 'libcrypto': 'openssl',
    'libcurl': 'curl', 'libcurl-gnutls': 'curl',
    'libsqlite3': 'sqlite', 'libpq': 'postgresql-libs',
    'libmysqlclient': 'mariadb-libs', 'libmariadb': 'mariadb-libs',
    'libavcodec': 'ffmpeg', 'libavformat': 'ffmpeg', 'libavutil': 'ffmpeg',
    'libswscale': 'ffmpeg', 'libswresample': 'ffmpeg',
    'libSDL2': 'sdl2', 'libpulse': 'libpulse', 'libasound': 'alsa-lib',
    'libGL': 'mesa', 'libGLX': 'mesa', 'libEGL': 'mesa',
    'libgbm': 'mesa', 'libdrm': 'libdrm', 'libvulkan': 'vulkan-icd-loader',
    'libfontconfig': 'fontconfig', 'libfreetype': 'freetype2',
    'libharfbuzz': 'harfbuzz',
    'libbz2': 'bzip2', 'liblzma': 'xz', 'libz': 'zlib',
    'libzstd': 'zstd', 'libbrotlidec': 'brotli', 'libbrotlienc': 'brotli',
    'libdbus-1': 'dbus', 'libicu': 'icu', 'libtiff': 'libtiff',
    'libpng': 'libpng', 'libjpeg': 'libjpeg-turbo',
    'libwebp': 'libwebp'
}

SYSTEM_LIBS = {
    'libc.so', 'libm.so', 'libpthread.so', 'libdl.so', 'librt.so',
    'libstdc++.so', 'libgcc_s.so', 'ld-linux', 'linux-vdso.so'
}

def run_cmd(cmd: List[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, **kwargs)

def extract_control(deb_path: str) -> Dict[str, str]:
    temp = tempfile.mkdtemp()
    try:
        run_cmd(['ar', 'x', deb_path], cwd=temp, check=True)
        
        control_file = None
        for f in Path(temp).glob('control.tar.*'):
            control_file = f
            break
        
        if not control_file:
            return {}
        
        if control_file.suffix == '.gz':
            run_cmd(['tar', 'xzf', str(control_file)], cwd=temp)
        elif control_file.suffix == '.xz':
            run_cmd(['tar', 'xJf', str(control_file)], cwd=temp)
        elif control_file.suffix == '.zst':
            run_cmd(['tar', '--zstd', '-xf', str(control_file)], cwd=temp)
        else:
            run_cmd(['tar', 'xf', str(control_file)], cwd=temp)
        
        control_path = Path(temp) / 'control'
        if not control_path.exists():
            return {}
        
        data = {}
        current_field = None
        current_value = []
        
        with open(control_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.rstrip('\n')
                
                if line and not line.startswith(' '):
                    if current_field:
                        data[current_field] = '\n'.join(current_value)
                    
                    if ':' in line:
                        field, value = line.split(':', 1)
                        current_field = field.strip()
                        current_value = [value.strip()]
                
                elif line.startswith(' ') and current_field:
                    current_value.append(line.strip())
        
        if current_field:
            data[current_field] = '\n'.join(current_value)
        
        return data
    
    finally:
        shutil.rmtree(temp, ignore_errors=True)

def find_elf_files(directory: str) -> List[Path]:
    elf_files = []
    for path in Path(directory).rglob('*'):
        if not path.is_file():
            continue
        try:
            with open(path, 'rb') as f:
                magic = f.read(4)
                if magic == b'\x7fELF':
                    elf_files.append(path)
        except:
            continue
    return elf_files

def get_elf_deps(elf_path: Path) -> Set[str]:
    deps = set()
    try:
        result = run_cmd(['readelf', '-d', str(elf_path)], timeout=10)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'NEEDED' in line:
                    match = re.search(r'\[(.*?)\]', line)
                    if match:
                        lib = match.group(1)
                        if not any(sys_lib in lib for sys_lib in SYSTEM_LIBS):
                            deps.add(lib)
    except:
        pass
    return deps

def map_lib_to_pkg(lib: str) -> Optional[str]:
    for pattern, pkg in LIB_MAPPINGS.items():
        if pattern in lib:
            return pkg
    
    match = re.match(r'lib(.+?)\.so', lib)
    if match:
        return match.group(1)
    
    return None

def verify_pkg(pkg: str) -> bool:
    try:
        result = run_cmd(['pacman', '-Ss', f'^{pkg}$'], timeout=5)
        return result.returncode == 0
    except:
        return False

def analyze_binary_deps(deb_path: str) -> List[str]:
    temp = tempfile.mkdtemp()
    try:
        run_cmd(['ar', 'x', deb_path], cwd=temp)
        
        data_file = None
        for f in Path(temp).glob('data.tar.*'):
            data_file = f
            break
        
        if not data_file:
            return []
        
        if data_file.suffix == '.gz':
            run_cmd(['tar', 'xzf', str(data_file)], cwd=temp)
        elif data_file.suffix == '.xz':
            run_cmd(['tar', 'xJf', str(data_file)], cwd=temp)
        elif data_file.suffix == '.zst':
            run_cmd(['tar', '--zstd', '-xf', str(data_file)], cwd=temp)
        else:
            run_cmd(['tar', 'xf', str(data_file)], cwd=temp)
        
        print(f"{Colors.CYAN}Scanning for ELF binaries...{Colors.NC}", file=sys.stderr)
        elf_files = find_elf_files(temp)
        print(f"Found {len(elf_files)} ELF files", file=sys.stderr)
        
        all_libs = set()
        for elf_file in elf_files:
            libs = get_elf_deps(elf_file)
            all_libs.update(libs)
        
        print(f"Detected {len(all_libs)} unique libraries", file=sys.stderr)
        
        packages = {}
        for lib in sorted(all_libs):
            pkg = map_lib_to_pkg(lib)
            if pkg:
                packages[pkg] = lib
        
        verified = []
        print("Verifying packages...", file=sys.stderr)
        for pkg in sorted(packages.keys()):
            if verify_pkg(pkg):
                verified.append(pkg)
                print(f"  ✓ {pkg} (from {packages[pkg]})", file=sys.stderr)
            else:
                print(f"  ✗ {pkg} (not in repos, check AUR)", file=sys.stderr)
        
        return verified
    
    finally:
        shutil.rmtree(temp, ignore_errors=True)

def translate_deb_pkg(deb_pkg: str) -> str:
    pkg = re.sub(r'\s*\([^)]*\)', '', deb_pkg).strip()
    
    if pkg in MAPPINGS:
        return MAPPINGS[pkg]
    
    if pkg.endswith('-dev'):
        base = pkg[:-4]
        if base in MAPPINGS:
            return MAPPINGS[base]
        return base
    
    if pkg.startswith('lib') and re.search(r'\d+$', pkg):
        base = re.sub(r'\d+$', '', pkg)
        if base in MAPPINGS:
            return MAPPINGS[base]
        return base
    
    return pkg

def extract_control_deps(control: Dict[str, str]) -> List[str]:
    if 'Depends' not in control:
        return []
    
    deps_raw = control['Depends']
    deps_list = [d.strip() for d in deps_raw.replace('\n', '').split(',')]
    
    arch_deps = []
    seen = set()
    
    for dep in deps_list:
        if '|' in dep:
            alternatives = [d.strip() for d in dep.split('|')]
            dep = alternatives[0]
        
        arch_dep = translate_deb_pkg(dep)
        if arch_dep and arch_dep not in seen:
            arch_deps.append(arch_dep)
            seen.add(arch_dep)
    
    return arch_deps

def generate_pkgbuild(config: Dict) -> str:
    depends_str = "depends=("
    for dep in config['depends']:
        depends_str += f"'{dep}' "
    depends_str += ")"
    
    return f"""# Maintainer: {config['maintainer']}
pkgname={config['pkgname']}
pkgver={config['pkgver']}
pkgrel={config['pkgrel']}
pkgdesc="{config['pkgdesc']}"
arch=('{config['arch']}')
url="{config['url']}"
license=('{config['license']}')
{depends_str}
source=("file://{config['source_path']}")
sha256sums=('SKIP')

package() {{
    cd "${{srcdir}}"
    
    ar x "{config['deb_filename']}"
    
    if [ -f data.tar.xz ]; then
        bsdtar -xf data.tar.xz -C "${{pkgdir}}"
    elif [ -f data.tar.gz ]; then
        bsdtar -xf data.tar.gz -C "${{pkgdir}}"
    elif [ -f data.tar.zst ]; then
        bsdtar -xf data.tar.zst -C "${{pkgdir}}"
    fi
    
    find "${{pkgdir}}" -type d -exec chmod 755 {{}} +
    find "${{pkgdir}}" -type f -exec chmod 644 {{}} +
    
    for dir in usr/bin usr/sbin bin sbin opt; do
        [ -d "${{pkgdir}}/${{dir}}" ] && find "${{pkgdir}}/${{dir}}" -type f -exec chmod 755 {{}} +
    done
    
    find "${{pkgdir}}" -type f -name "*.so*" -exec chmod 755 {{}} + 2>/dev/null || true
}}
"""

def main():
    print("╔═══════════════════════════════════════════════╗")
    print("║      deb2arch - .deb to Arch Converter        ║")
    print("║      Engineered by: oxbv1 | 0xb0rn3           ║")
    print(f"║      Version: {VERSION}                           ║")
    print("╚═══════════════════════════════════════════════╝")
    print()
    
    print("📦 Package Source")
    deb_input = input("Enter path to .deb file (or 1/2 for menu): ").strip()
    
    deb_path = deb_input.strip('\'"')
    deb_path = os.path.expanduser(deb_path)
    
    if not os.path.exists(deb_path):
        print(f"{Colors.RED}File not found: {deb_path}{Colors.NC}")
        sys.exit(1)
    
    print("\n🔍 Extracting package info...")
    control = extract_control(deb_path)
    
    print("\n📋 Package Information")
    
    maintainer = input("👤 Maintainer [Your Name <email@example.com>]: ").strip()
    maintainer = maintainer or "Your Name <email@example.com>"
    
    deb_filename = os.path.basename(deb_path)
    suggested_name = re.sub(r'_.*', '', deb_filename).replace('.deb', '').lower()
    pkgname = input(f"Package name [{suggested_name}]: ").strip() or suggested_name
    
    suggested_ver = re.search(r'_([0-9][0-9.]*)', deb_filename)
    suggested_ver = suggested_ver.group(1) if suggested_ver else "1.0.0"
    if 'Version' in control:
        suggested_ver = control['Version'].split('-')[0]
    pkgver = input(f"Version [{suggested_ver}]: ").strip() or suggested_ver
    
    pkgrel = input("Release [1]: ").strip() or "1"
    
    arch = input("Architecture [x86_64]: ").strip() or "x86_64"
    
    control_desc = control.get('Description', '').split('\n')[0] if 'Description' in control else ''
    pkgdesc = input(f"Description [{control_desc}]: ").strip() or control_desc
    
    url = input("URL: ").strip()
    
    license_val = input("License [MIT]: ").strip() or "MIT"
    
    print(f"\n{Colors.CYAN}🔬 Analyzing dependencies...{Colors.NC}")
    
    binary_deps = analyze_binary_deps(deb_path)
    control_deps = extract_control_deps(control)
    
    all_deps = list(set(binary_deps + control_deps))
    all_deps.sort()
    
    deps_str = ','.join(all_deps)
    manual_deps = input(f"\nDependencies [{deps_str}]: ").strip()
    
    if manual_deps:
        final_deps = [d.strip() for d in manual_deps.split(',') if d.strip()]
    else:
        final_deps = all_deps
    
    build_dir = input("\n📁 Build directory [/tmp/deb2arch-build]: ").strip()
    build_dir = build_dir or "/tmp/deb2arch-build"
    build_dir = os.path.expanduser(build_dir)
    
    os.makedirs(build_dir, exist_ok=True)
    
    install_pkg = input("🚀 Install after build? [y/N]: ").strip().lower()
    
    print("\n✏️  Generating PKGBUILD...")
    
    config = {
        'maintainer': maintainer,
        'pkgname': pkgname,
        'pkgver': pkgver,
        'pkgrel': pkgrel,
        'pkgdesc': pkgdesc,
        'arch': arch,
        'url': url,
        'license': license_val,
        'depends': final_deps,
        'source_path': deb_path,
        'deb_filename': deb_filename
    }
    
    pkgbuild_content = generate_pkgbuild(config)
    
    with open(os.path.join(build_dir, 'PKGBUILD'), 'w') as f:
        f.write(pkgbuild_content)
    
    print(f"{Colors.GREEN}✅ PKGBUILD created: {build_dir}/PKGBUILD{Colors.NC}")
    
    build_now = input("\n🔨 Build now? [Y/n]: ").strip().lower()
    
    if build_now != 'n':
        print(f"{Colors.CYAN}Building package (this may take a while)...{Colors.NC}")
        
        result = run_cmd(['makepkg', '-sf', '--noconfirm'], cwd=build_dir)
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✅ Build successful!{Colors.NC}")
            
            pkg_files = list(Path(build_dir).glob(f"{pkgname}-{pkgver}-{pkgrel}-*.pkg.tar.zst"))
            if pkg_files:
                pkg_file = pkg_files[0]
                print(f"{Colors.CYAN}📦 Package: {pkg_file}{Colors.NC}")
                
                if install_pkg == 'y':
                    print(f"\n{Colors.CYAN}Installing package...{Colors.NC}")
                    run_cmd(['sudo', 'pacman', '-U', str(pkg_file), '--noconfirm'])
                    print(f"{Colors.GREEN}✅ Installed!{Colors.NC}")
        else:
            print(f"{Colors.RED}❌ Build failed{Colors.NC}")
            print(f"Check {build_dir} for details")
            sys.exit(1)
    else:
        print(f"Build skipped. To build manually:")
        print(f"  cd {build_dir} && makepkg -sf")
    
    print(f"\n{Colors.GREEN}✨ Done!{Colors.NC}")

if __name__ == '__main__':
    main()
