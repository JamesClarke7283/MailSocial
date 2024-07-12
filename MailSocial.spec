# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['src/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('LICENSE.md', '.'), 
        ('assets', 'assets'),
        ('docs/LICENSE.md', 'docs'),
        ('.default_settings.toml', '.'),
        ('.contributions.json', '.')
    ],
    hiddenimports=['PIL._tkinter_finder'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,  # Highest level of optimization
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('O', None, 'OPTION'), ('O', None, 'OPTION')],
    name='mailsocial',  # Binary name for the command line
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['assets/logo.ico'],
    version='Mail Social',  # Display name for the application
)
