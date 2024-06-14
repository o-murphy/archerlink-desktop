# ------------------------------------------------------------------
# Copyright (c) 2020 PyInstaller Development Team.
#
# This file is distributed under the terms of the GNU General Public
# License (version 2.0 or later).
#
# The full license is available in LICENSE, distributed with
# this software.
#
# SPDX-License-Identifier: GPL-2.0-or-later
# ------------------------------------------------------------------
import os

from PyInstaller.compat import is_win
from PyInstaller.utils.hooks import collect_submodules, is_module_satisfies, get_package_paths

hiddenimports = ['fractions'] + collect_submodules("av")


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


# Starting with av 9.1.1, the DLLs shipped with Windows PyPI wheels are stored
# in site-packages/av.libs instead of directly in the site-packages/av.
if is_module_satisfies("av >= 9.1.1") and is_win:
    pkg_base, pkg_dir = get_package_paths("av")
    lib_dir = os.path.join(pkg_base, "av.libs")
    if os.path.isdir(lib_dir):
        # We collect DLLs as data files instead of binaries to suppress binary
        # analysis, which would result in duplicates (because it collects a copy
        # into the top-level directory instead of preserving the original layout).
        # In addition to DLls, this also collects .load-order* file (required on
        # python < 3.8), and ensures that Shapely.libs directory exists (required
        # on python >= 3.8 due to os.add_dll_directory call).
        datas = [
            (os.path.join(lib_dir, lib_file), 'av.libs')
            for lib_file in os.listdir(lib_dir) if not match_exclude_dll(lib_file)
        ]
        print(datas)
