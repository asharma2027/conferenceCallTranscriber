@echo off
:: Build standalone Windows executable with all dependencies bundled
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed ^
    --collect-all numpy ^
    --collect-all soundfile ^
    --collect-all sounddevice ^
    --collect-all torch ^
    --collect-all whisper ^
    --collect-all transformers ^
    app.py