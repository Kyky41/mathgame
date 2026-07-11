[app]
title = 加减法计算游戏
package.name = mathgame
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,otf
version = 0.1
requirements = hostpython3==3.10.11, python3==3.10.11, cython, pygame==2.5.2
orientation = portrait
fullscreen = 1
osx.kivy_version = 2.2.0

[app]
android.api = 30
android.minapi = 21
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724
android.accept_sdk_license = True
android.skip_update = True
android.auto_accept_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
