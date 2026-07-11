#!/bin/bash

# 定义目标目录（Buildozer 的 external 目录）
EXTERNAL_DIR="/home/asu_qin/mathgame/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/build/bootstrap_builds/sdl2/jni/SDL2_image/external"

# 需要创建假仓库的子模块列表（常见的）
SUBMODULES=(
    "sjpeg"
    "libavif"
    "dav1d"
    "libjxl"
    "skcms"
    "libtiff"
    "libwebp"
    "brotli"
    "highway"
    "lcms"
    "lodepng"
    "zlib"
    "libpng"
    "libjpeg"
    "libjpeg-turbo"
)

echo "开始创建假 Git 仓库..."

# 进入 external 目录
cd "$EXTERNAL_DIR" || exit 1

for module in "${SUBMODULES[@]}"; do
    if [ -d "$module" ]; then
        echo "⚠️  $module 已存在，跳过"
        continue
    fi
    echo "🔧 创建 $module ..."
    mkdir "$module"
    cd "$module"
    git init -q
    touch README
    git add README -q
    git commit -m "dummy" -q
    cd ..
    echo "✅ $module 创建完成"
done

echo "所有假仓库创建完成！"
