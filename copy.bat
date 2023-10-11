@REM NASにコピーするバッチ
@REM NasCopy.exe [コピー元のディレクトリ] [対象の拡張子A,対象の拡張子B,対象の拡張子C,...] [X週間前まで] [コピー先のディレクトリ] 

@REM 例)\\198.51.100.10\画像\202309\*.jpgを4週間前まで\\203.0.113.110\画像\2023\09\*.jpgとしてコピー
@REM NasCopy.exe \\198.51.100.10\画像\202309 jpg,bmp,png 4 \\203.0.113.110\画像\2023\09

@echo off
setlocal enabledelayedexpansion
cd %~dp0

