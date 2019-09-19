# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['rms_normalize.py'],
             pathex=['/Users/koiduvest/Documents/rmsnormalize/rmsnormalize'],
             binaries=[('prerequisites/Darwin/ffmpeg/ffmpeg', 'prerequisites/Darwin/ffmpeg')],
             datas=[],
             hiddenimports=['os', 'sys', 'argparse', 'platform', 'numpy', 'pydub', 'rmsnormalize'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=True)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [('v', None, 'OPTION')],
          name='rms_normalize',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
