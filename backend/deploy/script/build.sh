#!/usr/bin/env bash
# Usage: ./build.sh {SERVICE}
# 该脚本负责构建二进制文件
# 请不要直接执行这个脚本，这个脚本应当由 Makefile/Dockerfile 接管

RUN_NAME="$1"
ROOT_DIR=$(pwd) # 二进制文件将会编译至执行脚本时的目录

if [ -z "$RUN_NAME" ]; then
    echo "Error: Service name is required."
    exit 1
fi

python3 ../main.py
