import os
import PyInstaller.__main__

# 确保当前目录是脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PyInstaller.__main__.run([
    'video_duration.py',
    '--name=视频时长查看器',
    '--windowed',
    '--noconfirm',
    '--clean',
    '--add-data=icon.ico;.',  # 如果有图标文件
    '--hidden-import=tkinterdnd2',
    '--icon=icon.ico',  # 如果有图标文件
]) 