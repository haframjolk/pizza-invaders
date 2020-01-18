import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os"], "excludes": ["tkinter"],
    "include_files": ["img", "snd", "font"]
}
bdist_msi_options = {
    "install_icon": "app-icon.ico"
}
bdist_mac_options = {
    "iconfile": "app-icon.icns",
    "bundle_name": "Pizza Invaders",
    "custom_info_plist": "Info.plist"
}
bdist_dmg_options = {
    "volume_label": "Pizza Invaders",
    "applications_shortcut": True
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Pizza Invaders",
      url="https://github.com/reynmag/pizza-invaders",
      author="RAM",
      version="1.0.2",
      description="A Space Invaders clone featuring the President of Iceland",
      options={"build_exe": build_exe_options, "bdist_msi": bdist_msi_options, "bdist_mac": bdist_mac_options, "bdist_dmg": bdist_dmg_options},
      executables=[Executable("lokaverkefni.py",
                   base=base,
                   targetName="Pizza Invaders",
                   shortcutName="Pizza Invaders",
                   shortcutDir="DesktopFolder",
                   icon="app-icon.ico")])
