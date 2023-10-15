# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


Main_a = Analysis(
    ['Main.py'],
    pathex=[],
    binaries=[],
    datas=[("src", "src"), ("courses", "courses"), ("settings.json", "."), ("logs", "logs"), ("LICENSE", "."), ("docs\\README", ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
Main_pyz = PYZ(Main_a.pure, Main_a.zipped_data, cipher=block_cipher)

Main_exe = EXE(
    Main_pyz,
    Main_a.scripts,
    [],
    exclude_binaries=True,
    name='IT-Master',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="IconMain.ico"
)

ConstructorTests_a = Analysis(
    ['ConstructorTests.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
ConstructorTests_pyz = PYZ(ConstructorTests_a.pure, ConstructorTests_a.zipped_data, cipher=block_cipher)

ConstructorTests_exe = EXE(
    ConstructorTests_pyz,
    ConstructorTests_a.scripts,
    [],
    exclude_binaries=True,
    name='ConstructorTests',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="IconConstructorTests.ico"
)
coll = COLLECT(
    Main_exe,
    Main_a.binaries,
    Main_a.zipfiles,
    Main_a.datas,
    ConstructorTests_exe,
    ConstructorTests_a.binaries,
    ConstructorTests_a.zipfiles,
    ConstructorTests_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IT-Master',
)
