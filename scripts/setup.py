from setuptools import setup
import py2app

APP = ['scripts/assistant.py']  # Your main application script
DATA_FILES = [

]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'vosk', 'speech_recognition'],
    'resources': ['models/vosk-model'],  # Ensure that all necessary resources are included
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
