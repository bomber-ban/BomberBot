# BomberBot GUI 💻

[![GitHub Release](https://img.shields.io/github/v/release/bomber-ban/BomberBot?style=flat-square)](https://github.com/bomber-ban/BomberBot/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

An open-source application for working with the **BomberBot** service. Allows you to work outside of Telegram with our service.

 Pros:
 - **Traffic savings:** Minimal consumption of network resources.
 - **Security:** Your IP address is stored for only 1 hour to protect against DDoS attacks. No metrics collection like Telegram does.
 - **Cross-platform compatibility:** Available for Windows, Linux.
 - **Convenient GUI:** All work is done in a clear graphical interface.

> **Note:** The desktop application has limited functionality; only order creation is available. 


## What is BomberBot? 🧐

BomberBot is a **Software as a Service (SaaS)** platform specifically designed for **stress testing** telecommunications systems and VoIP telephony services.

* **Primary Service:** The core service is accessible via our official Telegram bot: [@OfficialBomberBot](https://t.me/OfficialBomberBot).
* **Goal:** Provides an easy way to perform stress tests on cellular networks worldwide, managing tasks right from your desktop or phone (telegram bot).


##  Download 📦

The easiest way to get started is to download a ready-made build for your OS.

**[⬇️ All releases and downloads](https://github.com/bomber-ban/BomberBot/releases)**


## How to use? 🚀

1. Download the latest version of the software for your operating system (or run it yourself from the source code / compile the applications and run them).

2.  Go to the official Telegram bot: [@OfficialBomberBot](https://t.me/OfficialBomberBot).
3.  Type `/start` and then `/api_key`.

> **Important:** Don't forget to top up your account balance in the bot before use.

4. Launch the application and log in with your API secret.

5. Select the operating mode and fill in all fields.


##  Run from source 🧑‍💻

Prerequisites:
 🐍 **Python 3.11.9**
 🌳 **GIT**
 ### Recommended: Using a Virtual Environment
 
 > **Important:**  It is highly recommended to use a virtual environment (`venv` or `conda`) to manage dependencies and avoid conflicts with other Python projects on your system.

```
git clone https://github.com/bomber-ban/BomberBot.git
cd BomberBot
pip install -r requirements.txt
python3 app.py
```


## Build from source ⚙️

###  **Windows 10/11** 🪟

**Prerequisites:**
 🐍 **Python 3.11.9** _( https://www.python.org/downloads/release/python-3119/ )_ 
 🌳 **GIT** _( https://git-scm.com/install/windows )_


```
git clone https://github.com/bomber-ban/BomberBot.git
cd BomberBot
py -m venv .venv
.venv\Script\activate
pip install -r requirements.txt
pip install PyInstaller pyinstaller-hooks-contrib keyring keyrings.alt
```

```
pyinstaller app.py ^
    --name BomberBot ^
    --onefile ^
    --windowed ^
    --icon="build\windows\bomberbot_icon.ico" ^
    --add-data "build\windows\bomberbot_icon.ico;build\windows\bomberbot_icon.ico" ^
    --add-data "gui;gui" ^
    --add-data "gui/styles;gui/styles" ^
    --add-data "gui/gifs;gui/gifs" ^
    --add-data ".venv/Lib/site-packages/PySide6/plugins;PySide6/plugins" ^
    --hidden-import keyring ^
    --hidden-import win32cred ^
    --hidden-import storage.credentials ^
    --hidden-import aiohttp ^
    --hidden-import asyncio ^
    --hidden-import json ^
    --hidden-import attrs ^
    --hidden-import yarl ^
    --hidden-import multidict ^
    --hidden-import idna ^
    --hidden-import certifi ^
    --distpath "build/windows/dist" ^
    --workpath "build/windows/temp_build"
```

**✅ Done! 
You can find your `.exe` in `build/windows/dist/BomberBot.exe`** 
*( it will be portable version, also you can add it to your Taskbar)*


### **Linux** Debian 12+/Ubuntu 22.04+🐧

**Prerequisites:**
 🐍 **Python 3.11.9+**
 
```
sudo apt update
sudo apt-get install git patchelf build-essentials python3-dev imagemagick
```

```
git clone https://github.com/bomber-ban/BomberBot.git
cd BomberBot
python3 -m venv .venv
```

```
python3 -m nuitka \
    --standalone \
    --onefile \
    --include-data-dir=gui=gui \
    --enable-plugin=pyside6 \
    --include-data-dir=gui/styles=gui/styles \
    --include-data-dir=gui/gifs=gui/gifs \
    --include-module=keyring \
    --include-package=aiohttp \
    --include-package=asyncio \
    --include-package=json \
    --include-package=attrs \
    --include-package=yarl \
    --include-package=multidict \
    --include-package=idna \
    --include-package=certifi \
    --follow-imports \
    --output-dir=build/linux/nuitka \
    --output-filename=BomberBot \
    app.py
```

```
cd build/linux
chmod +x ./make-appimage.sh
./make-appimage.sh
cd dist
./BomberBot.AppImage
```

**✅ Done! Your application is ready:**
**`BomberBot.AppImage` - click it to start use, it will be automatically added to your applications. Also, you can Pin to Dash if you wish.**


##  API & Integration 🔌

Interested in incorporating **BomberBot** functionality into your own service or software?

* **API Documentation:** **[Visit the Developer Portal](https://developer.bomberbot.cc/)**


##  Contacts & Support 💬

| Platform     | Address                                                                        |
| :----------- | :----------------------------------------------------------------------------- |
| **GitHub**   | [bomber-ban](https://github.com/bomber-ban/)                                   |
| **Telegram** | @e_sprt                                                                        |
| **Matrix**   | @d3v1ant:matrix.org                                                            |
| **Tox**      | `54933BE715B7D27372A0168923751DD6CA9CBA60DEA82520A4CB38782763FA7B18DB7CBB5C85` |

---
##  License 📄

This project is distributed under the **MIT License**. For more details, see the **[LICENSE](LICENSE)** file in the repository root.
