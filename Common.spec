# -*- mode: python ; coding: utf-8 -*-


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
    noarchive=False,
)
Main_pyz = PYZ(Main_a.pure)

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
    icon="IconMain.ico",
)

TestCreator_a = Analysis(
    ['TestCreator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
TestCreator_pyz = PYZ(TestCreator_a.pure)

TestCreator_exe = EXE(
    TestCreator_pyz,
    TestCreator_a.scripts,
    [],
    exclude_binaries=True,
    name='TestCreator',
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
    icon="IconTestCreator.ico",
)
coll = COLLECT(
    Main_exe,
    Main_a.binaries,
    Main_a.datas,
    TestCreator_exe,
    TestCreator_a.binaries,
    TestCreator_a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='IT-Master',
)
