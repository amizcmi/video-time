@echo off
chcp 65001 >nul

echo 开始打包视频时长查看器 v0.3...

:: 检查 Python 环境
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo 错误：未找到 Python，请确保 Python 已安装并添加到环境变量
    pause
    exit /b 1
)

:: 检查并安装必要的包
echo 检查并安装必要的包...
python -m pip install --upgrade pip
pip install pyinstaller opencv-python

:: 清理旧的构建文件
echo 清理旧的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: 开始打包
echo 开始打包程序...
pyinstaller --noconfirm ^
    --windowed ^
    --name "VideoTimeViewer_0.3" ^
    --clean ^
    --icon=vticon.ico ^
    video_duration.py

:: 等待一下确保文件写入完成
timeout /t 2 >nul

:: 检查打包结果
if exist "dist" (
    if exist "dist\VideoTimeViewer_0.3" (
        if exist "dist\VideoTimeViewer_0.3\VideoTimeViewer_0.3.exe" (
            echo 打包成功！
            echo 可执行文件位置：dist\VideoTimeViewer_0.3\VideoTimeViewer_0.3.exe
            
            :: 重命名为中文名称
            cd dist
            ren "VideoTimeViewer_0.3" "视频时长查看器_0.3"
            echo 已重命名为中文名称
        ) else (
            echo 打包失败：未找到生成的exe文件
            pause
            exit /b 1
        )
    ) else (
        echo 打包失败：未找到输出目录
        pause
        exit /b 1
    )
) else (
    echo 打包失败：未找到dist目录
    pause
    exit /b 1
)

:: 清理临时文件
echo 清理临时文件...
if exist build rmdir /s /q build
if exist *.spec del *.spec

echo 完成！
pause 