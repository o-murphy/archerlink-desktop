# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath, runtime_hooks

# analyse = {**get_deps_minimal(video=None, audio=None)}
# analyse[hiddenimports] += ['pkg_resources.extern', ]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('gui.kv', '.'),
        ('icon.png', '.'),
        ('config.toml', '.'),
    ],
    hiddenimports=[
        'pkg_resources.extern',
        'kivy.core.image.img_sdl2',
        'kivy.core.text.text_sdl2',
        'kivymd.icon_definitions',
    ],
    hookspath=hookspath(),
    hooksconfig={},
    runtime_hooks=runtime_hooks(),
    excludes=[],
    noarchive=False,
    # optimize=0,
)


pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='ArcherLink',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version.txt',
    icon='icon.ico'  # Adding the icon file here
)
