# PyInstaller spec file for Employee Management System
# Build with:  pyinstaller login.spec
# Output .exe will be in the dist/ folder.

a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('cover_pic.jpeg', '.'),
        ('bg.jpeg', '.'),
        ('config.ini', '.'),
    ],
    hiddenimports=['ems', 'database', 'pymysql', 'pandas', 'openpyxl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='EmployeeManagementSystem',
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
    icon=None,
)
