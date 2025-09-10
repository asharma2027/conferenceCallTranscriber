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
Use [PyInstaller](https://pyinstaller.org/) to build a standalone executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed app.py
```
The executable will appear in the `dist` folder as `app.exe`. Double-click it to launch the GUI.
## Notes
This project captures system-wide audio using loopback recording. To record audio from a specific application window, additional configuration or virtual audio routing may be required.