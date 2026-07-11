#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Buildozer 依赖自动处理脚本${NC}"
echo -e "${GREEN}========================================${NC}"

PACKAGES_DIR="$HOME/mathgame/.buildozer/android/platform/build-arm64-v8a_armeabi-v7a/packages"
DEPS_DIR="$HOME/deps"

if [ ! -d "$DEPS_DIR" ]; then
    echo -e "${RED}错误：目录 $DEPS_DIR 不存在，请创建并放入下载的 .tar.gz 文件${NC}"
    exit 1
fi

declare -A DEPS
DEPS["cpython-3.10.11.tar.gz"]="hostpython3:cpython-3.10.11.tar.gz"
DEPS["libffi-3.4.2.tar.gz"]="libffi:libffi-3.4.2.tar.gz"
DEPS["openssl-1.1.1w.tar.gz"]="openssl:openssl-1.1.1w.tar.gz"
DEPS["SDL2_image-2.8.2.tar.gz"]="sdl2_image:SDL2_image-2.8.2.tar.gz"
DEPS["SDL_mixer-release-2.6.3.tar.gz"]="sdl2_mixer:SDL_mixer-release-2.6.3.tar.gz"
DEPS["SDL_ttf-release-2.20.2.tar.gz"]="sdl2_ttf:SDL_ttf-release-2.20.2.tar.gz"
DEPS["sqlite-autoconf-3420000.tar.gz"]="sqlite3:sqlite-autoconf-3420000.tar.gz"
DEPS["SDL-release-2.28.5.tar.gz"]="sdl2:SDL-release-2.28.5.tar.gz"

echo -e "\n${YELLOW}开始处理依赖...${NC}"

for SRC_FILE in "${!DEPS[@]}"; do
    IFS=':' read -r TARGET_DIR DEST_FILE <<< "${DEPS[$SRC_FILE]}"
    SRC_PATH="$DEPS_DIR/$SRC_FILE"
    DEST_PATH="$PACKAGES_DIR/$TARGET_DIR/$DEST_FILE"
    MARK_FILE="$PACKAGES_DIR/$TARGET_DIR/.mark-$DEST_FILE"

    if [ ! -f "$SRC_PATH" ]; then
        echo -e "${RED}✖ 文件不存在：$SRC_FILE${NC}"
        continue
    fi

    mkdir -p "$PACKAGES_DIR/$TARGET_DIR"
    cp "$SRC_PATH" "$DEST_PATH"
    touch "$MARK_FILE"
    echo -e "${GREEN}✔ $SRC_FILE -> $TARGET_DIR${NC}"
done

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  所有依赖处理完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${YELLOW}现在可以运行：cd ~/mathgame && buildozer -v android debug${NC}"
