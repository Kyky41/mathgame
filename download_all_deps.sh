#!/bin/bash

# 定义颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Buildozer 依赖批量下载脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 定义项目构建目录
BUILD_DIR="$HOME/mathgame/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a"
PACKAGES_DIR="$BUILD_DIR/packages"

# 确保 packages 目录存在
mkdir -p "$PACKAGES_DIR"

# 定义下载函数
download_and_mark() {
    local PACKAGE_NAME=$1
    local URL=$2
    local FILENAME=$3
    local TARGET_DIR="$PACKAGES_DIR/$PACKAGE_NAME"
    local MARK_FILE="$TARGET_DIR/.mark-$FILENAME"

    # 创建目标目录
    mkdir -p "$TARGET_DIR"

    # 检查是否已经下载并标记
    if [ -f "$TARGET_DIR/$FILENAME" ] && [ -f "$MARK_FILE" ]; then
        echo -e "${GREEN}✔ $PACKAGE_NAME 已缓存，跳过${NC}"
        return 0
    fi

    echo -e "${YELLOW}⬇ 正在下载 $PACKAGE_NAME ...${NC}"

    # 尝试下载
    if wget -q --show-progress -O "$TARGET_DIR/$FILENAME" "$URL"; then
        touch "$MARK_FILE"
        echo -e "${GREEN}✔ $PACKAGE_NAME 下载完成${NC}"
        return 0
    else
        echo -e "${RED}✖ $PACKAGE_NAME 下载失败，请检查网络或手动下载${NC}"
        return 1
    fi
}

echo -e "\n${YELLOW}开始批量下载所有依赖...${NC}\n"

# ---- 定义所有依赖 ----

# 1. hostpython3 (已处理，跳过)
echo -e "${GREEN}✔ hostpython3 已缓存 (跳过)${NC}"

# 2. libffi
download_and_mark "libffi" \
    "https://github.com/libffi/libffi/archive/v3.4.2.tar.gz" \
    "v3.4.2.tar.gz"

# 3. openssl
download_and_mark "openssl" \
    "https://www.openssl.org/source/openssl-1.1.1w.tar.gz" \
    "openssl-1.1.1w.tar.gz"

# 4. sdl2_image
download_and_mark "sdl2_image" \
    "https://github.com/libsdl-org/SDL_image/archive/release-2.6.3.tar.gz" \
    "release-2.6.3.tar.gz"

# 5. sdl2_mixer
download_and_mark "sdl2_mixer" \
    "https://github.com/libsdl-org/SDL_mixer/archive/release-2.6.3.tar.gz" \
    "release-2.6.3.tar.gz"

# 6. sdl2_ttf
download_and_mark "sdl2_ttf" \
    "https://github.com/libsdl-org/SDL_ttf/archive/release-2.20.2.tar.gz" \
    "release-2.20.2.tar.gz"

# 7. sqlite3
download_and_mark "sqlite3" \
    "https://www.sqlite.org/2023/sqlite-autoconf-3420000.tar.gz" \
    "sqlite-autoconf-3420000.tar.gz"

# 8. sdl2 (主库)
download_and_mark "sdl2" \
    "https://github.com/libsdl-org/SDL/archive/release-2.28.5.tar.gz" \
    "release-2.28.5.tar.gz"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  所有依赖下载完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}现在可以运行 buildozer -v android debug 开始打包${NC}"
