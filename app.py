import os
import queue
import tempfile
import threading
from datetime import datetime
import numpy as np
import PySimpleGUI as sg
import sounddevice as sd
import whisper
from transformers import pipeline
class AudioRecorder:
    """Record system audio using sounddevice loopback."""
    def __init__(self, samplerate: int = 16000, channels: int = 1):
        self.samplerate = samplerate
        self.channels = channels
        self.q = queue.Queue()
        self.recording = False
        self.thread = None
    def _callback(self, indata, frames, time, status):  # pylint: disable=unused-argument
        if self.recording:
            self.q.put(indata.copy())
    def start(self):
        self.recording = True
        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=self._callback,
            blocksize=1024,
            dtype="float32",
            device=None,  # default loopback
            latency="low",
        )
        self.stream.start()
        self.thread = threading.Thread(target=self._record)
        self.thread.start()
    def _record(self):
        self.frames = []
        while self.recording:
            self.frames.append(self.q.get())
    def stop(self):
        self.recording = False
        if hasattr(self, "stream"):
            self.stream.stop()
            self.stream.close()
        if self.thread:
            self.thread.join()
        audio = np.concatenate(self.frames, axis=0)
        return audio
def transcribe_and_summarize(audio: np.ndarray, samplerate: int, downloads: str):
    """Transcribe audio with Whisper and summarize with transformers."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as wav_file:
        sd.write(wav_file.name, audio, samplerate)
        wav_path = wav_file.name
    model = whisper.load_model("base")
    result = model.transcribe(wav_path)
    transcript = result["text"].strip()
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    summary_text = summarizer(transcript, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    bullets = "\n".join(f"- {line.strip()}" for line in summary_text.split(". ") if line)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    transcript_path = os.path.join(downloads, f"call transcript {timestamp}.txt")
    summary_path = os.path.join(downloads, f"call summary {timestamp}.txt")
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(transcript)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(bullets)
    os.remove(wav_path)
    return transcript_path, summary_path
def main():
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    sg.theme("SystemDefault")
    layout = [
        [sg.Text("Conference Call Transcriber")],
        [sg.Button("Start Recording"), sg.Button("Stop Recording"), sg.Exit()],
        [sg.Output(size=(60, 10))],
    ]
    window = sg.Window("Transcriber", layout)
    recorder = AudioRecorder()
    while True:
        event, _values = window.read(timeout=100)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "Start Recording":
            print("Recording started...")
            recorder.start()
        if event == "Stop Recording":
            print("Processing audio...")
            audio = recorder.stop()
            try:
                transcript_path, summary_path = transcribe_and_summarize(
                    audio, recorder.samplerate, downloads
                )
                print(f"Transcript saved to: {transcript_path}")
                print(f"Summary saved to: {summary_path}")
            except Exception as exc:  # pylint: disable=broad-except
                print(f"Error: {exc}")
    window.close()
if __name__ == "__main__":
    main()