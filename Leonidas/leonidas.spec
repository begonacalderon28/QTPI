# leonidas.spec  –  dist/Leonidas/Leonidas.exe
# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
import os
import importlib.util
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

# ------------------------------------------------------------------ #
# 1)  Playwright: navegadores dentro del paquete (PLAYWRIGHT_BROWSERS_PATH=0)
# ------------------------------------------------------------------ #
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "0")

project_root = Path.cwd()

# Carpetas propias con recursos
extra_datas = [
    (project_root / "resources", "resources"),
    (project_root / "Logos",     "Logos"),
    (project_root / "bin",       "bin"),
]

# ── incluir .local-browsers (chromium) ────────────────────────────────
p_root = Path(importlib.util.find_spec("playwright").origin).parent
browsers_dir = p_root / ".local-browsers"
if browsers_dir.exists():
    extra_datas.append((browsers_dir, "playwright/.local-browsers"))
# ──────────────────────────────────────────────────────────────────────

# Ficheros de datos y módulos dinámicos que el hook oficial detecta
extra_datas += collect_data_files("playwright")
hiddenimports = collect_submodules("playwright")

block_cipher = None

# ------------------------------------------------------------------ #
# 2)  Analysis                                                       #
# ------------------------------------------------------------------ #
a = Analysis(
    ["main.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=[(str(src), str(dst)) for src, dst in extra_datas],
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)

# ------------------------------------------------------------------ #
# 3)  EXE                                                           #
# ------------------------------------------------------------------ #
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Leonidas",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,   # sin consola negra
    icon=str(project_root / "Logos" / "qtpi-leonidas-logo.ico"),
)

# ------------------------------------------------------------------ #
# 4)  Paquete ONEDIR                                                #
# ------------------------------------------------------------------ #
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="Leonidas",
)
