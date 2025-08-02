# Jigglepedia-Toolbox
Desktop app to create GIF, MP4 and WebM videos using exported frames from jigglepedia.com

# Instructions
1. Download the latest version from the Release page: https://github.com/VanillaSkyy/Jigglepedia-Toolbox/releases
2. Unzip and execute
3. Done!

# Build your own executable
## Requisites
- Python 3.10+: https://www.python.org/downloads/
- fmmpeg for Windows: https://www.gyan.dev/ffmpeg/builds/

## Instructions
1. Download the latest source code from the Release page: https://github.com/VanillaSkyy/Jigglepedia-Toolbox/releases
2. Create a folder named ``fmmpeg`` and drop ``ffmpeg.exe`` in there
3. Install ``pyinstaller`` and ``tkinterdnd2`` packages
4. Run ``pyinstaller --onefile --windowed --add-data "ffmpeg;ffmpeg" --add-data "app_icon.ico;." --icon=app_icon.ico jigglepedia_toolbox.py``
5. Done, you'll find the ``.exe`` inside ``dist/``
