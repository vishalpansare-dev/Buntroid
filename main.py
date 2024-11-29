import pyttsx3
engine = pyttsx3.init()
engine.say("Offline AI Assistant is ready!")
engine.runAndWait()
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication([])
window = QWidget()
window.setWindowTitle("Offline AI Assistant")
window.show()
app.exec_()

from vosk import Model, KaldiRecognizer
import wave

model = Model("/models/vosk-model-en-us-0.42-gigaspeech")
rec = KaldiRecognizer(model, 16000)

wf = wave.open("/models/test.wav", "rb")
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
