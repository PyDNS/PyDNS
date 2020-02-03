import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    '--name=pydns',
    '--console',
    'pydns.py',
])
