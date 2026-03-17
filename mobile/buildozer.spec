[app]
title = MenuApp
package.name = menuapp
package.domain = com.menuapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db,csv,json
source.exclude_exts = spec,pyc,__pycache__,.git,.idea
version = 1.0.0
requirements = python3,flet==0.23.0,cython
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 32
android.minapi = 21
android.ndk = 25a
android.accept_sdk_license = True
android.arch = arm64-v8a
# NDK 路径将在 CI 环境中通过 buildozer.local.spec 自动设置
# 本地开发如需指定，可取消下面注释并修改路径
# android.ndk_path = /path/to/your/ndk

[buildozer]
log_level = 2
warn_on_root = 1
