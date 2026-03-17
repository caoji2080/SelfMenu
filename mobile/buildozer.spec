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
android.ndk = 25c
android.accept_sdk_license = True
android.arch = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
