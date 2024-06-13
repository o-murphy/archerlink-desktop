# -*- mode: python ; coding: utf-8 -*-

from kivy_deps import sdl2, glew
from kivy.tools.packaging.pyinstaller_hooks import get_deps_minimal, get_deps_all, hookspath as kivy_hookspath, runtime_hooks

# analyse = {**get_deps_minimal(video=None, audio=None)}
# analyse[hiddenimports] += ['pkg_resources.extern', ]

# av_hookspath = [os.path.join(os.getcwd(), '__pyinstaller')]
hookspath = kivy_hookspath()  # + av_hookspath

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
    hookspath=hookspath,
    hooksconfig={},
    runtime_hooks=runtime_hooks(),
    excludes=[
        'Pillow',
        'PIL',
        'setuptools',
        'wheel',
    ],
    noarchive=False,
    # optimize=0,
)


exclude_dlls = [
    'libaom',
    'libass',
    'libbluray',
    'libdav1d',
    'libfontconfig',
    'libfreetype',
    'libfribidi',
    'libgcc_s_seh',
    'libgmp',
    'libharfbuzz',
    'libiconv',
    'liblzma',
    'libmp3lame',
    'libogg',
    'libopencore',
    'libopencore',
    'libopenjp2',
    'libopus',
    'libpng16',
    'libsharpyuv',
    'libspeex',
    'libstdc++',
    'libtwolame',
    'libvorbis',
    'libvorbisenc',
    'libvpx',
    'libwebp',
    'libwebpmux',
    'libwinpthread',
    'libxml2',
    'postproc',
    'zlib1',
    'xvidcore'
]


# Function to match and exclude DLLs
def match_exclude_dll(path):
    for p in exclude_dlls:
        if p in path:
            print(f"AV.LIBS EXCLUDED: {p}")
            return True
    return False

# Include all DLLs except the excluded ones
a.binaries = [(x[0], x[1], x[2]) for x in a.binaries if not match_exclude_dll(x[1])]

print(a.binaries)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    exclude_binaries=True,
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
