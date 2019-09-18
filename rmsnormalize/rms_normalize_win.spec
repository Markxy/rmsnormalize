# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['rms_normalize.py'],
             pathex=['D:\\Upwork\\Eli Liang\\rmsnormalize\\rmsnormalize'],
             binaries=[('.\\prerequisites\\Windows', 'prerequisites\\Windows')],
             datas=[],
             hiddenimports=['os', 'argparse', 'numpy', 'pydub', 'rmsnormalize', 'sys', 'platform'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rms_normalize',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
