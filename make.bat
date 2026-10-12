@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === 1/3 生成版本 A（清透玻璃版） ===
python build.py
echo === 2/3 生成版本 B（模拟器版） ===
python build_v2.py
echo === 3/3 生成说明文档并打包 ===
python package.py
pause
