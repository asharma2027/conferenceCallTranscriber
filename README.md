# Conference Call Transcriber
A simple Windows desktop application that records audio from the system, transcribes it locally using [Whisper](https://github.com/openai/whisper), and generates a bullet point summary using a local LLM.
## Features
- Records system audio.
- Local transcription with Whisper.
- Local summarization with a transformer model.
- Saves full transcript and bullet-point summary in the user's Downloads folder.
## Requirements
- Python 3.10+
- See `requirements.txt` for Python dependencies.
Install dependencies:
```bash
pip install -r requirements.txt
```
## Usage
Run the application:
```bash
python app.py
```
- Click **Start Recording** to begin capturing audio.
- Click **Stop Recording** to end the capture and process the transcript.
- Generated files will be named `call transcript <DATE>.txt` and `call summary <DATE>.txt` in the Downloads folder.
## Packaging for Windows
The app can be bundled into a standalone `.exe` that includes `numpy` and
all other dependencies so it runs on systems without Python installed.
Run the provided `build.bat` script or execute the equivalent commands
below:
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed \
  --collect-all numpy \
  --collect-all soundfile \
  --collect-all sounddevice \
  --collect-all torch \
  --collect-all whisper \
  --collect-all transformers \
  app.py
```
The resulting executable appears in `dist/app.exe`; double-click it to
launch the GUI.
## Notes
This project captures system-wide audio using loopback recording. To record audio from a specific application window, additional configuration or virtual audio routing may be required.