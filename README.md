# Voice Book Reader (Digital Narrator)
![CI](https://github.com/ykysny/Voice-Book-Reader/actions/workflows/tests.yml/badge.svg)

A simple text-to-speech app that reads books.
It is just a GUI (PySide6/Qt) for the amazing TTS "silero-models" (https://github.com/snakers4/silero-models).


https://github.com/ykysny/Voice-Book-Reader/assets/174832664/f53cf66e-29cd-44ae-b385-3feff8c7b5c3


## Features
- you can read several books at onсe (app remembers the last sentence and the speaker for each book)
- supported languages: English (default), Russian
- it is easy to add a new language, change the TTS model or the text preprocessing
- dark and light themes

## Installation
- create a virtual environment:
```
python3 -m venv path_to_virenv_folder
```
- activate the virtual environment:
```
source path_to_virenv_folder/bin/activate
```
- install dependencies (or you can check requirements.txt):
```
pip install sounddevice nltk num2words numpy pyside6 torch torchaudio
```
- put the "workspace" folder into the path_to_virenv_folder
- download TTS models:  
English: https://models.silero.ai/models/tts/en/v3_en.pt  
Russian: https://models.silero.ai/models/tts/ru/v4_ru.pt and https://models.silero.ai/models/tts/ru/v3_1_ru.pt
- put TTS models into the "workspace" folder

## Usage
- activate the virtual environment:
```
source path_to_virenv_folder/bin/activate
```
  go to the app folder and run:
```
cd path_to_env_folder/workspace
python3 main.py
```
- or you can use the shortcut "VBR.desktop" to launch the app in GNU/Linux:
```
[Desktop Entry]
Name=Voice Book Reader
Exec=bash -c "source path_to_virenv_folder/bin/activate; cd path_to_virenv_folder/workspace; python3 main.py"
Icon=path_to_virenv_folder/workspace/icons/dark/headphones.ico
Type=Application
Terminal=false
StartupNotify=true
```
## Details
- tested on GNU/Linux (Mint)
- books must be in the "books" folder
- only .txt books are supported(
- when the certain book is removed from "books" folder, its settings are deleted
- "nltk_data" folder is need for the text preprocessing (nltk library)
- the Russian TTS model "v4_ru.pt" is more fast, than the "v3_1_ru.pt", but is less qualitative
- the total size of the virtual environment folder is 6,2 GB (PyTorch is about 5 GB).

## How to switch language to Russian
Copy and replace files from the "languages/Russian" folder into the "workspace" folder.

## How to add a new language
You only need to rewrite "voice_engine.py" and "preprocessing.py" (6 small export functions).
You can use your TTS model or find out what languages are available at the "silero-models" project.

##
Icon pack: Qvadrons Icons by EpicCoders (https://icon-icons.com/pack/Qvadrons-Icons/789)
